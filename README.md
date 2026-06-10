# Lambda Calculus Game

A text-based game teaching lambda calculus through interactive challenges.

## Overview

Learn lambda calculus by solving progressive challenges. Write lambda functions to meet specifications, and as you complete challenges, your solutions become reusable aliases.

- **Backslash syntax**: Use `\` to denote lambda (e.g., `\x.x` is the identity function)
- **Step-by-step reduction**: See how your lambda expression evaluates
- **Free interpreter**: Test expressions before tackling challenges
- **Progressive challenges**: Unlock harder challenges by completing prerequisite challenges

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
git clone <your-repo-url>
cd lambda-calculus-game
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## Project Structure

```
lambda-calculus-game/
├── main.py                 # Entry point
├── interpreter/            # Lambda calculus interpreter
│   └── lambda_interpreter.py
├── game/                   # Game logic
│   ├── menu.py            # Main menu and UI
│   ├── challenge.py       # Challenge system
│   └── game_state.py      # Session state
└── challenges/            # Challenge definitions
    └── challenges.json
```

## Challenge Format

Challenges are stored in `challenges/challenges.json`:

```json
{
  "id": "ID",
  "name": "Challenge Name",
  "description": "What the player needs to do",
  "tests": [
    {
      "input": "test expression",
      "expected": "expected result"
    }
  ],
  "requirements": ["prereq_id1", "prereq_id2"]
}
```

## License

MIT
