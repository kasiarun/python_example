#!/usr/bin/env python3
"""
Smart Dependency Upgrade Agent using LLMs for intelligent issue detection
This version uses LangGraph with actual LLM calls to analyze and fix code issues
"""

import asyncio
import os
import subprocess
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from typing_extensions import Annotated, TypedDict
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    print("LangGraph or OpenAI not installed. Please install: pip install langgraph langchain-openai")
    LANGGRAPH_AVAILABLE = False
    exit(1)

# Configure LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "smart-dependency-agent"

@dataclass
class UpgradeResult:
    """Result of the upgrade process"""
    success: bool
    summary: str
    changes_made: List[str]
    errors: List[str]
    issues_found: List[str]

class AgentState(TypedDict):
    """State shared between agents"""
    repository_path: str
    file_contents: Dict[str, str]
    issues_found: List[Dict[str, Any]]
    suggested_fixes: List[Dict[str, Any]]
    applied_changes: List[str]
    test_results: Dict[str, Any]
    messages: Annotated[List[str], add_messages]

class SmartCodeAnalyzerAgent:
    """Agent that uses LLM to analyze code for issues"""
    
    def __init__(self):
        self.name = "Smart Code Analyzer"
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    
    async def analyze_code(self, state: AgentState) -> AgentState:
        """Use LLM to analyze code for potential issues"""
        print(f"🧠 {self.name}: Analyzing code with LLM")
        
        repo_path = state["repository_path"]
        file_contents = {}
        
        # Read all Python files
        python_files = list(Path(repo_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    file_contents[str(file_path)] = content
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        state["file_contents"] = file_contents
        
        # Analyze each file with LLM
        all_issues = []
        
        for file_path, content in file_contents.items():
            issues = await self._analyze_file_with_llm(file_path, content)
            all_issues.extend(issues)
        
        state["issues_found"] = all_issues
        state["messages"].append(f"Found {len(all_issues)} potential issues using LLM analysis")
        
        return state
    
    async def _analyze_file_with_llm(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Analyze a single file with LLM"""
        
        system_prompt = """You are a Python code analyzer. Analyze the provided code and identify:
1. Deprecated methods or functions
2. Security vulnerabilities 
3. Compatibility issues
4. Bad practices
5. Potential runtime errors

For each issue found, provide:
- issue_type: category of the issue
- description: what the problem is
- line_number: approximate line where issue occurs (if identifiable)
- severity: high/medium/low
- suggested_fix: how to fix it

Return your analysis as a JSON array of issues."""

        human_prompt = f"""Analyze this Python file: {file_path}

Code:
```python
{content}
```

Please identify any issues and return them as JSON."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Parse LLM response
            response_text = response.content
            
            # Extract JSON from response (handle cases where LLM adds extra text)
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                issues = json.loads(json_str)
                
                # Add file path to each issue
                for issue in issues:
                    issue['file_path'] = file_path
                
                return issues
            else:
                print(f"Could not parse LLM response for {file_path}")
                return []
                
        except Exception as e:
            print(f"Error analyzing {file_path} with LLM: {e}")
            return []

class SmartCodeFixerAgent:
    """Agent that uses LLM to generate and apply fixes"""
    
    def __init__(self):
        self.name = "Smart Code Fixer"
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    
    async def generate_fixes(self, state: AgentState) -> AgentState:
        """Generate fixes for identified issues using LLM"""
        print(f"🔧 {self.name}: Generating fixes with LLM")
        
        issues = state["issues_found"]
        file_contents = state["file_contents"]
        
        suggested_fixes = []
        
        # Group issues by file
        issues_by_file = {}
        for issue in issues:
            file_path = issue['file_path']
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        # Generate fixes for each file
        for file_path, file_issues in issues_by_file.items():
            if file_path in file_contents:
                fixes = await self._generate_fixes_for_file(file_path, file_contents[file_path], file_issues)
                suggested_fixes.extend(fixes)
        
        state["suggested_fixes"] = suggested_fixes
        state["messages"].append(f"Generated {len(suggested_fixes)} potential fixes")
        
        return state
    
    async def _generate_fixes_for_file(self, file_path: str, content: str, issues: List[Dict]) -> List[Dict]:
        """Generate fixes for a specific file"""
        
        system_prompt = """You are a Python code fixer. Given a file with identified issues, provide specific fixes.

For each fix, provide:
- issue_id: reference to the original issue
- fix_type: type of fix (replace, insert, delete)
- original_code: the problematic code to replace
- fixed_code: the corrected code
- explanation: why this fix is needed

Return fixes as a JSON array."""

        issues_text = "\n".join([f"- {issue['description']} (Line ~{issue.get('line_number', 'unknown')})" for issue in issues])
        
        human_prompt = f"""Fix the issues in this Python file: {file_path}

Current code:
```python
{content}
```

Issues to fix:
{issues_text}

Please provide specific fixes as JSON."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            response_text = response.content
            
            # Extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                fixes = json.loads(json_str)
                
                # Add file path to each fix
                for fix in fixes:
                    fix['file_path'] = file_path
                
                return fixes
            else:
                print(f"Could not parse fix response for {file_path}")
                return []
                
        except Exception as e:
            print(f"Error generating fixes for {file_path}: {e}")
            return []
    
    async def apply_fixes(self, state: AgentState) -> AgentState:
        """Apply the generated fixes to new files"""
        print(f"⚡ {self.name}: Applying fixes to new files")
        
        suggested_fixes = state["suggested_fixes"]
        applied_changes = []
        
        # Group fixes by file
        fixes_by_file = {}
        for fix in suggested_fixes:
            file_path = fix['file_path']
            if file_path not in fixes_by_file:
                fixes_by_file[file_path] = []
            fixes_by_file[file_path].append(fix)
        
        # Apply fixes to each file and create new fixed versions
        for file_path, file_fixes in fixes_by_file.items():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply each fix
                for fix in file_fixes:
                    if fix['fix_type'] == 'replace' and 'original_code' in fix and 'fixed_code' in fix:
                        original_code = fix['original_code'].strip()
                        fixed_code = fix['fixed_code'].strip()
                        
                        if original_code in content:
                            content = content.replace(original_code, fixed_code)
                            applied_changes.append(f"Fixed {fix.get('explanation', 'issue')} in {file_path}")
                
                # Write to new file if changes were made
                if content != original_content:
                    # Create new filename with _fixed suffix
                    path_obj = Path(file_path)
                    new_file_path = path_obj.parent / f"{path_obj.stem}_fixed{path_obj.suffix}"
                    
                    with open(new_file_path, 'w') as f:
                        f.write(content)
                    print(f"Created fixed version: {new_file_path}")
                    applied_changes.append(f"Created fixed version: {new_file_path}")
                
            except Exception as e:
                print(f"Error applying fixes to {file_path}: {e}")
        
        state["applied_changes"] = applied_changes
        state["messages"].append(f"Applied {len(applied_changes)} fixes")
        
        return state

class SmartTestRunnerAgent:
    """Agent that tests the fixed code"""
    
    def __init__(self):
        self.name = "Smart Test Runner"
    
    async def run_tests(self, state: AgentState) -> AgentState:
        """Run tests on both original and fixed code"""
        print(f"🧪 {self.name}: Testing original and fixed code")
        
        repo_path = state["repository_path"]
        test_results = {"passed": 0, "failed": 0, "errors": [], "fixed_files_tested": []}
        
        # Find Python files to test (prioritize _fixed files)
        python_files = list(Path(repo_path).rglob("*.py"))
        
        # Separate original and fixed files
        fixed_files = [f for f in python_files if "_fixed" in f.stem]
        original_files = [f for f in python_files if "_fixed" not in f.stem]
        
        # Test fixed files first if they exist
        files_to_test = fixed_files if fixed_files else original_files
        
        for file_path in files_to_test:
            try:
                # Try to run each Python file
                # Make path relative to the repo_path for subprocess
                relative_path = file_path.relative_to(Path(repo_path))
                result = subprocess.run(
                    ["python", str(relative_path)],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    test_results["passed"] += 1
                    if "_fixed" in file_path.stem:
                        test_results["fixed_files_tested"].append(str(file_path))
                        print(f"✅ Fixed file runs successfully: {file_path}")
                else:
                    test_results["failed"] += 1
                    test_results["errors"].append(f"{file_path}: {result.stderr}")
                    if "_fixed" in file_path.stem:
                        print(f"❌ Fixed file still has issues: {file_path}")
                    
            except Exception as e:
                test_results["failed"] += 1
                test_results["errors"].append(f"{file_path}: {str(e)}")
        
        state["test_results"] = test_results
        
        if test_results["fixed_files_tested"]:
            state["messages"].append(f"Tests completed: {test_results['passed']} passed, {test_results['failed']} failed. Fixed files tested: {len(test_results['fixed_files_tested'])}")
        else:
            state["messages"].append(f"Tests completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
        return state

class GitSyncAgent:
    """Agent that syncs with GitHub repository"""
    
    def __init__(self):
        self.name = "Git Sync Agent"
    
    async def sync_with_github(self, state: AgentState) -> AgentState:
        """Commit local changes first, then sync with GitHub repository"""
        print(f"🔄 {self.name}: Committing local changes and syncing with GitHub")
        
        repo_path = state["repository_path"]
        
        try:
            # Step 1: Check for uncommitted changes and commit them
            print("📋 Checking for uncommitted local changes...")
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if status_result.stdout.strip():
                print("📝 Found uncommitted changes, committing them...")
                
                # Add all changes
                add_result = subprocess.run(
                    ["git", "add", "."],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if add_result.returncode == 0:
                    # Commit with automated message
                    commit_result = subprocess.run(
                        ["git", "commit", "-m", "Auto-commit: Local changes before dependency analysis"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    
                    if commit_result.returncode == 0:
                        print("✅ Successfully committed local changes")
                        state["messages"].append("Committed local changes before analysis")
                    else:
                        print(f"⚠️ Git commit warning: {commit_result.stderr}")
                        state["messages"].append(f"Git commit completed with warnings: {commit_result.stderr}")
                else:
                    print(f"❌ Git add failed: {add_result.stderr}")
                    state["messages"].append(f"Git add failed: {add_result.stderr}")
            else:
                print("📍 No uncommitted changes found")
                state["messages"].append("No uncommitted changes to commit")
            
            # Step 2: Push any local commits to remote
            print("📤 Checking for local commits to push...")
            ahead_result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD", "^origin/main"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            commits_ahead = int(ahead_result.stdout.strip()) if ahead_result.returncode == 0 else 0
            
            if commits_ahead > 0:
                print(f"📤 Pushing {commits_ahead} local commits to remote...")
                push_result = subprocess.run(
                    ["git", "push", "origin", "main"],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if push_result.returncode == 0:
                    print("✅ Successfully pushed to GitHub")
                    state["messages"].append(f"Pushed {commits_ahead} commits to GitHub")
                else:
                    print(f"❌ Git push failed: {push_result.stderr}")
                    state["messages"].append(f"Git push failed: {push_result.stderr}")
            else:
                print("📍 No local commits to push")
                state["messages"].append("No local commits to push")
            
            # Step 3: Pull latest changes from remote
            print("📥 Pulling latest changes from remote...")
            pull_result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if pull_result.returncode == 0:
                print("✅ Successfully pulled from GitHub")
                state["messages"].append("Pulled latest changes from GitHub")
            else:
                print(f"⚠️ Git pull warning: {pull_result.stderr}")
                state["messages"].append(f"Git pull completed with warnings: {pull_result.stderr}")
            
        except Exception as e:
            print(f"❌ Error syncing with GitHub: {e}")
            state["messages"].append(f"Error syncing with GitHub: {e}")
        
        return state

class SmartDependencyUpgradeWorkflow:
    """Main workflow orchestrator using LangGraph with LLM agents"""
    
    def __init__(self):
        self.git_sync = GitSyncAgent()
        self.analyzer = SmartCodeAnalyzerAgent()
        self.fixer = SmartCodeFixerAgent()
        self.tester = SmartTestRunnerAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("git_sync", self.git_sync.sync_with_github)
        workflow.add_node("analyze", self.analyzer.analyze_code)
        workflow.add_node("generate_fixes", self.fixer.generate_fixes)
        workflow.add_node("apply_fixes", self.fixer.apply_fixes)
        workflow.add_node("test", self.tester.run_tests)
        
        # Add edges - start with git sync
        workflow.set_entry_point("git_sync")
        workflow.add_edge("git_sync", "analyze")
        workflow.add_edge("analyze", "generate_fixes")
        workflow.add_edge("generate_fixes", "apply_fixes")
        workflow.add_edge("apply_fixes", "test")
        workflow.add_edge("test", END)
        
        return workflow.compile()
    
    async def run_upgrade(self, repository_path: str) -> UpgradeResult:
        """Run the complete smart upgrade workflow"""
        print("🚀 Starting Smart Dependency Upgrade Workflow")
        
        initial_state = AgentState(
            repository_path=repository_path,
            file_contents={},
            issues_found=[],
            suggested_fixes=[],
            applied_changes=[],
            test_results={},
            messages=[]
        )
        
        try:
            final_state = await self.workflow.ainvoke(initial_state)
            
            success = final_state["test_results"].get("failed", 0) == 0
            issues_count = len(final_state["issues_found"])
            changes_count = len(final_state["applied_changes"])
            
            summary = f"Smart upgrade completed. Issues found: {issues_count}, Changes applied: {changes_count}"
            
            return UpgradeResult(
                success=success,
                summary=summary,
                changes_made=final_state["applied_changes"],
                errors=final_state["test_results"].get("errors", []),
                issues_found=[issue["description"] for issue in final_state["issues_found"]]
            )
            
        except Exception as e:
            return UpgradeResult(
                success=False,
                summary=f"Smart upgrade failed: {e}",
                changes_made=[],
                errors=[str(e)],
                issues_found=[]
            )

async def main():
    """Demonstrate the smart dependency upgrade workflow"""
    print("=== Smart Dependency Upgrade Agent Demo ===")
    
    # Initialize the workflow
    workflow = SmartDependencyUpgradeWorkflow()
    
    # Run upgrade on the python_hello directory
    result = await workflow.run_upgrade("python_hello")
    
    print(f"\n=== Results ===")
    print(f"Success: {result.success}")
    print(f"Summary: {result.summary}")
    
    if result.issues_found:
        print("\nIssues found by LLM:")
        for issue in result.issues_found:
            print(f"  - {issue}")
    
    if result.changes_made:
        print("\nChanges applied:")
        for change in result.changes_made:
            print(f"  - {change}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

if __name__ == "__main__":
    asyncio.run(main())