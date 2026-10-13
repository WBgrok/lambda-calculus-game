"""Automated tests for challenge validation and menu flow."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game.game_state import GameState
from game.menu import Menu
from interpreter.lambda_interpreter import Parser


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
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
        self.assertIn("Syntax error", results[0]["error"])

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

    def test_menu_completes_typed_challenge(self):
        menu = Menu(self.game_state)
        with patch("builtins.input", side_effect=[r"\x.\y.x", ""]):
            with redirect_stdout(io.StringIO()):
                completed = menu.challenge_menu("TRUE")

        self.assertTrue(completed)
        self.assertTrue(self.game_state.is_completed("TRUE"))
        self.assertIn("TRUE", self.game_state.get_all_aliases())


if __name__ == "__main__":
    unittest.main()
