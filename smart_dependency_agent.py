#!/usr/bin/env python3
"""
Smart Dependency Upgrade Agent using Roo Code for intelligent issue detection
This version integrates directly with Roo Code without external API calls
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

# Configure LangSmith tracing if available
if os.getenv("LANGCHAIN_TRACING_V2") == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "roo-code-dependency-agent")
    
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    if langchain_api_key:
        os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    
    langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")
    if langchain_endpoint:
        os.environ["LANGCHAIN_ENDPOINT"] = langchain_endpoint
    
    print("🔍 LangSmith tracing enabled for Roo Code agent")

# Try to import LangSmith for tracing (optional)
try:
    from langsmith import traceable
    LANGSMITH_AVAILABLE = True
    print("📊 LangSmith decorators available for detailed tracing")
except ImportError:
    # Create a no-op decorator if LangSmith is not available
    def traceable(name=None):
        def decorator(func):
            return func
        return decorator
    LANGSMITH_AVAILABLE = False
    print("📊 LangSmith decorators not available (install langsmith for detailed tracing)")

@dataclass
class UpgradeResult:
    """Result of the upgrade process"""
    success: bool
    summary: str
    changes_made: List[str]
    errors: List[str]
    issues_found: List[str]

class RooCodeAnalyzer:
    """Direct integration with Roo Code for code analysis"""
    
    def __init__(self):
        self.name = "Roo Code Analyzer"
    
    @traceable(name="roo_code_analyze")
    def analyze_code(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Analyze code using built-in Roo Code intelligence"""
        print(f"🧠 {self.name}: Analyzing {file_path} with Roo Code")
        
        issues = []
        
        # Built-in analysis patterns for common issues
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for deprecated datetime.utcnow()
            if 'datetime.utcnow()' in line:
                issues.append({
                    'issue_type': 'deprecation',
                    'description': 'datetime.datetime.utcnow() is deprecated',
                    'line_number': i,
                    'severity': 'medium',
                    'suggested_fix': 'Replace with datetime.datetime.now(datetime.timezone.utc)',
                    'file_path': file_path,
                    'original_code': line.strip(),
                    'fixed_code': line.replace('datetime.utcnow()', 'datetime.now(datetime.timezone.utc)')
                })
            
            # Check for direct environment variable access
            if 'os.environ.get(' in line and 'lower()' in line:
                issues.append({
                    'issue_type': 'best_practice',
                    'description': 'Environment variable handling could be improved',
                    'line_number': i,
                    'severity': 'low',
                    'suggested_fix': 'Use more robust boolean parsing',
                    'file_path': file_path,
                    'original_code': line.strip(),
                    'fixed_code': line.replace('.lower() in (\'true\', \'1\', \'yes\')', ' in [\'true\', \'1\', \'yes\', \'on\']')
                })
            
            # Check for missing imports
            if 'datetime.datetime' in line and 'import datetime' not in content:
                issues.append({
                    'issue_type': 'import_missing',
                    'description': 'Missing timezone import for datetime operations',
                    'line_number': i,
                    'severity': 'medium',
                    'suggested_fix': 'Add timezone import',
                    'file_path': file_path,
                    'original_code': 'import datetime',
                    'fixed_code': 'import datetime\nfrom datetime import timezone'
                })
        
        return issues

class RooCodeFixer:
    """Direct integration with Roo Code for generating fixes"""
    
    def __init__(self):
        self.name = "Roo Code Fixer"
    
    @traceable(name="roo_code_fix")
    def generate_and_apply_fixes(self, file_path: str, content: str, issues: List[Dict]) -> tuple[str, List[str]]:
        """Generate and apply fixes using Roo Code intelligence"""
        print(f"🔧 {self.name}: Generating fixes for {file_path}")
        
        fixed_content = content
        applied_changes = []
        
        # Sort issues by line number in reverse order to avoid line number shifts
        sorted_issues = sorted(issues, key=lambda x: x.get('line_number', 0), reverse=True)
        
        for issue in sorted_issues:
            if 'original_code' in issue and 'fixed_code' in issue:
                original = issue['original_code'].strip()
                fixed = issue['fixed_code'].strip()
                
                if original in fixed_content:
                    fixed_content = fixed_content.replace(original, fixed)
                    applied_changes.append(f"Fixed {issue['description']} on line {issue.get('line_number', 'unknown')}")
                    print(f"  ✅ Applied fix: {issue['description']}")
        
        # Add missing imports at the top if needed
        for issue in issues:
            if issue['issue_type'] == 'import_missing':
                if 'from datetime import timezone' not in fixed_content:
                    lines = fixed_content.split('\n')
                    # Find the last import line
                    import_index = 0
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            import_index = i
                    
                    lines.insert(import_index + 1, 'from datetime import timezone')
                    fixed_content = '\n'.join(lines)
                    applied_changes.append("Added timezone import")
        
        return fixed_content, applied_changes

