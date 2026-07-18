import math

class CalculatorAgent:
    def execute(self, action: str, params: dict) -> str:
        expression = (
            params.get("expression", "") or
            params.get("calculation", "") or
            params.get("query", "")
        )

        if not expression:
            return "No math expression given da"

        return self.calculate(expression)

    def calculate(self, expression: str) -> str:
        try:
            # Clean up spoken math to Python math
            expr = expression.lower()
            expr = expr.replace("x", "*")
            expr = expr.replace("×", "*")
            expr = expr.replace("÷", "/")
            expr = expr.replace("squared", "**2")
            expr = expr.replace("cubed", "**3")
            expr = expr.replace("square root of", "math.sqrt")
            expr = expr.replace("sqrt", "math.sqrt")
            expr = expr.replace("pi", str(math.pi))
            expr = expr.replace("^", "**")

            # Safe eval — only math allowed
            allowed = {
                "__builtins__": {},
                "math": math,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "round": round,
                "pow": pow,
            }

            result = eval(expr, allowed)

            # Clean result display
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            return f"🧮 {expression} = {result}"

        except ZeroDivisionError:
            return "❌ Cannot divide by zero da!"
        except Exception as e:
            return f"❌ Couldn't calculate '{expression}' — try rephrasing da"