def levenshtein_distance(a, b):
    # Basic implementation
    if len(a) < len(b):
        return levenshtein_distance(b, a)

    if len(b) == 0:
        return len(a)

    previous_row = range(len(b) + 1)
    for i, c1 in enumerate(a):
        current_row = [i + 1]
        for j, c2 in enumerate(b):
            insertions = previous_row[j + 1] + 1  
            deletions = current_row[j] + 1        
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def suggest_keywords(token, keywords, max_distance=2):
    token = token.lower()
    distances = [(kw, levenshtein_distance(token, kw)) for kw in keywords]
    distances.sort(key=lambda x: x[1])
    if distances and distances[0][1] <= max_distance:
        return distances[0][0]  # return a single closest keyword string
    return None


