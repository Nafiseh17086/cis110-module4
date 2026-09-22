"""
CIS 110 - Lab 4 self-check
==========================

Run this from the lab folder:

    python check_my_work.py

It reads your notebook, calls your functions with texts you have never seen,
and tells you which parts are working. It never changes your notebook.

This is a SELF-CHECK, not your grade. Part C (evaluating an AI refactor) is
graded by your instructor.
"""

import contextlib
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE / "lab4_text_analyzer.ipynb"
WORKING_COPY = HERE / "lab4_working_version.ipynb"
PROGRAM_MARKER = "LAB 4 PROGRAM"
STEP_LIMIT = 300_000          # lines of code before we assume an infinite loop


class StepLimit(Exception):
    pass


# --------------------------------------------------------------------------
# running student code safely
# --------------------------------------------------------------------------

def limited(func, *args):
    """Run func(*args), but stop it if it runs suspiciously long (infinite loop)."""
    count = [0]

    def tracer(frame, event, arg):
        if event == "line":
            count[0] += 1
            if count[0] > STEP_LIMIT:
                raise StepLimit()
        return tracer

    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return func(*args)
    finally:
        sys.settrace(None)


def fake_input(prompt=""):
    return ""


def strip_magics(src):
    return "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("!", "%")))


def explain(e):
    """Turn errors into advice a beginner can act on."""
    if isinstance(e, StepLimit):
        return ("never finished - probably an infinite loop. Check that every\n"
                "             loop moves forward, e.g. a while loop changes its condition.")
    if isinstance(e, NameError) and re.search(r"name '_{3,}' is not defined", str(e)):
        return "still has ____ blanks to fill in"
    if isinstance(e, NameError):
        return (f"uses a name Python does not know ({e}). Did you run the PROVIDED\n"
                "             cell, and spell every function name exactly as given?")
    if isinstance(e, SyntaxError):
        return f"has a typo Python cannot read (SyntaxError on line {e.lineno})"
    if isinstance(e, IndentationError):
        return f"has an indentation problem on line {e.lineno} - check your spaces"
    if isinstance(e, ZeroDivisionError):
        return "divided by zero - what happens when the text has no words?"
    if isinstance(e, IndexError):
        return "asked for a position that does not exist (IndexError) - empty list or string?"
    return f"stopped with an error: {type(e).__name__}: {e}"


def ascii_only(text):
    return str(text).encode("ascii", "replace").decode("ascii")


def cell_source(cell):
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def exercise_number(src):
    m = re.search(r"#\s*EXERCISE\s+(\d+)", src)
    return int(m.group(1)) if m else None


def load_notebook(path):
    """Run every code cell in order, the way Run All would. Returns (ns, errors, md_cells, program)."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    md_cells = [cell_source(c) for c in cells if c.get("cell_type") == "markdown"]
    code_cells = [cell_source(c) for c in cells if c.get("cell_type") == "code"]
    ns = {"__name__": "__lab4__", "input": fake_input}
    errors, program = {}, None
    for src in code_cells:
        if "# OPTIONAL" in src:
            continue
        if PROGRAM_MARKER in src:
            program = src
        count = [0]

        def tracer(frame, event, arg):
            if event == "line":
                count[0] += 1
                if count[0] > STEP_LIMIT:
                    raise StepLimit()
            return tracer

        try:
            code = compile(strip_magics(src), "<cell>", "exec")
            sys.settrace(tracer)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(code, ns)
            finally:
                sys.settrace(None)
        except Exception as e:
            n = exercise_number(src)
            if n and n not in errors:
                errors[n] = explain(e)
    return ns, errors, md_cells, program


def call(ns, name, *args):
    """Call the student's function; return (result, error-message-or-None)."""
    func = ns.get(name)
    if not callable(func):
        return None, f"no function called {name}() was found - keep the name exactly as given"
    try:
        return limited(func, *args), None
    except Exception as e:
        return None, explain(e)


def as_pairs(result):
    """Normalise [[word, count], ...] (tuples are fine too) for comparison."""
    try:
        return [[p[0], p[1]] for p in result]
    except Exception:
        return None


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.earned, self.possible, self.lines = 0, 0, []

    def check(self, points, passed, label, hint=""):
        self.possible += points
        if passed:
            self.earned += points
            self.lines.append(f"    PASS     {label}")
        else:
            self.lines.append(f"    NOT YET  {label}")
            if hint:
                self.lines.append(f"             hint: {ascii_only(hint)}")

    def heading(self, text):
        self.lines += ["", text]

    def note(self, text):
        self.lines.append(f"    {ascii_only(text)}")


