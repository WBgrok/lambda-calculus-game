# Lambda Calculus Game - Project Summary

## What's Been Created

A complete text-based lambda calculus learning game with the following components:

### 1. Core Interpreter (`interpreter/lambda_interpreter.py`)
- **Parser**: Supports lambda syntax with backslash (`\`) notation
- **Evaluator**: Performs step-by-step beta reduction
- **Features**:
  - Variable substitution with proper alpha conversion
  - Handles nested lambdas and applications
  - Returns structured evaluation results with typed reduction steps
  - Keeps reduction traces local to each evaluation
  - Supports aliases from completed challenges

### 2. Challenge System (`game/challenge.py`, `challenges/challenges.json`)
- **5 Initial Challenges**:
  - ID (Identity function) - No requirements
  - TRUE (First selector) - Requires ID
  - FALSE (Second selector) - Requires ID
  - FST (First element of pair) - Requires ID and TRUE
  - SCD (Second element of pair) - Requires ID and FALSE
- **Challenge Features**:
  - Multiple test cases per challenge
  - Requirement dependencies
  - Automated test verification
  - Aliases persist across session

### 3. Game State Management (`game/game_state.py`)
- Tracks completed challenges
- Saves and restores completed challenges and aliases as JSON in the user's home directory
- Offers confirmation-protected progress reset for a new game
- Loads challenge definitions from JSON
- Validates challenge requirements

### 4. Game Flow and Console UI (`game/controller.py`, `game/menu.py`)
- **Game Controller**: Handles menu navigation, challenge evaluation, and state changes
- **Console View**: Renders menus, challenge details, test results, and interpreter output
- **Main Menu**: Shows available challenges and free interpreter option
- **Challenge Interface**:
  - Displays challenge description
  - Shows available aliases
  - Accepts user solution
  - Runs automated tests with detailed results
  - Shows reduction steps
  - Option to switch to free interpreter
- **Free Interpreter**: 
  - Evaluate any lambda expression
  - Display step-by-step reduction
  - Use any completed challenge as alias
  - Exit by pressing Enter
- **ASCII UI**: Uses box drawing and formatted text

### 5. Entry Point (`main.py`)
- Simple game loop initialization

## How to Test It

1. **Run the automated tests**:
   ```bash
   python -m unittest discover -v
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```
   Follow the on-screen prompts to:
   - Choose a challenge or free interpreter
   - Write lambda expressions
   - See step-by-step reductions
   - Complete challenges to unlock aliases

## Architecture

```
main.py
  └─> GameState (loads challenges, tracks progress)
      ├─> Challenge (tests solutions)
      └─> GameController (coordinates game flow)
          ├─> ConsoleView (renders and collects console input)
          └─> Evaluator (reduces expressions)
              └─> Parser (parses lambda syntax)
```

## How the Challenge System Works

1. **Challenge Format** (JSON):
   ```json
   {
     "id": "ALIAS_NAME",
     "name": "Human-readable name",
     "description": "What user needs to do",
     "tests": [
       {"input": "test expression", "expected": "expected result"},
       ...
     ],
     "requirements": ["other_challenge_ids"]
   }
   ```

2. **Testing**: When user submits a solution:
   - Parse the solution expression
   - Apply it to each test case
   - Compare expected vs actual output
   - Show all reduction steps
   - Mark complete if all tests pass

3. **Aliases**: Completed challenges' IDs become aliases (e.g., `ID`, `TRUE`, `FALSE`)
   - Available in all subsequent inputs
   - Persist for entire session
   - Can be used in free interpreter or future challenges

## Syntax Reference

- `\x.body` - Lambda abstraction (lambda x. body)
- `expr1 expr2` - Application (apply expr1 to expr2)
- `(expr)` - Grouping
- `\x.\y.body` - Multiple parameters (curried)
- Aliases: Completed challenge IDs can be used by name

### Examples
- Identity: `\x.x`
- Constant function: `\x.\y.x` (TRUE)
- Application: `(\x.x) apple`

## Testing Completed

✓ Interpreter correctly parses lambda expressions
✓ Beta reduction works with proper variable substitution
✓ Step-by-step reduction display
✓ Identity function test passes
✓ TRUE function test passes
✓ Project structure complete

## Next Steps to Extend

1. Add more challenges (pairs, lists, Church numerals, arithmetic)
2. Add higher-level combinators (S, K, I combinators)
3. Implement challenge persistence (save/load progress)
4. Add hint system
5. Add scoring/difficulty ratings
6. Create web-based interface

## Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Entry point, starts game loop |
| `interpreter/lambda_interpreter.py` | Core lambda interpreter |
| `game/game_state.py` | Session state and challenge loading |
| `game/challenge.py` | Challenge testing system |
| `game/controller.py` | Game flow and actions |
| `game/menu.py` | Console presentation |
| `challenges/challenges.json` | Challenge definitions |
| `test_interpreter.py` | Interpreter verification tests |
| `README.md` | User-facing documentation |
| `SETUP.md` | Developer setup and GitHub instructions |
