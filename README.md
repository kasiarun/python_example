# Smart Dependency Upgrade Agent

An intelligent LLM-powered agent system that automates Python dependency upgrades using GPT-4 code analysis and LangGraph orchestration.

## 🎯 Overview

This project demonstrates a sophisticated multi-agent system that uses Large Language Models (LLMs) to intelligently detect and fix code compatibility issues, rather than relying on hardcoded patterns. The system leverages LangGraph for orchestration and provides complete observability through LangSmith tracing.

## 🏗️ LangGraph Multi-Agent Architecture

### Agent Workflow
```
🔄 Git Sync → 🧠 LLM Analysis → 🔧 Fix Generation → ⚡ Fix Application → 🧪 Testing
```

### Core Agents

#### 1. **Git Sync Agent**
- **Purpose**: Synchronize with remote repository
- **Actions**: 
  - Pull latest changes from GitHub
  - Ensure working with current codebase
- **Output**: Updated local repository

#### 2. **Smart Code Analyzer Agent** 
- **Purpose**: LLM-powered code analysis
- **Technology**: GPT-4 with temperature=0.1 for consistent analysis
- **Actions**:
  - Analyze Python files for issues using natural language understanding
  - Detect deprecated methods, security vulnerabilities, compatibility issues
  - Identify bad practices and potential runtime errors
- **Output**: Structured issue reports with severity and suggested fixes

#### 3. **Smart Code Fixer Agent**
- **Purpose**: Generate and apply intelligent fixes
- **Technology**: GPT-4 for fix generation
- **Actions**:
  - Generate specific code fixes based on LLM analysis
  - Apply surgical code modifications
  - Preserve code functionality while fixing issues
- **Output**: Applied code changes with explanations

#### 4. **Smart Test Runner Agent**
- **Purpose**: Validate applied changes
- **Actions**:
  - Execute modified code to ensure functionality
  - Capture and report any runtime errors
  - Validate that fixes don't break existing functionality
- **Output**: Test results and error reports

## 🔄 State Management

The system uses a shared `AgentState` that flows between agents:

```python
class AgentState(TypedDict):
    repository_path: str                    # Target repository
    file_contents: Dict[str, str]           # File contents for analysis
    issues_found: List[Dict[str, Any]]      # LLM-detected issues
    suggested_fixes: List[Dict[str, Any]]   # Generated fixes
    applied_changes: List[str]              # Applied modifications
    test_results: Dict[str, Any]           # Validation results
    messages: Annotated[List[str], add_messages]  # Agent communications
```

## 🧠 LLM Intelligence vs Traditional Patterns

### Traditional Approach (Avoided)
- ❌ Hardcoded regex patterns
- ❌ Static rule-based detection
- ❌ Limited to known issues
- ❌ Brittle and maintenance-heavy

### LLM-Powered Approach (Implemented)
- ✅ Natural language code understanding
- ✅ Context-aware issue detection
- ✅ Intelligent fix generation
- ✅ Adaptable to new patterns and issues
- ✅ Explains reasoning behind fixes

## 📊 Demonstration Results

### Issues Intelligently Detected by GPT-4:
1. **JSON Serialization Errors**: `datetime.datetime.now()` objects not serializable
2. **Missing File Encodings**: File operations without explicit `encoding='utf-8'`
3. **Deprecated Patterns**: Usage of less optimal coding approaches
4. **Security Concerns**: Potential vulnerabilities in file handling

### Intelligent Fixes Applied:
1. **DateTime Serialization**: `datetime.now()` → `datetime.now().isoformat()`
2. **File Encoding**: Added `encoding='utf-8'` to all file operations
3. **Error Handling**: Improved exception handling patterns
4. **Code Modernization**: Updated to current best practices

## 🔍 Observability & Tracing

### LangSmith Integration
- **Complete Workflow Tracing**: Every agent interaction logged
- **LLM Call Monitoring**: All GPT-4 requests and responses tracked
- **Decision Transparency**: Why specific fixes were chosen
- **Performance Metrics**: Agent execution times and success rates

### Configuration
```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "smart-dependency-agent"
```

## 🚀 Usage

### Prerequisites
```bash
pip install langgraph langchain-openai
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key"
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="your-langsmith-api-key"
export LANGSMITH_PROJECT="your-project-name"
```

### Running the Agent
```bash
python smart_dependency_agent.py
```

### Expected Output
```
=== Smart Dependency Upgrade Agent Demo ===
🚀 Starting Smart Dependency Upgrade Workflow
🔄 Git Sync Agent: Syncing with GitHub repository
✅ Successfully synced with GitHub
🧠 Smart Code Analyzer: Analyzing code with LLM
🔧 Smart Code Fixer: Generating fixes with LLM
⚡ Smart Code Fixer: Applying fixes
🧪 Smart Test Runner: Testing fixed code

=== Results ===
Success: True
Summary: Smart upgrade completed. Issues found: 6, Changes applied: 6
```

## 📁 Repository Structure

```
├── README.md                      # This comprehensive documentation
├── smart_dependency_agent.py      # Complete LangGraph agent system
└── python_hello/
    ├── file_processor.py          # Demo program (fixed by LLM)
    └── requirements.txt           # Dependency specifications
```

## 🔧 Technical Implementation

### LangGraph Workflow Definition
```python
def _build_workflow(self) -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Sequential agent execution
    workflow.add_node("git_sync", self.git_sync.sync_with_github)
    workflow.add_node("analyze", self.analyzer.analyze_code)
    workflow.add_node("generate_fixes", self.fixer.generate_fixes)
    workflow.add_node("apply_fixes", self.fixer.apply_fixes)
    workflow.add_node("test", self.tester.run_tests)
    
    # Linear workflow with state passing
    workflow.set_entry_point("git_sync")
    workflow.add_edge("git_sync", "analyze")
    workflow.add_edge("analyze", "generate_fixes")
    workflow.add_edge("generate_fixes", "apply_fixes")
    workflow.add_edge("apply_fixes", "test")
    workflow.add_edge("test", END)
    
    return workflow.compile()
```

### LLM Prompting Strategy
The system uses carefully crafted prompts for:
- **Code Analysis**: Structured issue detection with severity levels
- **Fix Generation**: Specific code modifications with explanations
- **JSON Response Parsing**: Reliable structured output from LLM

## 🎯 Key Benefits

1. **True Intelligence**: Uses LLM reasoning instead of pattern matching
2. **Adaptability**: Handles new types of issues without code changes
3. **Transparency**: Full tracing of all decisions and reasoning
4. **Scalability**: Easy to add new agents or modify existing ones
5. **Production Ready**: Handles real-world code issues effectively

## 🔮 Future Enhancements

- **Multi-language Support**: Extend beyond Python
- **Custom Rule Integration**: Combine LLM intelligence with domain-specific rules
- **Automated PR Creation**: Generate pull requests with fix summaries
- **Continuous Monitoring**: Schedule regular dependency health checks
- **Team Integration**: Slack/Teams notifications for upgrade results

## 📄 License

MIT License - See LICENSE file for details

---

*This project demonstrates the power of combining LLM intelligence with structured agent orchestration for automated code maintenance and dependency management.*