# APDS Travaux Pratiques (TP)

This branch (`tp`) contains laboratory practical exercises, coding tasks, and hands-on session work for the Advance Programming for Data Science (APDS) course at ITC.

---

## Practical Sessions (TP) Index

| Session | Title | Directory | Status |
| :--- | :--- | :--- | :--- |
| TP 01 | Introduction to Git and Version Control | `tp/practice-01/` | Initialized |
| TP 02 | Code Readability and Refactoring | `tp/practice-02/` | Pending |
| TP 03 | Modular Python Architecture | `tp/practice-03/` | Pending |
| TP 04 | Testing and Performance Profiling | `tp/practice-04/` | Pending |

---

## TP 01: Introduction to Git Tasks

1. Repository setup and configuration (`user.name`, `user.email`).
2. Creating and switching branches (`git switch -c <branch>`).
3. Simulating file changes and multi-commit workflows.
4. Handling merge conflicts between feature branches.
5. Pushing branches and opening Pull Requests on GitHub.

---

## Workflow for TP Submissions

For each practical lab session:

1. Create a session branch from `tp`:
   ```bash
   git switch tp
   git switch -c tp-01-practice
   ```

2. Add your code and practical deliverables into `tp/practice-01/`.
3. Commit and push:
   ```bash
   git add .
   git commit -m "feat(tp01): complete practice 01 tasks"
   git push -u origin tp-01-practice
   ```

4. Submit a Pull Request into `tp`.