class Tester:
    """Runs a group of calls and remembers the first thing that went wrong."""

    def __init__(self, ns):
        self.ns, self.problem = ns, None

    def expect(self, name, args, want, same=None):
        got, err = call(self.ns, name, *args)
        ok = err is None and (same(got, want) if same else got == want)
        if not ok and self.problem is None:
            shown = ", ".join(repr(a) if len(repr(a)) < 40 else repr(a)[:37] + "...'" for a in args)
            self.problem = (f"{name}({shown}) " +
                            (err if err else f"returned {got!r:.60}, expected {want!r:.60}"))
        return ok

    def all(self, checks):
        return all([c for c in checks])


# --------------------------------------------------------------------------
# the tests
# --------------------------------------------------------------------------

HIDDEN_TEXT = """Maps are older than writing. Long before anyone kept records, people
scratched rivers and hills into clay, bone and stone! A map is a promise: the
river bends here, the hill rises there, and the path between them is safe.
Why do we still trust maps? Because a good map leaves things out. It shows the
river, the hill and the path, and it forgets the rest. Every map is a choice
about what matters, and every choice leaves something out."""
HIDDEN_STOP = ["a", "and", "the", "is", "it", "we", "do", "are", "than", "into",
               "before", "anyone", "between", "them", "here", "there", "about", "what"]
HIDDEN_WORDS = 81
HIDDEN_AVG = 4.21
HIDDEN_TOP = [["map", 3], ["choice", 2], ["every", 2], ["hill", 2], ["leaves", 2],
              ["maps", 2], ["out", 2], ["path", 2], ["river", 2], ["because", 1]]
HIDDEN_LONGEST = ("A map is a promise: the river bends here, the hill rises there, "
                  "and the path between them is safe")


def part_a(r, ns, errors):
    def show_error(n):
        if n in errors:
            r.note(f"NOTE     your Exercise {n} cell {errors[n]}")

    # ---- Exercise 1 -------------------------------------------------------
    r.heading("Exercise 1 - List workout")
    show_error(1)
    t = Tester(ns)
    original = [3, 5, 7, 9]
    ok = t.all([
        t.expect("first_and_last", ([3, 5, 7, 9],), [3, 9]),
        t.expect("first_and_last", (["x"],), ["x", "x"]),
        t.expect("without_ends", ([3, 5, 7, 9],), [5, 7]),
        t.expect("without_ends", (["a", "b"],), []),
        t.expect("without_ends", (original,), [5, 7]),
    ]) and original == [3, 5, 7, 9]
    r.check(1, ok, "first_and_last and without_ends return the right NEW lists",
            t.problem or "without_ends must not change the list it is given - use a slice")
    items = [1, 2, 3]
    got, err = call(ns, "replace_first", items, 9)
    r.check(1, err is None and items == [9, 2, 3], "replace_first changes the list itself",
            err or f"after replace_first([1, 2, 3], 9) the list was {items} - "
                   "assign to items[0] instead of building a new list")

    # ---- Exercise 2 -------------------------------------------------------
    r.heading("Exercise 2 - Clean and build text")
    show_error(2)
    t = Tester(ns)
    ok = t.all([t.expect("clean_word", ("Hello!",), "hello"),
                t.expect("clean_word", ("WORLD",), "world"),
                t.expect("clean_word", ('"Wait,',), "wait")])
    r.check(1, ok, "clean_word: lowercase, punctuation off the ends",
            t.problem or "use lower() and strip(PUNCTUATION)")
    t = Tester(ns)
    ok = t.all([t.expect("clean_word", ("don't",), "don't"),
                t.expect("clean_word", ("(well-known).",), "well-known"),
                t.expect("clean_word", ("--",), ""),
                t.expect("clean_word", ("?!",), ""),
                t.expect("clean_word", ("it's.",), "it's")])
    r.check(1, ok, "clean_word: keeps inside punctuation, all-punctuation gives \"\"",
            t.problem or "strip() only removes characters from the two ends")
    t = Tester(ns)
    ok = t.all([t.expect("initials", ("ada lovelace",), "A.L."),
                t.expect("initials", ("grace brewster hopper",), "G.B.H."),
                t.expect("initials", ("  alan   turing ",), "A.T."),
                t.expect("initials", ("cher",), "C.")])
    r.check(1, ok, "initials builds \"A.L.\" style strings",
            t.problem or "split() the name, then add part[0].upper() + \".\" for each part")

    # ---- Exercise 3 -------------------------------------------------------
    r.heading("Exercise 3 - One of each pattern")
    show_error(3)
    t = Tester(ns)
    ok = t.all([t.expect("total_letters", (["ab", "cde"],), 5),
                t.expect("total_letters", ([],), 0),
                t.expect("total_letters", (["x", "x", "x", "x"],), 4)])
    r.check(1, ok, "accumulate: total_letters", t.problem or "add len(word) to total for every word")
    t = Tester(ns)
    ok = t.all([t.expect("first_starting_with", (["cat", "horse", "hen"], "h"), "horse"),
                t.expect("first_starting_with", (["hat", "cat"], "h"), "hat"),
                t.expect("first_starting_with", (["cat", "dog", "hen"], "h"), "hen"),
                t.expect("first_starting_with", (["cat", "dog"], "z"), ""),
                t.expect("first_starting_with", ([], "a"), "")])
    hint = t.problem or ""
    if "hen" in hint and "returned ''" in hint:
        hint += " - is your 'not found' return inside the loop? It belongs after it."
    r.check(1, ok, "search: first_starting_with finds the FIRST match, or \"\"", hint)
    t = Tester(ns)
    words = ["cat", "horse", "cow", "giraffe"]
    ok = t.all([t.expect("only_long", (words, 3), ["horse", "giraffe"]),
                t.expect("only_long", ([], 2), []),
                t.expect("only_long", (["abc", "abcd"], 3), ["abcd"])]) and words == ["cat", "horse", "cow", "giraffe"]
    r.check(1, ok, "filter: only_long keeps words LONGER than n, in order",
            t.problem or "build a new list - do not remove items from the one you are given")

    # ---- Exercise 4 -------------------------------------------------------
    r.heading("Exercise 4 - Name that pattern")
    show_error(4)
    want = {"pattern_a": "accumulate", "pattern_b": "search", "pattern_c": "filter", "pattern_d": "search"}
    wrong = [k[-1].upper() for k, v in want.items()
             if str(ns.get(k, "")).strip().lower() != v]
    r.check(2, not wrong, "all four snippets named correctly",
            f"look again at snippet(s) {', '.join(wrong)} - is it combining, stopping at the first, or keeping some?")


