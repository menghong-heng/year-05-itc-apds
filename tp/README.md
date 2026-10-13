# APDS TP 01: Lecture Slides Summary

Course: Advance Programming for Data Science (APDS)  
Department: Department of Applied Mathematics and Statistics (AMS), Institute of Technology of Cambodia (ITC)  
Lecturer: Mr. VANN Visal  
Student: Heng Menghong (ID: e20220258)  
Date: October 13, 2026  

---

## Slide Content Overview

This document provides a text summary of the lecture slides presented during the TP 01 session. The lecture follows four main parts:

1. **Introduction** (Course repository setup and Git branch strategy)
2. **Clean Code, PEP 8, and Debugging** (Naming conventions, modules, packages, OOP structures, docstrings, clean code rules, and debugging techniques)
3. **Tips and Tricks to Help Ensure Your Code Follows PEP 8** (Modern autoformatting with Ruff and editor integration)
4. **Reference** (Recommended literature and official style guides)

---

## 1. Introduction

### Course and Git Repository Setup
The course Advance Programming for Data Science emphasizes writing reliable, maintainable code for data workflows. Version control with Git is introduced as the standard way to organize, track, and collaborate on software.

### Branching Architecture
Rather than putting all files onto a single branch, the repository uses a clean four-branch separation:
- `main`: Stores stable documentation, course guidelines, and the master syllabus index.
- `lectures`: Reserved for weekly lecture notes, slide breakdowns, and reading notes.
- `assignments`: Used for take-home assignments, problem sets, and graded homework submissions.
- `tp`: Dedicated to in-class laboratory practicals (Travaux Pratiques) and hands-on session summaries.

### Why Multi-Branching Matters in Teamwork
- Isolates different types of coursework so work in progress does not break stable documentation.
- Allows students to simulate standard industry Git workflows: creating feature branches, committing small logical increments, pushing to remote, and opening pull requests for review.

---

## 2. Clean Code, PEP 8, and Debugging

### 2.1 Clean Code Foundations
Clean code is code that is easy to read, easy to understand, and easy to maintain. According to the core philosophy of software craftsmanship:
- Code is read far more often than it is written.
- The primary goal of clean code is to minimize the time and mental effort needed for another programmer to understand what the code is doing.

### 2.2 PEP 8 Naming Conventions
Python provides standard naming rules under PEP 8 to make the role of each identifier clear at a glance:

| Category | Naming Style | Example | Notes |
| :--- | :--- | :--- | :--- |
| Variables | `snake_case` | `total_count`, `batch_size` | Lowercase letters separated by underscores |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` | All uppercase letters separated by underscores |
| Functions | `snake_case` | `calculate_average()`, `filter_records()` | Typically action verbs |
| Classes | `PascalCase` | `StudentRecord`, `DataPipeline` | Capitalized words without underscores |
| Methods | `snake_case` | `get_summary()`, `validate_id()` | Functions inside classes |
| Modules | `snake_case` | `data_cleaner.py`, `models.py` | Short lowercase filenames |
| Packages | lowercase | `analytics`, `dataprocessor` | Short lowercase directory names without underscores |
| Internal/Private | `_leading_underscore` | `_gpa`, `_is_cached` | Signals non-public attributes |

#### Practical Naming Rules:
- Avoid generic and meaningless names like `tmp`, `data`, `res`, `val`, `x`, `a`.
- Use domain-specific descriptive names like `student_records`, `filtered_results`.
- Attach units to variable names when applicable (`timeout_seconds`, `file_size_mb`).

### 2.3 Constants in Python
- Python does not have a built-in `const` keyword.
- By convention, constants are written in `UPPER_SNAKE_CASE` at the module level.
- In modern Python (3.8+), programmers use `typing.Final` to indicate to linters and type checkers that a value should never be reassigned.

### 2.4 Modules and Packages
- **Module**: A single Python file (`.py`) that contains related functions, classes, and variables.
- **Package**: A folder containing multiple Python modules along with an `__init__.py` file.
  - The `__init__.py` file marks the directory as a Python package.
  - Packages use the special `__all__` list inside `__init__.py` to declare which functions and classes are part of the public API.
  - Using modules and packages prevents large, messy single-file scripts and encourages code reuse.

### 2.5 Object-Oriented Concepts: Classes, Functions, and Methods
The slides review key distinctions in Python programming:
- **Function**: An independent block of code defined using `def` outside of any class.
- **Method**: A function defined inside a class that operates on objects or class state.

#### Types of Methods in Python:
1. **Instance Method**:
   - Takes `self` as the first parameter.
   - Accesses and modifies data belonging to a specific instance of the class.
2. **Class Method (`@classmethod`)**:
   - Takes `cls` as the first parameter.
   - Operates on the class level, commonly used as alternative constructors (for example, creating an object from a dictionary or JSON).
3. **Static Method (`@staticmethod`)**:
   - Does not take `self` or `cls`.
   - Acts as an ordinary helper function that is grouped inside the class namespace for logical organization.
4. **Properties (`@property` and `@setter`)**:
   - Allows attribute access with validation logic without having to write separate getter and setter methods.

### 2.6 Comments and Docstrings
- **Comments (`#`)**:
  - Should explain **why** something was done, not **what** the code already clearly shows.
  - Bad comments restate the obvious (e.g., `# increment count by 1`).
  - Good comments explain non-obvious reasoning, mathematical formulas, or edge cases.
