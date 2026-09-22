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
