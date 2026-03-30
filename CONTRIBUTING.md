# Contributing to BMAD BDA

Thank you for considering contributing to BMAD BDA! This extension aims to close the production lifecycle gap in the BMAD Method.

## How to Contribute

### 1. Report Issues

Found a bug or have a feature request?

- Check [existing issues](https://github.com/vforvaick/bmad-devops-analytics/issues)
- Open a new issue with clear description
- Include reproduction steps for bugs
- Tag appropriately: `bug`, `enhancement`, `documentation`, `adapter`

### 2. Submit Pull Requests

**Before starting work:**
1. Check if there's an existing issue
2. Comment on the issue that you're working on it
3. Fork the repository
4. Create a feature branch: `git checkout -b feature/your-feature-name`

**Development workflow:**
1. Make your changes
2. Test thoroughly (see Testing section)
3. Update documentation if needed
4. Commit with clear messages (see Commit Convention)
5. Push and create a Pull Request

**PR Guidelines:**
- Link to related issue(s)
- Describe what changed and why
- Include testing evidence
- Update CHANGELOG.md
- Ensure all checks pass

### 3. Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear instructions
- Add examples or use cases
- Improve workflow documentation
- Translate to other languages

### 4. Create Custom Adapters

Have a custom observability stack? Contribute an adapter!

See `adapters/README.md` for adapter development guide.

**Adapter contributions should include:**
- Implementation of `IEvidenceAdapter` interface
- README with setup instructions
- Example configuration
- Health check implementation
- Tests

## Development Setup

### Prerequisites

- Node.js 18+
- BMAD Method v6+ installed
- Docker (for testing VPS adapter)
- Access to test VPS or cloud account

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/bda.git
cd bda

# Install dependencies (if any)
npm install

# Link to local BMAD project for testing
cd /path/to/your-bmad-project/_bmad/_config/custom/modules/
ln -s /path/to/bda bda

# Rebuild BMAD
cd /path/to/your-bmad-project
npx bmad-method install --action update --yes

# Copy to .agents/skills for IDE detection
cp -r _bmad/bda/workflows/* .agents/skills/
```

### Testing

**Test workflows:**

```bash
# In your BMAD test project
/bmad-bda-release-readiness
/bmad-bda-deployment-verification
/bmad-bda-observability-setup
# etc.
```

**Test adapters:**

```bash
# Unit tests (when implemented)
npm test

# Integration tests with real stack
docker-compose -f adapters/vps-default/docker-compose.test.yml up
npm run test:integration
```

**Test against real deployment:**

1. Use a staging/test project
2. Run complete Phase 5 workflow
3. Verify all artifacts generated correctly
4. Verify insights are actionable

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring (no feature/bug change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Scopes:**
- `workflow`: Workflow changes
- `agent`: Agent definition changes
- `adapter`: Adapter implementation
- `docs`: Documentation
- `template`: Template changes

**Examples:**

```bash
feat(adapter): add AWS CloudWatch adapter
fix(workflow): correct evidence collection timeout
docs(quickstart): add troubleshooting section
chore(deps): update BMAD Method to v6.2
```

## Code Style

### YAML (agents, module config)

```yaml
# Use 2-space indentation
name: Agent Name
role: role-name

# Arrays on new lines
expertise:
  - Item one
  - Item two

# Multi-line strings with pipe
description: |
  First paragraph.
  
  Second paragraph.
```

### Markdown (documentation)

- Use ATX-style headers (`#`, `##`, `###`)
- Code blocks with language specification
- Tables for structured data
- Emoji for visual hierarchy (sparingly)

### TypeScript (adapter implementations)

```typescript
// Use async/await
async collectLogs(since: Date): Promise<LogEntry[]> {
  // Implementation
}

// Proper error handling
try {
  const data = await fetchData();
  return data;
} catch (error) {
  throw new AdapterError(`Failed to collect logs: ${error.message}`);
}

// Type everything
interface LogEntry {
  timestamp: Date;
  level: string;
  message: string;
  metadata: Record<string, any>;
}
```

## Architecture Principles

### 1. Human-in-the-Loop by Default

All workflows produce **drafts** for human review. Never auto-commit to PRD or epics without explicit approval.

### 2. Adapter Contract Over Implementation

Workflows should work with any adapter implementing `IEvidenceAdapter`. Don't hardcode stack-specific logic in workflows.

### 3. Evidence-Driven Insights

All recommendations must be backed by concrete production evidence. No speculation or best practices without data.

### 4. BMAD Convention Compliance

Follow BMAD patterns:
- Agents have clear roles and constraints
- Workflows have defined inputs/outputs
- Artifacts go to `_bmad-output/production-artifacts/`
- Use BMAD handoff patterns between agents

### 5. Graceful Degradation

Support multiple environments (VPS, Vercel, shared hosting) with degraded but functional operation when full stack unavailable.

## Adding New Features

### Adding a Workflow

1. Create workflow directory: `workflows/your-workflow/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: bmad-bda-your-workflow
   description: Your workflow description. Use when the user says "trigger phrase"
   ---
   ```
3. Add `bmad-skill-manifest.yaml` with metadata
4. Update `module.yaml` to register workflow
5. Add documentation in `docs/workflows/`
6. Test end-to-end

### Adding an Agent

1. Create agent YAML: `agents/your-agent.yaml`
2. Define role, expertise, responsibilities
3. Specify context requirements
4. Document handoff patterns
5. Update `module.yaml`
6. Add agent guide in `docs/agents/`

### Adding an Adapter

1. Create adapter directory: `adapters/your-adapter/`
2. Implement `IEvidenceAdapter` interface
3. Add `README.md` with setup instructions
4. Add `docker-compose.yml` or config templates
5. Implement `healthCheck()` method
6. Add tests
7. Update main README.md

## Testing Checklist

Before submitting PR:

- [ ] All workflows complete successfully
- [ ] Generated artifacts are well-formed
- [ ] Documentation is updated
- [ ] Examples are tested
- [ ] No hardcoded values (use env vars)
- [ ] Error messages are helpful
- [ ] Adapters pass health checks
- [ ] Works on fresh BMAD project
- [ ] Follows BMAD conventions

## Review Process

1. **Automated Checks** - Linting, tests (when implemented)
2. **Maintainer Review** - Code quality, architecture fit
3. **Documentation Review** - Clarity, completeness
4. **Testing** - Manually tested against real BMAD project
5. **Merge** - Squash and merge to main

## Release Process

Releases follow semantic versioning:

- **v1.x.x** - Mode A (human-in-the-loop) - Current
- **v2.x.x** - Mode B (assisted drafting) - Future
- **v3.x.x** - Mode C (autonomous) - Experimental

Minor versions (v1.1, v1.2) add:
- New adapters
- Workflow improvements
- Documentation enhancements

Patch versions (v1.0.1) fix:
- Bugs
- Documentation errors
- Minor improvements

## Community

- **Discussions**: [GitHub Discussions](https://github.com/vforvaick/bmad-devops-analytics/discussions)
- **BMAD Discord**: [Join here](https://discord.gg/bmad-method)
- **Email**: vforvaick@example.com (for sensitive topics)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in documentation (if applicable)

## Code of Conduct

Be respectful, inclusive, and constructive. We're building tools to help developers ship better products.

- Assume good intent
- Provide constructive feedback
- Focus on ideas, not people
- Help others learn

## Questions?

Not sure where to start? Open a discussion or reach out!

**Thank you for contributing to BMAD BDA!** 🚀