- **Docstrings (`"""..."""`)**:
  - Follow the PEP 257 standard.
  - Placed at the very top of modules, classes, and functions.
  - Document the purpose of the function, the parameters (`Args`), what it returns (`Returns`), and what errors it might throw (`Raises`).

### 2.7 Clean Code Rules for Flow and Logic
- **Guard Clauses / Early Returns**: Instead of nesting multiple `if-else` blocks inside each other, check for invalid conditions or edge cases at the very top of the function and return immediately. This keeps the main logic flat and easy to read.
- **Single Responsibility**: A function or class should have one clear purpose. If a function is doing parsing, calculating, and printing all at once, it should be split into smaller focused functions.
- **Eliminate Magic Numbers**: Never use raw unexplained numbers in logic. Define them as named constants so their meaning is clear.

### 2.8 Debugging Techniques
The slides discuss practical ways to find and fix bugs:
- **Interactive Debugging with `breakpoint()`**:
  - Python 3.7+ includes the built-in `breakpoint()` function, which pauses execution and opens the `pdb` command-line debugger.
  - Common `pdb` controls: `n` (next line), `s` (step into function), `c` (continue running), `p <variable>` (print value), `q` (quit).
- **Structured Logging vs. Print Debugging**:
  - Relying solely on `print()` creates cluttered output that is hard to manage.
  - Using the standard `logging` library allows messages to be categorized by level (`INFO`, `WARNING`, `ERROR`) and includes timestamps.
- **Defensive Assertions**:
  - Using `assert` statements to check that assumptions remain true during execution (for example, confirming that a score is within a valid range).

---

## 3. Tips and Tricks to Help Ensure Your Code Follows PEP 8

### 3.1 Why Automated Tooling is Necessary
Manually checking indentation, whitespace, quote styles, and import order is time-consuming and inconsistent. Modern development relies on automated tools to enforce standards effortlessly.

### 3.2 Introduction to Ruff
The lecture introduces **Ruff**, a fast linter and code formatter written in Rust:
- It replaces several older tools at once (Flake8, Black, isort, and pyupgrade).
- It runs 10 to 100 times faster than legacy Python linters.
- It can both detect style issues and automatically fix them.

### 3.3 Basic Ruff Commands
- `ruff check .`: Scans the project files and lists all linting issues.
- `ruff check --fix .`: Automatically corrects fixable linting errors (such as unused imports or sorting imports).
- `ruff format .`: Formats code automatically to match standard PEP 8 formatting rules (indentation, line breaks, quotes).

### 3.4 Configuration via `pyproject.toml`
Instead of passing flags in the terminal every time, Ruff rules can be configured in a project configuration file (`pyproject.toml` or `ruff.toml`):
- Setting target Python version (e.g., `py310`).
- Setting maximum line length (commonly 88 characters).
- Selecting rule sets (pycodestyle errors, Pyflakes logic checks, isort import sorting).

### 3.5 Editor Integration
- Installing the Ruff extension in editors like VS Code.
- Enabling **Format on Save** so that code is automatically styled according to PEP 8 every time a file is saved.

---

## 4. References

1. **Dustin Boswell & Trevor Foucher (2011)**: *The Art of Readable Code*, O'Reilly Media.
2. **PEP 8**: *Style Guide for Python Code* ([peps.python.org/pep-0008](https://peps.python.org/pep-0008/)).
3. **PEP 257**: *Docstring Conventions* ([peps.python.org/pep-0257](https://peps.python.org/pep-0257/)).
4. **Ruff Official Documentation**: Fast Python linter and formatter ([docs.astral.sh/ruff](https://docs.astral.sh/ruff/)).
5. **APDS Lecture Slides Chapter 01 & TP 01**: Department of Applied Mathematics and Statistics, ITC (Lecturer: Mr. VANN Visal).
