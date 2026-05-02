import sys

def process_untrusted_input():
    user_data = sys.stdin.read()
    result = eval(user_data)
    return result
