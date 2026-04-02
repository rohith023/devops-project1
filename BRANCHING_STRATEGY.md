# Git Branching Strategy

This project uses a modified Git Flow branching model for version control and collaboration.

## Branch Types

### 1. Main Branch (`main`)
- **Purpose**: Production-ready, stable code
- **Protections**: 
  - Requires pull request reviews
  - Must pass all CI/CD checks before merge
- **Merges From**: `develop` branch (via pull request)
- **Tags**: Release version tags (v1.0.0, v1.1.0, etc.)

```bash
# View main branch
git log --oneline main

# Create release from develop
git checkout main
git pull origin main
git merge --no-ff develop
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

---

### 2. Develop Branch (`develop`)
- **Purpose**: Integration branch for features and fixes
- **Protections**:
  - Requires pull request reviews
  - Must pass all CI/CD checks before merge
- **Merges From**: 
  - Feature branches
  - Bugfix branches
- **Merges To**: `main` branch for releases

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# Complete feature and create PR to develop
git push origin feature/new-feature
# Create Pull Request on GitHub to merge into develop
```

---

### 3. Feature Branches (`feature/*`)
- **Naming**: `feature/descriptive-name`
- **Created From**: `develop`
- **Purpose**: Develop new features
- **Merge Back To**: `develop` (via pull request)
- **Deletion**: Delete after merge

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-api-endpoint

# Work on feature
git add .
git commit -m "feat: Add new API endpoint

- Implement /predict/batch endpoint
- Add input validation
- Update documentation"

# Push and create PR
git push origin feature/new-api-endpoint

