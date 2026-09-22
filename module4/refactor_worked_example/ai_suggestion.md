# The AI suggestion and the decision — a worked example

This is the written record behind the video **Refactoring with an AI Assistant:
A Worked Example**. It is laid out exactly like Part C of Lab 4, so you can see
what a full-credit evaluation looks like. The code is **not** from Lab 4. It is
an instructor-written stand-in for a student's working solution.

| File | What it is |
|---|---|
| [`before.py`](before.py) | The working but clumsy original |
| [`suggestion.py`](suggestion.py) | The assistant's suggestion, exactly as given |
| [`after.py`](after.py) | What we kept: the suggestion **accepted in part** |
| [`compare.py`](compare.py) | Runs the same tests against all three versions |

---

**C1. Working version saved.** `before.py` passed every test before the assistant
was asked anything.

**C2. The prompt**

> Here is a Python function I wrote and tested. Suggest ONE refactor that would
> make it easier to read. Do not change what it returns. Explain the change in
> plain language.

**C3. The suggestion, verbatim**

````
Your function works, but it loops over the list three times using indexes. Python
has built-in functions for this. Here is a more concise version:

def class_report(scores):
    average = sum(scores) / len(scores)
    return [round(average, 1), max(scores), [s for s in scores if s < 70]]

sum() adds the list, max() finds the highest value, and the list comprehension
builds the list of low scores in one line. It returns exactly the same result.
````

Notice that the assistant was asked for **one** refactor and gave three, all
combined into one change. That is common, and it is a reason to pull the
suggestion apart before you decide.

**C4. Evaluation**

1. **Correctness.** `python compare.py` runs five tests against all three
   versions, and every test agrees. The test that mattered most was
   `[70, 70, 70]`: the boundary between "below 70" and "70 or above" is where a
   rewrite could slip, and it did not. I also checked the empty list, which the
   assistant did not mention. All three versions crash on it. The suggestion did
   not break anything, but it did not fix that either.
2. **Readability.** Replacing the first two loops with `sum()` and `max()` is
   clearly better: each name says exactly what it does. `for score in scores`
   is better than `for i in range(len(scores))` because we never needed `i`.
   Deleting `else: below = below` removes a line that did nothing. **But** the new
   `return` line now does three jobs at once, and the average, the highest score
   and the low scores no longer have names. When something is wrong, named
   variables are what you print.
3. **Understanding.** I can explain every piece. The list comprehension is fine
   for experienced readers, but the plain loop says *filter* in a way a Module 4
   reader recognizes immediately.

**C5. Decision — Accepted in part**

Kept `sum()` and `max()`, and looping over the scores directly. Did **not** keep
the single-line `return` or the list comprehension: the named variables and the
visible filter loop are easier to read and easier to debug. The behavior is
unchanged, and `compare.py` proves it.
