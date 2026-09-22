# BEFORE: a working but clumsy student-style solution.
# Used in the video "Refactoring with an AI Assistant: A Worked Example".
# It is correct - every test in compare.py passes - it is just harder to read than it needs to be.

def class_report(scores):
    """Return [average rounded to 1 decimal, highest score, list of scores below 70]."""
    total = 0
    for i in range(len(scores)):
        total = total + scores[i]
    average = total / len(scores)

    highest = scores[0]
    for i in range(len(scores)):
        if scores[i] > highest:
            highest = scores[i]

    below = []
    for i in range(len(scores)):
        if scores[i] < 70:
            below.append(scores[i])
        else:
            below = below

    return [round(average, 1), highest, below]


if __name__ == "__main__":
    print(class_report([88, 64, 95, 71, 59]))    # [75.4, 95, [64, 59]]
