import ast

def evaluate_user_input(user_input):
    try:
        return ast.literal_eval(user_input)
    except Exception:
        raise ValueError("Invalid input")

