"""Automated tests for the lambda calculus interpreter."""

import unittest

from interpreter.lambda_interpreter import (
    EvaluationResult,
    Evaluator,
    Parser,
    parse_and_eval,
)


class InterpreterTests(unittest.TestCase):
    def test_identity_reduces_to_its_argument(self):
        result = parse_and_eval(r"(\x.x) apple")

        self.assertIsInstance(result, EvaluationResult)
        self.assertEqual(str(result.initial_expression), r"(\x.x) apple")
        self.assertEqual(str(result.final_expression), "apple")
        self.assertGreater(len(result.steps), 1)
        self.assertEqual(result.steps[0].description, "Initial expression")

    def test_beta_reduction_avoids_capturing_free_variable(self):
        result = parse_and_eval(r"(\x.\y.x) y")

        self.assertEqual(str(result.final_expression), r"\y_1.y")

    def test_application_is_left_associative(self):
        result = parse_and_eval(r"(\x.\y.x) first second")

        self.assertEqual(str(result.final_expression), "first")

    def test_evaluation_results_keep_independent_reduction_traces(self):
        evaluator = Evaluator()
        first = evaluator.evaluate(Parser(r"(\x.x) first").parse())
        second = evaluator.evaluate(Parser(r"(\x.x) second").parse())

        self.assertEqual(str(first.final_expression), "first")
        self.assertEqual(str(second.final_expression), "second")
        self.assertEqual(str(first.steps[-1].expression), "first")

    def test_maximum_reduction_steps_stops_infinite_reduction(self):
        expression = Parser(r"(\x.x x) (\x.x x)").parse()
        evaluator = Evaluator(max_steps=10)

        with self.assertRaisesRegex(RuntimeError, "maximum steps"):
            evaluator.evaluate(expression)


if __name__ == "__main__":
    unittest.main()
