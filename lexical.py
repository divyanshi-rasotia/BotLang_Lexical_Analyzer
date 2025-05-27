import re

# Define BotLang keywords
KEYWORDS = {
    "boot", "shutdown", "ping", "beep", "set", "check", "else", "repeat",
    "stop", "go", "function", "end", "true", "false", "send"
}

# Token Patterns (simplified regex-based)
token_patterns = {
    "KEYWORD": r"^[a-zA-Z_][a-zA-Z0-9_]*$",
    "IDENTIFIER": r"^[a-zA-Z_][a-zA-Z0-9_]*$",
    "NUMBER": r"^[0-9]+(\.[0-9]+)?$",
    "STRING": r'^".*"$',
    "OPERATOR": r"^[+\-*/=<>!&|]+$",
    "DELIMITER": r"^[;{}(),]$"
}

# Delimiters used for token splitting
delimiters = r'(\s+|;|\{|\}|\(|\)|,|\+|\-|\|\/|=|<|>|!|\".*?\"|\n)'

# Symbol Table
symbol_table = []

# Function to classify a token
def classify_token(token):
    token = token.strip()
    if token == "":
        return None

    # Keywords take precedence
    if token in KEYWORDS:
        return "KEYWORD"

    if re.match(token_patterns["STRING"], token):
        return "STRING"

    if re.match(token_patterns["NUMBER"], token):
        return "NUMBER"

    if re.match(token_patterns["OPERATOR"], token):
        return "OPERATOR"

    if re.match(token_patterns["DELIMITER"], token):
        return "DELIMITER"

    if re.match(token_patterns["IDENTIFIER"], token):
        return "IDENTIFIER"

    return "UNKNOWN"

# Function to tokenize and analyze the code
def analyze_code(text):
    display_tokens = []      # For showing in UI, e.g. "token --> type"
    token_stream = []        # For error analysis: list of (token, token_type, line_num)
    suggestions = []
    lines = text.splitlines()

    for line_num, line in enumerate(lines, start=1):
        split_tokens = re.split(delimiters, line)
        for token in split_tokens:
            token = token.strip()
            if not token or token.isspace():
                continue

            token_type = classify_token(token)
            if token_type is None:
                continue

            display_tokens.append(f"{token}  -->  {token_type}")
            token_stream.append((token, token_type, line_num))

    return display_tokens, token_stream, suggestions

# Helper: Group tokens by their type from token_stream
def group_tokens_by_type(token_stream):
    grouped = {
        "KEYWORD": set(),
        "IDENTIFIER": set(),
        "NUMBER": set(),
        "STRING": set(),
        "OPERATOR": set(),
        "DELIMITER": set(),
        "UNKNOWN": set()
    }
    for token, token_type, _ in token_stream:
        if token_type in grouped:
            grouped[token_type].add(token)
        else:
            grouped["UNKNOWN"].add(token)
    # Convert sets to sorted lists for nicer display
    for key in grouped:
        grouped[key] = sorted(grouped[key])
    return grouped
