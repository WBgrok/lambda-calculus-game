#!/usr/bin/env python3
"""
Lambda Calculus Game - Main Entry Point
"""

from game.game_state import GameState, ProgressLoadError, ProgressSaveError
from game.controller import main_loop


def main():
    """Start the game"""
    try:
        game_state = GameState()
        main_loop(game_state)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except (ProgressLoadError, ProgressSaveError) as exc:
        print(f"\nProgress error: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
