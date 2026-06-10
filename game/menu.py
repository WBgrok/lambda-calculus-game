"""Game menu and UI"""

from typing import Optional
from game.game_state import GameState
from game.challenge import Challenge
from interpreter.lambda_interpreter import parse_and_eval


class UI:
    """ASCII UI utilities"""
    
    WIDTH = 80
    
    @staticmethod
    def header(text: str) -> str:
        """Format a header"""
        return f"\n{'=' * UI.WIDTH}\n{text.center(UI.WIDTH)}\n{'=' * UI.WIDTH}\n"
    
    @staticmethod
    def section(text: str) -> str:
        """Format a section header"""
        return f"\n{text}\n{'-' * len(text)}\n"
    
    @staticmethod
    def box(text: str, width: Optional[int] = None) -> str:
        """Format text in a box"""
        width = width or UI.WIDTH
        lines = text.split('\n')
        
        result = "┌" + "─" * (width - 2) + "┐\n"
        for line in lines:
            padded = line.ljust(width - 4)
            result += f"│ {padded} │\n"
        result += "└" + "─" * (width - 2) + "┘"
        
        return result
    
    @staticmethod
    def indent(text: str, spaces: int = 2) -> str:
        """Indent text"""
        prefix = " " * spaces
        return "\n".join(prefix + line for line in text.split("\n"))


class Menu:
    """Main menu and navigation"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def main_menu(self) -> Optional[str]:
        """
        Display main menu.
        Returns: 'challenge:<id>', 'free', or None (quit)
        """
        while True:
            print(UI.header("Lambda Calculus Game"))
            
            available = self.game_state.get_available_challenges()
            
            if not available:
                print("No challenges available yet.")
                return None
            
            print("Available Challenges:")
            print("-" * 40)
            
            for i, ch in enumerate(available, 1):
                completed = "✓" if self.game_state.is_completed(ch['id']) else " "
                print(f"{i}. [{completed}] {ch['name']} ({ch['id']})")
            
            print("\nOptions:")
            print(f"{len(available) + 1}. Free Interpreter")
            print(f"{len(available) + 2}. Quit")
            print()
            
            try:
                choice = input("Enter your choice: ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(available):
                    return f"challenge:{available[choice_num - 1]['id']}"
                elif choice_num == len(available) + 1:
                    return "free"
                elif choice_num == len(available) + 2:
                    return None
            except (ValueError, IndexError):
                pass
            
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
    
    def challenge_menu(self, challenge_id: str) -> bool:
        """
        Display challenge and allow user to solve it.
        Returns: True if challenge was completed, False otherwise
        """
        ch_dict = self.game_state.get_challenge(challenge_id)
        if not ch_dict:
            print(f"Challenge {challenge_id} not found.")
            return False
        
        challenge = Challenge(ch_dict)
        
        while True:
            print(UI.header(f"Challenge: {challenge.name}"))
            print(UI.box(challenge.description, UI.WIDTH))
            
            # Show what aliases are available
            if self.game_state.aliases:
                print(UI.section("Available Aliases (from completed challenges)"))
                for alias_id in sorted(self.game_state.aliases.keys()):
                    print(f"  {alias_id}: {self.game_state.aliases[alias_id]}")
            
            print(UI.section("Requirements"))
            if challenge.requirements:
                for req in challenge.requirements:
                    status = "✓" if self.game_state.is_completed(req) else "✗"
                    print(f"  [{status}] {req}")
            else:
                print("  None")
            
            print(UI.section("Your Solution"))
            print("(Enter empty line to switch to free interpreter)")
            
            user_input = input("Enter your lambda expression: ").strip()
            
            if not user_input:
                # Switch to free interpreter
                print("\n[Switching to free interpreter mode]")
                self.free_interpreter()
                continue
            
            # Test the solution
            all_passed, results = challenge.test_solution(user_input, self.game_state.get_all_aliases())
            
            print(UI.section("Test Results"))
            
            for i, result in enumerate(results, 1):
                status = "PASS" if result['passed'] else "FAIL"
                print(f"Test {i}: [{status}]")
                
                if result['error']:
                    print(f"  Error: {result['error']}")
                else:
                    print(f"  Input:    {result['input']}")
                    print(f"  Expected: {result['expected']}")
                    print(f"  Got:      {result['actual']}")
                    
                    if result.get('steps'):
                        print(f"\n  Reduction steps:")
                        for step_expr, step_desc in result['steps'][:5]:  # Show first 5 steps
                            print(f"    {step_desc}")
                            print(f"    → {step_expr}")
                        if len(result['steps']) > 5:
                            print(f"    ... ({len(result['steps']) - 5} more steps)")
                
                print()
            
            if all_passed:
                print(UI.box(f"✓ Challenge '{challenge.name}' completed!", UI.WIDTH))
                print(f"\nThe function '{challenge_id}' is now available as an alias.")
                # Parse the solution to store it as an expression for future use as alias
                from interpreter.lambda_interpreter import Parser
                parser = Parser(user_input, self.game_state.get_all_aliases())
                solution_expr = parser.parse()
                self.game_state.complete_challenge(challenge_id, solution_expr)
                input("Press Enter to return to main menu...")
                return True
            else:
                print("Some tests failed. Try again!")
                input("Press Enter to try again...")
    
    def free_interpreter(self) -> Optional[str]:
        """
        Free-form lambda expression interpreter.
        Returns: 'menu' to return to menu, None to quit
        """
        print(UI.header("Free Lambda Interpreter"))
        print("Enter lambda expressions to evaluate step-by-step.")
        print("(Use \\ for lambda, e.g., \\x.x for identity)")
        print()
        
        while True:
            if self.game_state.aliases:
                print("Available aliases: " + ", ".join(sorted(self.game_state.aliases.keys())))
            
            print("\n(Enter empty line to return to menu)")
            user_input = input("Expression: ").strip()
            
            if not user_input:
                return "menu"
            
            try:
                result, steps = parse_and_eval(user_input, self.game_state.get_all_aliases())
                
                print(UI.section("Reduction Steps"))
                for expr, description in steps[:20]:  # Show first 20 steps
                    print(f"{description}")
                    print(f"  → {expr}")
                
                if len(steps) > 20:
                    print(f"... ({len(steps) - 20} more steps)")
                
                print(UI.section("Final Result"))
                print(f"{result}")
                print()
            
            except Exception as e:
                print(f"\nError: {e}\n")


def main_loop(game_state: GameState):
    """Main game loop"""
    menu = Menu(game_state)
    
    while True:
        choice = menu.main_menu()
        
        if choice is None:
            print("\nThanks for playing! Goodbye!")
            break
        elif choice.startswith("challenge:"):
            challenge_id = choice.split(":")[1]
            menu.challenge_menu(challenge_id)
        elif choice == "free":
            result = menu.free_interpreter()
            if result != "menu":
                break
