"""Automated regression tests for the additional challenge definitions."""

import unittest

from game.game_state import GameState
from interpreter.lambda_interpreter import Parser


class AdditionalChallengeTests(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        solutions = {
            "ID": r"\x.x",
            "TRUE": r"\x.\y.x",
            "FALSE": r"\x.\y.y",
        }
        for challenge_id, source in solutions.items():
            self.game_state.complete_challenge(challenge_id, Parser(source).parse())

    def assert_challenge_passes(self, challenge_id, solution):
        challenge = self.game_state.get_challenge(challenge_id)
        passed, results = challenge.test_solution(
            solution,
            self.game_state.get_all_aliases(),
        )
        self.assertTrue(passed, msg=f"{challenge_id} results: {results}")

    def test_pair_challenge(self):
        self.assert_challenge_passes("PAIR", r"\a.\b.\f.f a b")

    def test_swap_challenge(self):
        self.assert_challenge_passes("SWAP", r"\x.\y.y x")

    def test_conditional_challenge(self):
        self.assert_challenge_passes("IF", r"\b.\a.\c.b a c")

    def test_boolean_not_challenge(self):
        self.assert_challenge_passes("NOT", r"\b.b FALSE TRUE")


if __name__ == "__main__":
    unittest.main()
