# Environment Setup Guide

This guide follows the same steps as the **Setting Up Python and VS Code**
screencast in Module 1. Use whichever you prefer — or both.

It takes about **20–30 minutes**. Do it before the first day of class.
If you get stuck, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

---

## Step 1 — Install Python 3.12 or later

### Windows
1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   the latest Python 3 installer.
2. Run it. On the **first screen**, tick **"Add python.exe to PATH"**.
   This is the step people most often miss.
3. Click **Install Now**.
4. Open a new **Command Prompt** and type `python --version`.
   You should see `Python 3.12` or higher.

### macOS
1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   the latest Python 3 installer for macOS.
2. Open it and follow the installer.
3. Open a new **Terminal** window and type `python3 --version`.
   You should see `Python 3.12` or higher.

> On macOS, always type `python3` where these instructions say `python`.

---

## Step 2 — Install Visual Studio Code

1. Go to [code.visualstudio.com](https://code.visualstudio.com/) and download
   VS Code for your system.
2. Install it with the default options. On Windows, ticking **"Add to PATH"**
   is helpful.

---

## Step 3 — Install the Python and Jupyter extensions

1. Open VS Code.
2. Click the **Extensions** icon on the left (four small squares).
3. Search for **Python** and install the one published by **Microsoft**.
4. Search for **Jupyter** and install the one published by **Microsoft**.

The Jupyter extension is what lets you open the lab notebooks (`.ipynb` files).

---

## Step 4 — Create your course folder

1. Make a folder called `CIS110` somewhere you own — **Documents** is ideal.
2. Download the Module 2 zip from Canvas and **extract it** into that folder:
   - Windows: right-click the zip → **Extract All**.
   - macOS: double-click the zip.
3. In VS Code, choose **File → Open Folder** and open the extracted
   `cis110-module4` folder.

> Never work from inside the zip file itself — your work will not save.

---

## Step 5 — Install the notebook package

In VS Code, open **Terminal → New Terminal**, then type:

```
python -m pip install -r requirements.txt
```

(`python3` on macOS, or `py` on Windows.)

---

## Step 6 — Run the verification script

In the same terminal, type:

```
python setup/verify_environment.py
```

Every line should say **PASS**. If any say **NOT YET**, follow the fix it
prints, or look it up in [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

**Still stuck?** Copy the whole output and post it to the **Q&A** discussion.
Please do this before the first sync session, so we can use the session to fix
anything left over.

---

## Step 7 — Open the lab

Click `lab4_text_analyzer.ipynb`. When VS Code asks you to **Select Kernel**,
choose **Python Environments**, then the Python 3.12 you installed.

You're ready.
