def evaluate_input(user_code):
    try:
        return eval(user_code)
    except Exception as e:
        return str(e)
