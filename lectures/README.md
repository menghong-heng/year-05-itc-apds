# APDS Lecture Materials and Notes

This branch (`lectures`) tracks lecture summaries, theoretical slides breakdown, and illustrative code snippets for the Advance Programming for Data Science course at ITC.

---

## Lecture Schedule and Modules

| Chapter | Topic | Status | Reference Material |
| :--- | :--- | :--- | :--- |
| Chapter 01 | Introduction to Git and Version Control | Completed | Slides by Mr. VANN Visal |
| Chapter 02 | Code Aesthetics and Intentional Naming | In Progress | *The Art of Readable Code* (Ch 1-6) |
| Chapter 03 | Control Flow Simplification and Modularity | Upcoming | *The Art of Readable Code* (Ch 7-10) |
| Chapter 04 | Pythonic Architecture and OOP for Data Science | Upcoming | Advanced Python Guidelines |
| Chapter 05 | Testing, Profiling, and Performance | Upcoming | Pytest and Optimization Suites |

---

## Chapter 01: Introduction to Git Summary

### 1. Fundamental Concepts
- Repository: Database tracking project history and file tree states.
- Commit: Cryptographically hashed snapshot of staged modifications at a specific point in time.
- Branch: Independent line of development isolating experimental or feature work.
- Merge: Operation combining diverged commit histories into a target branch.
- Clone: Creating an identical local clone of a remote repository.
- Stash: Temporarily shelving uncommitted changes to work on a clean working tree.

### 2. Standard Command Reference

#### Repository Setup
```bash
git init
git clone https://github.com/menghong-heng/year-05-itc-apds.git
git config --global user.name "Heng Menghong"
git config --global user.email "menghongheng@gmail.com"
```

#### Routine Operations
```bash
git status
git add <filename>
git add .
git commit -m "feat: descriptive commit message"
git log --oneline --graph
```

#### Branching Operations
```bash
# Create and switch to a branch
git switch -c feature-name

# Switch between existing branches
git switch main
git switch lectures

# Merge changes into current branch
git merge feature-name

# Delete branch after merge
git branch -d feature-name
```

#### Syncing with Remote
```bash
git push origin <branch-name>
git pull origin <branch-name>
```

#### Resolving Conflicts
When Git encounters competing changes in the same lines during a merge:
1. Identify conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Decide on the intended state and edit the conflicting files.
3. Stage resolved files: `git add <filename>`.
4. Finalize merge: `git commit -m "fix: resolve merge conflicts"`.

---

## Contributing to Lectures Branch

- Keep lecture notes structured chronologically by chapter.
- Use clean Markdown formatting without decorative emojis.
- Store runnable Python demonstration scripts alongside chapter folders.
