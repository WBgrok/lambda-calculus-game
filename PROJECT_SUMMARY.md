# Project Summary

Lambda Calculus Game is a Python console application that teaches lambda
calculus through challenge-based practice.

## Current features

- Parser for variables, lambda abstractions, application, and parentheses.
- Normal-order-style beta reduction with capture-avoiding substitution and a
  maximum reduction-step limit.
- Structured `EvaluationResult` and immutable `ReductionStep` values for
  evaluation output.
- Thirteen JSON-defined challenges: `ID`, `TRUE`, `FALSE`, `PAIR`, `FST`,
  `SCD`, `SWAP`, `SQR`, `IF`, `NOT`, `AND`, `OR`, and `XOR`.
- Prerequisite-based challenge unlocking and completed solutions available as
  aliases.
- Automatic progress save/restore in the user's home directory, plus a
  confirmation-protected new-game reset.
- No third-party runtime or test dependencies.

## Main modules

| Path | Responsibility |
| --- | --- |
| `main.py` | Initialize state and start the game |
| `game/controller.py` | Coordinate menus, challenge testing, and game actions |
| `game/menu.py` | Console input and presentation |
| `game/game_state.py` | Challenge state and JSON progress persistence |
| `game/challenge.py` | Challenge/test models and solution validation |
| `interpreter/lambda_interpreter.py` | Parser, evaluator, AST, and evaluation result |
| `challenges/challenges.json` | Challenge descriptions, tests, and prerequisites |

## Progress file

Progress is stored in
`Path.home() / ".lambda-calculus-game" / "progress.json"`. The versioned JSON
file records completed challenge IDs and the corresponding lambda expressions.
An invalid or incompatible save is reported as a progress-load error rather
than silently ignored.

## Verification

Run all tests from the project root:

```bash
python -m unittest discover -v
```

The tests cover interpreter behavior, aliases, all challenge solutions and
catalog prerequisites, controller navigation, and progress save/load/reset.
Progress tests use temporary files.
