# AFTER: the version we kept - the suggestion ACCEPTED IN PART.
# Kept from the suggestion: sum() and max(), and looping over the scores directly.
# Not kept: squeezing everything into the return line, and the list comprehension.

def class_report(scores):
    """Return [average rounded to 1 decimal, highest score, list of scores below 70]."""
    average = sum(scores) / len(scores)
    highest = max(scores)

    below = []
    for score in scores:          # FILTER: keep the scores under 70, in order
        if score < 70:
            below.append(score)

    return [round(average, 1), highest, below]


if __name__ == "__main__":
    print(class_report([88, 64, 95, 71, 59]))    # [75.4, 95, [64, 59]]
