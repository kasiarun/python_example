#!/usr/bin/env python3
"""
Dependency Upgrade Agent using LangGraph
This demonstrates the system described in the README for fixing compatibility issues
"""

import asyncio
import os
import subprocess
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from typing_extensions import Annotated, TypedDict
except ImportError:
    print("LangGraph not installed. This is a demonstration of the architecture.")
    print("Install with: pip install langgraph")
    
    # Mock classes for demonstration
    class StateGraph:
        def __init__(self): pass
        def add_node(self, name, func): pass
        def add_edge(self, from_node, to_node): pass
        def set_entry_point(self, node): pass
        def compile(self): return self
        async def ainvoke(self, state): return state
    
    class TypedDict: pass
    def add_messages(x): return x
    END = "END"

@dataclass
class UpgradeResult:
    """Result of the upgrade process"""
    success: bool
    summary: str
    changes_made: List[str]
    errors: List[str]

class AgentState(TypedDict):
    """State shared between agents"""
    repository_path: str
    current_issues: List[str]
    dependencies_to_upgrade: Dict[str, str]
    code_changes: List[str]
    test_results: Dict[str, Any]
    messages: Annotated[List[str], add_messages]

class RepositoryScannerAgent:
    """Agent that scans repository for issues and outdated dependencies"""
    
    def __init__(self):
        self.name = "Repository Scanner"
    
    async def scan_repository(self, state: AgentState) -> AgentState:
        """Scan repository for issues and outdated dependencies"""
        repo_path = state["repository_path"]
        issues = []
        dependencies = {}
        
        print(f"🔍 {self.name}: Scanning repository at {repo_path}")
        
        # Scan for Python files with potential issues
        python_files = list(Path(repo_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Check for deprecated pandas methods
                if "fillna(method=" in content:
                    issues.append(f"Deprecated pandas fillna method in {file_path}")
                
                # Check for insecure requests
                if "verify=False" in content:
                    issues.append(f"Insecure requests usage in {file_path}")
                
                # Check for other deprecated patterns
                if "pd.DataFrame.append" in content:
                    issues.append(f"Deprecated DataFrame.append in {file_path}")
                    
            except Exception as e:
                issues.append(f"Error reading {file_path}: {e}")
        
        # Check requirements.txt for outdated dependencies
        req_file = Path(repo_path) / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '==' in line:
                            package, version = line.split('==')
                            dependencies[package] = version
        
        state["current_issues"] = issues
        state["dependencies_to_upgrade"] = dependencies
        state["messages"].append(f"Found {len(issues)} issues and {len(dependencies)} dependencies")
        
        return state

class DependencyAnalyzerAgent:
    """Agent that analyzes dependencies and suggests upgrades"""
    
    def __init__(self):
        self.name = "Dependency Analyzer"
    
    async def analyze_dependencies(self, state: AgentState) -> AgentState:
        """Analyze dependencies and suggest upgrades"""
        print(f"🔬 {self.name}: Analyzing dependencies")
        
        dependencies = state["dependencies_to_upgrade"]
        upgrade_suggestions = {}
        
        # Simulate checking for latest versions (in real implementation, would use PyPI API)
        version_upgrades = {
            "requests": "2.31.0",
            "pandas": "2.1.0", 
            "numpy": "1.24.0",
            "urllib3": "2.0.0",
            "certifi": "2023.7.22"
        }
        
        for package, current_version in dependencies.items():
            if package in version_upgrades:
                latest_version = version_upgrades[package]
                if current_version != latest_version:
                    upgrade_suggestions[package] = {
                        "current": current_version,
                        "latest": latest_version,
                        "security_fix": package in ["requests", "urllib3", "certifi"]
                    }
        
        state["dependencies_to_upgrade"] = upgrade_suggestions
        state["messages"].append(f"Analyzed {len(upgrade_suggestions)} packages for upgrade")
        
        return state

class CodeModifierAgent:
    """Agent that modifies code to fix compatibility issues"""
    
    def __init__(self):
        self.name = "Code Modifier"
    
    async def modify_code(self, state: AgentState) -> AgentState:
        """Modify code to fix compatibility issues"""
        print(f"🔧 {self.name}: Modifying code to fix issues")
        
        repo_path = state["repository_path"]
        changes_made = []
        
        # Fix deprecated pandas fillna method
        python_files = list(Path(repo_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix deprecated fillna method
                content = re.sub(
                    r"\.fillna\(method='ffill'\)",
                    ".ffill()",
                    content
                )
                
                content = re.sub(
                    r"\.fillna\(method='bfill'\)",
                    ".bfill()",
                    content
                )
                
                # Fix insecure requests
                content = re.sub(
                    r"verify=False",
                    "verify=True",
                    content
                )
                
                # Fix file path issues
                content = re.sub(
                    r"'python_hello/results\.csv'",
                    "'results.csv'",
                    content
                )
                
                content = re.sub(
                    r"'python_hello/summary\.txt'",
                    "'summary.txt'",
                    content
                )
                
                if content != original_content:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    changes_made.append(f"Fixed compatibility issues in {file_path}")
                    
            except Exception as e:
                changes_made.append(f"Error modifying {file_path}: {e}")
        
        state["code_changes"] = changes_made
        state["messages"].append(f"Made {len(changes_made)} code changes")
        
        return state

class TestRunnerAgent:
    """Agent that runs tests to validate changes"""
    
    def __init__(self):
        self.name = "Test Runner"
    
    async def run_tests(self, state: AgentState) -> AgentState:
        """Run tests to validate the changes"""
        print(f"🧪 {self.name}: Running tests")
        
        repo_path = state["repository_path"]
        test_results = {"passed": 0, "failed": 0, "errors": []}
        
        try:
            # Try to run the main program
            result = subprocess.run(
                ["python", "main.py"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                test_results["passed"] += 1
                test_results["main_program"] = "PASSED"
            else:
                test_results["failed"] += 1
                test_results["main_program"] = f"FAILED: {result.stderr}"
                test_results["errors"].append(result.stderr)
                
        except Exception as e:
            test_results["failed"] += 1
            test_results["errors"].append(f"Test execution error: {e}")
        
        state["test_results"] = test_results
        state["messages"].append(f"Tests completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
        return state

class DependencyUpgradeWorkflow:
    """Main workflow orchestrator using LangGraph"""
    
    def __init__(self):
        self.scanner = RepositoryScannerAgent()
        self.analyzer = DependencyAnalyzerAgent()
        self.modifier = CodeModifierAgent()
        self.tester = TestRunnerAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("scan", self.scanner.scan_repository)
        workflow.add_node("analyze", self.analyzer.analyze_dependencies)
        workflow.add_node("modify", self.modifier.modify_code)
        workflow.add_node("test", self.tester.run_tests)
        
        # Add edges
        workflow.set_entry_point("scan")
        workflow.add_edge("scan", "analyze")
        workflow.add_edge("analyze", "modify")
        workflow.add_edge("modify", "test")
        workflow.add_edge("test", END)
        
        return workflow.compile()
    
    async def run_upgrade(self, repository_path: str, create_pr: bool = False, run_tests: bool = True) -> UpgradeResult:
        """Run the complete upgrade workflow"""
        print("🚀 Starting Dependency Upgrade Workflow")
        
        initial_state = AgentState(
            repository_path=repository_path,
            current_issues=[],
            dependencies_to_upgrade={},
            code_changes=[],
            test_results={},
            messages=[]
        )
        
        try:
            final_state = await self.workflow.ainvoke(initial_state)
            
            success = final_state["test_results"].get("failed", 0) == 0
            summary = f"Upgrade completed. Issues found: {len(final_state['current_issues'])}, Changes made: {len(final_state['code_changes'])}"
            
            return UpgradeResult(
                success=success,
                summary=summary,
                changes_made=final_state["code_changes"],
                errors=final_state["test_results"].get("errors", [])
            )
            
        except Exception as e:
            return UpgradeResult(
                success=False,
                summary=f"Upgrade failed: {e}",
                changes_made=[],
                errors=[str(e)]
            )

async def main():
    """Demonstrate the dependency upgrade workflow"""
    print("=== Dependency Upgrade Agent Demo ===")
    
    # Initialize the workflow
    workflow = DependencyUpgradeWorkflow()
    
    # Run upgrade on the python_hello directory
    result = await workflow.run_upgrade(
        repository_path="python_hello",
        create_pr=False,
        run_tests=True
    )
    
    print(f"\n=== Results ===")
    print(f"Success: {result.success}")
    print(f"Summary: {result.summary}")
    
    if result.changes_made:
        print("\nChanges made:")
        for change in result.changes_made:
            print(f"  - {change}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

if __name__ == "__main__":
    asyncio.run(main())