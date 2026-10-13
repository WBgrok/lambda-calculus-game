"""Automated tests for challenge aliases."""

import unittest

from game.game_state import GameState
from interpreter.lambda_interpreter import Parser, parse_and_eval


class AliasTests(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        identity = Parser(r"\x.x").parse()
        self.game_state.complete_challenge("ID", identity)

    def test_completed_challenge_can_be_used_as_alias(self):
        result = parse_and_eval("ID apple", self.game_state.get_all_aliases())

        self.assertEqual(str(result.final_expression), "apple")

    def test_aliases_are_returned_as_a_copy(self):
        aliases = self.game_state.get_all_aliases()
        aliases.clear()

        self.assertIn("ID", self.game_state.get_all_aliases())


if __name__ == "__main__":
    unittest.main()
