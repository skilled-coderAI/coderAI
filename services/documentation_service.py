from typing import Dict, List, Optional
import ast
import re
from pathlib import Path
import json
import os

class DocGenerationService:
    """
    Service for automatically generating documentation from Python code.
    Integrates with CoderAI's model service for enhanced docstring generation.
    """
    def __init__(self, model_service=None):
        self.model_service = model_service
        self.docs_cache = {}
    
    def generate_docs(self, file_path: str) -> Dict:
        """
        Generate documentation for a Python file
        
        Args:
            file_path: Path to the Python file to document
            
        Returns:
            Dictionary containing the documentation structure
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            file_docs = {
                "file_path": file_path,
                "module_docstring": ast.get_docstring(tree) or "",
                "classes": [],
                "functions": []
            }
            
            # Generate module docstring if empty
            if not file_docs["module_docstring"] and self.model_service:
                prompt = f"Generate a concise module docstring for this Python file:\n\n{Path(file_path).name}\n\nFirst 100 chars: {code[:100]}..."
                file_docs["module_docstring"] = self.model_service.generate_response(prompt)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_doc = self._process_class(node, code)
                    file_docs["classes"].append(class_doc)
                elif isinstance(node, ast.FunctionDef) and not hasattr(node, 'parent_class'):
                    func_doc = self._process_function(node, code)
                    file_docs["functions"].append(func_doc)
            
            self.docs_cache[file_path] = file_docs
            return file_docs
        
        except Exception as e:
            return {
                "status": "error",
                "file": file_path,
                "error": str(e)
            }
    
    def _process_class(self, node: ast.ClassDef, code: str) -> Dict:
        """Process a class definition and generate documentation"""
        class_doc = {
            "name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "methods": [],
            "attributes": [],
            "base_classes": [self._get_node_source(base, code) for base in node.bases]
        }
        
        # If docstring is empty and model service is available, generate one
        if not class_doc["docstring"] and self.model_service:
            class_source = self._get_node_source(node, code)
            prompt = f"Generate a concise docstring for this Python class:\n\n{class_source}"
            class_doc["docstring"] = self.model_service.generate_response(prompt)
        
        # Process methods
        for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
            method.parent_class = node  # Mark as class method
            method_doc = self._process_function(method, code)
            class_doc["methods"].append(method_doc)
        
        # Extract attributes
        for stmt in [n for n in node.body if isinstance(n, ast.Assign)]:
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    class_doc["attributes"].append({
                        "name": target.id,
                        "type": self._infer_type(stmt.value),
                        "value": self._get_node_source(stmt.value, code)
                    })
        
        return class_doc
    
    def _process_function(self, node: ast.FunctionDef, code: str) -> Dict:
        """Process a function definition and generate documentation"""
        is_method = hasattr(node, 'parent_class')
        
        func_doc = {
            "name": node.name,
            "is_method": is_method,
            "docstring": ast.get_docstring(node) or "",
            "parameters": [],
            "returns": None,
            "decorators": [self._get_node_source(d, code) for d in node.decorator_list]
        }
        
        # Process parameters
        for arg in node.args.args:
            param = {"name": arg.arg, "type": None}
            if arg.annotation:
                param["type"] = self._get_node_source(arg.annotation, code)
            func_doc["parameters"].append(param)
        
        # Handle *args and **kwargs
        if node.args.vararg:
            func_doc["parameters"].append({
                "name": f"*{node.args.vararg.arg}",
                "type": self._get_node_source(node.args.vararg.annotation, code) if node.args.vararg.annotation else None
            })
        
        if node.args.kwarg:
            func_doc["parameters"].append({
                "name": f"**{node.args.kwarg.arg}",
                "type": self._get_node_source(node.args.kwarg.annotation, code) if node.args.kwarg.annotation else None
            })
        
        # Infer return type
        if node.returns:
            func_doc["returns"] = self._get_node_source(node.returns, code)
        
        # If docstring is empty and model service is available, generate one
        if not func_doc["docstring"] and self.model_service:
            func_source = self._get_node_source(node, code)
            prompt = f"Generate a concise docstring for this Python {'method' if is_method else 'function'}:\n\n{func_source}"
            func_doc["docstring"] = self.model_service.generate_response(prompt)
        
        return func_doc
    
    def _get_node_source(self, node: ast.AST, code: str) -> str:
        """Extract source code for a node"""
        if node is None:
            return ""
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            lines = code.split('\n')
            return '\n'.join(lines[node.lineno-1:node.end_lineno])
        return ""
    
    def _infer_type(self, node: ast.AST) -> str:
        """Infer the type of a value"""
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.List):
            return "list"
        elif isinstance(node, ast.Dict):
            return "dict"
        elif isinstance(node, ast.Set):
            return "set"
        elif isinstance(node, ast.Tuple):
            return "tuple"
        elif isinstance(node, ast.Call):
            if hasattr(node, 'func'):
                if isinstance(node.func, ast.Name):
                    return node.func.id
                elif isinstance(node.func, ast.Attribute):
                    return node.func.attr
        return "unknown"
    
    def generate_project_docs(self, project_path: str, exclude_dirs: List[str] = None) -> Dict:
        """
        Generate documentation for an entire project
        
        Args:
            project_path: Path to the project directory
            exclude_dirs: List of directories to exclude
            
        Returns:
            Dictionary containing documentation for all Python files
        """
        if exclude_dirs is None:
            exclude_dirs = ['.git', '.venv', '__pycache__', 'venv', 'env', 'node_modules']
        
        results = {}
        for path in Path(project_path).rglob('*.py'):
            # Skip excluded directories
            if any(excluded in str(path) for excluded in exclude_dirs):
                continue
                
            result = self.generate_docs(str(path))
            results[str(path)] = result
        
        return {
            "status": "success",
            "files_documented": len(results),
            "documentation": results
        }
    
    def export_docs(self, output_dir: str, format: str = "markdown") -> Dict[str, str]:
        """
        Export documentation in the specified format
        
        Args:
            output_dir: Directory to save the documentation files
            format: Format to export (markdown or json)
            
        Returns:
            Dictionary mapping file paths to their output paths
        """
        os.makedirs(output_dir, exist_ok=True)
        result = {}
        
        for file_path, docs in self.docs_cache.items():
            rel_path = Path(file_path).stem
            
            if format == "markdown":
                content = self._to_markdown(docs)
                output_path = os.path.join(output_dir, f"{rel_path}.md")
            elif format == "json":
                content = json.dumps(docs, indent=2)
                output_path = os.path.join(output_dir, f"{rel_path}.json")
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result[file_path] = output_path
        
        # Generate index file
        if format == "markdown":
            index_content = "# Project Documentation\n\n"
            for file_path, output_path in result.items():
                rel_output = os.path.basename(output_path)
                index_content += f"- [{Path(file_path).name}]({rel_output})\n"
            
            index_path = os.path.join(output_dir, "index.md")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
        
        return result
    
    def _to_markdown(self, docs: Dict) -> str:
        """Convert documentation to Markdown format"""
        md = f"# {Path(docs['file_path']).name}\n\n"
        
        if docs.get("module_docstring"):
            md += f"{docs['module_docstring']}\n\n"
        
        # Classes
        for cls in docs["classes"]:
            md += f"## Class: {cls['name']}"
            
            if cls["base_classes"]:
                bases = ", ".join(cls["base_classes"])
                md += f" ({bases})"
            
            md += "\n\n"
            md += f"{cls['docstring']}\n\n"
            
            if cls["attributes"]:
                md += "### Attributes\n\n"
                for attr in cls["attributes"]:
                    md += f"- `{attr['name']}`: {attr['type']}"
                    if attr.get("value"):
                        md += f" = {attr['value']}"
                    md += "\n"
                md += "\n"
            
            if cls["methods"]:
                md += "### Methods\n\n"
                for method in cls["methods"]:
                    params = ", ".join([f"{p['name']}: {p['type'] or 'Any'}" for p in method["parameters"]])
                    returns = f" -> {method['returns']}" if method["returns"] else ""
                    
                    # Add decorators
                    if method["decorators"]:
                        for decorator in method["decorators"]:
                            md += f"@{decorator}\n"
                    
                    md += f"#### `{method['name']}({params}){returns}`\n\n"
                    md += f"{method['docstring']}\n\n"
        
        # Functions
        if docs["functions"]:
            md += "## Functions\n\n"
            for func in docs["functions"]:
                params = ", ".join([f"{p['name']}: {p['type'] or 'Any'}" for p in func["parameters"]])
                returns = f" -> {func['returns']}" if func["returns"] else ""
                
                # Add decorators
                if func["decorators"]:
                    for decorator in func["decorators"]:
                        md += f"@{decorator}\n"
                
                md += f"### `{func['name']}({params}){returns}`\n\n"
                md += f"{func['docstring']}\n\n"
        
        return md