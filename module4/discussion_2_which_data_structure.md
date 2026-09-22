# Discussion 2: Which Data Structure, and Why — 20 points

> You have not formally met **dictionaries** or **sets** yet. That is
> intentional. Reason from **what the problem needs**, not from what you already
> know how to write. Module 5 will give you the tools.

## Three scenarios

**Scenario 1: the roster.** The registrar sends a class roster built from three
enrolment reports, so some students appear more than once:

```
Ana Diaz, Ben Okafor, Ana Diaz, Chen Wei, Ben Okafor, Dana Ruiz
```

You need each student exactly once.

**Scenario 2: the exam scores.** Scores arrive as students submit, and you must
be able to say later who submitted **first, second, third …**. Two students can
have the same score:

```
submitted in this order:  88, 92, 75, 92, 61
```

**Scenario 3: the lookup.** A program is given a student ID, such as `S1042`,
and must return the student's name, thousands of times a day, from a list of
about 12,000 students:

```
S1001 → Ana Diaz     S1002 → Ben Okafor     S1042 → Chen Wei   …
```

## Your initial post

For **each** scenario:

1. **Name the data structure** you would use. You may use Python's name for it
   (list, set, dictionary …) if you have read ahead, or describe it in plain
   words: *"a collection where each item can appear only once"*.
2. **Explain why**, pointing to the exact words in the scenario that drove your
   choice, such as *"exactly once"*, *"first, second, third"* or *"thousands of
   times a day"*.
3. **Say what would go wrong** with a plain list, or say why a plain list is fine.

**At least one scenario has a defensible second answer.** If you see it, argue
for it: say what would have to be true about the problem for the second answer
to be the better one.

Aim for 250–400 words in total.

## Instructions for interaction

- Post your initial response by **Thursday at 11:59 p.m. CT**.
- Respond to **at least two classmates** by **Sunday at 11:59 p.m. CT**, and
  choose **at least one who reached a different conclusion** than you did on the
  same scenario.
- In that reply, explain **what in the problem statement led each of you to a
  different structure**. You do not have to agree. You do have to find the
  exact point where your readings split.

## How it is graded — 20 points

| Criterion | Points |
|---|---|
| A choice for all three scenarios, each tied to specific words in the problem | 8 |
| What goes wrong with a plain list (or why it is fine) | 4 |
| A second defensible answer argued for at least one scenario | 3 |
| Two replies, one to a different conclusion, locating where the readings split | 5 |
