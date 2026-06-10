#!/usr/bin/env python3
"""Quick test of the lambda interpreter"""

from interpreter.lambda_interpreter import parse_and_eval

# Test identity
print("Test 1: Identity function")
expr = r"\x.x"
result, steps = parse_and_eval(expr)
print(f"  Expression: {expr}")
print(f"  Result: {result}")
print()

# Test identity applied to a variable
print("Test 2: Identity applied to 'apple'")
expr = r"(\x.x) apple"
result, steps = parse_and_eval(expr)
print(f"  Expression: {expr}")
print(f"  Reduction steps:")
for step_expr, desc in steps:
    print(f"    {desc}: {step_expr}")
print(f"  Result: {result}")
print()

# Test TRUE function
print("Test 3: TRUE function (\\x.\\y.x)")
expr = r"(\x.\y.x) first second"
result, steps = parse_and_eval(expr)
print(f"  Expression: {expr}")
print(f"  Reduction steps:")
for step_expr, desc in steps:
    print(f"    {desc}: {step_expr}")
print(f"  Result: {result}")
print()

print("All tests completed!")
