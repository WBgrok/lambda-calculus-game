"""Challenge management and testing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Tuple

from interpreter.lambda_interpreter import parse_and_eval


@dataclass(frozen=True)
class ChallengeTest:
    """A single test case for a challenge."""

    input_expr: str
    expected: str

    @classmethod
    def from_dict(cls, challenge_test: Mapping[str, str]) -> "ChallengeTest":
        """Build a test case from a JSON-like mapping."""
        return cls(
            input_expr=str(challenge_test["input"]),
            expected=str(challenge_test["expected"]),
        )

    def run(self, aliases: dict) -> Tuple[bool, str, str]:
        """
        Run the test.
        Returns: (passed, actual_result, explanation)
        """
        try:
            result = parse_and_eval(self.input_expr, aliases)
            actual_result = str(result.final_expression)
            return actual_result == self.expected, actual_result, None
        except Exception as exc:  # pragma: no cover - forward compatibility for runtime issues
            return False, None, str(exc)

    def as_dict(self) -> Dict[str, str]:
        """Return a JSON-friendly representation."""
        return {"input": self.input_expr, "expected": self.expected}


@dataclass
class Challenge:
    """A single challenge with human-friendly metadata and test cases."""

    id: str
    name: str
    description: str
    tests: List[ChallengeTest] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.tests = [ChallengeTest.from_dict(test) if isinstance(test, Mapping) else test for test in self.tests]
        self.requirements = list(self.requirements)

    @classmethod
    def from_dict(cls, challenge_dict: Mapping[str, Any]) -> "Challenge":
        """Build a Challenge from a JSON-like dictionary."""
        return cls(
            id=str(challenge_dict["id"]),
            name=str(challenge_dict["name"]),
            description=str(challenge_dict["description"]),
            tests=[
                ChallengeTest.from_dict(test)
                for test in challenge_dict.get("tests", [])
            ],
            requirements=list(challenge_dict.get("requirements", [])),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-compatible representation of the challenge."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tests": [test.as_dict() for test in self.tests],
            "requirements": list(self.requirements),
        }

    def __getitem__(self, key: str) -> Any:
        """Compatibility shim so older dict-style access still works."""
        return self.to_dict()[key]

    def get(self, key: str, default: Any = None) -> Any:
        """Dictionary-like access for compatibility."""
        return self.to_dict().get(key, default)

    def test_solution(self, user_solution: str, aliases: dict) -> Tuple[bool, List[dict]]:
        """
        Test user's solution against all tests.
        Returns: (all_passed, results)
        where results is list of {passed, input, expected, actual, error}
        """
        try:
            parse_and_eval(user_solution, aliases)
        except Exception as exc:  # pragma: no cover - runtime validation path
            return False, [{
                'passed': False,
                'input': user_solution,
                'expected': 'Valid lambda expression',
                'actual': None,
                'error': f"Syntax error: {exc}"
            }]

        results = []
        all_passed = True

        for test in self.tests:
            full_expr = f"({user_solution}) {test.input_expr}"

            try:
                evaluation = parse_and_eval(full_expr, aliases)
                actual_result = str(evaluation.final_expression)
                passed = actual_result == test.expected

                results.append({
                    'passed': passed,
                    'input': full_expr,
                    'expected': test.expected,
                    'actual': actual_result,
                    'error': None,
                    'steps': evaluation.steps
                })

                if not passed:
                    all_passed = False
            except Exception as exc:
                results.append({
                    'passed': False,
                    'input': full_expr,
                    'expected': test.expected,
                    'actual': None,
                    'error': str(exc),
                    'steps': []
                })
                all_passed = False

        return all_passed, results
