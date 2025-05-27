import re

# Define unrecognized/bad symbols
BAD_SYMBOLS = {'@', '#', '$', '`', '~', '^'}

def is_unterminated_string(token):
    return token.startswith('"') and not token.endswith('"')

def is_invalid_identifier(token):
    # Only valid if it starts with letter or _, and alphanumeric or _ only
    return not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token)

def contains_unrecognized_symbols(token):
    return any(char in BAD_SYMBOLS for char in token)

def detect_errors(token_stream):
    """
    Input: list of (token, token_type, line_number)
    Output: list of {line, token, error}
    """
    errors = []

    for token, token_type, line in token_stream:
        if token_type != "UNKNOWN":
            continue

        if is_unterminated_string(token):
            errors.append({
                "line": line,
                "token": token,
                "error": "Unterminated string literal"
            })
        elif contains_unrecognized_symbols(token):
            errors.append({
                "line": line,
                "token": token,
                "error": "Unrecognized symbol(s)"
            })
        elif is_invalid_identifier(token):
            errors.append({
                "line": line,
                "token": token,
                "error": "Invalid identifier"
            })
        else:
            errors.append({
                "line": line,
                "token": token,
                "error": "Unknown or invalid token"
            })

    return errors

# Example test
if __name__ == "__main__":
    token_stream = [
        ("boot", "KEYWORD", 1),
        ("system", "IDENTIFIER", 1),
        ("@badtoken", "UNKNOWN", 2),
        ('"Unclosed string', "UNKNOWN", 3),
        ("123abc", "UNKNOWN", 4)
    ]

    error_list = detect_errors(token_stream)
    print("--- Error Report ---")
    if not error_list:
        print("No lexical errors found.")
    else:
        for err in error_list:
            print(f"Line {err['line']}: {err['error']} --> '{err['token']}'")