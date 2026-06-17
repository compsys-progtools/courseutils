# Getting Python to Play Nice with Git Bash on Windows

This guide walks you through installing Git and Python on Windows (if you haven't already) and getting Python to actually work inside Git Bash—including fixing that annoying issue where the Python REPL just freezes up or refuses to open.

---

## Step 0: Install Git and Python

Already got both Git Bash and Python installed? Cool, jump straight to Step 1.

---

### Installing Git for Windows

1. Grab Git for Windows from the official site:  
   https://git-scm.com/download/win

2. Run the installer and stick with the default options unless you have a specific reason to change things.

3. Make sure Git Bash is selected during installation.

4. Once it's done, open Git Bash from the Start Menu.

Check that it installed correctly:

```bash
git --version
```

You should see something like:

```text
git version 2.x.x.windows.x
```

---

### Installing Python for Windows

1. Download Python from the official site:  
   **[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)**

2. Run the installer.

3. On the first screen, make sure you check this box:

```text
☑ Add Python to PATH
```

4. Hit Install Now.

Check that it works (in Command Prompt, not Git Bash yet):

```cmd
python --version
```

You should see:

```text
Python 3.x.x
```

If Python isn't recognized, restart your computer and give it another shot.

---

## Step 1: Open Git Bash

Fire up Git Bash from the Start Menu.

---

## Step 2: Navigate to Your Home Directory

```bash
cd ~
pwd
```

You should see:

```text
/c/Users/YourUsername
```

Or close and reopen Git Bash.

---

## Step 7: Verify Python Works

Check the Python version:

```bash
python --version
```

Start the Python shell:

```bash
python
```

You should see:

```text
Python 3.x.x (default, ...)
>>>
```

Exit Python:

```python
exit()
```

---

## Troubleshooting

### Python Command Not Found

* Make sure Python was installed with the "Add Python to PATH" option checked
* Double-check that the correct Python path was added to .bashrc
* Restart Git Bash after making changes

### Python REPL Freezes or Doesn't Accept Input

* Confirm the winpty alias exists in .bashrc
* Restart Git Bash

### Multiple Python Versions Installed

Check which Python Git Bash is actually using:

```bash
which python
```

---

## Quick Reference

| Task                 | Command          |
| -------------------- | ---------------- |
| Edit bash config     | nano ~/.bashrc   |
| Reload config        | source ~/.bashrc |
| Check Python version | python --version |
| Start Python shell   | python           |

---

## Related Reading

* **[https://prishitakapoor2.medium.com/configuring-git-bash-to-run-python-for-windows-a624aa4ae2c5](https://prishitakapoor2.medium.com/configuring-git-bash-to-run-python-for-windows-a624aa4ae2c5)**
* Git for Windows Documentation
* Python Official Documentation

