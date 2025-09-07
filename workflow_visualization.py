#!/usr/bin/env python3
"""
Visual representation of the LangGraph workflow execution
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_workflow_diagram():
    """Create a visual diagram of the LangGraph workflow"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'scanner': '#FF6B6B',
        'analyzer': '#4ECDC4', 
        'modifier': '#45B7D1',
        'tester': '#96CEB4',
        'state': '#FFEAA7',
        'flow': '#DDA0DD'
    }
    
    # Agent boxes
    agents = [
        {'name': 'Repository\nScanner Agent', 'pos': (2, 9), 'color': colors['scanner']},
        {'name': 'Dependency\nAnalyzer Agent', 'pos': (2, 7), 'color': colors['analyzer']},
        {'name': 'Code\nModifier Agent', 'pos': (2, 5), 'color': colors['modifier']},
        {'name': 'Test\nRunner Agent', 'pos': (2, 3), 'color': colors['tester']}
    ]
    
    # State components
    state_components = [
        {'name': 'repository_path', 'pos': (6, 10.5), 'input': True},
        {'name': 'current_issues', 'pos': (6, 9.5), 'input': False},
        {'name': 'dependencies_to_upgrade', 'pos': (6, 8.5), 'input': False},
        {'name': 'code_changes', 'pos': (6, 7.5), 'input': False},
        {'name': 'test_results', 'pos': (6, 6.5), 'input': False},
        {'name': 'messages', 'pos': (6, 5.5), 'input': False}
    ]
    
    # Draw agents
    for agent in agents:
        box = FancyBboxPatch(
            (agent['pos'][0]-0.8, agent['pos'][1]-0.4),
            1.6, 0.8,
            boxstyle="round,pad=0.1",
            facecolor=agent['color'],
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(agent['pos'][0], agent['pos'][1], agent['name'], 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw state components
    for i, comp in enumerate(state_components):
        color = colors['state'] if not comp['input'] else '#FFB6C1'
        box = FancyBboxPatch(
            (comp['pos'][0]-0.7, comp['pos'][1]-0.2),
            1.4, 0.4,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor='gray',
            linewidth=1
        )
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                ha='center', va='center', fontsize=8)
    
    # Draw workflow arrows between agents
    agent_positions = [(2, 9), (2, 7), (2, 5), (2, 3)]
    for i in range(len(agent_positions)-1):
        start = agent_positions[i]
        end = agent_positions[i+1]
        arrow = ConnectionPatch(
            (start[0], start[1]-0.4), (end[0], end[1]+0.4),
            "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=20, fc=colors['flow'], ec=colors['flow'],
            linewidth=3
        )
        ax.add_patch(arrow)
    
    # Draw state interaction arrows
    state_arrows = [
        # Scanner reads repository_path, writes current_issues & dependencies
        ((4.2, 10.5), (2.8, 9)),  # repository_path -> Scanner
        ((2.8, 9), (5.3, 9.5)),   # Scanner -> current_issues
        ((2.8, 9), (5.3, 8.5)),   # Scanner -> dependencies
        
        # Analyzer reads dependencies, writes enhanced dependencies
        ((5.3, 8.5), (2.8, 7)),   # dependencies -> Analyzer
        ((2.8, 7), (5.3, 8.5)),   # Analyzer -> dependencies (enhanced)
        
        # Modifier reads issues, writes code_changes
        ((5.3, 9.5), (2.8, 5)),   # current_issues -> Modifier
        ((2.8, 5), (5.3, 7.5)),   # Modifier -> code_changes
        
        # Tester reads code_changes, writes test_results
        ((5.3, 7.5), (2.8, 3)),   # code_changes -> Tester
        ((2.8, 3), (5.3, 6.5)),   # Tester -> test_results
    ]
    
    for start, end in state_arrows:
        arrow = ConnectionPatch(
            start, end, "data", "data",
            arrowstyle="->", shrinkA=2, shrinkB=2,
            mutation_scale=15, fc='gray', ec='gray',
            linewidth=1.5, alpha=0.7
        )
        ax.add_patch(arrow)
    
    # Add title and labels
    ax.text(5, 11.5, 'LangGraph Dependency Upgrade Agent Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    ax.text(2, 1.5, 'Agent Execution Flow', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.text(6, 4.5, 'Shared State', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color=colors['scanner'], label='Repository Scanner'),
        mpatches.Patch(color=colors['analyzer'], label='Dependency Analyzer'),
        mpatches.Patch(color=colors['modifier'], label='Code Modifier'),
        mpatches.Patch(color=colors['tester'], label='Test Runner'),
        mpatches.Patch(color=colors['state'], label='State Variables'),
        mpatches.Patch(color='#FFB6C1', label='Input State')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Add execution details
    details = [
        "1. Scanner: Finds 2 issues (deprecated fillna, insecure verify)",
        "2. Analyzer: Suggests 5 package upgrades with security priorities", 
        "3. Modifier: Applies 3 code fixes (fillna→ffill, verify=True, paths)",
        "4. Tester: Validates changes, confirms successful execution"
    ]
    
    for i, detail in enumerate(details):
        ax.text(0.5, 1.8 - i*0.3, detail, ha='left', va='center', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('langgraph_workflow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Workflow diagram saved as 'langgraph_workflow_diagram.png'")

def print_execution_trace():
    """Print the actual execution trace from our demo"""
    
    print("\n" + "="*60)
    print("🔍 ACTUAL EXECUTION TRACE FROM DEMO")
    print("="*60)
    
    trace_steps = [
        {
            "agent": "Repository Scanner Agent",
            "input_state": {
                "repository_path": "python_hello",
                "current_issues": [],
                "dependencies_to_upgrade": {},
                "messages": []
            },
            "actions": [
                "Scanned python_hello/main.py",
                "Found deprecated fillna(method='ffill')",
                "Found insecure verify=False",
                "Parsed requirements.txt",
                "Identified 5 outdated packages"
            ],
            "output_state": {
                "current_issues": [
                    "Deprecated pandas fillna method in python_hello/main.py",
                    "Insecure requests usage in python_hello/main.py"
                ],
                "dependencies_to_upgrade": {
                    "requests": "2.25.1",
                    "pandas": "1.3.0", 
                    "numpy": "1.19.5",
                    "urllib3": "1.26.5",
                    "certifi": "2020.12.5"
                },
                "messages": ["Found 2 issues and 5 dependencies"]
            }
        },
        {
            "agent": "Dependency Analyzer Agent",
            "input_state": "Previous output state",
            "actions": [
                "Analyzed current versions vs latest",
                "Identified security vulnerabilities",
                "Prioritized critical updates"
            ],
            "output_state": {
                "dependencies_to_upgrade": {
                    "requests": {"current": "2.25.1", "latest": "2.31.0", "security_fix": True},
                    "pandas": {"current": "1.3.0", "latest": "2.1.0", "security_fix": False},
                    "numpy": {"current": "1.19.5", "latest": "1.24.0", "security_fix": False},
                    "urllib3": {"current": "1.26.5", "latest": "2.0.0", "security_fix": True},
                    "certifi": {"current": "2020.12.5", "latest": "2023.7.22", "security_fix": True}
                },
                "messages": ["Analyzed 5 packages for upgrade"]
            }
        },
        {
            "agent": "Code Modifier Agent", 
            "input_state": "Previous output state",
            "actions": [
                "Applied regex: fillna(method='ffill') → ffill()",
                "Applied regex: verify=False → verify=True", 
                "Fixed file paths: python_hello/results.csv → results.csv",
                "Fixed file paths: python_hello/summary.txt → summary.txt"
            ],
            "output_state": {
                "code_changes": ["Fixed compatibility issues in python_hello/main.py"],
                "messages": ["Made 1 code changes"]
            }
        },
        {
            "agent": "Test Runner Agent",
            "input_state": "Previous output state", 
            "actions": [
                "Executed: python main.py in python_hello/",
                "Captured stdout and stderr",
                "Validated return code = 0",
                "Confirmed no deprecation warnings"
            ],
            "output_state": {
                "test_results": {
                    "passed": 1,
                    "failed": 0,
                    "main_program": "PASSED",
                    "errors": []
                },
                "messages": ["Tests completed: 1 passed, 0 failed"]
            }
        }
    ]
    
    for i, step in enumerate(trace_steps, 1):
        print(f"\n🤖 STEP {i}: {step['agent']}")
        print("-" * 50)
        print(f"📥 Input State: {step['input_state']}")
        print(f"⚡ Actions Performed:")
        for action in step['actions']:
            print(f"   • {action}")
        print(f"📤 Output State Updates: {step['output_state']}")
    
    print(f"\n✅ FINAL RESULT: Success=True, Issues=2, Changes=1")
    print("="*60)

if __name__ == "__main__":
    print("Creating LangGraph workflow visualization...")
    create_workflow_diagram()
    print_execution_trace()