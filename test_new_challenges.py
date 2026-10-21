"""Automated regression tests for the additional challenge definitions."""

import tempfile
import unittest
from pathlib import Path

from game.challenge import ChallengeTest
from game.game_state import GameState
from interpreter.lambda_interpreter import Parser


class AdditionalChallengeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        progress_path = Path(self.temp_dir.name) / "progress.json"
        self.game_state = GameState(progress_path=progress_path)
        solutions = {
            "ID": r"\x.x",
            "TRUE": r"\x.\y.x",
            "FALSE": r"\x.\y.y",
            "PAIR": r"\a.\b.\f.f a b",
            "FST": r"\p.p TRUE",
            "SCD": r"\p.p FALSE",
            "SWAP": r"\x.\y.y x",
            "SQR": r"\f.\x.f (f x)",
            "OR": r"\p.\q.p TRUE q",
            "AND": r"\p.\q.p q FALSE",
            "XOR": r"\p.\q.p (q FALSE TRUE) (q TRUE FALSE)",
            "NOT": r"\b.b FALSE TRUE",
            "IF": r"\b.\a.\c.b a c",
            "SIMPLE_LIST": r"\lst.FST (SCD (SCD lst))",
            "ANY": r"\lst.OR (FST lst) (OR (FST (SCD lst)) (FST (SCD (SCD lst))))",
            "PUSH": r"\item.\lst.PAIR item lst",
            "POP": r"\lst.SCD lst",
            "EMPTY": r"\lst.lst (\head.\tail.\ignored.FALSE) TRUE",
            "Y": r"\f.(\x.f (x x)) (\x.f (x x))",
            "STRIP_PREFIX": r"Y (\rec.\lst.IF (FST lst) lst (rec (SCD lst)))",
            "ACC": (
                r"\lst.\combine.\initial."
                r"Y (\rec.\remaining.\acc."
                r"remaining (\head.\tail.\dummy.rec tail (combine acc head)) acc)"
                r" lst initial"
            ),
            "ALL": r"\lst.ACC lst AND TRUE",
            "MAP": (
                r"\lst.\transform."
                r"Y (\rec.\remaining."
                r"remaining (\head.\tail.\dummy.PUSH (transform head) (rec tail)) FALSE)"
                r" lst"
            ),
            "NONE": (
                r"Y (\rec.\lst."
                r"lst (\head.\tail.\dummy.head FALSE (rec tail)) TRUE)"
            ),
            "FILTER": (
                r"\lst.\predicate."
                r"Y (\rec.\remaining."
                r"remaining ("
                r"\head.\tail.\dummy."
                r"predicate head (PUSH head (rec tail)) (rec tail)"
                r") FALSE) lst"
            ),
            "ZIP": (
                r"Y (\rec.\left.\right."
                r"left (\head.\tail.\dummy."
                r"PUSH (PAIR head (right TRUE)) (rec tail (right FALSE))"
                r") FALSE)"
            ),
            "EQBLIST": (
                r"Y (\rec.\left.\right."
                r"left (\head.\tail.\dummy."
                r"AND (NOT (XOR head (right TRUE))) (rec tail (right FALSE))"
                r") TRUE)"
            ),
            "CONCAT": (
                r"Y (\rec.\left.\right."
                r"left (\head.\tail.\dummy.PUSH head (rec tail right)) right)"
            ),
            "REVERSE": (
                r"\lst.Y (\rec.\remaining.\acc."
                r"remaining (\head.\tail.\dummy.rec tail (PUSH head acc)) acc)"
                r" lst FALSE"
            ),
        }
        for challenge_id, source in solutions.items():
            solution = Parser(
                source,
                self.game_state.get_all_aliases(),
            ).parse()
            self.game_state.complete_challenge(challenge_id, solution)

    def assert_challenge_passes(self, challenge_id, solution):
        challenge = self.game_state.get_challenge(challenge_id)
        passed, results = challenge.test_solution(
            solution,
            self.game_state.get_all_aliases(),
        )
        self.assertTrue(passed, msg=f"{challenge_id} results: {results}")

    def test_pair_challenge(self):
        self.assert_challenge_passes("PAIR", r"\a.\b.\f.f a b")

    def test_identity_challenge(self):
        self.assert_challenge_passes("ID", r"\x.x")

    def test_false_challenge(self):
        self.assert_challenge_passes("FALSE", r"\x.\y.y")

    def test_swap_challenge(self):
        self.assert_challenge_passes("SWAP", r"\x.\y.y x")

    def test_conditional_challenge(self):
        self.assert_challenge_passes("IF", r"\b.\a.\c.b a c")

    def test_boolean_not_challenge(self):
        self.assert_challenge_passes("NOT", r"\b.b FALSE TRUE")

    def test_first_and_second_pair_projection_challenges(self):
        self.assert_challenge_passes("FST", r"\p.p TRUE")
        self.assert_challenge_passes("SCD", r"\p.p FALSE")

    def test_simple_list_returns_third_element(self):
        self.assert_challenge_passes(
            "SIMPLE_LIST",
            r"\lst.FST (SCD (SCD lst))",
        )

    def test_any_true_in_list_challenge(self):
        self.assert_challenge_passes(
            "ANY",
            r"\lst.OR (FST lst) (OR (FST (SCD lst)) (FST (SCD (SCD lst))))",
        )

    def test_push_challenge(self):
        self.assert_challenge_passes("PUSH", r"\item.\lst.PAIR item lst")

    def test_pop_challenge(self):
        self.assert_challenge_passes("POP", r"\lst.SCD lst")

    def test_empty_list_challenge(self):
        self.assert_challenge_passes(
            "EMPTY",
            r"\lst.lst (\head.\tail.\ignored.FALSE) TRUE",
        )

    def test_y_combinator_challenge(self):
        self.assert_challenge_passes("Y", r"\f.(\x.f (x x)) (\x.f (x x))")

    def test_strip_prefix_challenge(self):
        self.assert_challenge_passes(
            "STRIP_PREFIX",
            r"Y (\rec.\lst.IF (FST lst) lst (rec (SCD lst)))",
        )

    def test_accumulate_challenge(self):
        self.assert_challenge_passes(
            "ACC",
            r"\lst.\combine.\initial."
            r"Y (\rec.\remaining.\acc."
            r"remaining (\head.\tail.\dummy.rec tail (combine acc head)) acc)"
            r" lst initial",
        )

    def test_all_true_challenge(self):
        self.assert_challenge_passes("ALL", r"\lst.ACC lst AND TRUE")

    def test_map_challenge(self):
        self.assert_challenge_passes(
            "MAP",
            r"\lst.\transform."
            r"Y (\rec.\remaining."
            r"remaining (\head.\tail.\dummy.PUSH (transform head) (rec tail)) FALSE)"
            r" lst",
        )

    def test_no_true_values_challenge(self):
        self.assert_challenge_passes(
            "NONE",
            r"Y (\rec.\lst."
            r"lst (\head.\tail.\dummy.head FALSE (rec tail)) TRUE)",
        )

    def test_filter_challenge(self):
        self.assert_challenge_passes(
            "FILTER",
            r"\lst.\predicate."
            r"Y (\rec.\remaining."
            r"remaining ("
            r"\head.\tail.\dummy."
            r"predicate head (PUSH head (rec tail)) (rec tail)"
            r") FALSE) lst",
        )

    def test_zip_challenge(self):
        self.assert_challenge_passes(
            "ZIP",
            r"Y (\rec.\left.\right."
            r"left (\head.\tail.\dummy."
            r"PUSH (PAIR head (right TRUE)) (rec tail (right FALSE))"
            r") FALSE)",
        )

    def test_equal_boolean_lists_challenge(self):
        self.assert_challenge_passes(
            "EQBLIST",
            r"Y (\rec.\left.\right."
            r"left (\head.\tail.\dummy."
            r"AND (NOT (XOR head (right TRUE))) (rec tail (right FALSE))"
            r") TRUE)",
        )

    def test_concatenate_lists_challenge(self):
        self.assert_challenge_passes(
            "CONCAT",
            r"Y (\rec.\left.\right."
            r"left (\head.\tail.\dummy.PUSH head (rec tail right)) right)",
        )

    def test_reverse_list_challenge(self):
        self.assert_challenge_passes(
            "REVERSE",
            r"\lst.Y (\rec.\remaining.\acc."
            r"remaining (\head.\tail.\dummy.rec tail (PUSH head acc)) acc)"
            r" lst FALSE",
        )

    def test_boolean_and_challenge(self):
        self.assert_challenge_passes("AND", r"\p.\q.p q FALSE")

    def test_boolean_or_challenge(self):
        self.assert_challenge_passes("OR", r"\p.\q.p TRUE q")

    def test_boolean_xor_challenge(self):
        self.assert_challenge_passes(
            "XOR",
            r"\p.\q.p (q FALSE TRUE) (q TRUE FALSE)",
        )

    def test_challenge_test_expected_expression_can_use_aliases(self):
        challenge_test = ChallengeTest(
            input_expr="TRUE apple banana",
            expected="TRUE apple banana",
        )

        passed, actual, error = challenge_test.run(
            self.game_state.get_all_aliases(),
        )

        self.assertTrue(passed)
        self.assertEqual(actual, "apple")
        self.assertIsNone(error)

    def test_apply_twice_challenge(self):
        self.assert_challenge_passes("SQR", r"\f.\x.f (f x)")

    def test_indirection_challenge(self):
        self.assert_challenge_passes(
            "INDIRECTION",
            r"\f.\a.\b.f b a",
        )

    def test_anything_challenge_accepts_any_valid_expression(self):
        self.assert_challenge_passes("ANYTHING", r"\x.x x")
        self.assert_challenge_passes("ANYTHING", "free_variable")

    def test_anything_challenge_rejects_invalid_expression(self):
        challenge = self.game_state.get_challenge("ANYTHING")

        passed, results = challenge.test_solution(
            r"\x.",
            self.game_state.get_all_aliases(),
        )

        self.assertFalse(passed)
        self.assertIn("LambdaSyntaxError", results[0]["error"])

    def test_catalog_requirements_reference_known_challenges(self):
        challenge_ids = {challenge.id for challenge in self.game_state.challenges_data}
        self.assertEqual(
            challenge_ids,
            {
                "ANYTHING",
                "ID", "TRUE", "FALSE", "PAIR", "FST", "SCD", "SIMPLE_LIST",
                "ANY", "PUSH", "POP", "EMPTY", "SWAP",
                "SQR", "INDIRECTION", "IF", "NOT", "AND", "OR", "XOR",
                "Y", "STRIP_PREFIX", "ACC", "ALL", "MAP", "NONE", "FILTER",
                "ZIP", "EQBLIST", "CONCAT", "REVERSE",
            },
        )
        for challenge in self.game_state.challenges_data:
            with self.subTest(challenge=challenge.id):
                self.assertTrue(challenge.tests or challenge.validation_only)
                self.assertTrue(set(challenge.requirements).issubset(challenge_ids))


if __name__ == "__main__":
    unittest.main()
