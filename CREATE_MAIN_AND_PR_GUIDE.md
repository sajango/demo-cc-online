# Guide: Creating Main Branch and Pull Request

This guide will help you create the `main` branch on GitHub and set up a Pull Request to trigger GitHub Actions CI/CD.

---

## 🎯 Objective

1. Create `main` branch on GitHub
2. Create Pull Request from `claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7` to `main`
3. Trigger GitHub Actions to validate the implementation

---

## 📋 Prerequisites

- You have push access to the repository
- The feature branch `claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7` is already pushed to GitHub
- You're logged into GitHub

---

## 🚀 Option 1: Create via GitHub Web Interface (Recommended)

### Step 1: Navigate to Your Repository

Go to: `https://github.com/sajango/demo-cc-online`

### Step 2: Create Main Branch

**Method A: Via Branches Page**

1. Click on the **"branches"** dropdown (shows current branch)
2. Click **"View all branches"** link
3. Click **"New branch"** button
4. Enter branch name: `main`
5. Select source: Choose the commit `cda01a1` (Merge pull request #1)
   - Or select `claude/fastapi-docker-setup-01Mketaf1YsheMLqAgofDHi2` as source
6. Click **"Create branch"**

**Method B: Via Settings**

1. Go to **Settings** → **Branches**
2. If no default branch exists, you'll see an option to create one
3. Create branch named `main`
4. Set it as the default branch

### Step 3: Create Pull Request

1. Go to the **"Pull requests"** tab
2. Click **"New pull request"** button
3. Set base branch: `main`
4. Set compare branch: `claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7`
5. Click **"Create pull request"**

### Step 4: Fill PR Details

**Title:**
```
feat: implement authentication system with JWT, OAuth, and CI/CD pipeline
```

**Description:**
Copy the content from `PULL_REQUEST_TEMPLATE.md` or use this summary:

```markdown
## Summary
Implements comprehensive authentication system with JWT and OAuth (Google, Apple),
UUID primary keys, and complete GitHub Actions CI/CD pipeline.

## Key Features
- JWT authentication (access + refresh tokens)
- Google OAuth & Apple Sign-In integration
- UUID primary keys instead of integers
- GitHub Actions CI/CD with code quality checks
- Automated testing with coverage reporting
- Security scanning (Bandit, Safety)

## Changes
- 55+ files changed
- 2,500+ lines added
- 2 database migrations
- 6 new API endpoints
- Comprehensive test suite
- Complete CI/CD pipeline

See PULL_REQUEST_TEMPLATE.md for full details.
```

### Step 5: Configure PR Settings

- **Reviewers**: Add reviewers if needed
- **Labels**: Add labels like `enhancement`, `authentication`, `ci/cd`
- **Assignees**: Assign yourself or team members
- **Milestone**: Set milestone if applicable

### Step 6: Create the PR

Click **"Create pull request"** button

---

## 🚀 Option 2: Create via Git Command Line (If GitHub allows)

If you have the GitHub CLI or can push branches directly:

### Step 1: Create and Push Main Branch Locally

```bash
# Switch to the base commit for main
git checkout -b main cda01a1

# Try to push (may require manual creation on GitHub first)
git push -u origin main
```

**Note:** If you get a 403 error, you'll need to create the main branch via GitHub web interface first (Option 1).

### Step 2: Switch Back to Feature Branch

```bash
git checkout claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7
```

### Step 3: Create PR via GitHub Web Interface

Follow Steps 3-6 from Option 1 above.

---

## 🚀 Option 3: Using GitHub API (Advanced)

If you have a GitHub Personal Access Token:

### Create Main Branch

```bash
# Using curl
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/sajango/demo-cc-online/git/refs \
  -d '{
    "ref": "refs/heads/main",
    "sha": "cda01a16c0a1a2b3c4d5e6f7a8b9c0d1e2f3a4b5"
  }'
```

**Note:** Replace `YOUR_GITHUB_TOKEN` with your actual token and the SHA with the correct commit hash.

### Create Pull Request

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/sajango/demo-cc-online/pulls \
  -d '{
    "title": "feat: implement authentication system with JWT, OAuth, and CI/CD pipeline",
    "body": "See PULL_REQUEST_TEMPLATE.md for details",
    "head": "claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7",
    "base": "main"
  }'
