def format_indian_number(number):
    """
    Format the given number in the Indian numbering system.
    Example: 12345678 -> 1,23,45,678
    """
    num_str = str(int(number))
    is_negative = num_str.startswith('-')
    
    if is_negative:
        num_str = num_str[1:]
    
    if len(num_str) <= 3:
        formatted = num_str
    else:
        last_three = num_str[-3:]
        remaining = num_str[:-3]
        remaining = ','.join([remaining[max(i-2, 0):i] for i in range(len(remaining), 0, -2)][::-1])
        formatted = f"{remaining},{last_three}" if remaining else last_three

    return f"-{formatted}" if is_negative else formatted