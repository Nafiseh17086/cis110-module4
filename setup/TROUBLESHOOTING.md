# Setup Troubleshooting

Find the problem that matches yours. If nothing here fixes it, run
`python setup/verify_environment.py`, copy **everything** it prints, and post
it to the Q&A discussion on Canvas.

---

## 1. Python is missing, or the version is too old

You need **Python 3.12 or later**.

**Windows**
1. Download the installer from [python.org/downloads](https://www.python.org/downloads/).
2. On the first screen of the installer, **tick "Add python.exe to PATH"**
   before clicking Install. This is the step people most often miss.
3. Close and reopen your terminal, then run `python --version`.

**macOS**
1. Download the installer from [python.org/downloads](https://www.python.org/downloads/).
2. Run it, then open a **new** Terminal window.
3. Use `python3` rather than `python`: `python3 --version`.

---

## 2. "python is not recognized" (Windows) — or typing `python` opens the Microsoft Store

Either Python was installed without the PATH box ticked, or Windows is
intercepting the command.

- **Quickest fix:** use the Windows launcher instead — type `py` wherever the
  instructions say `python`. For example: `py setup/verify_environment.py`.
- **If `python` opens the Microsoft Store:** go to *Settings → Apps → Advanced
  app settings → App execution aliases* and switch off the two entries named
  *python.exe* and *python3.exe*.
- **To fix it permanently:** run the python.org installer again, choose
  *Modify*, and make sure "Add Python to environment variables" is ticked.

---

## 3. ipykernel is missing

VS Code needs this small package to run notebooks. In a terminal:

```
python -m pip install ipykernel
```

(Use `python3` on macOS, or `py` on Windows.)

**If you see "externally-managed-environment" on macOS**, your Python came
from Homebrew. The simplest fix is to install Python from python.org as in
section 1 and use that one instead.

---

## 4. VS Code will not run the notebook, or asks you to "Select Kernel"

1. In VS Code, open the Extensions panel (the four-squares icon on the left).
2. Install **Python** and **Jupyter**, both published by Microsoft.
3. Reopen `lab4_text_analyzer.ipynb`.
4. Click **Select Kernel** in the top-right corner of the notebook, choose
   **Python Environments**, and pick the Python 3.12 you installed.

If the notebook opens as a wall of raw text instead of cells, the Jupyter
extension is missing — see step 2.

---

## 5. My cell seems frozen when it asks for input

When a cell runs `input()`, **VS Code shows the typing box at the very top of
the window**, above your notebook — not inside the cell. It is easy to miss.

Look up, type your answer into that box, and press Enter. The cell finishes
as soon as you do.

If you have lost track of it, click the **stop** square next to the cell and
run it again.

---

## 6. Nothing saves, or the self-check cannot find my notebook

You are probably working **inside the zip file** without extracting it first.

- **Windows:** right-click the zip → *Extract All* → open the extracted folder.
- **macOS:** double-click the zip; a normal folder appears beside it.

Then move that folder somewhere you own, such as *Documents*, and open it
from there in VS Code.

---

## 7. `python check_my_work.py` says it cannot find the notebook

Your terminal is not in the lab folder. In VS Code, the easiest fix is
*Terminal → New Terminal* while the lab folder is open — the terminal then
starts in the right place automatically.

Do not rename `lab4_text_analyzer.ipynb`; the self-check looks for that exact name.

---

## 8. A cell never finishes — it just keeps running

You have almost certainly written an **infinite loop**: a `while` loop whose
condition never becomes False.

1. Click the **stop / interrupt** button (■) at the top of the notebook, or next
   to the running cell.
2. Look at your loop. Something **inside** the loop must change the variable in
   the condition. For example, in `while value < limit:`, the loop body must
   change `value`.
3. Trace the first two or three times around the loop on paper. You will usually
   see the variable that never changes.

The self-check stops runaway loops automatically, and tells you which exercise
never finished.

---

## 9. The optional chart cell says matplotlib is missing

The chart cell in Lab 4 is **optional and not graded**. To use it, run this in a
terminal, then restart the notebook's kernel:

```
python -m pip install matplotlib
```

If VS Code still cannot find it, you probably installed it into a different
Python. Run the command using the same Python your notebook's kernel uses (see
section 3).

## 10. The self-check says `lab4_working_version.ipynb` not found

Part C needs a copy of your notebook saved **before** you ask an AI assistant.
In VS Code, open `lab4_text_analyzer.ipynb` and choose **File → Save As…**, and
save it in the **same folder** as `lab4_working_version.ipynb`. Keep working in
`lab4_text_analyzer.ipynb`, and do not edit the copy afterwards.
