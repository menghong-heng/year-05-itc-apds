# APDS Assignments and Practical Work (TP)

This branch (`assignments`) is dedicated to coursework assignments, laboratory practicals (Travaux Pratiques / TP), and problem sets for Advance Programming for Data Science (APDS) at ITC.

---

## Directory Structure

```
assignments/
|-- practice-01/          Introduction to Git, repository setup, branch workflows
|-- practice-02/          Code readability refactoring and clean code principles
|-- ...
`-- README.md             Assignment submission rules and tracking
```

---

## Assignment Tracking

| Assignment | Topic | Status | Submission Target |
| :--- | :--- | :--- | :--- |
| Practice 01 | Git fundamentals, branching, merge conflict simulation | Initialized | Week 01 / October 2026 |
| Practice 02 | Code styling and readability refactoring | Pending | Week 02 |
| Practice 03 | Python modularization and unit testing | Pending | Week 03 |

---

## Submission and Workflow Standards

To submit work completed under this course:

1. Create a dedicated feature branch from `assignments`:
   ```bash
   git switch assignments
   git switch -c tp-01-practice
   ```

2. Implement solutions inside the corresponding folder (e.g., `assignments/practice-01/`).
3. Commit with standard conventional commit messages:
   ```bash
   git commit -m "feat(tp01): implement git branching practice tasks"
   ```

4. Push the feature branch to GitHub:
   ```bash
   git push -u origin tp-01-practice
   ```

5. Open a Pull Request targeting the `assignments` branch.
