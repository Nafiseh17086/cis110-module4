# How to Complete an AI-Use Reflection

After every lab you submit a short AI-Use Reflection. It is worth **15 points
each week** — 150 points across the course — so it is worth doing well.

## Why you do this every week

Reflection turns "I used AI" into "I know *how* I used it, and whether it
helped." Over ten weeks, your reflections show you — and your instructor — how
your working habits change. In Module 10 you compare your last reflection with
your first.

## The five fields

| Field | What to write | Common mistake |
|---|---|---|
| **1. What I wrote on my own** | The parts you completed without AI. | Being vague — name the exercises or parts. |
| **2. What AI generated or suggested** | Anything an AI produced, and which tool. Paste exact prompts when the lab asks. | Leaving it blank. Write "none" if there was none. |
| **3. How I checked it was correct** | The *evidence* that your code works. | "It ran." Running is not the same as being correct. |
| **4. What I got wrong and how I fixed it** | At least one real moment where something failed. | Saying nothing went wrong. Something always does. |
| **5. The lab-specific question** | Answer the question given in that week's lab. | Answering a different question. |

## How it is graded — 15 points

| Criterion | Points |
|---|---|
| All five fields completed honestly | 5 |
| Field 3 describes specific evidence, not just "it worked" | 4 |
| Field 4 describes a real problem, how you noticed it, and what you changed | 4 |
| Field 5 answers the lab's question directly | 2 |

Honesty is never penalized. A reflection that says "I used AI and it gave me a
wrong answer that I didn't catch until the self-check" scores well. A reflection
that hides AI use is an integrity issue.

---

## A worked example

*This example is from a fictional student, for Lab 4 — a lab where AI was
permitted with disclosure: the same lab you are doing this week.*

> **Lab:** Lab 4 — Text Analyzer · **Permission level:** Assistance Permitted with Disclosure
>
> **1. What I wrote on my own**
> The whole working version: reading the text, counting words, the ten most
> frequent words, average word length, and the longest sentence. It passed all
> the provided tests before I used any AI.
>
> **2. What AI generated or suggested**
> I asked the course assistant: *"Suggest one refactor to make this code easier
> to read."* It suggested replacing my manual counting loop with
> `collections.Counter`.
>
> **3. How I checked it was correct**
> I ran the provided tests again after the change, and they still passed. I also
> tested a text where two words tie for most frequent, because I wanted to know
> whether `Counter` kept the tie in the same order as my loop. It did not — the
> order changed.
>
> **4. What I got wrong, and how I found and fixed it**
> My first longest-sentence function counted "Dr." as the end of a sentence. I
> found it because the longest sentence came out as three words, which was
> obviously wrong. I changed it to split only on a full stop followed by a space
> and a capital letter.
>
> **5. Lab question — what did you check before accepting the refactor?**
> I accepted half of it. `Counter` is clearer, so I kept it for counting. But
> because the tie order changed and the lab asks for a stable order, I kept my
> own code for the final ranking step.

**Why this example scores full marks:** every field is specific; field 3 names a
test the student designed themselves rather than just re-running; field 4 shows
how the bug was *noticed*; and field 5 explains a partial acceptance with a
concrete reason.

---

## Your template

Use [`ai_use_reflection_4.md`](../ai_use_reflection_4.md) in the main lab folder.
