"""Automated tests for challenge validation and menu flow."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from game.game_state import GameState
from game.controller import GameController
from game.menu import ConsoleView
from interpreter.lambda_interpreter import Parser


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        progress_path = Path(self.temp_dir.name) / "progress.json"
        self.game_state = GameState(progress_path=progress_path)
        identity = Parser(r"\x.x").parse()
        self.game_state.complete_challenge("ID", identity)

    def test_challenge_solution_passes_all_tests(self):
        challenge = self.game_state.get_challenge("TRUE")

        passed, results = challenge.test_solution(
            r"\x.\y.x",
            self.game_state.get_all_aliases(),
        )

        self.assertTrue(passed)
        self.assertTrue(all(result["passed"] for result in results))

    def test_invalid_solution_reports_failure(self):
        challenge = self.game_state.get_challenge("TRUE")

        passed, results = challenge.test_solution(
            r"\x",
            self.game_state.get_all_aliases(),
        )

        self.assertFalse(passed)
        self.assertIn("LambdaSyntaxError", results[0]["error"])

    def test_unexpected_challenge_failure_is_not_hidden(self):
        challenge = self.game_state.get_challenge("TRUE")
        with patch("game.challenge.parse_and_eval", side_effect=ValueError("bug")):
            with self.assertRaisesRegex(ValueError, "bug"):
                challenge.test_solution(
                    r"\x.\y.x",
                    self.game_state.get_all_aliases(),
                )

    def test_challenge_unlocks_after_all_prerequisites(self):
        available_ids = {
            challenge.id
            for challenge in self.game_state.get_available_challenges()
        }
        self.assertIn("TRUE", available_ids)
        self.assertNotIn("PAIR", available_ids)

        self.game_state.complete_challenge(
            "TRUE",
            Parser(r"\x.\y.x").parse(),
        )
        self.game_state.complete_challenge(
            "FALSE",
            Parser(r"\x.\y.y").parse(),
        )
        available_ids = {
            challenge.id
            for challenge in self.game_state.get_available_challenges()
        }
        self.assertIn("PAIR", available_ids)

    def test_console_menu_displays_only_unlocked_challenges(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="1"):
            with redirect_stdout(output):
                ConsoleView().show_main_menu(
                    self.game_state.get_available_challenges(),
                    self.game_state.completed_challenges,
                )

        self.assertIn("TRUE", output.getvalue())
        self.assertNotIn("PAIR", output.getvalue())

    def test_menu_completes_typed_challenge(self):
        controller = GameController(self.game_state)
        with patch("builtins.input", side_effect=[r"\x.\y.x", ""]):
            with redirect_stdout(io.StringIO()):
                completed = controller.challenge_menu("TRUE")

        self.assertTrue(completed)
        self.assertTrue(self.game_state.is_completed("TRUE"))
        self.assertIn("TRUE", self.game_state.get_all_aliases())

    def test_controller_routes_free_interpreter_then_quits(self):
        controller = GameController(self.game_state)
        available_count = len(self.game_state.get_available_challenges())
        with patch(
            "builtins.input",
            side_effect=[str(available_count + 1), "", str(available_count + 3)],
        ):
            with redirect_stdout(io.StringIO()):
                controller.run()

    def test_new_game_requires_confirmation_before_reset(self):
        controller = GameController(self.game_state)
        available_count = len(self.game_state.get_available_challenges())
        with patch(
            "builtins.input",
            side_effect=[str(available_count + 2), "n", str(available_count + 3)],
        ):
            with redirect_stdout(io.StringIO()):
                controller.run()

        self.assertTrue(self.game_state.is_completed("ID"))
        self.assertTrue(self.game_state.progress_path.exists())

    def test_confirmed_new_game_clears_saved_progress(self):
        controller = GameController(self.game_state)
        available_count = len(self.game_state.get_available_challenges())
        initial_available_count = sum(
            not challenge.requirements
            for challenge in self.game_state.challenges_data
        )
        with patch(
            "builtins.input",
            side_effect=[
                str(available_count + 2),
                "y",
                str(initial_available_count + 2),
            ],
        ):
            with redirect_stdout(io.StringIO()):
                controller.run()

        self.assertFalse(self.game_state.completed_challenges)
        self.assertFalse(self.game_state.aliases)
        self.assertFalse(self.game_state.progress_path.exists())

    def test_free_interpreter_does_not_hide_unexpected_errors(self):
        controller = GameController(self.game_state)
        with patch("builtins.input", return_value="anything"):
            with patch("game.controller.parse_and_eval", side_effect=ValueError("bug")):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(ValueError, "bug"):
                        controller.free_interpreter()


if __name__ == "__main__":
    unittest.main()
