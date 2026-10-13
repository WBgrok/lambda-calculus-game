# Setup Instructions

## Local Development

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. Navigate to the project directory:
```bash
cd lambda-calculus-game
```

2. No additional dependencies needed (uses only Python standard library)

### Running the Game

```bash
python main.py
```

### Running the Automated Tests

The project uses Python's built-in `unittest`; no test package installation is
needed:
```bash
python -m unittest discover -v
```

On Windows, an isolated virtual environment is optional:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m unittest discover -v
```

## Pushing to GitHub

### First Time Setup

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name it "lambda-calculus-game"
   - Do NOT initialize with README (we already have one)
   - Click "Create repository"

2. In the project directory, configure and push:

```bash
# Set your GitHub username and email
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"

# Create initial commit if not already done
git add .
git commit -m "Initial project setup: Lambda calculus game prototype"

# Add remote and push
git remote add origin https://github.com/YOUR-USERNAME/lambda-calculus-game.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

3. If you get authentication errors:
   - For HTTPS: Use a personal access token instead of password
     - Create one at https://github.com/settings/tokens
     - Use token as password when prompted
   - For SSH: Set up SSH keys at https://github.com/settings/keys

### Making Changes and Committing

```bash
# Stage changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Project Structure

```
lambda-calculus-game/
├── README.md                 # Project overview
├── main.py                   # Game entry point
├── test_interpreter.py       # Interpreter tests
├── interpreter/
│   ├── __init__.py
│   └── lambda_interpreter.py # Core lambda calculus interpreter
├── game/
│   ├── __init__.py
│   ├── game_state.py         # Session state management
│   ├── challenge.py          # Challenge system
│   └── menu.py               # UI and menus
└── challenges/
    ├── __init__.py
    └── challenges.json       # Challenge definitions
```

## Game Features (Prototype)

- **Lambda Interpreter**: Supports backslash syntax (`\x.body`)
- **Step-by-step Reduction**: Shows each beta reduction step
- **Challenge System**: Progressive challenges with test verification
- **Aliases**: Completed challenges become reusable aliases
- **Free Interpreter**: Test expressions freely between challenges
- **ASCII UI**: Text-based interface with formatted menus

## Next Steps

See README.md for gameplay information and challenge format.
