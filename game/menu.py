"""Console presentation for the game."""

from __future__ import annotations

from typing import Optional, Sequence

from game.challenge import Challenge
from interpreter.lambda_interpreter import Expr, ReductionStep


class UI:
    """ASCII formatting utilities."""

    WIDTH = 80

    @staticmethod
    def header(text: str) -> str:
        """Format a header."""
        return f"\n{'=' * UI.WIDTH}\n{text.center(UI.WIDTH)}\n{'=' * UI.WIDTH}\n"

    @staticmethod
    def section(text: str) -> str:
        """Format a section header."""
        return f"\n{text}\n{'-' * len(text)}\n"

    @staticmethod
    def box(text: str, width: Optional[int] = None) -> str:
        """Format text in a box."""
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
        """Indent text."""
        prefix = " " * spaces
        return "\n".join(prefix + line for line in text.split("\n"))


class ConsoleView:
    """Render game state and collect raw console input."""

    def show_main_menu(self, available: Sequence[Challenge], completed: set[str]) -> str:
        print(UI.header("Lambda Calculus Game"))

        if not available:
            print("No challenges available yet.")
            return ""

        print("Available Challenges:")
        print("-" * 40)
        for index, challenge in enumerate(available, 1):
            status = "✓" if challenge.id in completed else " "
            print(f"{index}. [{status}] {challenge.name} ({challenge.id})")

        print("\nOptions:")
        print(f"{len(available) + 1}. Free Interpreter")
        print(f"{len(available) + 2}. Quit\n")
        return input("Enter your choice: ").strip()

    def show_invalid_menu_choice(self):
        print("Invalid choice. Please try again.")

    def show_goodbye(self):
        print("\nThanks for playing! Goodbye!")

    def show_challenge(
        self,
        challenge: Challenge,
        aliases: dict[str, Expr],
        completed: set[str],
    ):
        print(UI.header(f"Challenge: {challenge.name}"))
        print(UI.box(challenge.description, UI.WIDTH))

        if aliases:
            print(UI.section("Available Aliases (from completed challenges)"))
            for alias_id in sorted(aliases):
                print(f"  {alias_id}: {aliases[alias_id]}")

        print(UI.section("Requirements"))
        if challenge.requirements:
            for requirement in challenge.requirements:
                status = "✓" if requirement in completed else "✗"
                print(f"  [{status}] {requirement}")
        else:
            print("  None")

        print(UI.section("Your Solution"))
        print("(Enter empty line to switch to free interpreter)")

    def prompt_solution(self) -> str:
        return input("Enter your lambda expression: ").strip()

    def show_switch_to_free_interpreter(self):
        print("\n[Switching to free interpreter mode]")

    def show_test_results(self, results: list[dict]):
        print(UI.section("Test Results"))
        for index, result in enumerate(results, 1):
            status = "PASS" if result["passed"] else "FAIL"
            print(f"Test {index}: [{status}]")

            if result["error"]:
                print(f"  Error: {result['error']}")
            else:
                print(f"  Input:    {result['input']}")
                print(f"  Expected: {result['expected']}")
                print(f"  Got:      {result['actual']}")

                steps = result.get("steps")
                if steps:
                    print("\n  Reduction steps:")
                    for step in steps[:5]:
                        print(f"    {step.description}")
                        print(f"    → {step.expression}")
                    if len(steps) > 5:
                        print(f"    ... ({len(steps) - 5} more steps)")
            print()

    def show_challenge_completed(self, challenge_id: str, name: str):
        print(UI.box(f"✓ Challenge '{name}' completed!", UI.WIDTH))
        print(f"\nThe function '{challenge_id}' is now available as an alias.")

    def show_challenge_incomplete(self):
        print("Some tests failed. Try again!")

    def pause(self, prompt: str):
        input(prompt)

    def show_unknown_challenge(self, challenge_id: str):
        print(f"Challenge {challenge_id} not found.")

    def show_free_interpreter_intro(self):
        print(UI.header("Free Lambda Interpreter"))
        print("Enter lambda expressions to evaluate step-by-step.")
        print("(Use \\ for lambda, e.g., \\x.x for identity)\n")

    def show_alias_names(self, aliases: dict[str, Expr]):
        if aliases:
            print("Available aliases: " + ", ".join(sorted(aliases)))

    def prompt_expression(self) -> str:
        print("\n(Enter empty line to return to menu)")
        return input("Expression: ").strip()

    def show_reduction_steps(self, steps: Sequence[ReductionStep]):
        print(UI.section("Reduction Steps"))
        for step in steps[:20]:
            print(step.description)
            print(f"  → {step.expression}")
        if len(steps) > 20:
            print(f"... ({len(steps) - 20} more steps)")

    def show_final_result(self, result: Expr):
        print(UI.section("Final Result"))
        print(f"{result}\n")

    def show_error(self, error: Exception):
        print(f"\nError: {error}\n")
