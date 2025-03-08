from typing import Dict, List, Optional, Set, Tuple, Any
import ast
import networkx as nx
import json
import os
from pathlib import Path
import re
import logging

class CodeVisualizationService:
    """
    Service for analyzing and visualizing code structures and relationships.
    Generates interactive visualizations of code dependencies, inheritance hierarchies,
    and call graphs.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_types = {
            "module": "#4285F4",  # Google Blue
            "class": "#34A853",   # Google Green
            "function": "#FBBC05", # Google Yellow
            "method": "#EA4335",  # Google Red
            "import": "#9C27B0",  # Purple
            "variable": "#607D8B"  # Blue Grey
        }
        self.logger = logging.getLogger(__name__)
        
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a Python file and extract its structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Add module node
            module_name = Path(file_path).stem
            module_id = f"module::{file_path}"
            self.graph.add_node(
                module_id, 
                type="module", 
                name=module_name, 
                file=file_path,
                color=self.node_types["module"]
            )
            
            tree = ast.parse(code)
            self._process_ast(tree, file_path, module_id)
            
            return {
                "status": "success",
                "file": file_path,
                "nodes": len(self.graph.nodes),
                "edges": len(self.graph.edges),
                "module": module_name
            }
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {
                "status": "error",
                "file": file_path,
                "error": str(e)
            }
    
    def _process_ast(self, tree: ast.AST, file_path: str, module_id: str) -> None:
        """Process the AST and build the graph"""
        # Track imports
        imports = {}
        
        # First pass: collect all class and function definitions
        for node in ast.walk(tree):
            # Process imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self._process_import(node, file_path, module_id, imports)
            
            # Process classes
            elif isinstance(node, ast.ClassDef):
                class_id = f"class::{file_path}::{node.name}"
                self.graph.add_node(
                    class_id, 
                    type="class", 
                    name=node.name, 
                    file=file_path,
                    color=self.node_types["class"],
                    docstring=ast.get_docstring(node) or ""
                )
                self.graph.add_edge(module_id, class_id, type="contains")
                
                # Process base classes
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_name = base.id
                        # Check if base class is imported
                        if base_name in imports:
                            base_id = imports[base_name]
                            self.graph.add_edge(class_id, base_id, type="inherits")
                        else:
                            # Look for base class in the same file
                            base_id = f"class::{file_path}::{base_name}"
                            if base_id in self.graph:
                                self.graph.add_edge(class_id, base_id, type="inherits")
                
                # Process methods
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                    method_id = f"method::{file_path}::{node.name}::{method.name}"
                    self.graph.add_node(
                        method_id, 
                        type="method", 
                        name=method.name, 
                        class_name=node.name,
                        file=file_path,
                        color=self.node_types["method"],
                        docstring=ast.get_docstring(method) or ""
                    )
                    self.graph.add_edge(class_id, method_id, type="contains")
            
            # Process functions
            elif isinstance(node, ast.FunctionDef) and not hasattr(node, 'parent_class'):
                func_id = f"function::{file_path}::{node.name}"
                self.graph.add_node(
                    func_id, 
                    type="function", 
                    name=node.name, 
                    file=file_path,
                    color=self.node_types["function"],
                    docstring=ast.get_docstring(node) or ""
                )
                self.graph.add_edge(module_id, func_id, type="contains")
        
        # Second pass: analyze function calls and variable references
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                self._process_call(node, file_path)
    
    def _process_import(self, node: ast.AST, file_path: str, module_id: str, imports: Dict) -> None:
        """Process import statements"""
        if isinstance(node, ast.Import):
            for name in node.names:
                import_id = f"import::{name.name}"
                self.graph.add_node(
                    import_id, 
                    type="import", 
                    name=name.name, 
                    file=file_path,
                    color=self.node_types["import"]
                )
                self.graph.add_edge(module_id, import_id, type="imports")
                
                # Track the import
                alias = name.asname or name.name
                imports[alias] = import_id
        
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            for name in node.names:
                import_id = f"import::{module_name}.{name.name}"
                self.graph.add_node(
                    import_id, 
                    type="import", 
                    name=f"{module_name}.{name.name}", 
                    file=file_path,
                    color=self.node_types["import"]
                )
                self.graph.add_edge(module_id, import_id, type="imports")
                
                # Track the import
                alias = name.asname or name.name
                imports[alias] = import_id
    
    def _process_call(self, node: ast.Call, file_path: str) -> None:
        """Process function/method calls"""
        # Get the caller context (function or method that contains this call)
        caller_context = self._get_caller_context(node, file_path)
        if not caller_context:
            return
        
        # Process the function being called
        if isinstance(node.func, ast.Name):
            # Direct function call
            func_name = node.func.id
            called_id = f"function::{file_path}::{func_name}"
            
            # Only add edge if the function exists in our graph
            if called_id in self.graph:
                self.graph.add_edge(caller_context, called_id, type="calls")
        
        elif isinstance(node.func, ast.Attribute):
            # Method call or attribute access
            if isinstance(node.func.value, ast.Name):
                # Simple method call like obj.method()
                obj_name = node.func.value.id
                method_name = node.func.attr
                
                # Look for methods in classes defined in this file
                for node_id in self.graph.nodes():
                    if node_id.startswith(f"class::{file_path}::"):
                        class_name = node_id.split("::")[-1]
                        method_id = f"method::{file_path}::{class_name}::{method_name}"
                        if method_id in self.graph:
                            self.graph.add_edge(caller_context, method_id, type="calls")
    
    def _get_caller_context(self, node: ast.AST, file_path: str) -> Optional[str]:
        """Get the ID of the function or method that contains a node"""
        # Walk up the AST to find the containing function or method
        parent = getattr(node, 'parent', None)
        while parent:
            if isinstance(parent, ast.FunctionDef):
                # Check if it's a method
                if hasattr(parent, 'parent') and isinstance(parent.parent, ast.ClassDef):
                    return f"method::{file_path}::{parent.parent.name}::{parent.name}"
                else:
                    return f"function::{file_path}::{parent.name}"
            parent = getattr(parent, 'parent', None)
        
        return None
    
    def analyze_project(self, project_path: str, exclude_dirs: List[str] = None) -> Dict:
        """Analyze an entire project directory"""
        if exclude_dirs is None:
            exclude_dirs = ['.git', '.venv', '__pycache__', 'venv', 'env', 'node_modules']
        
        results = []
        file_count = 0
        
        # Reset graph for a new project
        self.graph = nx.DiGraph()
        
        # Add project node
        project_name = Path(project_path).name
        project_id = f"project::{project_path}"
        self.graph.add_node(
            project_id, 
            type="project", 
            name=project_name, 
            path=project_path,
            color="#3F51B5"  # Indigo
        )
        
        for path in Path(project_path).rglob('*.py'):
            # Skip excluded directories
            if any(excluded in str(path) for excluded in exclude_dirs):
                continue
                
            file_count += 1
            result = self.analyze_file(str(path))
            
            # Add edge from project to module
            if result["status"] == "success":
                module_id = f"module::{str(path)}"
                self.graph.add_edge(project_id, module_id, type="contains")
            
            results.append(result)
        
        # Add parent references to AST nodes for context tracking
        for path in Path(project_path).rglob('*.py'):
            # Skip excluded directories
            if any(excluded in str(path) for excluded in exclude_dirs):
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                tree = ast.parse(code)
                self._add_parent_references(tree)
                
                # Process calls with parent context
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        self._process_call(node, str(path))
            except Exception as e:
                self.logger.error(f"Error processing calls in {path}: {str(e)}")
        
        return {
            "status": "success",
            "files_analyzed": file_count,
            "nodes": len(self.graph.nodes),
            "edges": len(self.graph.edges),
            "details": results
        }
    
    def _add_parent_references(self, node: ast.AST, parent: ast.AST = None) -> None:
        """Add parent references to AST nodes for context tracking"""
        node.parent = parent
        for child in ast.iter_child_nodes(node):
            self._add_parent_references(child, node)
    
    def get_class_hierarchy(self) -> Dict:
        """Get the class inheritance hierarchy"""
        hierarchy = {}
        
        # Find all classes
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get("type") == "class":
                class_name = attrs.get("name")
                file_path = attrs.get("file")
                
                # Find base classes
                base_classes = []
                for _, target, edge_data in self.graph.out_edges(node_id, data=True):
                    if edge_data.get("type") == "inherits":
                        target_attrs = self.graph.nodes[target]
                        base_classes.append({
                            "name": target_attrs.get("name"),
                            "file": target_attrs.get("file")
                        })
                
                # Find child classes
                child_classes = []
                for source, _, edge_data in self.graph.in_edges(node_id, data=True):
                    if edge_data.get("type") == "inherits":
                        source_attrs = self.graph.nodes[source]
                        child_classes.append({
                            "name": source_attrs.get("name"),
                            "file": source_attrs.get("file")
                        })
                
                hierarchy[class_name] = {
                    "file": file_path,
                    "base_classes": base_classes,
                    "child_classes": child_classes
                }
        
        return hierarchy
    
    def get_call_graph(self) -> Dict:
        """Get the function/method call graph"""
        call_graph = {}
        
        # Find all functions and methods
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get("type") in ["function", "method"]:
                func_name = attrs.get("name")
                file_path = attrs.get("file")
                
                # For methods, include the class name
                if attrs.get("type") == "method":
                    func_name = f"{attrs.get('class_name')}.{func_name}"
                
                # Find called functions/methods
                calls = []
                for _, target, edge_data in self.graph.out_edges(node_id, data=True):
                    if edge_data.get("type") == "calls":
                        target_attrs = self.graph.nodes[target]
                        target_name = target_attrs.get("name")
                        
                        # For methods, include the class name
                        if target_attrs.get("type") == "method":
                            target_name = f"{target_attrs.get('class_name')}.{target_name}"
                        
                        calls.append({
                            "name": target_name,
                            "file": target_attrs.get("file"),
                            "type": target_attrs.get("type")
                        })
                
                # Find functions/methods that call this one
                called_by = []
                for source, _, edge_data in self.graph.in_edges(node_id, data=True):
                    if edge_data.get("type") == "calls":
                        source_attrs = self.graph.nodes[source]
                        source_name = source_attrs.get("name")
                        
                        # For methods, include the class name
                        if source_attrs.get("type") == "method":
                            source_name = f"{source_attrs.get('class_name')}.{source_name}"
                        
                        called_by.append({
                            "name": source_name,
                            "file": source_attrs.get("file"),
                            "type": source_attrs.get("type")
                        })
                
                call_graph[func_name] = {
                    "file": file_path,
                    "type": attrs.get("type"),
                    "calls": calls,
                    "called_by": called_by
                }
        
        return call_graph
    
    def export_graph(self, format: str = "json", output_path: Optional[str] = None) -> str:
        """Export the graph in the specified format"""
        if format == "json":
            data = nx.node_link_data(self.graph)
            result = json.dumps(data, indent=2)
        
        elif format == "d3":
            # D3.js specific format
            nodes = []
            for node_id, attrs in self.graph.nodes(data=True):
                nodes.append({
                    "id": node_id,
                    "name": attrs.get("name", ""),
                    "type": attrs.get("type", ""),
                    "file": attrs.get("file", ""),
                    "color": attrs.get("color", "#999999"),
                    "docstring": attrs.get("docstring", "")
                })
            
            links = []
            for source, target, attrs in self.graph.edges(data=True):
                links.append({
                    "source": source,
                    "target": target,
                    "type": attrs.get("type", ""),
                    "value": 1
                })
            
            result = json.dumps({"nodes": nodes, "links": links}, indent=2)
        
        elif format == "cytoscape":
            # Cytoscape.js format
            elements = {"nodes": [], "edges": []}
            
            for node_id, attrs in self.graph.nodes(data=True):
                elements["nodes"].append({
                    "data": {
                        "id": node_id,
                        "name": attrs.get("name", ""),
                        "type": attrs.get("type", ""),
                        "file": attrs.get("file", ""),
                        "color": attrs.get("color", "#999999"),
                        "docstring": attrs.get("docstring", "")
                    }
                })
            
            for source, target, attrs in self.graph.edges(data=True):
                elements["edges"].append({
                    "data": {
                        "id": f"{source}-{target}",
                        "source": source,
                        "target": target,
                        "type": attrs.get("type", "")
                    }
                })
            
            result = json.dumps(elements, indent=2)
        
        elif format == "graphml":
            if output_path is None:
                raise ValueError("output_path is required for GraphML format")
            
            nx.write_graphml(self.graph, output_path)
            return output_path
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            return output_path
        
        return result
    
    def generate_html_visualization(self, output_path: str) -> str:
        """Generate an interactive HTML visualization"""
        # Export graph in D3 format
        graph_data = self.export_graph(format="d3")
        
        # HTML template with D3.js
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Code Visualization</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                body { 
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .container {
                    display: flex;
                    height: 100vh;
                }
                .sidebar {
                    width: 250px;
                    padding: 20px;
                    background-color: #f5f5f5;
                    border-right: 1px solid #ddd;
                    overflow-y: auto;
                }
                .graph-container {
                    flex-grow: 1;
                    overflow: hidden;
                    position: relative;
                }
                .node {
                    cursor: pointer;
                }
                .link {
                    stroke: #999;
                    stroke-opacity: 0.6;
                }
                .node text {
                    font-size: 12px;
                }
                .details {
                    padding: 10px;
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    width: 300px;
                    max-height: 400px;
                    overflow-y: auto;
                    display: none;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="sidebar">
                    <h2>Code Visualization</h2>
                    <div>
                        <h3>Filters</h3>
                        <div>
                            <input type="checkbox" id="filter-module" checked>
                            <label for="filter-module">Modules</label>
                        </div>
                        <div>
                            <input type="checkbox" id="filter-class" checked>
                            <label for="filter-class">Classes</label>
                        </div>
                        <div>
                            <input type="checkbox" id="filter-function" checked>
                            <label for="filter-function">Functions</label>
                        </div>
                        <div>
                            <input type="checkbox" id="filter-method" checked>
                            <label for="filter-method">Methods</label>
                        </div>
                    </div>
                </div>
                <div class="graph-container">
                    <svg width="100%" height="100%"></svg>
                    <div class="details" id="node-details"></div>
                </div>
            </div>
            <script>
                // Graph data
                const graphData = GRAPH_DATA_PLACEHOLDER;
                
                // D3 visualization code here
                // ...
            </script>
        </body>
        </html>
        """
        
        # Replace placeholder with actual graph data
        html_content = html_template.replace("GRAPH_DATA_PLACEHOLDER", graph_data)
        
        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path