# After PR approval and merge:
git branch -d feature/new-api-endpoint
```

---

### 4. Bugfix Branches (`bugfix/*`)
- **Naming**: `bugfix/issue-description`
- **Created From**: `develop`
- **Purpose**: Fix bugs in development
- **Merge Back To**: `develop` (via pull request)

```bash
# Create bugfix branch
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-prediction-model

# Fix the bug
git add .
git commit -m "fix: Resolve prediction model accuracy issue

- Update model training parameters
- Fix data preprocessing bug
- Add test cases for edge cases"

git push origin bugfix/fix-prediction-model
```

---

### 5. Hotfix Branches (`hotfix/*`)
- **Naming**: `hotfix/issue-description`
- **Created From**: `main`
- **Purpose**: Critical production fixes
- **Merge Back To**: `main` AND `develop`
- **Increment**: Patch version (v1.0.0 → v1.0.1)

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/fix-critical-bug

# Fix the critical issue
git add .
git commit -m "fix: Critical production bug fix

- Resolve database connection issue
- Add failover mechanism"

# Merge to main (create PR)
git push origin hotfix/fix-critical-bug

# After PR approval to main:
git checkout main
git merge --no-ff hotfix/fix-critical-bug
git tag -a v1.0.1 -m "Hotfix release 1.0.1"
git push origin main --tags

# Also merge to develop
git checkout develop
git merge --no-ff hotfix/fix-critical-bug
git push origin develop

# Delete hotfix branch
git branch -d hotfix/fix-critical-bug
```

---

## Commit Message Convention

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, semicolons, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding or updating tests
- **chore**: Changes to build process, dependencies, etc.
- **ci**: Changes to CI/CD configuration

### Examples

```bash
# Good commit message
git commit -m "feat(api): Add prediction confidence score

- Include model confidence in API response
- Add confidence threshold validation
- Update API documentation"

# Another example
git commit -m "fix(model): Resolve training data corruption

Prevents duplicate entries in training dataset
Fixes issue #42"

# Hotfix example
git commit -m "fix(critical): Fix database connection timeout

- Increase connection pool size
- Add retry logic
- Add monitoring alert"
```

---

## Pull Request Workflow

### Creating a Pull Request

```bash
# 1. Create and push feature branch
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "feat: My feature description"
git push origin feature/my-feature

# 2. On GitHub:
# - Go to repository
# - Click "Compare & pull request"
# - Add PR title and description
# - Request reviewers
# - Submit PR

# 3. GitHub Actions runs automatically:
# - Code checkout
# - Dependencies installation
# - Tests execution
# - Docker build
# - Security scanning
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Other (please describe)

## Related Issues
Closes #123

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] CI/CD pipeline passes
```

### Merging PR

```bash
# After PR approval:
# Option 1: Squash and merge (one commit)
# Option 2: Create a merge commit
# Option 3: Rebase and merge

# Default strategy: Create a merge commit with --no-ff flag
git merge --no-ff feature/my-feature
```

---

## Workflow Examples

### Example 1: New Feature Development

```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/data-export

# 3. Make changes
# ... edit files ...

# 4. Commit with good message
git add .
git commit -m "feat: Add CSV data export functionality

- Implement /export endpoint
- Add data formatting options
- Include error handling
- Add unit tests"

# 5. Push and create PR
git push origin feature/data-export
# Create PR on GitHub, request review

# 6. After approval, merge and clean up
git checkout develop
git pull origin develop
git merge --no-ff feature/data-export
git push origin develop
git branch -d feature/data-export
```

### Example 2: Bug Fix

```bash
# 1. Create bugfix from develop
git checkout develop
git pull origin develop
git checkout -b bugfix/memory-leak

# 2. Fix the bug
git add .
git commit -m "fix: Resolve memory leak in model prediction

Root cause: Not releasing model predictions
Solution: Add explicit cleanup after prediction"

# 3. Push and create PR
git push origin bugfix/memory-leak

# 4. After approval
git checkout develop
git merge --no-ff bugfix/memory-leak
git push origin develop
git branch -d bugfix/memory-leak
```

### Example 3: Production Hotfix

```bash
# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/auth-bypass

# 2. Fix critical issue
git add .
git commit -m "fix: Close authentication bypass vulnerability

Severity: Critical
Impact: Unauthorized access to API
Solution: Add request signature validation"

# 3. Merge to main with tag
git checkout main
git merge --no-ff hotfix/auth-bypass
git tag -a v2.1.1 -m "Security hotfix"
git push origin main --tags

# 4. Also merge to develop
git checkout develop
git pull origin develop
git merge --no-ff hotfix/auth-bypass
git push origin develop

# 5. Clean up
git branch -d hotfix/auth-bypass
```

---

## Useful Git Commands

### View Branch Information
```bash
# List all branches
git branch -a

# View branch history
git log --graph --oneline --all

# Show commits in feature not in develop
git log develop..feature/my-feature

# Show commits in develop not in feature
git log feature/my-feature..develop
```

### Synchronize Branches
```bash
# Update develop with latest main
git checkout develop
git fetch origin
git rebase origin/main

# Or merge (keeps history)
git checkout develop
git merge --no-ff origin/main
```

### Manage Branches
```bash
# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature

# Rename branch
git branch -m old-name new-name

# Push renamed branch
git push origin --delete old-name
git push origin new-name
```

### Fixing Mistakes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Revert commit (creates new commit)
git revert <commit-hash>
```

---

## Branch Protection Rules

For production safety, configure these in GitHub:

1. **Main Branch Protection**:
   - Require pull request reviews before merging
   - Require status checks to pass (CI/CD)
   - Require branches to be up to date
   - Include administrators in restrictions

2. **Develop Branch Protection**:
   - Require pull request reviews
   - Require status checks to pass
   - Allow force pushes: No

---

## Release Process

```bash
# 1. Prepare release on develop branch
git checkout develop
# ... finalize changes, update version ...
git commit -m "chore: Prepare v1.1.0 release"
git push origin develop

# 2. Create Pull Request from develop to main
# - Title: "Release v1.1.0"
# - Allow time for review

# 3. After approval, merge to main
# 4. Tag the release
git checkout main
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin main --tags

# 5. Merge back to develop
git checkout develop
git merge --no-ff main
git push origin develop
```

---

## Repository State

### Current Branches
```
main           - Production branch (protected)
develop        - Integration branch (protected)
feature/*      - Feature development
bugfix/*       - Bug fixes
hotfix/*       - Critical production fixes
```

### Branch Relationships
```
main (v1.0.0)
  ↑
  ├── develop
      ├── feature/add-prediction-endpoint
      ├── feature/improve-ml-model
      ├── bugfix/fix-error-handling
      └── hotfix/critical-patch
```

---

## Best Practices

1. **Keep branches short-lived** (max 1-2 weeks)
2. **Rebase before pushing** to keep history clean
3. **Never force push** to shared branches
4. **Use descriptive branch names**
5. **Link PRs to issues** when applicable
6. **Request at least 2 reviewers** for main branch PRs
7. **Delete merged branches** to reduce clutter
8. **Use merge commits** (--no-ff) to preserve branching history
9. **Sign commits** with GPG for security (optional)
10. **Automate** with branch protection rules

---

## Tools and Integration

### GitHub Features
- Branch protection rules
- Required status checks
- Pull request templates
- Automated reviews
- Commit signing

### CI/CD Integration
- GitHub Actions runs on all PRs
- Tests must pass before merge
- Code coverage tracking
- Security scanning

### Useful Extensions
```bash
# Enhanced git log visualization
git log --graph --decorate --oneline --all

# Git flow extension
brew install git-flow  # macOS
sudo apt-get install git-flow  # Linux
```

---

**Last Updated**: April 2, 2024
**Strategy**: Git Flow Modified
**Status**: Active
