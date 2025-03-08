from typing import Dict, List, Optional
from pathlib import Path
import pytest
import asyncio
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult:
    test_id: str
    status: str
    duration: float
    error_message: Optional[str] = None
    timestamp: datetime = datetime.now()

class TestingService:
    def __init__(self):
        self.test_results: Dict[str, List[TestResult]] = {}
    
    async def discover_tests(self, project_path: str) -> List[str]:
        """Discover all test files in the project"""
        test_files = []
        for path in Path(project_path).rglob('test_*.py'):
            test_files.append(str(path))
        return test_files
    
    async def run_tests(self, test_paths: List[str]) -> Dict[str, TestResult]:
        """Run tests and collect results"""
        results = {}
        for test_path in test_paths:
            try:
                # Run pytest in a separate process
                process = await asyncio.create_subprocess_exec(
                    'pytest',
                    test_path,
                    '-v',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                # Parse test results
                test_id = Path(test_path).stem
                if process.returncode == 0:
                    status = 'passed'
                    error_message = None
                else:
                    status = 'failed'
                    error_message = stderr.decode()
                
                results[test_id] = TestResult(
                    test_id=test_id,
                    status=status,
                    duration=0.0,  # TODO: Implement actual duration tracking
                    error_message=error_message
                )
                
            except Exception as e:
                results[Path(test_path).stem] = TestResult(
                    test_id=Path(test_path).stem,
                    status='error',
                    duration=0.0,
                    error_message=str(e)
                )
        
        return results
    
    def get_test_history(self, test_id: str) -> List[TestResult]:
        """Get historical test results for a specific test"""
        return self.test_results.get(test_id, [])
    
    def store_test_result(self, result: TestResult) -> None:
        """Store a test result in the history"""
        if result.test_id not in self.test_results:
            self.test_results[result.test_id] = []
        self.test_results[result.test_id].append(result)