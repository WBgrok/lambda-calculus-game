# Findings for 2026-10-13

## Project state

The lambda-calculus game is small, focused, and easy to understand. It has a clear teaching goal and the core interpreter is already built around a workable parser + beta-reduction evaluator.

## Strong points

- The game loop is compact and easy to follow.
- The challenge/progression concept is clear and useful for teaching.
- The interpreter supports step-by-step reduction, which is valuable for pedagogy.
- Challenge requirements and alias unlocking are a good fit for the project’s purpose.

## Improvement opportunities

### 1. Typed domain models — started

The code currently relies heavily on raw dictionaries for challenge definitions and test results. This makes the code more fragile than it needs to be and scatters schema assumptions across the project.

The challenge and challenge-test definitions have been converted to dataclasses while retaining dictionary-style compatibility for existing callers. Test results still use dictionaries and can be migrated in a later pass if their shape needs to grow.

### 2. Separate UI from game logic — implemented

The menu layer currently handles display, input validation, challenge evaluation, and state mutation in one place. Extracting this into a view/controller split would make the project easier to extend and test.

The console rendering and prompts now live in `game/menu.py` as `ConsoleView`; `GameController` in `game/controller.py` owns navigation, challenge evaluation, and state changes.

### 3. Stronger evaluation abstractions — implemented

The lambda evaluator is fine for a teaching tool, but the current `parse_and_eval` flow and result handling are not structured enough for deeper validation or future features like richer challenge feedback, debug modes, or persistence.

`parse_and_eval()` now returns an `EvaluationResult` with an immutable trace of `ReductionStep` values. The controller and challenge runner consume this result directly.

### 4. Better error boundaries — implemented

The interpreter now raises named `LambdaSyntaxError` and `EvaluationLimitError` exceptions. Challenge and interactive interpreter flows catch only those expected user-facing failures, while unexpected exceptions propagate. The top-level entry point no longer catches and re-raises every exception.

### 5. Persistence and tooling — next

The project currently lacks a formal test runner setup in the local environment, and there is no persisted progress model yet. Adding a lightweight save file or SQLite-backed progress system would be a worthwhile next milestone.

## Immediate next step

Implement persisted game progress so completed challenges and their aliases survive across runs.
