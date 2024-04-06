def is_positive(value):
    try:
        string_number = float(value)
    except ValueError:
        return False

    return string_number > 0
