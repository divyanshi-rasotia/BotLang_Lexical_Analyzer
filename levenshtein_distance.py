import re

def levenshtein_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = list(range(n + 1))
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            insert_cost = previous_row[j] + 1
            delete_cost = current_row[j - 1] + 1
            replace_cost = previous_row[j - 1] + (a[j - 1] != b[i - 1])
            current_row[j] = min(insert_cost, delete_cost, replace_cost)
    return current_row[n]

def suggest_keywords(word, valid_keywords):
    # Find the keyword with the smallest Levenshtein distance
    closest_keyword = min(valid_keywords, key=lambda kw: levenshtein_distance(word, kw))
    return closest_keyword

def check_file_for_suggestions(file_path, botlang_keywords):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    suggestions = {}
    
    for line_number, line in enumerate(lines, start=1):
        # Extract all words, excluding content within double quotes (string literals)
        string_literals = re.findall(r'"(.*?)"', line)
        string_words = set()
        for s in string_literals:
            string_words.update(re.findall(r'\b\w+\b', s))

        tokens = re.findall(r'\b\w+\b', line)
        for token in tokens:
            # Skip tokens inside string literals or numeric or boolean literals
            if token in botlang_keywords or token in string_words or token.isdigit():
                continue
            if token in ["true", "false"]:
                continue
            # Suggest corrections only for unrecognized keywords
            if token not in botlang_keywords and token not in string_words:
                suggested = suggest_keywords(token, botlang_keywords)
                suggestions[(line_number, token)] = suggested

    return suggestions

# --- MAIN PART ---
botlang_keywords = [
    "boot", "shutdown", "ping", "beep", "set", "check", "else", "repeat",
    "stop", "go", "function", "end", "true", "false", "send"
]

file_path = "sample.txt"  # Replace with your file name

output = check_file_for_suggestions(file_path, botlang_keywords)

for (line_number, token), sugg in output.items():
    print(f"Line {line_number}: Unrecognized: '{token}' → Did you mean: {sugg}?")