# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants working with the demo-cc-online repository.

## Repository Overview

**Repository**: demo-cc-online
**Status**: New repository (bootstrapping phase)
**Purpose**: [To be defined as project evolves]

## Directory Structure

```
demo-cc-online/
├── .git/              # Git version control
├── src/               # Source code (to be created)
├── tests/             # Test files (to be created)
├── docs/              # Documentation (to be created)
├── .github/           # GitHub workflows and templates (to be created)
└── CLAUDE.md          # This file
```

### Expected Structure (As Codebase Grows)

- `src/` - Main source code directory
- `tests/` or `__tests__/` - Test files
- `docs/` - All documentation files (except README.md and CLAUDE.md)
  - `docs/design/` - Design documents and specifications
  - `docs/reports/` - Test reports, analysis reports
  - `docs/api/` - API documentation
  - `docs/guides/` - User guides and tutorials
  - `docs/architecture/` - Architecture diagrams and documentation
- `config/` - Configuration files
- `scripts/` - Build and utility scripts
- `public/` or `static/` - Static assets (if web project)

## Development Workflow

### Branch Strategy

**Current Branch**: `claude/claude-md-mhy6mdgcj7l8hgaa-01VjexzcAtWebznjqUxyb5wa`

All AI assistant development work should:
1. **ALWAYS** work on the designated Claude feature branch
2. **NEVER** push directly to main/master without explicit permission
3. Create descriptive commits as work progresses
4. Push to the feature branch when changes are complete

### Git Conventions

#### Branch Naming
- Feature branches: `claude/claude-md-{session-id}`
- All AI assistant branches must start with `claude/` and end with the matching session ID

#### Commit Messages
Follow conventional commit format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, semicolons, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

**Examples**:
```
feat: add user authentication module
fix(api): resolve race condition in data fetching
docs: update README with installation instructions
refactor(utils): simplify date formatting logic
```

#### Git Operations Best Practices

**Pushing Changes**:
- Always use: `git push -u origin <branch-name>`
- Branch must start with `claude/` and end with session ID
- Retry on network failures: up to 4 times with exponential backoff (2s, 4s, 8s, 16s)

**Fetching/Pulling**:
- Prefer specific branches: `git fetch origin <branch-name>`
- Retry on failures with same exponential backoff strategy

## Code Style and Conventions

### General Principles

