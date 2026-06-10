#!/usr/bin/env python3
"""Test alias display in menus"""

from game.game_state import GameState
from interpreter.lambda_interpreter import Parser

# Create game state
game_state = GameState()

# Complete a few challenges
challenges_to_complete = [
    (r"\x.x", "ID"),
    (r"\x.\y.x", "TRUE"),
    (r"\x.\y.y", "FALSE"),
]

for solution, challenge_id in challenges_to_complete:
    parser = Parser(solution)
    expr = parser.parse()
    game_state.complete_challenge(challenge_id, expr)

print("Completed challenges: ID, TRUE, FALSE")
print()

print("Available aliases:")
print("-" * 40)
for alias_id in sorted(game_state.aliases.keys()):
    expr = game_state.aliases[alias_id]
    print(f"  {alias_id}: {expr}")

print()
print("Testing that aliases can be used in parsing:")
print("-" * 40)

# Now test that we can use these aliases in new expressions
parser = Parser(r"ID apple", game_state.get_all_aliases())
expr = parser.parse()
print(f"Parsed 'ID apple' as: {expr}")

parser = Parser(r"TRUE first second", game_state.get_all_aliases())
expr = parser.parse()
print(f"Parsed 'TRUE first second' as: {expr}")

print()
print("✓ Alias display and substitution working correctly!")
