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

## Reference Materials and Textbooks

- Textbook: *The Art of Readable Code* by Dustin Boswell and Trevor Foucher (O'Reilly Media)
- Course Slides: Department of Applied Mathematics and Statistics, ITC (Lecturer: Mr. VANN Visal)
  - Chapter 01: Introduction to Git and Team Collaboration
  - Subsequent chapters covering advanced programming paradigms and software design
- Documentation:
  - Git Official Documentation: [git-scm.com/doc](https://git-scm.com/doc)
  - Python Standard Library and PEP 8 Style Guide: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)

---

## Repository Architecture and Branch Strategy

To maintain a clean separation between instructional materials, development work, and assignment submissions, this repository follows a dedicated multi-branch structure:

```
year-05-itc-apds/
|-- main                  Production-ready documentation, course index, and milestones
|-- lectures              Lecture notes, theoretical summaries, slide code samples
`-- assignments           Practical work (TP), assignment deliverables, exercises
```

### Branch Descriptions

- `main`: The root branch containing the primary course documentation, syllabus index, and merged milestones. Direct pushes to `main` are restricted to administrative and consolidated updates.
- `lectures`: Contains slide notes, code demonstrations, reading notes, and reference implementations covered during weekly lecture sessions.
- `assignments`: Designated branch for laboratory practicals (Travaux Pratiques / TP), individual coding tasks, and assignment submissions.
- `assignment`: Tracking branch aliased to `assignments` to support automated checking scripts and assignment verification.

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

## Standard Workflow Guidelines

As presented in Lecture 01, all development work follows standard team collaboration protocols:

1. Clone repository:
   ```bash
   git clone https://github.com/menghong-heng/year-05-itc-apds.git
   cd year-05-itc-apds
   ```

2. Switch to the target branch or create a feature branch:
   ```bash
   git switch assignments
   git switch -c tp-01-practice
   ```

3. Stage and commit changes with descriptive commit messages:
   ```bash
   git add .
   git commit -m "Complete Practice 01 Git workflow tasks"
   ```

4. Push feature branch to the remote repository:
   ```bash
   git push -u origin tp-01-practice
   ```

5. Open a Pull Request on GitHub against `assignments` or `main` for review.

---

## License and Academic Integrity

This repository is maintained for educational purposes as part of the M-DAS curriculum at the Institute of Technology of Cambodia. All course submissions adhere to the academic honesty regulations of ITC.
