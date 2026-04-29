def evaluate_user_input(user_input):
    try:
        return eval(user_input)
    except Exception as e:
        return str(e)
