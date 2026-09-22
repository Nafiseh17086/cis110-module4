# Module 4 — Videos and Media

All videos are captioned. Links are added on Canvas when each video is published.

---

## Refactoring with an AI Assistant: A Worked Example
**Module 4 · 5–6 minutes · screencast · [link on Canvas]**

The video starts from a **working but clumsy** student-style solution, asks an
AI assistant for **one** refactor, and walks through the evaluation out loud,
including the decision **not** to take part of the suggestion.

**Watch the process more than the code.** The modeled behavior is what Part C of
Lab 4 asks you to do:

1. **Before** asking: the original works and passes its tests.
2. **Asking:** one clear prompt that says *do not change what it returns*.
3. **Pulling the reply apart:** the assistant was asked for one change and
   offered three. Each is judged separately.
4. **Testing, not trusting:** the same tests are run on the old and new
   versions, plus a boundary case chosen on purpose.
5. **Deciding on readability *for this reader*:** shorter is not automatically
   clearer.
6. **Recording the decision** in the reflection.

**Follow along:** every file from the video is in
[`refactor_worked_example/`](refactor_worked_example/ai_suggestion.md). Run
`python compare.py` in that folder to see all three versions tested side by side.

**Takeaway:** an AI suggestion is a proposal, and you are the reviewer. "I
checked it and said no" is a professional result, not a failure.

---

## Three short explainers (about 1 minute each)

Vertical videos you can watch on your phone. Click a picture to open the video,
then use GitHub's **Download** button (or **View raw**) if it does not play in
the page. On Canvas they are embedded directly.

| | | |
|---|---|---|
| [![Why Programmers Must Still Learn to Write Code](videos/why_programmers_must_still_learn_to_write_code_poster.jpg)](videos/why_programmers_must_still_learn_to_write_code.mp4) | [![Why Reading AI Code Is Harder Than Writing It](videos/why_reading_ai_code_is_harder_than_writing_it_poster.jpg)](videos/why_reading_ai_code_is_harder_than_writing_it.mp4) | [![How to Write an AI Reflection Log](videos/how_to_write_an_ai_reflection_log_poster.jpg)](videos/how_to_write_an_ai_reflection_log.mp4) |
| **[Why Programmers Must Still Learn to Write Code](videos/why_programmers_must_still_learn_to_write_code.mp4)** · 1:07 | **[Why Reading AI Code Is Harder Than Writing It](videos/why_reading_ai_code_is_harder_than_writing_it.mp4)** · 1:17 | **[How to Write an AI Reflection Log](videos/how_to_write_an_ai_reflection_log.mp4)** · 1:08 |
| **Watch before:** Lab 4 Part A | **Watch before:** Lab 4 Part C | **Watch before:** AI-Use Reflection 4 |

### Why Programmers Must Still Learn to Write Code
A counting loop, `for i in range(len(my_list) - 1)`, looks right and quietly
skips the **last** item. Stepping through it with a trace table is what proves it.
**Connects to:** the off-by-one boundary questions in Exercises 3, 7 and 8.

### Why Reading AI Code Is Harder Than Writing It
A plausible-looking `while index > 1:` loop skips the **first** item of the
list. Reading code you did not write means tracing it yourself, not trusting
that it looks right.
**Connects to:** Part C, step 5: test the suggestion and design one test of
your own aimed at what it might break.

### How to Write an AI Reflection Log
Walks through a text-analyzer reflection: your **unassisted baseline**, the
**prompt and AI suggestion** (an "unverified claim" until you check it),
**evidence of verification** (run the tests *and* trace by hand, which is where
a case-sensitivity bug shows up: `"Apple"` vs `"apple"`), then the **rejection
and revision**.
**Connects to:** Part C and [AI-Use Reflection 4](../ai_use_reflection_4.md).
The video's four stages map onto your template's five fields: baseline → fields
1 and 3, suggestion → field 2, verification → field 3, decision → field 5.
In this course, "the tests" means `python check_my_work.py`.
