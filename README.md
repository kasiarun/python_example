# Dependency Upgrade Agent

An intelligent agent system that automates Python dependency upgrades using Roo code modification capabilities and LangGraph orchestration.

## Features

- **Intelligent Dependency Analysis**: Scans repositories for outdated dependencies and security vulnerabilities
- **Smart Code Modifications**: Uses Roo's AST-level understanding to handle API changes and refactoring
- **Automated Testing**: Runs test suites to validate upgrades before committing
- **Git Integration**: Creates branches, commits, and pull requests with detailed documentation
- **Multi-Agent Architecture**: Uses LangGraph to orchestrate specialized agents for each task

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Repository      │    │ Dependency      │    │ Upgrade         │
│ Scanner Agent   │───▶│ Analyzer Agent  │───▶│ Planner Agent   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Documentation   │    │ PR Creator      │    │ Test Runner     │
│ Agent           │◀───│ Agent           │◀───│ Agent           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐              │
                       │ Roo Code        │◀─────────────┘
                       │ Modifier Agent  │
                       └─────────────────┘
```

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Upgrade dependencies in current directory
dep-upgrade --repo-path . --create-pr

# Upgrade specific dependencies
dep-upgrade --repo-path /path/to/repo --dependencies requests,numpy --dry-run

# Upgrade with custom configuration
dep-upgrade --config config.yaml --repo-path /path/to/repo
```

### Python API

```python
from dependency_upgrade_agent import DependencyUpgradeWorkflow

# Initialize the workflow
workflow = DependencyUpgradeWorkflow()

# Run upgrade process
result = await workflow.run_upgrade(
    repository_path="/path/to/repo",
    create_pr=True,
    run_tests=True
)

print(f"Upgrade completed: {result.summary}")
```

## Configuration

Create a `config.yaml` file to customize the upgrade process:

```yaml
# Repository settings
git:
  branch_prefix: "upgrade/"
  commit_message_template: "chore: upgrade {package} from {old_version} to {new_version}"
  
# Testing configuration
testing:
  run_tests: true
  test_commands:
    - "pytest"
    - "mypy ."
  
# Upgrade preferences
upgrades:
  include_prereleases: false
  max_major_version_jumps: 1
  security_only: false
  
# AI/LLM configuration
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.1
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

## License

MIT License