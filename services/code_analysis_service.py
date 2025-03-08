from typing import Dict, List, Any, Optional
import ast
import re

class CodeAnalysisService:
    """Service for analyzing code and providing AI-powered insights"""
    
    def __init__(self):
        """Initialize the code analysis service"""
        self.patterns = {
            'code_smells': {
                'long_method': 50,  # lines threshold
                'complex_condition': 3,  # logical operators threshold
                'duplicate_code': 0.8  # similarity threshold
            },
            'best_practices': [
                r'print\(',  # debug statements
                r'except:\s*pass',  # bare except clauses
                r'\b(TODO|FIXME)\b'  # pending tasks
            ]
        }
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code for potential improvements and issues
        
        Args:
            code: The source code to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = ast.parse(code)
            
            analysis = {
                'complexity_score': self._calculate_complexity(tree),
                'code_smells': self._detect_code_smells(code, tree),
                'best_practices': self._check_best_practices(code),
                'suggestions': self._generate_suggestions(code, tree)
            }
            
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_complexity(self, tree: ast.AST) -> float:
        """Calculate code complexity score"""
        complexity = 0
        
        for node in ast.walk(tree):
            # Count control flow statements
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            # Count logical operators
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _detect_code_smells(self, code: str, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect potential code smells"""
        smells = []
        
        # Check for long methods
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = len(code.split('\n')[node.lineno-1:node.end_lineno])
                if lines > self.patterns['code_smells']['long_method']:
                    smells.append({
                        'type': 'long_method',
                        'message': f'Method {node.name} is too long ({lines} lines)',
                        'location': node.lineno
                    })
        
        return smells
    
    def _check_best_practices(self, code: str) -> List[Dict[str, Any]]:
        """Check adherence to best practices"""
        violations = []
        
        for pattern in self.patterns['best_practices']:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_no = code.count('\n', 0, match.start()) + 1
                violations.append({
                    'type': 'best_practice',
                    'message': f'Potential violation of best practices at line {line_no}',
                    'location': line_no
                })
        
        return violations
    
    def _generate_suggestions(self, code: str, tree: ast.AST) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Analyze imports
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        if len(imports) > 10:
            suggestions.append('Consider organizing imports into logical groups')
        
        # Analyze class complexity
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 10:
                    suggestions.append(f'Class {node.name} might benefit from being split into smaller classes')
        
        return suggestions
    
    def get_code_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate various code metrics
        
        Args:
            code: The source code to analyze
            
        Returns:
            Dictionary containing code metrics
        """
        try:
            tree = ast.parse(code)
            
            metrics = {
                'loc': len(code.split('\n')),
                'classes': len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                'functions': len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                'imports': len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
            }
            
            return metrics
        except Exception as e:
            return {'error': str(e)}