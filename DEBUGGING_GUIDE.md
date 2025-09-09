# LangGraph Local Debugger Integration Guide

This guide shows you how to integrate and use local debugging tools with LangGraph StateGraph workflows.

## 🚀 Quick Start

### 1. Interactive Debugging Session
```bash
python langgraph_debugger_guide.py --debug
```

### 2. VS Code Debugging
1. Open VS Code in this directory
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select "Debug LangGraph Workflow" from dropdown
4. Press F5 to start debugging

## 🛠️ Available Debugging Methods

### Method 1: Python Built-in Debugger (pdb)
- **Breakpoints**: Set `pdb.set_trace()` in your node functions
- **Interactive**: Step through code line by line
- **Commands**:
  - `n` - Next line
  - `c` - Continue execution
  - `p variable_name` - Print variable
  - `pp state` - Pretty print state
  - `q` - Quit debugger

### Method 2: Custom State Inspection
- **State Logging**: Automatic logging of state transitions
- **Debug Info**: Embedded debugging information in state
- **Execution History**: Complete trace of workflow execution

### Method 3: VS Code Integration
- **Visual Debugging**: Set breakpoints by clicking line numbers
- **Variable Inspector**: View all variables in sidebar
- **Debug Console**: Evaluate expressions during execution
- **Call Stack**: See the execution path

### Method 4: Performance Debugging
- **Timing**: Measure execution time per node
- **Memory Usage**: Track memory consumption
- **Performance Reports**: Detailed analysis of bottlenecks

### Method 5: Checkpointing
- **Step-by-Step**: Execute workflow one step at a time
- **State Persistence**: Save and restore workflow state
- **Replay**: Re-run from any checkpoint

## 📁 Files Overview

### Core Files
- **`langgraph_debugger_guide.py`** - Complete debugging tutorial and examples
- **`.vscode/launch.json`** - VS Code debugging configuration
- **`smart_dependency_agent.py`** - Production LangGraph workflow

### Generated Debug Files
- **`langgraph_debug.log`** - Execution logs
- **`*_debug_report.json`** - Detailed state history
- **`my_workflow_diagram.md`** - Workflow visualization

## 🔍 Debugging Your Own LangGraph Workflows

### Step 1: Add Debug Capabilities to Nodes
```python
import pdb
import logging

async def my_debug_node(state: MyState) -> MyState:
    # Add logging
    logging.info(f"Processing state: {state}")
    
    # Optional breakpoint
    pdb.set_trace()  # Pauses execution here
    
    # Your node logic here
    result = process_data(state['input'])
    
    # Update state
    state['output'] = result
    return state
```

### Step 2: Create Debuggable Workflow
```python
from langgraph.checkpoint.memory import MemorySaver

# Add checkpointing for step-by-step debugging
memory = MemorySaver()
workflow = workflow.compile(checkpointer=memory)

# Run with thread_id for persistence
config = {"configurable": {"thread_id": "debug-session-1"}}
result = await workflow.ainvoke(initial_state, config=config)
```

### Step 3: Add State Inspection
```python
class MyDebugState(TypedDict):
    # Your regular state fields
    input_data: str
    output_data: str
    
    # Debug fields
    debug_info: Dict[str, Any]
    step_count: int
    errors: List[str]
```

## 🎯 Common Debugging Scenarios

### Scenario 1: Node Not Executing
**Problem**: A node in your workflow isn't being called
**Debug Steps**:
1. Check workflow edges: `print(workflow.get_graph().edges)`
2. Verify node names match exactly
3. Add logging to entry point
4. Use VS Code debugger to step through flow

### Scenario 2: State Not Updating
**Problem**: State changes aren't persisting between nodes
**Debug Steps**:
1. Add `pdb.set_trace()` before and after state updates
2. Check if you're returning the updated state
3. Verify state schema matches TypedDict
4. Use state inspection logging

### Scenario 3: Performance Issues
**Problem**: Workflow is running slowly
**Debug Steps**:
1. Use `PerformanceDebugger` class
2. Time each node execution
3. Monitor memory usage
4. Check for blocking operations

### Scenario 4: Conditional Logic Not Working
**Problem**: Conditional edges aren't routing correctly
**Debug Steps**:
1. Add logging to conditional functions
2. Print the return value of condition checks
3. Verify condition function return values match edge mapping
4. Use breakpoints in conditional logic

## 🔧 VS Code Setup

### Required Extensions
- Python (Microsoft)
- Python Debugger (Microsoft)

### Debugging Configuration
The `.vscode/launch.json` file includes:
- **Debug LangGraph Workflow**: Debug the tutorial examples
- **Debug Smart Dependency Agent**: Debug the production workflow

### Debugging Tips
1. **Set Breakpoints**: Click left of line numbers
2. **Conditional Breakpoints**: Right-click breakpoint → Edit Breakpoint
3. **Logpoints**: Add logging without modifying code
4. **Watch Variables**: Add expressions to Watch panel
5. **Debug Console**: Evaluate code during debugging

## 📊 Debug Output Examples

### Execution Log
```
🔄 Transition: input_processor → analyzer
   State: {'step_count': 1, 'data_size': 4, 'message_count': 1}

🔄 Transition: analyzer → result_formatter  
   State: {'step_count': 2, 'data_size': 4, 'message_count': 2}
```

### Performance Report
```
📊 PERFORMANCE REPORT
========================================
input_processor:
  Time: 0.045s (23.1%)
  Memory: +2.34MB

analyzer:
  Time: 0.123s (63.1%)
  Memory: +1.12MB

result_formatter:
  Time: 0.027s (13.8%)
  Memory: +0.45MB

Total Time: 0.195s
Total Memory Change: +3.91MB
```

## 🚨 Troubleshooting

### Common Issues

1. **ImportError: No module named 'langgraph'**
   ```bash
   pip install langgraph langchain-openai
   ```

2. **Debugger not stopping at breakpoints**
   - Ensure `justMyCode: false` in launch.json
   - Check that breakpoints are on executable lines
   - Verify Python interpreter is correct

3. **State not serializable**
   - Use `default=str` in json.dumps()
   - Avoid complex objects in state
   - Convert datetime to strings

4. **Memory issues with large states**
   - Use state snapshots instead of full state
   - Clear unnecessary data between nodes
   - Monitor memory usage with PerformanceDebugger

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Python Debugging Guide](https://docs.python.org/3/library/pdb.html)
- [VS Code Python Debugging](https://code.visualstudio.com/docs/python/debugging)

## 🎉 Happy Debugging!

With these tools and techniques, you can effectively debug any LangGraph StateGraph workflow. Start with simple logging, add breakpoints where needed, and use VS Code's visual debugging for complex issues.