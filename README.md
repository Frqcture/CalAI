# CalAI

AI-powered calibration and diagnostics intelligence platform for automotive engineers.

## Quick Setup

1. Clone the repository.
2. Create environment-specific files (for example, `.env`) locally.
3. Use Docker Compose as the primary deployment method for self-hosted installations.

## Documentation

- Full project specification: `/home/runner/work/CalAI/CalAI/docs/PROJECT_SPECIFICATION.md`

## `.gitignore` Setup Guidance

Add a `.gitignore` file at the repository root and include entries that prevent committing local/runtime artifacts, for example:

```gitignore
# Environment files
.env
.env.*

# Python
__pycache__/
*.pyc

# Node
node_modules/
.next/

# Logs and local artifacts
*.log
coverage/
dist/
```

Adjust entries based on the stack components you add to the repository.
