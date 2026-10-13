# APDS TP 01: Lecture Slides Summary

Course: Advance Programming for Data Science (APDS)  
Department: Department of Applied Mathematics and Statistics (AMS), Institute of Technology of Cambodia (ITC)  
Lecturer: Mr. VANN Visal  
Student: Heng Menghong (ID: e20220258)  
Date: October 13, 2026  

---

## Slide Content Agenda

Based on the classroom lecture slides:

1. **Introduction**
2. **Clean Code, PEP 8, and Debugging**
3. **Tips and Tricks to Help Ensure Your Code Follows PEP 8**
4. **Reference**

---

## 1) Introduction: Core Python Building Blocks

The introduction of the lecture focused on the fundamental building blocks of Python programs and how to structure code properly:

- **Variables**: Named locations in memory used to store data values. In Python, variables are dynamically typed and should be named using lowercase letters separated by underscores (`snake_case`, e.g., `student_count`, `total_score`).
- **Constants**: Values that are not intended to change during program execution. Python has no native constant keyword, so constants are indicated by convention using all uppercase letters (`UPPER_SNAKE_CASE`, e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`).
- **Functions**: Reusable blocks of code defined with `def` that take inputs (arguments), perform a set of actions, and return an output.
- **Classes**: Blueprints for creating objects that bundle data (attributes) and functionality together. Class names follow `PascalCase` (e.g., `StudentRecord`, `DataAnalyzer`).
- **Methods**: Functions that are defined inside a class and belong to objects created from that class. They typically take `self` as their first parameter to access the object's data.
- **Modules**: A single Python file (`.py`) containing variables, functions, and class definitions that can be imported and reused in other scripts.
- **Packages**: A directory containing multiple Python modules and an `__init__.py` file, allowing larger projects to be organized into clean, reusable namespaces.

---

## 2) Clean Code, PEP 8, and Debugging

### Clean Code Principles
- **Readability**: Code should be written so that any teammate can read and understand it quickly without needing extra explanation.
- **Breaking Down Long Functions**: If a function becomes too long or tries to do multiple tasks at once, break it down into smaller, focused helper functions where each function has a single, clear responsibility.
- **Naming Conventions**: Choose clear, descriptive names that state the purpose of the variable or function. Avoid single-letter or vague names like `x`, `tmp`, `data`, or `res`.
- **Comments**:
  - Explain the **why** behind non-obvious logic, not what the code already clearly shows.
  - Do not write redundant comments that merely repeat the code.
- **Docstrings**:
  - Use triple-quoted strings (`"""..."""`) at the beginning of functions, classes, and modules.
  - Briefly summarize what the function does, its parameters, and its return value.
- **Control Flow**: Avoid deeply nested `if/else` ladders by using early returns (guard clauses) to exit immediately on invalid input or error conditions.

### PEP 8 Guidelines (Style Guide for Python Code)

PEP 8 is the official style guide for writing Python code. Its core philosophy is that code readability is paramount, and consistency across projects allows programmers to understand each other's code effortlessly.

#### 1. Code Layout and Line Length
- **Indentation**: Use exactly 4 spaces per indentation level. Never use or mix tabs.
- **Maximum Line Length**: Limit all lines to a maximum of 79 characters (or 88 characters under modern Black/Ruff standards). This allows multiple files to be opened side-by-side in split editors without horizontal scrolling.
- **Line Breaks Around Operators**: When breaking long mathematical or logical expressions across multiple lines, break **before** the binary operator (Knuth's style), keeping the operator with its operand:
  ```python
  total_score = (
      assignment_score
      + midterm_score
      + final_exam_score
  )
  ```
- **Blank Lines Structure**:
  - Separate top-level classes and functions with **2 blank lines**.
  - Separate methods inside a class with **1 blank line**.
  - Use single blank lines inside functions sparingly to separate distinct logical steps.

#### 2. Imports Organization and Grouping
- **Placement**: All imports must be placed at the very top of the file, immediately after any module-level docstrings, and before module constants.
- **Separate Lines**: Each import should be on its own line:
  ```python
  # Good
  import os
  import sys

  # Avoid
  import os, sys
  ```
- **Three-Block Grouping Order**: Imports must be grouped in this exact order, separated by a single blank line:
  1. **Standard Library Imports** (e.g., `os`, `sys`, `math`, `logging`, `typing`)
  2. **Related Third-Party Imports** (e.g., `numpy`, `pandas`, `requests`)
  3. **Local Application / Module Imports** (e.g., `from models import StudentRecord`)
- **Avoid Wildcard Imports**: Never use `from module import *`. Wildcards pollute the global namespace, hide where functions originate, and confuse linters.

#### 3. Whitespace Rules in Expressions
- **Binary Operators**: Always surround assignment (`=`), comparisons (`==`, `!=`, `<`, `>`), and arithmetic (`+`, `-`, `*`, `/`) operators with a single space on both sides (`total = count + 1`).
- **Keyword Arguments / Defaults**: Do **not** use spaces around the `=` sign when defining default parameter values or passing keyword arguments:
  ```python
  def connect(host, port=8080, timeout=30):
      ...
  ```
- **Parentheses, Brackets, and Braces**: Do not put spaces immediately inside opening or before closing delimiters:
  ```python
  # Good
  scores = [90, 85, 78]
  print(scores[0])

  # Avoid
  scores = [ 90, 85, 78 ]
  print( scores[ 0 ] )
  ```
- **Commas and Colons**: Never put space before a comma or colon; always put a space immediately after (`(x, y)` and `{key: value}`).
- **Function Calls**: Never put space between the function name and the open parenthesis (`calculate(a, b)` not `calculate (a, b)`).

#### 4. Quotes and String Literals
- In Python, single quotes `'...'` and double quotes `"..."` work identically. Choose one style and keep it consistent throughout the project.
- For docstrings, PEP 8 and PEP 257 strictly mandate triple double-quotes: `"""..."""`.
- When a string contains quotes, use the alternative quote to avoid ugly backslash escaping (e.g., `"It's easy"` instead of `'It\'s easy'`).

#### 5. Pythonic Programming Idioms and Best Practices
- **Comparing to `None`**: Always compare singletons like `None` using `is` or `is not`, never equality operators:
  ```python
  # Good
  if result is None:
      ...

  # Bad
  if result == None:
      ...
  ```
- **Testing for Emptiness**: For Python sequences (lists, tuples, strings, dictionaries), use the fact that empty sequences are inherently falsy:
  ```python
  # Good
  if not student_records:
      ...

  # Bad
  if len(student_records) == 0:
      ...
  ```
- **Boolean Comparisons**: Never compare boolean variables to `True` or `False` using `==`:
  ```python
  # Good
  if is_passed:
      ...

  # Bad
  if is_passed == True:
      ...
  ```
- **Exception Catching**: Always catch specific exceptions (`except (ValueError, KeyError):`), and avoid bare `except:` clauses which accidentally catch `SystemExit` and `KeyboardInterrupt`.

### Debugging Techniques
- **Checking Errors and Reading Tracebacks**:
  - When Python throws an error, the traceback shows the call stack, the exact line number where the failure happened, and the error type (`TypeError`, `ValueError`, `KeyError`, `IndexError`).
  - Reading the bottom line of the traceback first gives the immediate error reason.
- **Logging vs. Print**:
  - Relying on `print()` statements for debugging can clutter code and output.
  - Using Python's built-in `logging` module allows tracking events with severity levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) and can be easily turned on or off without deleting code lines.
- **Error Handling**: Using `try ... except` blocks to anticipate and handle expected runtime issues gracefully instead of letting the script crash unexpectedly.
- **Breakpoints**: Python provides the built-in `breakpoint()` function to pause code execution at a specific line and open an interactive debugging session (`pdb`) to inspect variables and step through code.

---

## 3) Tips and Tricks to Help Ensure Your Code Follows PEP 8

### 3.1 Indentation Style
- **4 Spaces per Level**: Always use exactly 4 spaces per indentation level. Never use tabs.
- **Never Mix Tabs and Spaces**: Python 3 disallows mixing tabs and spaces for indentation; using spaces uniformly prevents unexpected `IndentationError` bugs across different operating systems.
- **Continuation Lines**: When wrapping long lines across multiple lines, align wrapped arguments with the opening delimiter or use a hanging indent with an extra 4 spaces.

### 3.2 Spacing and Whitespace Rules
- **Spaces Around Operators**: Surround binary operators (`=`, `+=`, `==`, `<`, `>`, `+`, `-`, `*`, `/`) with a single space on each side (`x = a + b`).
- **No Extraneous Spaces**: Avoid putting spaces immediately inside parentheses, brackets, or braces (write `spam(ham[1], {eggs: 2})`, not `spam( ham[ 1 ], { eggs: 2 } )`).
- **Commas and Colons**: Do not place a space before a comma or colon; always place one space after (`[1, 2, 3]` and `{key: value}`).
- **Blank Lines Rhythm**:
  - Use **2 blank lines** to surround top-level function and class definitions.
  - Use **1 blank line** between method definitions inside a class.
  - Use blank lines sparingly inside functions to separate logical paragraphs or phases of computation.

### 3.3 Capitalization Rules
- **Classes**: Use **Capitalized Words** (`PascalCase` / `CapWords`), where every word starts with a capital letter (e.g., `StudentRecord`, `DataAnalyzer`).
- **Constants**: Use all **Capital Letters** (`UPPER_SNAKE_CASE`) with underscores for values that remain constant (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `PI`).
- **Comments**: Always start a block comment or inline comment with a **Capital letter** and format it as a complete sentence (`# Filter out invalid records before computing GPA.`).
- **Docstrings**: Capitalize the first letter of the docstring summary line and conclude it with a period (`"""Calculate the average GPA across all student records."""`).

### 3.4 Automating PEP 8 with Ruff
Manually checking indentation, whitespace, and capitalization across multiple files is tedious. The lecture introduced **Ruff** as a fast tool to enforce and autoformat these rules:

1. **Install Ruff**:
   ```bash
   pip install ruff
   ```

2. **Autoformat Code**:
   ```bash
   ruff format .
   ```
   This automatically fixes indentation, spacing, quotes, and line breaks across all Python files in the directory to match PEP 8.

3. **Check and Fix Style Issues**:
   ```bash
   ruff check --fix .
   ```
   Detects common style issues (like unused imports or wrong spacing) and automatically fixes them.

### 3.5 Editor Integration
- Use code editors like VS Code with the Ruff extension.
- Enable **Format on Save** so your code is automatically formatted according to PEP 8 every time you save a file.

---

## 4) Reference

- **Dustin Boswell & Trevor Foucher (2011)**: *The Art of Readable Code*, O'Reilly Media.
- **PEP 8**: *Style Guide for Python Code* ([peps.python.org/pep-0008](https://peps.python.org/pep-0008/)).
- **PEP 257**: *Docstring Conventions* ([peps.python.org/pep-0257](https://peps.python.org/pep-0257/)).
- **Python Official Documentation**: [docs.python.org](https://docs.python.org/)
- **Ruff Documentation**: [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- **Course Slides**: Department of Applied Mathematics and Statistics, ITC (Lecturer: Mr. VANN Visal).
