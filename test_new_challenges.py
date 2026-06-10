#!/usr/bin/env python3
"""Test new challenges from Lambda.txt"""

from game.game_state import GameState
from game.challenge import Challenge
from interpreter.lambda_interpreter import Parser

# Create game state and mark prerequisites as completed
game_state = GameState()

challenges_to_setup = [
    (r"\x.x", "ID"),
    (r"\x.\y.x", "TRUE"),
    (r"\x.\y.y", "FALSE"),
]

for solution, challenge_id in challenges_to_setup:
    parser = Parser(solution)
    expr = parser.parse()
    game_state.complete_challenge(challenge_id, expr)

print("✓ Completed: ID, TRUE, FALSE")
print()

# Test PAIR
print("=" * 60)
print("Testing PAIR challenge")
print("=" * 60)
pair_dict = game_state.get_challenge("PAIR")
pair_challenge = Challenge(pair_dict)

user_solution = r"\a.\b.\f.f a b"
print(f"User solution: {user_solution}\n")

all_passed, results = pair_challenge.test_solution(user_solution, game_state.get_all_aliases())

for i, result in enumerate(results, 1):
    status = "✓" if result['passed'] else "✗"
    print(f"Test {i}: [{status}]")
    print(f"  Expected: {result['expected']}")
    print(f"  Got:      {result['actual']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    print()

print(f"Result: {'✓ PASS' if all_passed else '✗ FAIL'}\n")

# Test SWAP
print("=" * 60)
print("Testing SWAP challenge")
print("=" * 60)
swap_dict = game_state.get_challenge("SWAP")
swap_challenge = Challenge(swap_dict)

user_solution = r"\x.\y.y x"
print(f"User solution: {user_solution}\n")

all_passed, results = swap_challenge.test_solution(user_solution, game_state.get_all_aliases())

for i, result in enumerate(results, 1):
    status = "✓" if result['passed'] else "✗"
    print(f"Test {i}: [{status}]")
    print(f"  Expected: {result['expected']}")
    print(f"  Got:      {result['actual']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    print()

print(f"Result: {'✓ PASS' if all_passed else '✗ FAIL'}\n")

# Test IF
print("=" * 60)
print("Testing IF challenge")
print("=" * 60)
if_dict = game_state.get_challenge("IF")
if_challenge = Challenge(if_dict)

user_solution = r"\b.\a.\c.b a c"
print(f"User solution: {user_solution}\n")

all_passed, results = if_challenge.test_solution(user_solution, game_state.get_all_aliases())

for i, result in enumerate(results, 1):
    status = "✓" if result['passed'] else "✗"
    print(f"Test {i}: [{status}]")
    print(f"  Expected: {result['expected']}")
    print(f"  Got:      {result['actual']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    print()

print(f"Result: {'✓ PASS' if all_passed else '✗ FAIL'}\n")

# Test NOT
print("=" * 60)
print("Testing NOT challenge")
print("=" * 60)
not_dict = game_state.get_challenge("NOT")
not_challenge = Challenge(not_dict)

user_solution = r"\b.b FALSE TRUE"
print(f"User solution: {user_solution}\n")

all_passed, results = not_challenge.test_solution(user_solution, game_state.get_all_aliases())

for i, result in enumerate(results, 1):
    status = "✓" if result['passed'] else "✗"
    print(f"Test {i}: [{status}]")
    print(f"  Expected: {result['expected']}")
    print(f"  Got:      {result['actual']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    print()

print(f"Result: {'✓ PASS' if all_passed else '✗ FAIL'}\n")
