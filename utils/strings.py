def is_positive(value):
    try:
        string_number = float(value)
    except (ValueError, TypeError):
        return False

    return string_number > 0
