# Git Commit & Release Guide

This document is my quick reference for committing, versioning, and publishing new releases using Conventional Commits + python-semantic-release.

---

# 1. Check Current Status

```bash
git status
```

---

# 2. Add Changes

## Add all files
```bash
git add .
```

## Add specific file
```bash
git add path/to/file
```

---

# 3. Commit Using Conventional Commits

IMPORTANT:
Commit messages control automatic version bumping.

---

# Commit Types

## Patch Release (bug fixes)
Version:
```txt
0.1.0 → 0.1.1
```

Commit:
```bash
git commit -m "fix: resolve windows path issue"
```

Use for:
- bug fixes
- small corrections
- non-breaking improvements

---

## Minor Release (new features)
Version:
```txt
0.1.0 → 0.2.0
```

Commit:
```bash
git commit -m "feat: add docker service startup"
```

Use for:
- new features
- enhancements
- backward-compatible additions

---

## Major Release (breaking changes)
Version:
```txt
0.1.0 → 1.0.0
```

Commit:
```bash
git commit -m "feat!: redesign cli api"
```

OR

```bash
git commit -m "feat: redesign cli api

BREAKING CHANGE: cli commands changed"
```

Use for:
- breaking APIs
- incompatible CLI changes
- architecture rewrites

---

# Other Useful Commit Types

## Documentation
```bash
git commit -m "docs: update installation guide"
```

## Refactoring
```bash
git commit -m "refactor: simplify command parser"
```

## Tests
```bash
git commit -m "test: add integration tests"
```

## CI/CD
```bash
git commit -m "ci: update github workflow"
```

## Chores
```bash
git commit -m "chore: update dependencies"
```

---

# 4. Push Changes

```bash
git push
```

After pushing:

- GitHub Actions runs
- semantic-release checks commits
- version automatically bumps
- tag gets created
- GitHub release gets created
- package gets published to PyPI

---

# 5. Release Flow Example

## Example 1 — Bug Fix

```bash
git add .
git commit -m "fix: resolve path normalization bug"
git push
```

Automatic result:
```txt
0.1.0 → 0.1.1
```

---

## Example 2 — New Feature

```bash
git add .
git commit -m "feat: add redis auto startup"
git push
```

Automatic result:
```txt
0.1.0 → 0.2.0
```

---

## Example 3 — Breaking Change

```bash
git add .
git commit -m "feat!: redesign agent config system"
git push
```

Automatic result:
```txt
0.1.0 → 1.0.0
```

---

# 6. Rules to Remember

## DO

✔ Use meaningful commit messages  
✔ Use conventional commit prefixes  
✔ Push only working code  
✔ Run tests before push  
✔ Keep commits focused and small  

---

## DON'T

✘ Don't use:
```txt
update
changes
fixed stuff
misc
```

✘ Don't push broken builds  
✘ Don't mix unrelated changes in one commit  

---

# 7. Common Commit Prefixes

| Prefix | Purpose |
|---|---|
| feat | new feature |
| fix | bug fix |
| docs | documentation |
| refactor | code cleanup |
| test | tests |
| ci | CI/CD changes |
| chore | maintenance |

---

# 8. Check Current Version

## Local tag list
```bash
git tag
```

## Latest release
```bash
git describe --tags --abbrev=0
```

---

# 9. Useful Commands

## View commit history
```bash
git log --oneline
```

## Undo last commit (keep changes)
```bash
git reset --soft HEAD~1
```

## Create new branch
```bash
git checkout -b feature/new-feature
```

---

# 10. Full Daily Workflow

```bash
# check changes
git status

# stage files
git add .

# commit
git commit -m "feat: add postgres health checks"

# push
git push
```

Then automation handles:
- versioning
- changelog
- tagging
- GitHub release
- PyPI publishing

---

# 11. Semantic Release Rules

| Commit | Version Impact |
|---|---|
| fix: | patch |
| feat: | minor |
| feat!: | major |
| docs: | none |
| refactor: | none |
| chore: | none |

---

# 12. Good Commit Examples

```bash
git commit -m "feat: add background service manager"

git commit -m "fix: handle missing docker daemon"

git commit -m "docs: improve README examples"

git commit -m "refactor: simplify websocket logic"

git commit -m "test: add cli integration tests"

git commit -m "ci: add pytest workflow"
```

---

# 13. Bad Commit Examples

```txt
update
changes
new code
fixed bug
misc
asdf
temp
```

---

# 14. Goal

The goal is:

```txt
Write code
→ commit properly
→ push
→ everything else happens automatically
```