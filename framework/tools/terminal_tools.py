"""
CoderAI Framework Terminal Tools
This module provides terminal operation tools for the CoderAI framework.
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, Any, List, Optional
from ..registry import registry

@registry.register(type="tool")
def run_command(command: str, cwd: str = None, timeout: int = 60, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run a shell command.
    
    Args:
        command: Command to run
        cwd: Working directory to run the command in
        timeout: Timeout in seconds
        
    Returns:
        Dictionary containing the command output
    """
    try:
        # Expand user directory if needed
        if cwd:
            cwd = os.path.expanduser(cwd)
            
        # Check if directory exists
        if cwd and not os.path.exists(cwd):
            return {
                "success": False,
                "error": f"Directory '{cwd}' does not exist",
            }
            
        # Run command
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
                "stdout": stdout,
                "stderr": stderr,
                "return_code": -1,
            }
            
        return {
            "success": return_code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def run_python(code: str, cwd: str = None, timeout: int = 60, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run Python code.
    
    Args:
        code: Python code to run
        cwd: Working directory to run the code in
        timeout: Timeout in seconds
        
    Returns:
        Dictionary containing the code output
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
            f.write(code)
            temp_file = f.name
            
        try:
            # Expand user directory if needed
            if cwd:
                cwd = os.path.expanduser(cwd)
                
            # Check if directory exists
            if cwd and not os.path.exists(cwd):
                return {
                    "success": False,
                    "error": f"Directory '{cwd}' does not exist",
                }
                
            # Get Python executable
            python_executable = sys.executable
            
            # Run Python code
            command = f"{python_executable} {temp_file}"
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                text=True,
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return_code = process.returncode
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                return {
                    "success": False,
                    "error": f"Code execution timed out after {timeout} seconds",
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": -1,
                }
                
            return {
                "success": return_code == 0,
                "stdout": stdout,
                "stderr": stderr,
                "return_code": return_code,
            }
        finally:
            # Delete temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def run_script(script_path: str, args: List[str] = None, cwd: str = None, timeout: int = 60, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run a script.
    
    Args:
        script_path: Path to the script to run
        args: Arguments to pass to the script
        cwd: Working directory to run the script in
        timeout: Timeout in seconds
        
    Returns:
        Dictionary containing the script output
    """
    try:
        # Expand user directory if needed
        script_path = os.path.expanduser(script_path)
        
        # Check if script exists
        if not os.path.exists(script_path):
            return {
                "success": False,
                "error": f"Script '{script_path}' does not exist",
            }
            
        # Check if script is executable
        if not os.path.isfile(script_path):
            return {
                "success": False,
                "error": f"Path '{script_path}' is not a file",
            }
            
        # Expand user directory if needed
        if cwd:
            cwd = os.path.expanduser(cwd)
            
        # Check if directory exists
        if cwd and not os.path.exists(cwd):
            return {
                "success": False,
                "error": f"Directory '{cwd}' does not exist",
            }
            
        # Prepare command
        command = [script_path]
        if args:
            command.extend(args)
            
        # Run script
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            text=True,
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return {
                "success": False,
                "error": f"Script execution timed out after {timeout} seconds",
                "stdout": stdout,
                "stderr": stderr,
                "return_code": -1,
            }
            
        return {
            "success": return_code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
