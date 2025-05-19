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
delimiters = r'(\s+|;|\{|\}|\(|\)|,|\+|\-|\|\/|=|<|>|!|\".?\"|\n)'

# Symbol Table
symbol_table = []

# Function to classify a token
def classify_token(token):
    token = token.strip()
    if token == "":
        return None

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
def analyze_code(filepath):
    with open(filepath, 'r') as file:
        line_num = 1
        for line in file:
            print(f"\nLine {line_num}: {line.strip()}")
            tokens = re.split(delimiters, line)
            for token in tokens:
                token = token.strip()
                if not token or token.isspace():
                    continue

                token_type = classify_token(token)
                if token_type:
                    symbol_table.append((token, token_type))
                    print(f"  {token:15} --> {token_type}")
            line_num += 1

# Main
if __name__ == "__main__":
    source_file = "sample_for_lexicalanalysis.txt" 
    analyze_code(source_file)

    print("\n--- Symbol Table ---")
    for lexeme, token_type in symbol_table:
        print(f"{lexeme:15} : {token_type}")


        