# Smart Dependency Upgrade Agent

An intelligent, LLM-powered system that automatically detects, analyzes, and fixes code issues using LangGraph workflow orchestration.

## Overview

The Smart Dependency Upgrade Agent is a sophisticated multi-agent system that leverages Large Language Models (LLMs) to intelligently analyze Python codebases, identify issues such as deprecated methods, security vulnerabilities, and compatibility problems, then automatically generate and apply fixes.

## Architecture

The system is built using **LangGraph** for workflow orchestration and consists of five specialized agents working in sequence:

### 🔄 GitSyncAgent
- **Purpose**: Ensures repository synchronization before analysis
- **Key Features**:
  - Auto-commits uncommitted local changes
  - Pushes local commits to remote repository
  - Pulls latest changes from remote
- **Workflow Position**: Entry point of the system

### 🧠 SmartCodeAnalyzerAgent
- **Purpose**: Uses Roo Code to analyze code for potential issues
- **Analysis Categories**:
  - Deprecated methods or functions
  - Security vulnerabilities
  - Compatibility issues
  - Bad practices
  - Potential runtime errors
- **Output**: Structured JSON with issue details, severity, and suggested fixes

### 🔧 SmartCodeFixerAgent
- **Purpose**: Generates and applies intelligent fixes using LLM
- **Capabilities**:
  - Generates specific code fixes based on identified issues
  - Applies fixes through string replacement
  - Creates new `_fixed.py` versions of modified files
- **Fix Types**: Replace, insert, delete operations

### 🧪 SmartTestRunnerAgent
- **Purpose**: Validates fixes by running the code
- **Testing Strategy**:
  - Prioritizes testing fixed files over original files
  - Executes Python files to verify they run without errors
  - Tracks success/failure rates and error details

### 📊 Workflow Orchestrator
- **Purpose**: Coordinates the entire upgrade process
- **Technology**: LangGraph StateGraph for workflow management
- **State Management**: Shared state across all agents with message passing

## Key Features

### 🤖 LLM-Powered Intelligence
- Uses Roo Code for code analysis and fix generation
- Structured prompts for consistent, high-quality results
- JSON-based communication between LLM and agents

### 🔄 Git Integration
- Automatic commit and push of local changes before analysis
- Ensures remote repository is always up-to-date
- Seamless integration with existing Git workflows

### 📈 Comprehensive Analysis
- Multi-category issue detection (deprecation, security, compatibility)
- Severity classification (high/medium/low)
- Line-number identification for precise issue location

### ⚡ Automated Fixes
- Intelligent code replacement based on LLM suggestions
- Safe file handling with `_fixed` suffix preservation
- Rollback capability through original file preservation

### 🧪 Validation & Testing
- Automatic execution testing of fixed code
- Error tracking and reporting
- Success rate monitoring

## Workflow Sequence

```
1. GitSync → 2. Analyze → 3. Generate Fixes → 4. Apply Fixes → 5. Test → End
```

### Detailed Flow:
1. **Git Sync**: Commit local changes, push to remote, pull latest
2. **Code Analysis**: Roo Code analyzes all Python files for issues
3. **Fix Generation**: Roo Code generates specific fixes for identified issues
4. **Fix Application**: Apply fixes and create new fixed versions
5. **Testing**: Execute fixed files to validate functionality

## Configuration

### Environment Variables
```bash
# Optional: LangSmith tracing (if desired)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=smart-dependency-agent
LANGCHAIN_API_KEY=your_langsmith_api_key
```

### Dependencies
```bash
pip install python-dotenv
```

**Note**: No external API keys required! Roo Code integration is built-in.

## Usage

### Basic Usage
```python
from smart_dependency_agent import SmartDependencyUpgradeWorkflow

# Initialize the workflow
workflow = SmartDependencyUpgradeWorkflow()

# Run upgrade on a directory
result = await workflow.run_upgrade("path/to/your/code")

# Check results
print(f"Success: {result.success}")
print(f"Issues found: {len(result.issues_found)}")
print(f"Changes applied: {len(result.changes_made)}")
```

