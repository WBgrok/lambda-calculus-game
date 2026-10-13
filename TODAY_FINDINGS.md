# Project Findings — 2026-10-13

## Current state

The project is a working Python console game for learning lambda calculus.
Challenge definitions live in JSON; the parser and evaluator are kept separate
from the game controller and console view.

## Implemented improvements

- Challenge and challenge-test definitions use dataclasses.
- The console presentation is separated from game flow.
- Evaluation returns a structured result with an immutable reduction trace.
- Parser errors and reduction-limit errors have named exception types; expected
  input errors are handled without swallowing unexpected programming errors.
- Completed challenges and their aliases are saved to
  `Path.home() / ".lambda-calculus-game" / "progress.json"`.
- The main menu resumes saved progress by default and requires confirmation
  before starting a new game and deleting the save.
- Automated tests use Python's built-in `unittest` and require no extra
  dependencies.

## Test coverage

The test suite covers interpreter reduction and syntax errors, aliases, every
challenge in the JSON catalog, prerequisite references, controller navigation,
and progress loading, saving, validation, and reset. Persistence tests use
temporary directories and do not touch a real user save.

## Small remaining cleanup opportunities

- Challenge solution results are still represented as dictionaries. A typed
  result model could replace them if the result shape grows.
- Challenge catalog validation currently occurs through loading and tests;
  stricter schema validation could be added if challenge authors need clearer
  diagnostics.

No database or additional framework is currently needed for the project's
scope.