1. **Readability First**: Write clear, self-documenting code
2. **Consistency**: Follow existing patterns in the codebase
3. **DRY (Don't Repeat Yourself)**: Extract common logic into reusable functions
4. **SOLID Principles**: Follow object-oriented design principles where applicable
5. **Keep It Simple**: Prefer simple solutions over complex ones

### Code Organization

- Group related functionality together
- Use meaningful file and directory names
- Limit file length (typically < 300 lines)
- One primary export per file when possible

### Naming Conventions

**To be established based on project language**:
- Variables: descriptive, camelCase or snake_case
- Functions: verb-based, camelCase or snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case or camelCase (be consistent)

### Comments and Documentation

- Write self-documenting code first
- Add comments for complex logic or non-obvious decisions
- Document public APIs and exported functions
- Keep comments up-to-date with code changes

## Testing Guidelines

### Test Organization

- Mirror source directory structure in test directory
- Name test files clearly: `*.test.*`, `*.spec.*`, or `test_*.py`
- Group related tests in describe/context blocks

### Test Quality

- **Arrange-Act-Assert (AAA)** pattern
- One logical assertion per test when possible
- Use descriptive test names that explain the scenario
- Test edge cases and error conditions
- Maintain test independence (no test should depend on another)

### Coverage Goals

- Aim for >80% code coverage
- 100% coverage for critical business logic
- Focus on meaningful tests over coverage metrics

## Security Best Practices

### Code Security

1. **Input Validation**: Always validate and sanitize user input
2. **Avoid Common Vulnerabilities**:
   - SQL Injection: Use parameterized queries
   - XSS: Escape output, use CSP headers
   - CSRF: Implement CSRF tokens
   - Command Injection: Avoid shell execution with user input
3. **Authentication & Authorization**: Implement proper auth checks
4. **Secrets Management**: Never commit secrets, use environment variables
5. **Dependencies**: Keep dependencies updated, audit for vulnerabilities

### Files to Never Commit

- `.env`, `.env.local`, `.env.*`
- `credentials.json`, `secrets.json`
- API keys, passwords, tokens
- Private keys, certificates
- Database dumps with sensitive data

## Documentation Standards

### File Organization Rules

**IMPORTANT**: All documentation files must be properly organized according to these rules:

1. **Root-Level Documentation** (allowed in project root):
   - `README.md` - Project overview, setup, and usage instructions
   - `CLAUDE.md` - AI assistant guidelines and conventions
   - `LICENSE` - Project license file
   - `CHANGELOG.md` - Version history and changes (if used)

2. **Documentation Directory** (`docs/`):
   - ALL other markdown files must be placed in the `docs/` directory
   - This includes but not limited to:
     - Design documents
     - Architecture documentation
     - Test reports
     - Analysis reports
     - Technical specifications
     - API documentation
     - User guides
     - Any other `.md` files

3. **Subdirectory Organization within `docs/`**:
   ```
   docs/
   ├── design/          # Design documents and specifications
   ├── reports/         # Test reports, analysis reports
   ├── api/             # API documentation
   ├── guides/          # User guides and tutorials
   └── architecture/    # Architecture diagrams and docs
   ```

**Examples**:
- ✅ Correct: `docs/reports/test-report-2025-11-14.md`
- ✅ Correct: `docs/design/database-schema.md`
- ✅ Correct: `README.md` (root level exception)
- ❌ Wrong: `test-report.md` (root level)
- ❌ Wrong: `design-doc.md` (root level)

### Code Documentation

- **README.md**: Project overview, setup, usage
- **API Documentation**: For all public APIs
- **Architecture Docs**: For complex systems
- **Inline Comments**: For complex algorithms

### Keeping Documentation Current

- Update docs when changing functionality
- Include documentation updates in the same commit as code changes
- Review documentation during code review

## AI Assistant Specific Guidelines

### Task Management

1. **Use TodoWrite Tool Frequently**:
   - Break down complex tasks into smaller steps
   - Track progress for multi-step operations
   - Mark tasks as in_progress before starting
   - Mark tasks as completed immediately after finishing
   - Only ONE task in_progress at a time

2. **Planning Large Tasks**:
   ```
   - Research/understand existing code
   - Design the solution
   - Implement core functionality
   - Add tests
   - Update documentation
   - Review and refactor
   ```

### Code Changes

1. **Read Before Edit**: Always use Read tool before editing files
2. **Prefer Edit Over Write**: Edit existing files rather than rewriting
3. **Preserve Formatting**: Match existing indentation and style
4. **Test After Changes**: Run tests after making modifications

### Communication

1. **Concise Responses**: Keep explanations brief and technical
2. **No Emojis**: Unless explicitly requested
3. **Technical Accuracy**: Prioritize correctness over validation
4. **Show, Don't Tell**: Provide code references with line numbers

### Tool Usage

1. **Parallel Execution**: Run independent tools in parallel
2. **Specialized Tools**: Use Task tool for complex searches
3. **Appropriate Tools**:
   - `Read` for reading files (not `cat`)
   - `Edit` for editing files (not `sed`)
   - `Grep` for searching content (not `grep` command)
   - `Glob` for finding files (not `find`)

### File References

Always include file paths with line numbers when referencing code:
```
The error is handled in src/services/api.ts:145
```

## Project-Specific Conventions

### To Be Defined

As the project evolves, add:
- Technology stack specifics
- Framework conventions
- API design patterns
- Database schema conventions
- Build and deployment processes
- Environment setup instructions
- Common troubleshooting steps

## Workflow Checklist for AI Assistants

When working on a task:

- [ ] Understand the requirement fully
- [ ] Create TodoWrite plan for complex tasks
- [ ] Search/read existing code to understand context
- [ ] Make minimal, focused changes
- [ ] Follow existing code style and patterns
- [ ] Add/update tests for new functionality
- [ ] Verify no security vulnerabilities introduced
- [ ] Update documentation if needed
- [ ] Test changes work as expected
- [ ] Create descriptive commit message
- [ ] Commit changes with proper message format
- [ ] Push to the correct Claude feature branch
- [ ] Mark tasks as completed

## Resources and References

### Git Resources
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

### Security Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Best Practices](https://cheatsheetseries.owasp.org/)

### Testing Resources
- [Testing Best Practices](https://testingjavascript.com/)
- [AAA Pattern](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)

## Version History

- **2025-11-14**: Added documentation file organization rules - All .md files (except README.md and CLAUDE.md) must be placed in docs/ directory
- **2025-11-14**: Initial CLAUDE.md creation - Repository bootstrap phase

---

**Note to AI Assistants**: This document should be updated as the codebase evolves. When you notice patterns, conventions, or important information that would help future AI assistants, update this file accordingly.