### Command Line Usage
```bash
python smart_dependency_agent.py
```

## Output Structure

### UpgradeResult
```python
@dataclass
class UpgradeResult:
    success: bool                # Overall success status
    summary: str                 # Human-readable summary
    changes_made: List[str]      # List of applied changes
    errors: List[str]           # Any errors encountered
    issues_found: List[str]     # Issues identified by Roo Code
```

### Agent State
The shared state object contains:
- `repository_path`: Target directory path
- `file_contents`: Dictionary of file contents
- `issues_found`: List of identified issues with metadata
- `suggested_fixes`: List of Roo Code-generated fixes
- `applied_changes`: List of successfully applied changes
- `test_results`: Testing outcomes and statistics
- `messages`: Communication log between agents

## Example Output

```
=== Smart Dependency Upgrade Agent Demo ===
🚀 Starting Smart Dependency Upgrade Workflow
🔄 Git Sync Agent: Committing local changes and syncing with GitHub
📍 No uncommitted changes found
📍 No local commits to push
✅ Successfully pulled from GitHub
🧠 Smart Code Analyzer: Analyzing code with Roo Code
🔧 Smart Code Fixer: Generating fixes with Roo Code
⚡ Smart Code Fixer: Applying fixes to new files
Created fixed version: python_hello/file_processor_fixed.py
🧪 Smart Test Runner: Testing original and fixed code
✅ Fixed file runs successfully: python_hello/file_processor_fixed.py

=== Results ===
Success: True
Summary: Smart upgrade completed. Issues found: 2, Changes applied: 3

Issues found by Roo Code:
  - The method datetime.datetime.utcnow().isoformat() is deprecated.
  - The debug mode is being set by checking an environment variable directly.

Changes applied:
  - Fixed deprecated datetime method in python_hello/file_processor.py
  - Fixed environment variable handling in python_hello/file_processor.py
  - Created fixed version: python_hello/file_processor_fixed.py
```

## Technical Details

### LangGraph Integration
- **StateGraph**: Manages workflow state and transitions
- **Node Definition**: Each agent is a workflow node
- **Edge Configuration**: Defines execution sequence
- **State Persistence**: Maintains context across agent transitions

### Roo Code Prompt Engineering
- **System Prompts**: Define agent roles and capabilities
- **Human Prompts**: Provide specific code and context
- **JSON Parsing**: Structured response handling
- **Error Recovery**: Graceful handling of malformed responses

### File Management
- **Safe Operations**: Original files are never modified
- **Versioning**: `_fixed` suffix for modified files
- **Path Handling**: Cross-platform path management
- **Error Handling**: Comprehensive exception management

## Limitations & Considerations

### Current Limitations
- Python-only code analysis (extensible to other languages)
- No external API dependencies (fully self-contained)
- Limited to text-based fixes (no complex refactoring)
- Built-in Roo Code intelligence for analysis and fixes

### Best Practices
- Test in development environments first
- Review generated fixes before production deployment
- Maintain backup copies of original code
- Monitor API usage and costs
- Validate fixes in your specific context

## Future Enhancements

### Planned Features
- Multi-language support (JavaScript, Java, etc.)
- Integration with CI/CD pipelines
- Custom rule definition and validation
- Advanced refactoring capabilities
- Performance optimization suggestions
- Security vulnerability scanning integration

### Extensibility
The modular agent architecture allows for easy extension:
- Add new analysis agents for specific domains
- Integrate additional testing frameworks
- Extend fix application strategies
- Add custom validation rules

## Contributing

The Smart Dependency Upgrade Agent is designed for extensibility. Key extension points:

1. **New Agents**: Implement new agents following the existing pattern
2. **Analysis Rules**: Extend the Roo Code prompts for new issue categories
3. **Fix Strategies**: Add new fix application methods
4. **Testing Integration**: Integrate with additional testing frameworks

## License

This project is designed for educational and development purposes. The Roo Code integration is self-contained and requires no external API access or credits.