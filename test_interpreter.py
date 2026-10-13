"""Automated tests for the lambda calculus interpreter."""

import unittest

from interpreter.lambda_interpreter import parse_and_eval


class InterpreterTests(unittest.TestCase):
    def test_identity_reduces_to_its_argument(self):
        result, steps = parse_and_eval(r"(\x.x) apple")

        self.assertEqual(str(result), "apple")
        self.assertGreater(len(steps), 1)

    def test_beta_reduction_avoids_capturing_free_variable(self):
        result, _ = parse_and_eval(r"(\x.\y.x) y")

        self.assertEqual(str(result), r"\y_1.y")

    def test_application_is_left_associative(self):
        result, _ = parse_and_eval(r"(\x.\y.x) first second")

        self.assertEqual(str(result), "first")

    def test_maximum_reduction_steps_stops_infinite_reduction(self):
        from interpreter.lambda_interpreter import Evaluator, Parser

        expression = Parser(r"(\x.x x) (\x.x x)").parse()
        evaluator = Evaluator(max_steps=10)

        with self.assertRaisesRegex(RuntimeError, "maximum steps"):
            evaluator.evaluate(expression)


if __name__ == "__main__":
    unittest.main()
