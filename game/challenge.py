"""Challenge management and testing"""

from typing import Tuple, List
from interpreter.lambda_interpreter import parse_and_eval, Expr, Var


class ChallengeTest:
    """Test case for a challenge"""
    
    def __init__(self, input_expr: str, expected: str):
        self.input_expr = input_expr
        self.expected = expected
    
    def run(self, aliases: dict) -> Tuple[bool, str, str]:
        """
        Run the test.
        Returns: (passed, actual_result, explanation)
        """
        try:
            result, steps = parse_and_eval(self.input_expr, aliases)
            actual_result = str(result)
            
            passed = actual_result == self.expected
            return passed, actual_result, None
        except Exception as e:
            return False, None, str(e)


class Challenge:
    """A single challenge"""
    
    def __init__(self, challenge_dict: dict):
        self.id = challenge_dict['id']
        self.name = challenge_dict['name']
        self.description = challenge_dict['description']
        self.tests = [ChallengeTest(t['input'], t['expected']) for t in challenge_dict['tests']]
        self.requirements = challenge_dict.get('requirements', [])
    
    def test_solution(self, user_solution: str, aliases: dict) -> Tuple[bool, List[dict]]:
        """
        Test user's solution against all tests.
        Returns: (all_passed, results)
        where results is list of {passed, input, expected, actual, error}
        """
        # Parse the user's solution once
        try:
            solution_expr, _ = parse_and_eval(user_solution, aliases)
        except Exception as e:
            return False, [{
                'passed': False,
                'input': user_solution,
                'expected': 'Valid lambda expression',
                'actual': None,
                'error': f"Syntax error: {e}"
            }]
        
        results = []
        all_passed = True
        
        for test in self.tests:
            # Substitute the user's solution into the test
            full_expr = f"({user_solution}) {test.input_expr}"
            
            try:
                result, steps = parse_and_eval(full_expr, aliases)
                actual_result = str(result)
                passed = actual_result == test.expected
                
                results.append({
                    'passed': passed,
                    'input': full_expr,
                    'expected': test.expected,
                    'actual': actual_result,
                    'error': None,
                    'steps': steps
                })
                
                if not passed:
                    all_passed = False
            except Exception as e:
                results.append({
                    'passed': False,
                    'input': full_expr,
                    'expected': test.expected,
                    'actual': None,
                    'error': str(e),
                    'steps': []
                })
                all_passed = False
        
        return all_passed, results
