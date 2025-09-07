#!/usr/bin/env python3
"""
Generate visual diagram of the Smart Dependency Agent LangGraph architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create a comprehensive architecture diagram"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Main workflow diagram
    ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2, rowspan=2)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.set_title('Smart Dependency Agent - LangGraph Architecture', fontsize=16, fontweight='bold', pad=20)
    ax1.axis('off')
    
    # State diagram
    ax2 = plt.subplot2grid((3, 2), (2, 0))
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)
    ax2.set_title('AgentState Structure', fontsize=12, fontweight='bold')
    ax2.axis('off')
    
    # Data flow diagram
    ax3 = plt.subplot2grid((3, 2), (2, 1))
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 6)
    ax3.set_title('Data Flow', fontsize=12, fontweight='bold')
    ax3.axis('off')
    
    # Colors
    colors = {
        'git': '#FF6B6B',
        'analyzer': '#4ECDC4',
        'fixer': '#45B7D1',
        'tester': '#96CEB4',
        'workflow': '#FFEAA7',
        'state': '#DDA0DD',
        'llm': '#FFB347'
    }
    
    # Main workflow nodes
    nodes = [
        {'name': 'GitSyncAgent', 'pos': (1.5, 6.5), 'color': colors['git'], 'desc': 'Repository\nSynchronization'},
        {'name': 'SmartCodeAnalyzerAgent', 'pos': (1.5, 5), 'color': colors['analyzer'], 'desc': 'AI Code Analysis\n(GPT-4)'},
        {'name': 'SmartCodeFixerAgent\n(Generate)', 'pos': (1.5, 3.5), 'color': colors['fixer'], 'desc': 'AI Fix Generation\n(GPT-4)'},
        {'name': 'SmartCodeFixerAgent\n(Apply)', 'pos': (1.5, 2), 'color': colors['fixer'], 'desc': 'Apply Fixes\nto Files'},
        {'name': 'SmartTestRunnerAgent', 'pos': (1.5, 0.5), 'color': colors['tester'], 'desc': 'Test & Validate\nFixed Code'}
    ]
    
    # Draw workflow nodes
    for i, node in enumerate(nodes):
        # Main node
        box = FancyBboxPatch(
            (node['pos'][0] - 0.7, node['pos'][1] - 0.3),
            1.4, 0.6,
            boxstyle="round,pad=0.1",
            facecolor=node['color'],
            edgecolor='black',
            linewidth=2
        )
        ax1.add_patch(box)
        ax1.text(node['pos'][0], node['pos'][1], node['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Description box
        desc_box = FancyBboxPatch(
            (node['pos'][0] + 1.2, node['pos'][1] - 0.25),
            2, 0.5,
            boxstyle="round,pad=0.05",
            facecolor='white',
            edgecolor='gray',
            linewidth=1
        )
        ax1.add_patch(desc_box)
        ax1.text(node['pos'][0] + 2.2, node['pos'][1], node['desc'], 
                ha='center', va='center', fontsize=8)
        
        # Arrows between nodes
        if i < len(nodes) - 1:
            arrow = patches.FancyArrowPatch(
                (node['pos'][0], node['pos'][1] - 0.3),
                (nodes[i+1]['pos'][0], nodes[i+1]['pos'][1] + 0.3),
                arrowstyle='->', mutation_scale=20, color='black', linewidth=2
            )
            ax1.add_patch(arrow)
    
    # LangGraph StateGraph box
    graph_box = FancyBboxPatch(
        (5, 1), 4, 5,
        boxstyle="round,pad=0.2",
        facecolor=colors['workflow'],
        edgecolor='black',
        linewidth=2,
        alpha=0.3
    )
    ax1.add_patch(graph_box)
    ax1.text(7, 6.2, 'LangGraph StateGraph', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    
    # State flow
    state_items = [
        'repository_path: str',
        'file_contents: Dict[str, str]',
        'issues_found: List[Dict]',
        'suggested_fixes: List[Dict]',
        'applied_changes: List[str]',
        'test_results: Dict[str, Any]',
        'messages: List[str]'
    ]
    
    # AgentState structure
    state_box = FancyBboxPatch(
        (0.5, 0.5), 9, 5,
        boxstyle="round,pad=0.2",
        facecolor=colors['state'],
        edgecolor='black',
        linewidth=2,
        alpha=0.3
    )
    ax2.add_patch(state_box)
    
    for i, item in enumerate(state_items):
        ax2.text(1, 4.5 - i*0.6, f"• {item}", ha='left', va='center', fontsize=9)
    
    # Data flow phases
    phases = [
        'Input: Repository Path',
        'Analysis: LLM Code Review',
        'Generation: LLM Fix Creation',
        'Application: Code Modification',
        'Validation: Test Execution'
    ]
    
    phase_colors = [colors['git'], colors['analyzer'], colors['fixer'], colors['fixer'], colors['tester']]
    
    for i, (phase, color) in enumerate(zip(phases, phase_colors)):
        phase_box = FancyBboxPatch(
            (0.5, 4.5 - i*0.8), 9, 0.6,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='black',
            linewidth=1,
            alpha=0.7
        )
        ax3.add_patch(phase_box)
        ax3.text(5, 4.8 - i*0.8, phase, ha='center', va='center', 
                fontsize=10, fontweight='bold')
    
    # Add LLM integration indicators
    llm_positions = [(4.5, 5), (4.5, 3.5)]
    for pos in llm_positions:
        llm_box = FancyBboxPatch(
            (pos[0] - 0.3, pos[1] - 0.15),
            0.6, 0.3,
            boxstyle="round,pad=0.05",
            facecolor=colors['llm'],
            edgecolor='orange',
            linewidth=2
        )
        ax1.add_patch(llm_box)
        ax1.text(pos[0], pos[1], 'GPT-4', ha='center', va='center', 
                fontsize=8, fontweight='bold')
    
    # Add legend
    legend_elements = [
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['git'], label='Git Operations'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['analyzer'], label='AI Analysis'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['fixer'], label='AI Fixing'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['tester'], label='Testing'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['llm'], label='LLM Integration'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['workflow'], label='LangGraph Orchestration')
    ]
    
    ax1.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    return fig

def create_sequence_diagram():
    """Create a sequence diagram showing the workflow execution"""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_title('Smart Dependency Agent - Execution Sequence', fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Actors
    actors = ['Workflow', 'GitSync', 'Analyzer', 'Fixer', 'Tester']
    actor_positions = [1, 2.5, 4, 5.5, 7]
    
    # Draw actor columns
    for i, (actor, pos) in enumerate(zip(actors, actor_positions)):
        # Actor box
        actor_box = FancyBboxPatch(
            (pos - 0.4, 11), 0.8, 0.6,
            boxstyle="round,pad=0.1",
            facecolor='lightblue',
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(actor_box)
        ax.text(pos, 11.3, actor, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Lifeline
        ax.plot([pos, pos], [11, 0.5], 'k--', alpha=0.5, linewidth=1)
    
    # Sequence steps
    steps = [
        {'from': 0, 'to': 1, 'y': 10, 'label': '1. sync_with_github()', 'color': '#FF6B6B'},
        {'from': 1, 'to': 0, 'y': 9.5, 'label': 'sync complete', 'color': '#FF6B6B'},
        {'from': 0, 'to': 2, 'y': 9, 'label': '2. analyze_code()', 'color': '#4ECDC4'},
        {'from': 2, 'to': 2, 'y': 8.5, 'label': 'LLM analysis', 'color': '#FFB347'},
        {'from': 2, 'to': 0, 'y': 8, 'label': 'issues found', 'color': '#4ECDC4'},
        {'from': 0, 'to': 3, 'y': 7.5, 'label': '3. generate_fixes()', 'color': '#45B7D1'},
        {'from': 3, 'to': 3, 'y': 7, 'label': 'LLM fix generation', 'color': '#FFB347'},
        {'from': 3, 'to': 0, 'y': 6.5, 'label': 'fixes generated', 'color': '#45B7D1'},
        {'from': 0, 'to': 3, 'y': 6, 'label': '4. apply_fixes()', 'color': '#45B7D1'},
        {'from': 3, 'to': 0, 'y': 5.5, 'label': 'fixes applied', 'color': '#45B7D1'},
        {'from': 0, 'to': 4, 'y': 5, 'label': '5. run_tests()', 'color': '#96CEB4'},
        {'from': 4, 'to': 0, 'y': 4.5, 'label': 'test results', 'color': '#96CEB4'},
    ]
    
    # Draw sequence arrows
    for step in steps:
        from_pos = actor_positions[step['from']]
        to_pos = actor_positions[step['to']]
        y = step['y']
        
        if from_pos != to_pos:  # Regular message
            arrow = patches.FancyArrowPatch(
                (from_pos, y), (to_pos, y),
                arrowstyle='->', mutation_scale=15, 
                color=step['color'], linewidth=2
            )
            ax.add_patch(arrow)
            
            # Label
            mid_x = (from_pos + to_pos) / 2
            ax.text(mid_x, y + 0.1, step['label'], ha='center', va='bottom', 
                   fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        else:  # Self-call
            # Draw self-loop
            loop_width = 0.3
            ax.add_patch(patches.Rectangle((from_pos, y - 0.1), loop_width, 0.2, 
                                         facecolor=step['color'], alpha=0.3))
            ax.text(from_pos + loop_width/2, y, step['label'], ha='center', va='center', 
                   fontsize=8, rotation=0)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Create architecture diagram
    print("Creating architecture diagram...")
    fig1 = create_architecture_diagram()
    fig1.savefig('smart_agent_architecture.png', dpi=300, bbox_inches='tight')
    print("Architecture diagram saved as 'smart_agent_architecture.png'")
    
    # Create sequence diagram
    print("Creating sequence diagram...")
    fig2 = create_sequence_diagram()
    fig2.savefig('smart_agent_sequence.png', dpi=300, bbox_inches='tight')
    print("Sequence diagram saved as 'smart_agent_sequence.png'")
    
    plt.show()