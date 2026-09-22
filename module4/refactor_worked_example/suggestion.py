# THE AI SUGGESTION, pasted exactly as the assistant gave it (see ai_suggestion.md).
# Kept here only so compare.py can test it. It is NOT the version we kept.

def class_report(scores):
    average = sum(scores) / len(scores)
    return [round(average, 1), max(scores), [s for s in scores if s < 70]]