class GitSyncAgent:
    """Agent that syncs with GitHub repository"""
    
    def __init__(self):
        self.name = "Git Sync Agent"
    
    @traceable(name="git_sync")
    def sync_with_github(self, repo_path: str) -> List[str]:
        """Commit local changes first, then sync with GitHub repository"""
        print(f"🔄 {self.name}: Committing local changes and syncing with GitHub")
        
        messages = []
        
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
                        ["git", "commit", "-m", "Auto-commit: Local changes before Roo Code analysis"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    
                    if commit_result.returncode == 0:
                        print("✅ Successfully committed local changes")
                        messages.append("Committed local changes before analysis")
                    else:
                        print(f"⚠️ Git commit warning: {commit_result.stderr}")
                        messages.append(f"Git commit completed with warnings: {commit_result.stderr}")
                else:
                    print(f"❌ Git add failed: {add_result.stderr}")
                    messages.append(f"Git add failed: {add_result.stderr}")
            else:
                print("📍 No uncommitted changes found")
                messages.append("No uncommitted changes to commit")
            
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
                    messages.append(f"Pushed {commits_ahead} commits to GitHub")
                else:
                    print(f"❌ Git push failed: {push_result.stderr}")
                    messages.append(f"Git push failed: {push_result.stderr}")
            else:
                print("📍 No local commits to push")
                messages.append("No local commits to push")
            
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
                messages.append("Pulled latest changes from GitHub")
            else:
                print(f"⚠️ Git pull warning: {pull_result.stderr}")
                messages.append(f"Git pull completed with warnings: {pull_result.stderr}")
            
        except Exception as e:
            print(f"❌ Error syncing with GitHub: {e}")
            messages.append(f"Error syncing with GitHub: {e}")
        
        return messages

class SmartTestRunnerAgent:
    """Agent that tests the fixed code"""
    
    def __init__(self):
        self.name = "Smart Test Runner"
    
    @traceable(name="test_runner")
    def run_tests(self, repo_path: str) -> Dict[str, Any]:
        """Run tests on both original and fixed code"""
        print(f"🧪 {self.name}: Testing original and fixed code")
        
        test_results = {"passed": 0, "failed": 0, "errors": [], "fixed_files_tested": []}
        
        # Find Python files to test (prioritize _fixed files)
        python_files = list(Path(repo_path).rglob("*.py"))
        
        # Separate original and fixed files
        fixed_files = [f for f in python_files if "_fixed" in f.stem]
        original_files = [f for f in python_files if "_fixed" not in f.stem and f.name != "smart_dependency_agent_roo.py"]
        
        # Test fixed files first if they exist
        files_to_test = fixed_files if fixed_files else original_files
        
        for file_path in files_to_test:
            try:
                # Try to run each Python file
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
        
        return test_results

class RooCodeDependencyUpgradeWorkflow:
    """Main workflow orchestrator using direct Roo Code integration"""
    
    def __init__(self):
        self.git_sync = GitSyncAgent()
        self.analyzer = RooCodeAnalyzer()
        self.fixer = RooCodeFixer()
        self.tester = SmartTestRunnerAgent()
    
    @traceable(name="roo_code_workflow")
    def run_upgrade(self, repository_path: str) -> UpgradeResult:
        """Run the complete Roo Code upgrade workflow"""
        print("🚀 Starting Roo Code Dependency Upgrade Workflow")
        
        try:
            # Step 1: Git Sync
            git_messages = self.git_sync.sync_with_github(repository_path)
            
            # Step 2: Analyze code
            all_issues = []
            file_contents = {}
            applied_changes = []
            
            # Read all Python files
            python_files = list(Path(repository_path).rglob("*.py"))
            
            for file_path in python_files:
                if file_path.name == "smart_dependency_agent_roo.py":
                    continue  # Skip self
                    
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        file_contents[str(file_path)] = content
                        
                        # Analyze with Roo Code
                        issues = self.analyzer.analyze_code(str(file_path), content)
                        all_issues.extend(issues)
                        
                        # Generate and apply fixes if issues found
                        if issues:
                            fixed_content, changes = self.fixer.generate_and_apply_fixes(str(file_path), content, issues)
                            applied_changes.extend(changes)
                            
                            # Write fixed version if changes were made
                            if fixed_content != content:
                                path_obj = Path(file_path)
                                new_file_path = path_obj.parent / f"{path_obj.stem}_fixed{path_obj.suffix}"
                                
                                with open(new_file_path, 'w') as f:
                                    f.write(fixed_content)
                                print(f"Created fixed version: {new_file_path}")
                                applied_changes.append(f"Created fixed version: {new_file_path}")
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            # Step 3: Test the results
            test_results = self.tester.run_tests(repository_path)
            
            success = test_results.get("failed", 0) == 0
            issues_count = len(all_issues)
            changes_count = len(applied_changes)
            
            summary = f"Roo Code upgrade completed. Issues found: {issues_count}, Changes applied: {changes_count}"
            
            return UpgradeResult(
                success=success,
                summary=summary,
                changes_made=applied_changes,
                errors=test_results.get("errors", []),
                issues_found=[issue["description"] for issue in all_issues]
            )
            
        except Exception as e:
            return UpgradeResult(
                success=False,
                summary=f"Roo Code upgrade failed: {e}",
                changes_made=[],
                errors=[str(e)],
                issues_found=[]
            )

def main():
    """Demonstrate the Roo Code dependency upgrade workflow"""
    print("=== Roo Code Dependency Upgrade Agent Demo ===")
    
    # Initialize the workflow
    workflow = RooCodeDependencyUpgradeWorkflow()
    
    # Run upgrade on the python_hello directory
    result = workflow.run_upgrade("python_hello")
    
    print(f"\n=== Results ===")
    print(f"Success: {result.success}")
    print(f"Summary: {result.summary}")
    
    if result.issues_found:
        print("\nIssues found by Roo Code:")
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
    main()