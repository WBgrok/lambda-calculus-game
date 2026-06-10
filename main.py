#!/usr/bin/env python3
"""
Lambda Calculus Game - Main Entry Point
"""

from game.game_state import GameState
from game.menu import main_loop


def main():
    """Start the game"""
    try:
        game_state = GameState()
        main_loop(game_state)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
