"""Coordinate game state, challenge logic, and the console view."""

from __future__ import annotations

from typing import Optional

from game.game_state import GameState
from game.menu import ConsoleView
from interpreter.lambda_interpreter import Parser, parse_and_eval


class GameController:
    """Handle game flow and delegate console interaction to a view."""

    def __init__(self, game_state: GameState, view: Optional[ConsoleView] = None):
        self.game_state = game_state
        self.view = view or ConsoleView()

    def run(self):
        """Run the main game loop."""
        while True:
            available = self.game_state.get_available_challenges()
            choice = self.view.show_main_menu(
                available,
                self.game_state.completed_challenges,
            )

            if not available:
                choice = ""
            else:
                try:
                    choice_number = int(choice)
                except ValueError:
                    self.view.show_invalid_menu_choice()
                    self.view.pause("Press Enter to continue...")
                    continue

                if 1 <= choice_number <= len(available):
                    self.challenge_menu(available[choice_number - 1].id)
                    continue
                if choice_number == len(available) + 1:
                    if self.free_interpreter() != "menu":
                        break
                    continue
                if choice_number != len(available) + 2:
                    self.view.show_invalid_menu_choice()
                    self.view.pause("Press Enter to continue...")
                    continue

            self.view.show_goodbye()
            break

    def challenge_menu(self, challenge_id: str) -> bool:
        """Run the interaction for one challenge."""
        challenge = self.game_state.get_challenge(challenge_id)
        if challenge is None:
            self.view.show_unknown_challenge(challenge_id)
            return False

        while True:
            self.view.show_challenge(
                challenge,
                self.game_state.get_all_aliases(),
                self.game_state.completed_challenges,
            )
            user_input = self.view.prompt_solution()

            if not user_input:
                self.view.show_switch_to_free_interpreter()
                self.free_interpreter()
                continue

            all_passed, results = challenge.test_solution(
                user_input,
                self.game_state.get_all_aliases(),
            )
            self.view.show_test_results(results)

            if all_passed:
                solution_expr = Parser(
                    user_input,
                    self.game_state.get_all_aliases(),
                ).parse()
                self.game_state.complete_challenge(challenge_id, solution_expr)
                self.view.show_challenge_completed(challenge_id, challenge.name)
                self.view.pause("Press Enter to return to main menu...")
                return True

            self.view.show_challenge_incomplete()
            self.view.pause("Press Enter to try again...")

    def free_interpreter(self) -> Optional[str]:
        """Evaluate free-form expressions until the user returns to the menu."""
        self.view.show_free_interpreter_intro()

        while True:
            aliases = self.game_state.get_all_aliases()
            self.view.show_alias_names(aliases)
            user_input = self.view.prompt_expression()

            if not user_input:
                return "menu"

            try:
                evaluation = parse_and_eval(user_input, aliases)
                self.view.show_reduction_steps(evaluation.steps)
                self.view.show_final_result(evaluation.final_expression)
            except Exception as exc:
                self.view.show_error(exc)


def main_loop(game_state: GameState):
    """Run the game using its console view."""
    GameController(game_state).run()
