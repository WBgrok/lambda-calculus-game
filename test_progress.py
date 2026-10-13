"""Automated tests for saved game progress."""

import json
import tempfile
import unittest
from pathlib import Path

from game.game_state import GameState, ProgressLoadError, ProgressSaveError
from interpreter.lambda_interpreter import Parser, parse_and_eval


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.progress_path = Path(self.temp_dir.name) / "progress.json"

    def test_completed_challenges_and_aliases_load_on_next_run(self):
        state = GameState(progress_path=self.progress_path)
        state.complete_challenge("ID", Parser(r"\x.x").parse())
        state.complete_challenge(
            "TRUE",
            Parser(r"\x.\y.x", state.get_all_aliases()).parse(),
        )

        restored = GameState(progress_path=self.progress_path)

        self.assertEqual(restored.completed_challenges, {"ID", "TRUE"})
        self.assertEqual(str(restored.get_alias("ID")), r"\x.x")
        self.assertEqual(str(restored.get_alias("TRUE")), r"\x.\y.x")
        result = parse_and_eval("ID apple", restored.get_all_aliases())
        self.assertEqual(str(result.final_expression), "apple")
        self.assertEqual(
            json.loads(self.progress_path.read_text(encoding="utf-8"))["version"],
            GameState.PROGRESS_VERSION,
        )

    def test_invalid_save_data_fails_explicitly(self):
        self.progress_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaisesRegex(ProgressLoadError, "Invalid saved progress"):
            GameState(progress_path=self.progress_path)

    def test_unknown_challenge_in_save_fails_explicitly(self):
        self.progress_path.write_text(
            json.dumps({
                "version": GameState.PROGRESS_VERSION,
                "completed_challenges": ["UNKNOWN"],
                "aliases": {"UNKNOWN": r"\x.x"},
            }),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ProgressLoadError, "unknown completed"):
            GameState(progress_path=self.progress_path)

    def test_completed_challenge_without_prerequisites_fails_to_load(self):
        self.progress_path.write_text(
            json.dumps({
                "version": GameState.PROGRESS_VERSION,
                "completed_challenges": ["TRUE"],
                "aliases": {"TRUE": r"\x.\y.x"},
            }),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ProgressLoadError, "missing prerequisites"):
            GameState(progress_path=self.progress_path)

    def test_reset_deletes_save_and_clears_current_state(self):
        state = GameState(progress_path=self.progress_path)
        state.complete_challenge("ID", Parser(r"\x.x").parse())

        state.reset_progress()

        self.assertFalse(self.progress_path.exists())
        self.assertFalse(state.completed_challenges)
        self.assertFalse(state.aliases)

    def test_save_failure_is_reported_and_does_not_mark_challenge_complete(self):
        blocked_save_path = Path(self.temp_dir.name) / "blocked" / "progress.json"
        state = GameState(progress_path=blocked_save_path)
        blocked_save_path.parent.write_text(
            "blocks directory creation",
            encoding="utf-8",
        )

        with self.assertRaises(ProgressSaveError):
            state.complete_challenge("ID", Parser(r"\x.x").parse())

        self.assertFalse(state.completed_challenges)
        self.assertFalse(state.aliases)


if __name__ == "__main__":
    unittest.main()