def part_b(r, ns, errors, quiet=False):
    """Part B tests. Returns points earned out of 10."""
    def show_error(n):
        if n in errors and not quiet:
            r.note(f"NOTE     your Exercise {n} cell {errors[n]}")

    # ---- Exercise 5 -------------------------------------------------------
    r.heading("Exercise 5 - Get the words")
    show_error(5)
    t = Tester(ns)
    ok = t.all([t.expect("get_words", ("The cat -- and THE dog!",), ["the", "cat", "and", "the", "dog"]),
                t.expect("get_words", ("Hello,   world.\nBye!",), ["hello", "world", "bye"])])
    r.check(1, ok, "splits and cleans every word",
            t.problem or "split() the text, then clean_word() each piece")
    t = Tester(ns)
    ok = t.all([t.expect("get_words", ("",), []),
                t.expect("get_words", ("-- ... !",), []),
                t.expect("get_words", ("Stop -- go",), ["stop", "go"])])
    r.check(1, ok, "leaves out pieces that clean to \"\"",
            t.problem or "only append a word if it is not empty")

    # ---- Exercise 6 -------------------------------------------------------
    r.heading("Exercise 6 - Count and average")
    show_error(6)
    t = Tester(ns)
    ok = t.all([t.expect("word_count", (HIDDEN_TEXT,), HIDDEN_WORDS),
                t.expect("word_count", ("",), 0),
                t.expect("word_count", ("one -- two",), 2)])
    r.check(1, ok, "word_count", t.problem or "count the words that get_words returns")
    t = Tester(ns)
    close = lambda got, want: isinstance(got, (int, float)) and abs(got - want) < 1e-9
    ok = t.all([t.expect("average_word_length", ("a bb",), 1.5, close),
                t.expect("average_word_length", ("I am here",), 2.33, close),
                t.expect("average_word_length", (HIDDEN_TEXT,), HIDDEN_AVG, close),
                t.expect("average_word_length", ("",), 0.0, close)])
    r.check(1, ok, "average_word_length, rounded to 2 decimals, 0.0 for empty text",
            t.problem or "total letters / number of words, then round(value, 2)")

    # ---- Exercise 7 -------------------------------------------------------
    r.heading("Exercise 7 - Top ten words")
    show_error(7)
    unordered = lambda got, want: (as_pairs(got) is not None and
                                   sorted(as_pairs(got)) == sorted(want))
    ordered = lambda got, want: as_pairs(got) == want
    t = Tester(ns)
    ok = t.all([t.expect("top_words", ("the cat sat on the mat the cat", ["the", "on"], 10),
                         [["cat", 2], ["mat", 1], ["sat", 1]], unordered),
                t.expect("top_words", ("Dog, dog. DOG!", [], 10), [["dog", 3]], unordered)])
    r.check(1, ok, "counts are right and stop words are left out",
            t.problem or "count with two side-by-side lists; skip a word if it is in stop_words")
    t = Tester(ns)
    ok = t.all([t.expect("top_words", ("pear apple pear fig apple pear kiwi", [], 10),
                         [["pear", 3], ["apple", 2], ["fig", 1], ["kiwi", 1]], ordered),
                t.expect("top_words", ("d c b a", [], 10), [["a", 1], ["b", 1], ["c", 1], ["d", 1]], ordered),
                t.expect("top_words", (HIDDEN_TEXT, HIDDEN_STOP, 10), HIDDEN_TOP, ordered)])
    r.check(1, ok, "highest count first, ties in alphabetical order",
            t.problem or "sort alphabetically first, then sort(key=by_count, reverse=True)")
    t = Tester(ns)
    twelve = "a b c d e f g h i j k l a"
    ok = t.all([t.expect("top_words", ("pear apple pear fig apple pear kiwi", [], 2),
                         [["pear", 3], ["apple", 2]], ordered),
                t.expect("top_words", (twelve, []), None,
                         lambda got, want: as_pairs(got) is not None and len(got) == 10
                         and as_pairs(got)[0] == ["a", 2]),
                t.expect("top_words", ("one two", [], 5), [["one", 1], ["two", 1]], ordered),
                t.expect("top_words", ("", [], 10), [], ordered)])
    r.check(1, ok, "returns at most n pairs (10 when n is not given)",
            t.problem or "return pairs[:n], and keep n=10 as the default in the def line")

    # ---- Exercise 8 -------------------------------------------------------
    r.heading("Exercise 8 - Longest sentence")
    show_error(8)
    t = Tester(ns)
    ok = t.all([t.expect("longest_sentence", ("Hi there. How are you today? Fine!",), "How are you today"),
                t.expect("longest_sentence", ("One. Two three four! Five six?",), "Two three four"),
                t.expect("longest_sentence", (HIDDEN_TEXT,), HIDDEN_LONGEST)])
    r.check(1, ok, "finds the sentence with the most words (. ! and ? all end one)",
            t.problem or "replace ! and ? with . then split('.')")
    t = Tester(ns)
    ok = t.all([t.expect("longest_sentence", ("Red fish. Blue fish.",), "Red fish"),
                t.expect("longest_sentence", ("Short one. This   one\nis  longer.",), "This one is longer"),
                t.expect("longest_sentence", ("",), "")])
    r.check(1, ok, "ties keep the first; spaces squeezed; empty text gives \"\"",
            t.problem or "only replace the longest when the new one is LONGER (> not >=)")

    # ---- Exercise 9 -------------------------------------------------------
    r.heading("Exercise 9 - Text bar chart")
    show_error(9)
    pairs = [["trail", 5], ["lake", 3], ["a", 1]]

    def chart_ok(got, want):
        if not isinstance(got, list) or len(got) != len(want):
            return False
        for line, (word, count) in zip(got, want):
            parts = str(line).split()
            if not parts or parts[0] != word or str(line).count("#") != count or parts[-1] != str(count):
                return False
        return True

    got, err = call(ns, "bar_chart", pairs)
    got_empty, err2 = call(ns, "bar_chart", [])
    ok = err is None and err2 is None and chart_ok(got, pairs) and got_empty == []
    problem = err or err2
    if not problem and not ok:
        if not isinstance(got, list):
            problem = f"bar_chart returned {type(got).__name__}, not a list of lines - return lines, do not print them"
        else:
            problem = (f"bar_chart([['trail', 5], ['lake', 3], ['a', 1]]) returned {got!r:.80}; "
                       "expected 3 lines like 'trail        ##### 5'")
    r.check(1, ok, "one line per pair: word, count # marks, count",
            problem or "return a LIST of strings; build each with f\"{word:<12} {'#' * count} {count}\"")

    # ---- Exercise 10 ------------------------------------------------------
    r.heading("Exercise 10 - The full report   (must run)")
    show_error(10)
    func = ns.get("analyze")
    if not callable(func):
        r.note("NOT YET  no analyze() function found - keep '# LAB 4 PROGRAM' in that cell")
    else:
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                limited_print(func, HIDDEN_TEXT, HIDDEN_STOP)
            text = out.getvalue()
            missing = [label for label, piece in [
                ("the word count", str(HIDDEN_WORDS)), ("the average", f"{HIDDEN_AVG:.2f}"),
                ("the top word 'map'", "map"), ("the bar chart", "###"),
                ("the longest sentence", "the river bends here")] if piece not in text]
            if missing:
                r.note("NOT YET  the report is missing " + ", ".join(missing))
            else:
                r.note("RUNS     prints the whole report correctly for a new text")
        except Exception as e:
            r.note(f"NOT YET  analyze() {explain(e)}")


