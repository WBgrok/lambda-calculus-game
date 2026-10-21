# Project Summary

Lambda Calculus Game is a Python application that teaches lambda calculus
through challenge-based practice in the console or a static browser edition.

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
- Static browser game powered by Pyodide, reusing the Python logic and loading
  the challenge catalog as a separate JSON asset.
- Browser progress stored in `localStorage`, separate from console progress.
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
| `web/` | Static browser frontend and JSON-facing Python bridge |

## Progress file

Progress is stored in
`Path.home() / ".lambda-calculus-game" / "progress.json"`. The versioned JSON
file records completed challenge IDs and the corresponding lambda expressions.
An invalid or incompatible save is reported as a progress-load error rather
than silently ignored.

The browser edition stores the same versioned progress document under the
`lambda-calculus-game.progress` key in `localStorage`. Browser and console saves
are independent.

## Browser edition

Run `python -m http.server 8000` from the repository root and open
`http://localhost:8000/web/`. Static hosting must include the `web/`, `game/`,
`interpreter/`, and `challenges/` directories at their relative paths. See
[README.md](README.md) for deployment details.

## Verification

Run all tests from the project root:

```bash
python -m unittest discover -v
```

The tests cover interpreter behavior, aliases, all challenge solutions and
catalog prerequisites, controller navigation, and progress save/load/reset.
Progress tests use temporary files. Browser bridge tests cover injected
challenge data, browser progress restoration, challenge submissions, and reset.
