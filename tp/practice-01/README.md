# APDS TP 01: Git Workflow, Clean Code, PEP 8, and Modern Tooling with Ruff

Comprehensive laboratory recap for **Travaux Pratiques 01 (TP 01)** in **Advance Programming for Data Science (APDS)**, Department of Applied Mathematics and Statistics (AMS), Institute of Technology of Cambodia (ITC).

---

## Laboratory Overview and Metadata

- **Course**: Advance Programming for Data Science (APDS)
- **Academic Year**: Year 05, Semester 01 (2026-2027)
- **Lecturer**: Mr. VANN Visal
- **Student**: Heng Menghong (ID: e20220258)
- **Repository**: [https://github.com/menghong-heng/year-05-itc-apds.git](https://github.com/menghong-heng/year-05-itc-apds.git)
- **Lab Session Date**: October 13, 2026
- **Class Slide Agenda**:
  1. Introduction & Multi-Branch Git Architecture
  2. Clean Code, PEP 8, and Debugging
  3. Tips and Tricks to Help Ensure Your Code Follows PEP 8
  4. References and Tooling

---

## 1. Introduction: Git Repository Architecture and Multi-Branch Strategy

In modern software development and data science pipelines, version control is the baseline for reproducibility, team collaboration, and release integrity.

### 1.1 Central Repository Architecture

The course repository is structured across five dedicated branches, each with a strict responsibility boundary:

```
year-05-itc-apds/
|-- main                  Production-ready documentation, course index, and milestones
|-- lectures              Lecture summaries, slide breakdowns, and theoretical notes
|-- tp                    Travaux Pratiques (TP) lab sessions and hands-on exercises
|-- assignments           Formal coursework assignments, problem sets, and submissions
`-- projects              Term projects, midterm prototypes, and final capstone
```

### 1.2 Essential Git Workflow Commands

```bash
# 1. Initialize local repository and set default branch
git init -b main

# 2. Add remote repository URL
git remote add origin https://github.com/menghong-heng/year-05-itc-apds.git

# 3. Create and switch to a dedicated TP session branch
git switch tp
git switch -c tp-01-practice

# 4. Stage changes, commit with descriptive message, and push
git add .
git commit -m "feat(tp01): complete Git recap, clean code, and Ruff tooling"
git push -u origin tp-01-practice

# 5. Syncing and pulling updates from remote
git switch main
git pull origin main
```

---

## 2. Clean Code, PEP 8, and Debugging

### 2.1 Variables and Naming Conventions

PEP 8 defines specific naming conventions to visually communicate the role and scope of every identifier:

| Identifier Type | Convention | Example | Description |
| :--- | :--- | :--- | :--- |
| **Variables** | `snake_case` | `student_count`, `batch_size` | Lowercase words separated by underscores. |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_BATCH_SIZE`, `MAX_RETRIES` | Uppercase words separated by underscores. |
| **Functions** | `snake_case` | `calculate_average_gpa()` | Verb-first, lowercase words. |
| **Classes** | `PascalCase` | `StudentRecord`, `BatchProcessor` | Capitalized words without underscores. |
| **Methods** | `snake_case` | `is_honor_roll()`, `add_record()` | Instance and class methods. |
| **Private/Internal** | `_leading_underscore` | `_gpa`, `_records` | Signals internal implementation detail. |

#### Principles from *The Art of Readable Code*:
1. **Pack Information into Names**: Avoid ambiguous generic names like `tmp`, `data`, `res`, `var`, or single-letter names (`x`, `d`). Use specific domain names like `student_records`, `unfiltered_ratings`.
2. **Attach Units and Attributes**: When variables carry specific units or states, encode them explicitly:
   - `timeout_seconds` instead of `timeout`
   - `max_payload_mb` instead of `max_size`
   - `is_authenticated` instead of `auth`

---

### 2.2 Constants and Scoping

Python does not feature a native language keyword like `const`. In modern Python (3.8+), we enforce constant intent using:
1. `UPPER_SNAKE_CASE` naming convention.
2. `typing.Final` annotation for static type checkers (`mypy` / IDEs).

```python
from typing import Final

# Module-level immutable constants
DEFAULT_BATCH_SIZE: Final[int] = 64
MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.0
SUPPORTED_FORMATS: Final[tuple[str, ...]] = ("json", "csv", "parquet")
```

---

### 2.3 Modules and Packages Architecture

- **Module**: A single Python source file (`.py`) containing related functions, classes, and constants (e.g., `constants.py`, `models.py`).
- **Package**: A directory containing multiple modules and an `__init__.py` file. The `__init__.py` initializes the package and specifies the public API via `__all__`.

#### Package Structure in TP 01:
```
tp/practice-01/
`-- data_processor/
    |-- __init__.py          # Exposes public API via __all__
    |-- constants.py         # System constants with typing.Final
    |-- models.py            # StudentRecord, BatchProcessor classes
    `-- utils.py             # Pure utility functions and guard clauses
```

#### Clean Import Conventions:
```python
# Absolute imports (Recommended for clarity)
from data_processor.constants import DEFAULT_BATCH_SIZE
from data_processor.models import StudentRecord

# Controlling exports in __init__.py
__all__ = ["StudentRecord", "BatchProcessor", "DEFAULT_BATCH_SIZE"]
```

> [!CAUTION] Avoid Wildcard Imports
> Never write `from data_processor import *`. Wildcard imports pollute the namespace, obscure where names originate, and trigger linting errors in Ruff.

---

### 2.4 Object-Oriented Programming (OOP): Classes, Methods, and Functions

#### Functions vs. Methods
- **Function**: A standalone callable block of code independent of any class (`def calculate_grade_letter(gpa: float) -> str:`).
- **Method**: A function bound to a class or instance.

#### Method Types in Python Classes:
1. **Instance Method**: Receives `self` as the first parameter. Accesses and modifies object instance state.
2. **Class Method (`@classmethod`)**: Receives `cls` as the first parameter. Commonly used for alternative constructors (e.g., `StudentRecord.from_dict(data)`).
3. **Static Method (`@staticmethod`)**: Bound to the class namespace but receives neither `self` nor `cls`. Acts as a utility helper related to the class domain.
4. **Properties (`@property` and `@setter`)**: Provides controlled encapsulation and validation without clumsy Java-style `getGpa()` and `setGpa()` methods.

```python
class StudentRecord:
    def __init__(self, student_id: str, name: str, gpa: float = 0.0) -> None:
        self.student_id = student_id
        self.name = name
        self._gpa = 0.0
        self.gpa = gpa  # Routes through property setter

    @property
    def gpa(self) -> float:
        return self._gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        if not (0.0 <= value <= 4.0):
            raise ValueError(f"GPA must be between 0.0 and 4.0. Received: {value}")
        self._gpa = round(value, 2)

    # Instance method
    def is_honor_roll(self) -> bool:
        return self.gpa >= 3.50

    # Class method (Alternative constructor)
    @classmethod
    def from_dict(cls, data: dict) -> "StudentRecord":
        return cls(student_id=data["student_id"], name=data["name"], gpa=data.get("gpa", 0.0))

    # Static method
    @staticmethod
    def validate_id_format(student_id: str) -> bool:
        return student_id.startswith("e") and len(student_id) == 9

    # Dunder methods for representation
    def __repr__(self) -> str:
        return f"StudentRecord(student_id='{self.student_id}', name='{self.name}', gpa={self.gpa})"
```

---

### 2.5 Comments and Docstrings

#### Comments
- **What NOT to comment**: Do not restate what the code clearly says.
  ```python
  # BAD: Restating the obvious
  i = i + 1  # Increment i by 1
  ```
- **What TO comment**: Explain the *intent*, the *why*, mathematical formulas, or non-obvious workarounds:
  ```python
  # GOOD: Explaining the rationale and context
  # Subtract 1e-6 epsilon to prevent zero-division error during floating-point normalization
  ```

#### Docstrings (PEP 257 & Google Style)
Every public module, class, and function must have a docstring documenting parameters, return values, and raised exceptions:

```python
def calculate_grade_letter(gpa: float) -> str:
    """Converts a numerical GPA to an academic letter grade.

    Args:
        gpa: Numerical GPA between 0.0 and 4.0.

    Returns:
        str: Grade letter ('A', 'B', 'C', 'D', 'F').

    Raises:
        ValueError: If gpa is outside the [0.0, 4.0] interval.
    """
```

---

### 2.6 Clean Code Principles

The core metric of clean code from *The Art of Readable Code*:
> **"Code should be written to minimize the time it would take for someone else to understand it."**

#### Key Techniques:
1. **Guard Clauses / Early Returns**: Eliminate deeply nested `if-else` staircases by validating preconditions and returning early.
2. **Single Responsibility Principle (SRP)**: Each function should perform exactly one task well.
3. **Eliminate Magic Numbers**: Replace raw literals (`3.5`, `86400`, `0.78`) with named constants (`MINIMUM_HONOR_GPA`, `SECONDS_PER_DAY`).
4. **Intermediate Explanatory Variables**: Break giant multi-line boolean conditions into readable named boolean flags:
   ```python
   is_itc_student = student_id.startswith("e")
   has_honors_gpa = gpa >= 3.50
   is_eligible_for_scholarship = is_itc_student and has_honors_gpa
   ```

---

### 2.7 Debugging and Defensive Programming

1. **Built-in `breakpoint()` & `pdb`**:
   - Insert `breakpoint()` directly in Python 3.7+ code to pause execution and enter the interactive debugger.
   - Core `pdb` commands:
     - `n` (next): Execute next line.
     - `s` (step): Step into function.
     - `c` (continue): Resume execution until next breakpoint.
     - `p <var>` (print): Print variable value.
     - `q` (quit): Exit debugger immediately.

2. **Structured Logging vs. Print Debugging**:
   - Naked `print()` statements leave clutter, lack timestamps, and cannot be filtered by severity.
   - Use the standard `logging` library:
     ```python
     import logging
     logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
     logger = logging.getLogger(__name__)
     logger.info("Batch processing started.")
     logger.warning("Unrecognized student format detected.")
     logger.error("Database connection refused.")
     ```

3. **Defensive Assertions**:
   - Use `assert` statements to verify internal invariants during development:
     ```python
     assert 0.0 <= gpa <= 4.0, f"Critical constraint violated: GPA {gpa} out of bounds"
     ```

---

## 3. Tips and Tricks to Ensure Code Follows PEP 8 with Ruff

[Ruff](https://astral.sh/ruff) is an extremely fast Python linter and code formatter written in Rust. It replaces Flake8, Black, isort, pydocstyle, and pyupgrade in a single tool.

### 3.1 Installation and Verification

Using `uv` (recommended):
```bash
uv tool install ruff
# or run directly without installation
uvx ruff --version
```

Using standard `pip`:
```bash
pip install ruff
```

### 3.2 Key Ruff CLI Commands

```bash
# 1. Inspect and lint code across the project
ruff check .

# 2. Automatically fix all autofixable lint errors
ruff check --fix .

# 3. Format all Python files (replaces Black formatting)
ruff format .

# 4. Format and verify simultaneously
ruff check --fix . && ruff format .
```

### 3.3 Configuration via `pyproject.toml`

Ruff is centrally configured in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py310"
line-length = 88
exclude = [".git", ".venv", "__pycache__"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes logic & syntax errors
    "I",   # isort (import sorting)
    "B",   # flake8-bugbear
    "UP",  # pyupgrade (modern syntax)
    "SIM", # flake8-simplify
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 3.4 VS Code Format-on-Save Integration

In `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  }
}
```

---

## 4. References

1. **Boswell, D., & Foucher, T. (2011)**. *The Art of Readable Code*. O'Reilly Media.
2. **Van Rossum, G., Warsaw, B., & Coghlan, N. (2001)**. *PEP 8 – Style Guide for Python Code*. [peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
3. **Goodger, D., & Van Rossum, G. (2001)**. *PEP 257 – Docstring Conventions*. [peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)
4. **Astral Software (2024)**. *Ruff: An extremely fast Python linter and code formatter*. [docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
5. **Department of Applied Mathematics and Statistics (ITC)**. *APDS Lecture Slides Chapter 01 & TP 01* (Lecturer: Mr. VANN Visal).