def limited_print(func, *args):
    """Like limited(), but lets the function print."""
    count = [0]

    def tracer(frame, event, arg):
        if event == "line":
            count[0] += 1
            if count[0] > STEP_LIMIT:
                raise StepLimit()
        return tracer

    sys.settrace(tracer)
    try:
        return func(*args)
    finally:
        sys.settrace(None)


def part_c(r, md_cells):
    r.heading("Exercise 11 - Evaluate an AI refactor   (graded by your instructor)")

    def find(prefix):
        return next((m for m in md_cells if m.strip().startswith(prefix)), None)

    c1 = find("**C1.")
    if c1 is None:
        r.note("NOT FOUND  C1 - keep the **C1. ...** heading at the top of the cell")
    else:
        ticked = len(re.findall(r"^\s*[-*]\s*\[[xX]\]", c1, flags=re.M))
        r.note(f"{'DONE      ' if ticked >= 2 else 'NOT YET   '} C1 working version saved ({ticked} of 2 boxes ticked)")
    for tag, what in [("C2", "prompt"), ("C3", "suggestion, verbatim"), ("C4", "evaluation"), ("C5", "decision")]:
        cell = find(f"**{tag}.")
        if cell is None:
            r.note(f"NOT FOUND  {tag} - keep the **{tag}. ...** heading at the top of the cell")
        elif "Replace this sentence" in cell:
            r.note(f"NOT YET    {tag} {what} - still has the placeholder text")
        else:
            r.note(f"WRITTEN    {tag} {what}")
    if WORKING_COPY.exists():
        ns, errors, _, _ = load_notebook(WORKING_COPY)
        sub = Report()
        part_b(sub, ns, errors, quiet=True)
        r.note(f"FOUND      lab4_working_version.ipynb - its Part B scores "
               f"{sub.earned} / {sub.possible}")
        if sub.earned < sub.possible:
            r.note("           Your saved working version should pass Part B BEFORE you ask an AI.")
    else:
        r.note("NOT YET    lab4_working_version.ipynb not found - save it before Part C")


