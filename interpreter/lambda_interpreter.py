r"""
Lambda calculus interpreter with step-by-step reduction.
Supports backslash syntax for lambda: \x.body
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ExprType(Enum):
    VARIABLE = "var"
    LAMBDA = "lambda"
    APPLICATION = "app"


@dataclass
class Expr:
    """Base class for lambda expressions"""
    pass


@dataclass
class Var(Expr):
    """Variable: x, y, etc."""
    name: str
    
    def __repr__(self):
        return self.name


@dataclass
class Lambda(Expr):
    r"""Lambda abstraction: \x.body"""
    param: str
    body: Expr
    
    def __repr__(self):
        return f"\\{self.param}.{self.body}"


@dataclass
class App(Expr):
    r"""Application: func arg"""
    func: Expr
    arg: Expr
    
    def __repr__(self):
        func_str = str(self.func)
        arg_str = str(self.arg)
        
        # Add parens if needed for clarity
        if isinstance(self.func, Lambda):
            func_str = f"({func_str})"
        if isinstance(self.arg, (Lambda, App)):
            arg_str = f"({arg_str})"
        
        return f"{func_str} {arg_str}"


class Parser:
    r"""Parse lambda expressions with backslash syntax"""
    
    def __init__(self, text: str, aliases: Optional[Dict[str, Expr]] = None):
        self.text = text.strip()
        self.pos = 0
        self.aliases = aliases or {}
    
    def parse(self) -> Expr:
        """Parse a complete expression"""
        expr = self._parse_expr()
        if self.pos < len(self.text):
            raise SyntaxError(f"Unexpected characters at position {self.pos}: {self.text[self.pos:]}")
        return expr
    
    def _parse_expr(self) -> Expr:
        """Parse lambda abstraction or application"""
        return self._parse_app()
    
    def _parse_app(self) -> Expr:
        """Parse application (left-associative)"""
        expr = self._parse_atom()
        
        while self.pos < len(self.text) and self.text[self.pos] not in '.):':
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            expr = App(expr, self._parse_atom())
        
        return expr
    
    def _parse_atom(self) -> Expr:
        """Parse atomic expression: variable, lambda, or parenthesized expr"""
        self._skip_whitespace()
        
        if self.pos >= len(self.text):
            raise SyntaxError("Unexpected end of input")
        
        if self.text[self.pos] == '\\':
            return self._parse_lambda()
        elif self.text[self.pos] == '(':
            return self._parse_parens()
        else:
            return self._parse_var()
    
    def _parse_lambda(self) -> Lambda:
        r"""Parse lambda abstraction: \x.body"""
        self.pos += 1  # consume \
        self._skip_whitespace()
        
        # Parse parameter
        if self.pos >= len(self.text) or not self._is_var_char(self.text[self.pos]):
            raise SyntaxError(f"Expected variable after \\ at position {self.pos}")
        
        param = self._parse_identifier()
        self._skip_whitespace()
        
        if self.pos >= len(self.text) or self.text[self.pos] != '.':
            raise SyntaxError(f"Expected '.' after lambda parameter at position {self.pos}")
        
        self.pos += 1  # consume .
        body = self._parse_expr()
        
        return Lambda(param, body)
    
    def _parse_parens(self) -> Expr:
        """Parse parenthesized expression"""
        self.pos += 1  # consume (
        self._skip_whitespace()
        
        expr = self._parse_expr()
        
        self._skip_whitespace()
        if self.pos >= len(self.text) or self.text[self.pos] != ')':
            raise SyntaxError(f"Expected ')' at position {self.pos}")
        
        self.pos += 1  # consume )
        return expr
    
    def _parse_var(self) -> Expr:
        """Parse variable or alias"""
        name = self._parse_identifier()
        
        # Check if it's an alias
        if name in self.aliases:
            return self.aliases[name]
        
        return Var(name)
    
    def _parse_identifier(self) -> str:
        """Parse variable/alias name"""
        start = self.pos
        while self.pos < len(self.text) and self._is_var_char(self.text[self.pos]):
            self.pos += 1
        return self.text[start:self.pos]
    
    @staticmethod
    def _is_var_char(c: str) -> bool:
        """Check if character is valid in variable name"""
        return c.isalnum() or c == '_'
    
    def _skip_whitespace(self):
        """Skip whitespace"""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1


class Evaluator:
    """Evaluate lambda expressions with step-by-step reduction"""
    
    def __init__(self, aliases: Optional[Dict[str, Expr]] = None, max_steps: int = 10000):
        self.aliases = aliases or {}
        self.max_steps = max_steps
        self.steps: List[Tuple[Expr, str]] = []
    
    def evaluate(self, expr: Expr) -> Expr:
        """Evaluate expression and collect reduction steps"""
        self.steps = [(expr, "Initial expression")]
        
        step_count = 0
        while step_count < self.max_steps:
            if isinstance(expr, App) and isinstance(expr.func, Lambda):
                # Beta reduction
                new_expr = self._beta_reduce(expr.func, expr.arg)
                self.steps.append((new_expr, f"Beta reduction: ({expr.func.param}) applied to {expr.arg}"))
                expr = new_expr
                step_count += 1
            elif isinstance(expr, App):
                # Reduce the function first
                new_func = self._single_step(expr.func)
                if new_func is expr.func:
                    # Function doesn't reduce, try argument
                    new_arg = self._single_step(expr.arg)
                    if new_arg is expr.arg:
                        # Can't reduce further
                        break
                    expr = App(expr.func, new_arg)
                    self.steps.append((expr, "Reduce argument"))
                    step_count += 1
                else:
                    expr = App(new_func, expr.arg)
                    self.steps.append((expr, "Reduce function"))
                    step_count += 1
            else:
                # No more reductions possible
                break
        
        if step_count >= self.max_steps:
            raise RuntimeError(f"Evaluation exceeded maximum steps ({self.max_steps})")
        
        return expr
    
    def _single_step(self, expr: Expr) -> Expr:
        """Perform one reduction step, return same expr if no reduction possible"""
        if isinstance(expr, App) and isinstance(expr.func, Lambda):
            return self._beta_reduce(expr.func, expr.arg)
        elif isinstance(expr, App):
            new_func = self._single_step(expr.func)
            if new_func is not expr.func:
                return App(new_func, expr.arg)
            new_arg = self._single_step(expr.arg)
            if new_arg is not expr.arg:
                return App(expr.func, new_arg)
        return expr
    
    def _beta_reduce(self, lam: Lambda, arg: Expr) -> Expr:
        """Apply lambda to argument (beta reduction)"""
        return self._substitute(lam.body, lam.param, arg)
    
    def _substitute(self, expr: Expr, var: str, replacement: Expr) -> Expr:
        """Substitute var with replacement in expr"""
        if isinstance(expr, Var):
            return replacement if expr.name == var else expr
        elif isinstance(expr, Lambda):
            if expr.param == var:
                # Variable is bound by this lambda, don't substitute
                return expr
            if self._free_vars(replacement).intersection({expr.param}):
                # Need to alpha-convert to avoid capture
                fresh_param = self._fresh_var(expr.param, {var}, self._free_vars(replacement))
                new_body = self._substitute(expr.body, expr.param, Var(fresh_param))
                new_body = self._substitute(new_body, var, replacement)
                return Lambda(fresh_param, new_body)
            else:
                new_body = self._substitute(expr.body, var, replacement)
                return Lambda(expr.param, new_body)
        elif isinstance(expr, App):
            new_func = self._substitute(expr.func, var, replacement)
            new_arg = self._substitute(expr.arg, var, replacement)
            return App(new_func, new_arg)
        return expr
    
    @staticmethod
    def _free_vars(expr: Expr) -> set:
        """Get set of free variables in expression"""
        if isinstance(expr, Var):
            return {expr.name}
        elif isinstance(expr, Lambda):
            free = Evaluator._free_vars(expr.body)
            free.discard(expr.param)
            return free
        elif isinstance(expr, App):
            return Evaluator._free_vars(expr.func) | Evaluator._free_vars(expr.arg)
        return set()
    
    @staticmethod
    def _fresh_var(base: str, avoid: set, free_vars: set) -> str:
        """Generate a fresh variable name"""
        candidate = base
        counter = 0
        while candidate in avoid or candidate in free_vars:
            counter += 1
            candidate = f"{base}_{counter}"
        return candidate
    
    def format_steps(self) -> str:
        """Format evaluation steps for display"""
        lines = []
        for i, (expr, description) in enumerate(self.steps):
            lines.append(f"Step {i}: {description}")
            lines.append(f"  → {expr}")
        return "\n".join(lines)


def parse_and_eval(text: str, aliases: Optional[Dict[str, Expr]] = None) -> Tuple[Expr, List[Tuple[Expr, str]]]:
    """Parse and evaluate a lambda expression"""
    parser = Parser(text, aliases)
    expr = parser.parse()
    
    evaluator = Evaluator(aliases)
    result = evaluator.evaluate(expr)
    
    return result, evaluator.steps
