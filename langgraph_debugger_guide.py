#!/usr/bin/env python3
"""
LangGraph Local Debugger Integration Guide
Complete tutorial on debugging LangGraph StateGraph workflows locally
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import pdb  # Python debugger
import traceback

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('langgraph_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# State definition with debugging info
class DebugAgentState(TypedDict):
    """State with debugging capabilities"""
    input_data: str
    processed_data: List[str]
    results: Dict[str, Any]
    messages: Annotated[List[str], add_messages]
    debug_info: Dict[str, Any]
    step_count: int
    errors: List[str]

# Method 1: Using Python's built-in debugger (pdb)
class DebugNode:
    """Base class for debuggable nodes"""
    
    def __init__(self, name: str, enable_breakpoint: bool = False):
        self.name = name
        self.enable_breakpoint = enable_breakpoint
        self.logger = logging.getLogger(f"Node.{name}")
    
    def debug_state(self, state: DebugAgentState, step: str):
        """Debug helper to inspect state"""
        self.logger.info(f"🔍 {self.name} - {step}")
        self.logger.info(f"State keys: {list(state.keys())}")
        self.logger.info(f"Step count: {state.get('step_count', 0)}")
        
        # Add debug info to state
        if 'debug_info' not in state:
            state['debug_info'] = {}
        
        state['debug_info'][f"{self.name}_{step}"] = {
            'timestamp': asyncio.get_event_loop().time(),
            'state_size': len(str(state)),
            'keys': list(state.keys())
        }
        
        # Optional breakpoint
        if self.enable_breakpoint:
            print(f"🛑 BREAKPOINT: {self.name} - {step}")
            print(f"Current state: {json.dumps(state, indent=2, default=str)}")
            pdb.set_trace()  # This will pause execution and open debugger

async def debug_input_processor(state: DebugAgentState) -> DebugAgentState:
    """Input processor with debugging capabilities"""
    node = DebugNode("InputProcessor", enable_breakpoint=True)
    
    try:
        node.debug_state(state, "START")
        
        # Process input
        input_data = state.get('input_data', '')
        node.logger.info(f"Processing input: {input_data}")
        
        if not input_data:
            raise ValueError("No input data provided")
        
        processed = input_data.upper().split()
        
        # Update state
        state['processed_data'] = processed
        state['messages'].append(f"Processed {len(processed)} words")
        state['step_count'] = state.get('step_count', 0) + 1
        
        node.debug_state(state, "END")
        
    except Exception as e:
        node.logger.error(f"Error in {node.name}: {e}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"{node.name}: {str(e)}")
        # Re-raise to see full traceback
        raise
    
    return state

async def debug_analyzer(state: DebugAgentState) -> DebugAgentState:
    """Analyzer with debugging capabilities"""
    node = DebugNode("Analyzer", enable_breakpoint=False)
    
    try:
        node.debug_state(state, "START")
        
        processed_data = state.get('processed_data', [])
        node.logger.info(f"Analyzing {len(processed_data)} items")
        
        # Simulate analysis
        analysis = {
            'word_count': len(processed_data),
            'unique_words': len(set(processed_data)),
            'avg_length': sum(len(word) for word in processed_data) / len(processed_data) if processed_data else 0
        }
        
        state['results'] = analysis
        state['messages'].append(f"Analysis complete: {analysis}")
        state['step_count'] += 1
        
        node.debug_state(state, "END")
        
    except Exception as e:
        node.logger.error(f"Error in {node.name}: {e}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"{node.name}: {str(e)}")
        raise
    
    return state

# Method 2: Custom debugging with state inspection
class LangGraphDebugger:
    """Custom debugger for LangGraph workflows"""
    
    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.execution_log = []
        self.state_history = []
        self.logger = logging.getLogger(f"Debugger.{workflow_name}")
    
    def log_state_transition(self, from_node: str, to_node: str, state: DebugAgentState):
        """Log state transitions between nodes"""
        transition = {
            'from': from_node,
            'to': to_node,
            'timestamp': asyncio.get_event_loop().time(),
            'state_snapshot': self._create_state_snapshot(state)
        }
        
        self.execution_log.append(transition)
        self.state_history.append(dict(state))
        
        self.logger.info(f"🔄 Transition: {from_node} → {to_node}")
        self.logger.debug(f"State snapshot: {transition['state_snapshot']}")
    
    def _create_state_snapshot(self, state: DebugAgentState) -> Dict:
        """Create a serializable snapshot of the state"""
        return {
            'step_count': state.get('step_count', 0),
            'data_size': len(state.get('processed_data', [])),
            'message_count': len(state.get('messages', [])),
            'has_results': bool(state.get('results')),
            'error_count': len(state.get('errors', []))
        }
    
    def print_execution_summary(self):
        """Print a summary of the execution"""
        print("\n" + "="*60)
        print(f"🔍 EXECUTION SUMMARY: {self.workflow_name}")
        print("="*60)
        
        for i, transition in enumerate(self.execution_log):
            print(f"{i+1}. {transition['from']} → {transition['to']}")
            print(f"   State: {transition['state_snapshot']}")
        
        print(f"\nTotal transitions: {len(self.execution_log)}")
        print(f"Final state keys: {list(self.state_history[-1].keys()) if self.state_history else 'None'}")
    
    def save_debug_report(self, filename: str = None):
        """Save detailed debug report to file"""
        if not filename:
            filename = f"{self.workflow_name}_debug_report.json"
        
        report = {
            'workflow_name': self.workflow_name,
            'execution_log': self.execution_log,
            'state_history': self.state_history,
            'summary': {
                'total_transitions': len(self.execution_log),
                'total_states': len(self.state_history),
                'final_state_keys': list(self.state_history[-1].keys()) if self.state_history else []
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Debug report saved to: {filename}")

# Method 3: Workflow with checkpointing for step-by-step debugging
def create_debuggable_workflow() -> StateGraph:
    """Create a workflow with debugging capabilities"""
    
    # Use MemorySaver for checkpointing (allows step-by-step execution)
    memory = MemorySaver()
    
    workflow = StateGraph(DebugAgentState)
    
    # Add nodes
    workflow.add_node("input_processor", debug_input_processor)
    workflow.add_node("analyzer", debug_analyzer)
    
    # Set up flow
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "analyzer")
    workflow.add_edge("analyzer", END)
    
    # Compile with checkpointing
    return workflow.compile(checkpointer=memory)

# Method 4: Interactive debugging session
async def interactive_debug_session():
    """Run an interactive debugging session"""
    print("🐛 Starting Interactive LangGraph Debug Session")
    print("="*50)
    
    # Create debugger
    debugger = LangGraphDebugger("InteractiveSession")
    
    # Create workflow
    workflow = create_debuggable_workflow()
    
    # Initial state
    initial_state = DebugAgentState(
        input_data="hello world debugging test",
        processed_data=[],
        results={},
        messages=[],
        debug_info={},
        step_count=0,
        errors=[]
    )
    
    print("🚀 Starting workflow execution...")
    print("💡 Tip: When debugger pauses, use these commands:")
    print("   - 'n' (next line)")
    print("   - 'c' (continue)")
    print("   - 'p variable_name' (print variable)")
    print("   - 'pp state' (pretty print state)")
    print("   - 'q' (quit)")
    
    try:
        # Run with thread_id for checkpointing
        config = {"configurable": {"thread_id": "debug-session-1"}}
        final_state = await workflow.ainvoke(initial_state, config=config)
        
        print("\n✅ Workflow completed successfully!")
        print(f"Final results: {final_state.get('results', {})}")
        
        # Print debug summary
        debugger.print_execution_summary()
        debugger.save_debug_report()
        
    except Exception as e:
        print(f"\n❌ Workflow failed with error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        
        # Save error report
        debugger.save_debug_report("error_debug_report.json")

# Method 5: VS Code debugging integration
def setup_vscode_debugging():
    """Instructions for VS Code debugging setup"""
    vscode_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug LangGraph Workflow",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/langgraph_debugger_guide.py",
                "console": "integratedTerminal",
                "justMyCode": False,
                "env": {
                    "PYTHONPATH": "${workspaceFolder}",
                    "LANGCHAIN_TRACING_V2": "true",
                    "LANGCHAIN_PROJECT": "langgraph-debug"
                },
                "args": ["--debug"]
            }
        ]
    }
    
    print("🔧 VS Code Debug Configuration:")
    print("Add this to your .vscode/launch.json file:")
    print(json.dumps(vscode_config, indent=2))
    
    print("\n📝 VS Code Debugging Tips:")
    print("1. Set breakpoints by clicking left of line numbers")
    print("2. Use F5 to start debugging")
    print("3. Use F10 to step over, F11 to step into")
    print("4. Inspect variables in the Debug sidebar")
    print("5. Use Debug Console to evaluate expressions")

# Method 6: Performance debugging
class PerformanceDebugger:
    """Debug performance issues in LangGraph workflows"""
    
    def __init__(self):
        self.timings = {}
        self.memory_usage = {}
    
    async def time_node_execution(self, node_name: str, node_func, state):
        """Time how long each node takes to execute"""
        import time
        import psutil
        import os
        
        # Get initial memory
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Time execution
        start_time = time.time()
        result = await node_func(state)
        end_time = time.time()
        
        # Get final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Store metrics
        self.timings[node_name] = end_time - start_time
        self.memory_usage[node_name] = final_memory - initial_memory
        
        print(f"⏱️  {node_name}: {self.timings[node_name]:.3f}s, Memory: {self.memory_usage[node_name]:+.2f}MB")
        
        return result
    
    def print_performance_report(self):
        """Print performance analysis"""
        print("\n📊 PERFORMANCE REPORT")
        print("="*40)
        
        total_time = sum(self.timings.values())
        total_memory = sum(self.memory_usage.values())
        
        for node_name in self.timings:
            time_pct = (self.timings[node_name] / total_time) * 100
            print(f"{node_name}:")
            print(f"  Time: {self.timings[node_name]:.3f}s ({time_pct:.1f}%)")
            print(f"  Memory: {self.memory_usage[node_name]:+.2f}MB")
        
        print(f"\nTotal Time: {total_time:.3f}s")
        print(f"Total Memory Change: {total_memory:+.2f}MB")

async def main():
    """Main function to demonstrate debugging techniques"""
    import sys
    
    if "--debug" in sys.argv:
        # Run interactive debug session
        await interactive_debug_session()
    else:
        # Show setup instructions
        print("🐛 LangGraph Local Debugger Integration Guide")
        print("="*50)
        print("\n1. Interactive Debugging:")
        print("   python langgraph_debugger_guide.py --debug")
        
        print("\n2. VS Code Integration:")
        setup_vscode_debugging()
        
        print("\n3. Available Debugging Methods:")
        print("   - Python pdb breakpoints")
        print("   - Custom state inspection")
        print("   - Execution logging")
        print("   - Performance profiling")
        print("   - Checkpointing for step-by-step execution")
        
        print("\n4. Debug Files Generated:")
        print("   - langgraph_debug.log (execution logs)")
        print("   - *_debug_report.json (detailed state history)")
        
        print("\n🚀 Run with --debug flag to start interactive session!")

if __name__ == "__main__":
    asyncio.run(main())