def main():
    if not NOTEBOOK.exists():
        print(f"Could not find {NOTEBOOK.name} next to this script.")
        print("Run check_my_work.py from inside the lab folder, and do not rename the notebook.")
        return 2
    ns, errors, md_cells, program = load_notebook(NOTEBOOK)
    r = Report()
    if "PUNCTUATION" not in ns or "STOP_WORDS" not in ns:
        r.note("NOTE     the PROVIDED cell did not run - do not change or delete it")
    part_a(r, ns, errors)
    a_earned = r.earned
    r.heading("---------- Part B: the Text Analyzer ----------")
    part_b(r, ns, errors)
    b_earned = r.earned - a_earned
    if b_earned < 10 and call(ns, "clean_word", "Hello!")[0] != "hello":
        r.note("NOTE     Part B uses your clean_word from Exercise 2 - fix that first.")
    part_c(r, md_cells)

    print("=" * 66)
    print("  CIS 110 - Lab 4 self-check")
    print("=" * 66)
    for line in r.lines:
        print(ascii_only(line))
    print()
    print("-" * 66)
    print(f"  Self-check: {r.earned} / {r.possible} points on the auto-checked exercises")
    print(f"              Part A {a_earned} / 10    Part B {b_earned} / 10")
    print("  Part C (15 points) is graded by your instructor.")
    print("-" * 66)
    return 0 if r.earned == r.possible else 1


if __name__ == "__main__":
    sys.exit(main())
