def process_user_input(user_input):
    result = {
        "original": user_input,
        "length": len(str(user_input)),
        "upper": str(user_input).upper(),
        "lower": str(user_input).lower(),
        "stripped": str(user_input).strip(),
        "words": str(user_input).split(),
        "word_count": len(str(user_input).split()),
        "reversed": str(user_input)[::-1],
        "char_frequency": {},
    }

    for char in str(user_input):
        result["char_frequency"][char] = result["char_frequency"].get(char, 0) + 1

    return result


def process_multiple_inputs(*args):
    return [process_user_input(item) for item in args]


def process_with_transformation(user_input, transform_fn):
    processed = process_user_input(user_input)
    processed["transformed"] = transform_fn(str(user_input))
    return processed