```

---

## ✅ After Creating the Pull Request

### What Will Happen Automatically

1. **GitHub Actions Triggers** 🤖
   - Main CI workflow starts
   - PR quick check runs
   - Multiple jobs execute in parallel

2. **Code Quality Checks** ✨
   - Black formatting validation
   - Flake8 linting
   - MyPy type checking

3. **Testing** 🧪
   - Unit tests on Python 3.11 & 3.12
   - Integration tests with MySQL & Redis
   - Code coverage generation

4. **Security Scanning** 🔒
   - Dependency vulnerability check (Safety)
   - Code security scan (Bandit)

5. **Artifacts Generated** 📦
   - Coverage reports (HTML + XML)
   - Security scan results
   - Test results

### Monitor the CI Pipeline

1. Go to the **"Actions"** tab in your repository
2. You'll see workflows running:
   - "CI - Code Quality & Tests"
   - "PR Quick Check"

3. Click on a workflow to see:
   - Job progress
   - Detailed logs
   - Test results
   - Error messages (if any)

4. Check the PR page:
   - Status checks will appear at the bottom
   - Green checkmarks = passed ✅
   - Red X = failed ❌
   - Yellow circle = running ⏳

### Download Artifacts

After CI completes:

1. Go to **Actions** → Select the workflow run
2. Scroll to **Artifacts** section
3. Download:
   - `coverage-report` - HTML coverage report
   - `security-reports` - Security scan results

---

## 🔧 Troubleshooting

### Issue: Cannot Create Main Branch

**Solution:** You may not have permissions. Ask a repository admin to:
1. Create the `main` branch
2. Set it as the default branch
3. Then you can create the PR

### Issue: PR Shows Too Many Commits

**Solution:** This is expected if main branch starts from an earlier commit. The PR will show all commits between the base and your feature branch.

### Issue: CI Workflows Not Running

**Solution:** Check that:
1. GitHub Actions is enabled in repository settings
2. Workflow files exist in `.github/workflows/`
3. Branch name matches trigger patterns in workflow files

### Issue: Some Checks Failing

**Solution:**
1. Click on the failed check to see details
2. Review the logs
3. Common issues:
   - **Formatting**: Run `./scripts/format-code.sh` and push
   - **Tests**: Fix failing tests locally first
   - **Dependencies**: Ensure requirements.txt is up to date

---

## 📊 Expected CI Results

All these checks should **pass** ✅:

- [ ] Black formatting check
- [ ] Flake8 linting (0 critical errors)
- [ ] Unit tests (Python 3.11)
- [ ] Unit tests (Python 3.12)
- [ ] Integration tests
- [ ] Code coverage generation
- [ ] Security scan (warnings ok)

---

## 🎉 Success Criteria

When everything is working correctly:

✅ Main branch created
✅ Pull request created
✅ GitHub Actions running
✅ All required checks passing
✅ PR ready for review
✅ Artifacts available for download

---

## 📞 Need Help?

If you encounter issues:

1. **Check Repository Settings**
   - Settings → Actions → Allow workflows

2. **Review Workflow Logs**
   - Actions tab → Click on failed workflow
   - Review each job's logs

3. **Validate Locally**
   ```bash
   ./scripts/check-code.sh
   ```

4. **Check Documentation**
   - `.github/workflows/README.md`
   - `CI_VALIDATION_REPORT.md`

---

## 📝 Quick Reference

**Repository**: https://github.com/sajango/demo-cc-online

**Branches**:
- Source: `claude/implement-use-uu-01XvpjDFAd8KzpF35U51yJb7`
- Target: `main`

**Base Commit for Main**: `cda01a1` (Merge pull request #1)

**Files to Review**:
- `PULL_REQUEST_TEMPLATE.md` - PR description
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/pr-quick-check.yml` - Quick PR checks
- `CI_VALIDATION_REPORT.md` - Validation results

---

## ✨ Next Steps After PR is Merged

1. Delete feature branch (optional)
2. Pull latest main branch locally
3. Start new feature branches from main
4. Monitor CI/CD on future PRs

---

*Guide created for demo-cc-online repository*
*Last updated: 2025-11-14*
