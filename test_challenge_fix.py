#!/usr/bin/env python3
"""Test the fixed challenge system with new test format"""

from game.game_state import GameState
from game.challenge import Challenge

# Create game state and mark ID as completed
game_state = GameState()

# Simulate completing ID challenge
from interpreter.lambda_interpreter import Parser
parser = Parser(r"\x.x")
id_solution = parser.parse()
game_state.complete_challenge("ID", id_solution)

print("Completed ID challenge")
print(f"Available aliases: {list(game_state.aliases.keys())}")
print()

# Now test TRUE challenge
true_challenge_dict = game_state.get_challenge("TRUE")
true_challenge = Challenge(true_challenge_dict)

print("Testing TRUE challenge:")
print(f"Description: {true_challenge_dict['description']}")
print()

# User writes the TRUE function
user_solution = r"\x.\y.x"

print(f"User solution: {user_solution}")
print()

# Test it
all_passed, results = true_challenge.test_solution(user_solution, game_state.get_all_aliases())

print("Test Results:")
print("=" * 60)
for i, result in enumerate(results, 1):
    status = "✓ PASS" if result['passed'] else "✗ FAIL"
    print(f"\nTest {i}: {status}")
    print(f"  Full expression: {result['input']}")
    print(f"  Expected: {result['expected']}")
    print(f"  Got:      {result['actual']}")
    
    if result['error']:
        print(f"  Error: {result['error']}")

print()
print("=" * 60)
if all_passed:
    print("✓ All tests passed!")
else:
    print("✗ Some tests failed")
