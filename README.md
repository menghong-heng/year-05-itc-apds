# Advance Programming for Data Science (APDS)

Course repository for Advance Programming for Data Science (APDS), Department of Applied Mathematics and Statistics (AMS), Institute of Technology of Cambodia (ITC).

---

## Course Information

- Institution: Institute of Technology of Cambodia (ITC)
- Department: Department of Applied Mathematics and Statistics (AMS)
- Program: Master / Engineering in Data Science (M-DAS)
- Academic Period: Year 05, Semester 01 (Academic Year 2026-2027)
- Lecturer: Mr. VANN Visal
- Student: Heng Menghong
- Student ID: e20220258
- Repository: [year-05-itc-apds](https://github.com/menghong-heng/year-05-itc-apds)

---

## Course Overview

Advance Programming for Data Science bridges theoretical data science methodologies with production-grade software engineering practices. The course emphasizes writing clean, readable, maintainable, and efficient code, using modern distributed version control workflows, and architecting robust data-driven applications.

### Key Learning Objectives

1. Professional Version Control: Master Git workflows, branch lifecycle management, conflict resolution, collaborative pull requests, and automated repository maintenance.
2. Code Craftsmanship: Apply core principles from *The Art of Readable Code* to write self-documenting, concise, and maintainable software.
3. Modular Software Architecture: Structure Python packages, manage dependencies, write unit tests, and implement defensive error handling.
4. Data Pipeline Engineering: Profile execution bottlenecks, optimize data structures, and prepare codebases for production analytics workflows.

---

## Python Environment and Runtime Specifications

All code in this repository is developed and validated against modern Python environments.

- Recommended Python Version: Python 3.10 or higher
- System Environment: Python 3.14.7 (64-bit)
- Virtual Environment Standard: Standard library `venv` module

### Environment Setup Instructions

To maintain reproducible environments and prevent global package pollution:

1. Create a local virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - On Linux / macOS (Bash / Zsh):
     ```bash
     source .venv/bin/activate
     ```

3. Upgrade pip and install standard development tools:
   ```bash
   python -m pip install --upgrade pip
   pip install pytest mypy ruff
   ```

Virtual environment directories (`.venv/`, `env/`, `venv/`) and cache artifacts (`__pycache__/`) are globally ignored by the repository [.gitignore](file:///D:/Documents/ITC/Year_05_Semester_01/APDS/Github/.gitignore).

---

## Reference Materials and Textbooks

- Textbook: *The Art of Readable Code* by Dustin Boswell and Trevor Foucher (O'Reilly Media)
- Course Slides: Department of Applied Mathematics and Statistics, ITC (Lecturer: Mr. VANN Visal)
  - Chapter 01: Introduction to Git and Team Collaboration
  - Subsequent chapters covering advanced programming paradigms and software design
- Documentation:
  - Git Official Documentation: [git-scm.com/doc](https://git-scm.com/doc)
  - Python Standard Library and PEP 8 Style Guide: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)

---

## Repository Architecture and Branch Usages

To maintain strict separation of concerns, the repository is partitioned into five dedicated branches:

```
year-05-itc-apds/
|-- main                  Production-ready documentation, course index, and milestones
|-- lectures              Lecture notes, theoretical summaries, slide code samples
|-- tp                    Travaux Pratiques (TP), practical lab exercises, and sessions
|-- assignments           Coursework assignments, homework, and problem set submissions
`-- projects              Course project milestones, prototypes, and final codebase
```

### 1. `main` Branch (Canonical Source of Truth)

- Purpose: The root branch serving as the central hub for verified course documentation, syllabus tracking, configuration files, and merged milestone releases.
- Usage Rules: Direct pushes to `main` are restricted to administrative documentation. All major deliverables must arrive via reviewed pull requests.
- Typical Commands:
  ```bash
  # Check out and sync latest main
  git switch main
  git pull origin main
  ```

### 2. `lectures` Branch (Instructional Notes and Demos)

- Purpose: Tracks lecture slide summaries, reading notes from *The Art of Readable Code*, and live code demonstrations created during weekly lectures.
- Usage Rules: Kept up-to-date chronologically by chapter. Demonstrations should be runnable standalone Python scripts.
- Typical Commands:
  ```bash
  # Switch to lectures branch and pull updates
  git switch lectures
  git pull origin lectures
  ```

### 3. `tp` Branch (Travaux Pratiques / Practical Labs)

- Purpose: Dedicated to in-class laboratory practical exercises (TP) conducted at ITC AMS lab facilities.
- Usage Rules:
  - Each lab session is developed on a dedicated session branch branched off `tp` (e.g. `tp-01-git-practice`).
  - Completed lab exercises are verified and merged into `tp`.
- Typical Commands:
  ```bash
  # Switch to tp branch
  git switch tp
  git pull origin tp

  # Create a feature branch for a practical session
  git switch -c tp-01-practice

  # Complete exercises inside tp/practice-01/, commit, and push
  git add .
  git commit -m "feat(tp01): implement git branching practice tasks"
  git push -u origin tp-01-practice

  # Open a Pull Request targeting 'tp' on GitHub
  ```

### 4. `assignments` Branch (Graded Coursework and Homework)

- Purpose: Manages formal coursework assignments, take-home problem sets, and graded deliverables requested by the lecturer.
- Usage Rules:
  - Solutions are built in dedicated folders per assignment (e.g., `assignments/assignment-01/`).
  - Work must adhere strictly to readability and formatting standards.
- Typical Commands:
  ```bash
  # Switch to assignments branch
  git switch assignments
  git pull origin assignments

  # Create an assignment working branch
  git switch -c assignment-01-clean-code

  # Stage, commit, and push
  git add .
  git commit -m "feat(assignment01): complete readability refactoring"
  git push -u origin assignment-01-clean-code

  # Open a Pull Request targeting 'assignments' on GitHub
  ```

### 5. `projects` Branch (Term and Capstone Projects)

- Purpose: Houses the collaborative term project, midterm mini-project, and end-of-semester software engineering deliverables.
- Usage Rules:
  - Feature-driven development following team collaboration guidelines from Lecture 01.
  - Includes unit tests, documentation, and data engineering pipelines.
- Typical Commands:
  ```bash
  # Switch to projects branch
  git switch projects
  git pull origin projects

  # Create a project feature branch
  git switch -c feature/data-pipeline

  # Commit modular additions
  git add .
  git commit -m "feat(pipeline): implement clean ETL processing module"
  git push -u origin feature/data-pipeline

  # Open a Pull Request targeting 'projects' on GitHub
  ```

---

## Syllabus Outline

### Part 1: Distributed Version Control and Collaboration
- Introduction to Git architecture: working tree, staging area (index), and commit repository
- Repository initialization, staging, committing, and inspecting commit history
- Branching models, branch switching (`git switch`), merging strategies, and branch cleanup
- Conflict resolution and stashing (`git stash`)
- Effective configuration of `.gitignore` for data science environments
- Collaborative workflows: Forking, branching, pull requests, and code review practices

### Part 2: Code Readability and Design Principles
- Code readability metric: minimizing the time required for another developer to understand the code
- Packing information into names: specific names, avoiding generic names, encoding units and attributes
- Code aesthetic and visual layout: formatting consistency, logical grouping, alignment
- Knowing what to comment and what not to comment: intent versus restatement
- Making control flow easy to read: simplifying conditionals, early returns, reducing nesting
- Breaking down giant expressions and extracting variables

### Part 3: Advanced Python for Data Science
- Functional programming tools, comprehensions, and generators
- Object-oriented design patterns for data processing classes
- Exception management, custom exceptions, and defensive assertions
- Type annotations (PEP 484) and static validation with `mypy`

### Part 4: Testing, Performance, and Deployment
- Unit testing with `pytest`
- Profiling memory and computational efficiency
- Reproducible environments using virtual environments and lockfiles

---

## License and Academic Integrity

This repository is maintained for educational purposes as part of the M-DAS curriculum at the Institute of Technology of Cambodia. All course submissions adhere to the academic honesty regulations of ITC.
