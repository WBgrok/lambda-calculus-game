"""Tests for the browser-facing Python API."""

import json
import unittest
from pathlib import Path

from game.game_state import ProgressLoadError
from web import bridge


class WebBridgeTests(unittest.TestCase):
    def setUp(self):
        challenge_path = (
            Path(__file__).parent / "challenges" / "challenges.json"
        )
        self.challenge_json = challenge_path.read_text(encoding="utf-8")
        self.state = json.loads(bridge.initialize(self.challenge_json))

    def test_catalog_starts_with_only_the_identity_challenge_unlocked(self):
        available = [
            challenge["id"]
            for challenge in self.state["challenges"]
            if challenge["unlocked"]
        ]

        self.assertEqual(available, ["ID"])
        self.assertEqual(self.state["progress"]["completed_challenges"], [])

    def test_solution_results_have_json_friendly_steps_and_update_progress(self):
        result = json.loads(bridge.submit_solution("ID", r"\x.x"))

        self.assertTrue(result["all_passed"])
        self.assertEqual(result["progress"]["completed_challenges"], ["ID"])
        self.assertTrue(result["state"]["challenges"][0]["completed"])
        self.assertIsInstance(result["results"][0]["steps"][0]["expression"], str)

    def test_failed_solution_does_not_update_progress(self):
        result = json.loads(bridge.submit_solution("ID", r"\x.y"))

        self.assertFalse(result["all_passed"])
        self.assertEqual(result["progress"]["completed_challenges"], [])

    def test_locked_and_unknown_challenges_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "locked"):
            bridge.submit_solution("TRUE", r"\x.\y.x")
        with self.assertRaisesRegex(ValueError, "Unknown challenge"):
            bridge.submit_solution("UNKNOWN", r"\x.x")

    def test_browser_progress_restores_completion_and_aliases(self):
        progress = json.dumps({
            "version": 1,
            "completed_challenges": ["ID"],
            "aliases": {"ID": r"\x.x"},
        })
        state = json.loads(bridge.initialize(self.challenge_json, progress))

        self.assertEqual(state["completed_count"], 1)
        self.assertTrue(state["challenges"][1]["unlocked"])
        result = json.loads(bridge.evaluate_expression("ID apple"))
        self.assertEqual(result["final_expression"], "apple")

    def test_new_game_clears_browser_progress(self):
        bridge.submit_solution("ID", r"\x.x")

        state = json.loads(bridge.new_game())

        self.assertEqual(state["completed_count"], 0)
        self.assertEqual(state["progress"]["aliases"], {})

    def test_invalid_browser_progress_is_reported(self):
        with self.assertRaisesRegex(ProgressLoadError, "unsupported save version"):
            bridge.initialize(
                self.challenge_json,
                json.dumps({"version": 999}),
            )


if __name__ == "__main__":
    unittest.main()
