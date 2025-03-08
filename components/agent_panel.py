"""
Agent Framework Panel Component for CoderAI
This component provides the UI for interacting with CoderAI Agent Framework capabilities.
"""

import streamlit as st
import json
from typing import Dict, List, Any, Optional

def render_agent_panel():
    """Render the Agent Framework panel in the CoderAI interface"""
    st.title("🤖 Agent Framework")
    st.markdown("### Powerful & Zero-Code LLM Agent Framework")
    
    # Access the Agent Framework core from session state
    agent_core = st.session_state.agent_core
    
    # Create tabs for different Agent Framework capabilities
    tabs = st.tabs(["Agent Playground", "Workflow Builder", "Tools Explorer"])
    
    with tabs[0]:  # Agent Playground
        render_agent_playground(agent_core)
    
    with tabs[1]:  # Workflow Builder
        render_workflow_builder(agent_core)
    
    with tabs[2]:  # Tools Explorer
        render_tools_explorer(agent_core)

def render_agent_playground(agent_core):
    """Render the Agent Playground interface"""
    st.header("Agent Playground")
    st.markdown("Create and interact with AI agents using natural language.")
    
    # Agent type selection
    agent_types = ["code_assistant", "code_evolution", "nlp_interface", "synthetic_data"]
    selected_agent = st.selectbox("Select Agent Type", agent_types)
    
    # Agent configuration
    with st.expander("Agent Configuration", expanded=False):
        st.markdown("Configure your agent's behavior and capabilities.")
        
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
        
        with col2:
            memory_enabled = st.checkbox("Enable Memory", value=True)
            tools_enabled = st.checkbox("Enable Tools", value=True)
    
    # Task input
    st.subheader("Task Description")
    task_description = st.text_area(
        "Describe your task in natural language",
        height=100,
        placeholder="e.g., Create a function that sorts a list of dictionaries by a specific key"
    )
    
    # Execute button
    if st.button("Execute Task", type="primary"):
        if not task_description:
            st.error("Please provide a task description.")
            return
        
        with st.spinner("Agent is working on your task..."):
            # Create agent configuration
            agent_config = {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "memory_enabled": memory_enabled,
                "tools_enabled": tools_enabled
            }
            
            try:
                # Create and execute the agent
                agent = agent_core.create_agent(selected_agent, agent_config)
                result = agent_core.execute_agent_task(agent, task_description)
                
                # Display results
                st.success("Task completed successfully!")
                
                # Result tabs
                result_tabs = st.tabs(["Output", "Code", "Explanation"])
                
                with result_tabs[0]:  # Output
                    st.json(result)
                
                with result_tabs[1]:  # Code
                    if "code" in result:
                        st.code(result["code"], language="python")
                    else:
                        st.info("No code was generated for this task.")
                
                with result_tabs[2]:  # Explanation
                    if "explanation" in result:
                        st.markdown(result["explanation"])
                    else:
                        st.info("No explanation was provided for this task.")
                
            except Exception as e:
                st.error(f"Error executing task: {str(e)}")
    
    # Example tasks
    with st.expander("Example Tasks", expanded=False):
        example_tasks = {
            "code_assistant": [
                "Create a function to calculate the Fibonacci sequence",
                "Write a class for managing a simple to-do list",
                "Implement a binary search algorithm"
            ],
            "code_evolution": [
                "Optimize this function for better performance: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
                "Refactor this code to use more modern Python features",
                "Improve the error handling in this function"
            ],
            "nlp_interface": [
                "I need a function that processes text and counts word frequencies",
                "Create a simple sentiment analysis function",
                "Generate a class for parsing JSON data from an API"
            ],
            "synthetic_data": [
                "Generate synthetic user data for testing a login system",
                "Create test data for a financial transaction system",
                "Generate sample data for a machine learning model"
            ]
        }
        
        st.markdown("### Example Tasks for " + selected_agent)
        for example in example_tasks.get(selected_agent, []):
            if st.button(example, key=f"example_{example[:20]}"):
                # This will set the task description when an example is clicked
                st.session_state.task_description = example
                st.experimental_rerun()

def render_workflow_builder(agent_core):
    """Render the Workflow Builder interface"""
    st.header("Workflow Builder")
    st.markdown("Create automated workflows by combining multiple agents and tools.")
    
    # Workflow name
    workflow_name = st.text_input("Workflow Name", placeholder="e.g., Code Refactoring Pipeline")
    
    # Workflow steps
    st.subheader("Workflow Steps")
    
    # Initialize workflow steps in session state if not present
    if "workflow_steps" not in st.session_state:
        st.session_state.workflow_steps = []
    
    # Display existing steps
    for i, step in enumerate(st.session_state.workflow_steps):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**Step {i+1}:** {step['description']}")
        with col2:
            if st.button("Edit", key=f"edit_step_{i}"):
                st.session_state.editing_step = i
        with col3:
            if st.button("Delete", key=f"delete_step_{i}"):
                st.session_state.workflow_steps.pop(i)
                st.experimental_rerun()
    
    # Add new step
    with st.expander("Add Workflow Step", expanded=len(st.session_state.workflow_steps) == 0):
        step_type = st.selectbox(
            "Step Type",
            ["Agent Task", "Tool Execution", "Conditional", "Loop"],
            key="new_step_type"
        )
        
        step_description = st.text_input(
            "Step Description",
            placeholder="e.g., Analyze code quality",
            key="new_step_description"
        )
        
        step_config = {}
        
        if step_type == "Agent Task":
            step_config["agent_type"] = st.selectbox(
                "Agent Type",
                ["code_assistant", "code_evolution", "nlp_interface", "synthetic_data"],
                key="new_step_agent_type"
            )
            
            step_config["task"] = st.text_area(
                "Task Description",
                placeholder="e.g., Analyze the code and suggest improvements",
                key="new_step_task"
            )
            
        elif step_type == "Tool Execution":
            available_tools = [tool["name"] for tool in agent_core.get_available_tools()]
            step_config["tool"] = st.selectbox("Tool", available_tools, key="new_step_tool")
            
            step_config["parameters"] = st.text_area(
                "Parameters (JSON)",
                placeholder='{"param1": "value1", "param2": "value2"}',
                key="new_step_parameters"
            )
            
        elif step_type == "Conditional":
            step_config["condition"] = st.text_area(
                "Condition",
                placeholder="e.g., result.success == True",
                key="new_step_condition"
            )
            
            step_config["if_true"] = st.text_input(
                "If True (Step ID)",
                placeholder="e.g., 2",
                key="new_step_if_true"
            )
            
            step_config["if_false"] = st.text_input(
                "If False (Step ID)",
                placeholder="e.g., 3",
                key="new_step_if_false"
            )
            
        elif step_type == "Loop":
            step_config["iterations"] = st.number_input(
                "Iterations",
                min_value=1,
                max_value=100,
                value=5,
                key="new_step_iterations"
            )
            
            step_config["target_step"] = st.text_input(
                "Target Step ID",
                placeholder="e.g., 1",
                key="new_step_target"
            )
        
        # Add step button
        if st.button("Add Step", key="add_step_button"):
            if not step_description:
                st.error("Please provide a step description.")
                return
                
            # Create new step
            new_step = {
                "type": step_type,
                "description": step_description,
                "config": step_config
            }
            
            # Add to workflow steps
            st.session_state.workflow_steps.append(new_step)
            st.success(f"Step added: {step_description}")
            st.experimental_rerun()
    
    # Save workflow
    if st.button("Save Workflow", type="primary", disabled=len(st.session_state.workflow_steps) == 0):
        if not workflow_name:
            st.error("Please provide a workflow name.")
            return
            
        with st.spinner("Saving workflow..."):
            try:
                # Create workflow configuration
                workflow_config = {
                    "name": workflow_name,
                    "steps": st.session_state.workflow_steps
                }
                
                # Save workflow
                result = agent_core.save_workflow(workflow_config)
                
                if result["success"]:
                    st.success(f"Workflow '{workflow_name}' saved successfully!")
                    # Clear workflow steps
                    st.session_state.workflow_steps = []
                    st.experimental_rerun()
                else:
                    st.error(f"Error saving workflow: {result['error']}")
                    
            except Exception as e:
                st.error(f"Error saving workflow: {str(e)}")

def render_tools_explorer(agent_core):
    """Render the Tools Explorer interface"""
    st.header("Tools Explorer")
    st.markdown("Explore and test the tools available to the Agent Framework.")
    
    # Get available tools
    available_tools = agent_core.get_available_tools()
    
    # Tool categories
    tool_categories = {
        "File Operations": [tool for tool in available_tools if tool["category"] == "file"],
        "Web Operations": [tool for tool in available_tools if tool["category"] == "web"],
        "Code Operations": [tool for tool in available_tools if tool["category"] == "code"],
        "Data Operations": [tool for tool in available_tools if tool["category"] == "data"],
        "Terminal Operations": [tool for tool in available_tools if tool["category"] == "terminal"],
        "RAG Operations": [tool for tool in available_tools if tool["category"] == "rag"],
        "Other": [tool for tool in available_tools if tool["category"] not in ["file", "web", "code", "data", "terminal", "rag"]]
    }
    
    # Create tabs for tool categories
    category_tabs = st.tabs(list(tool_categories.keys()))
    
    for i, (category, tools) in enumerate(tool_categories.items()):
        with category_tabs[i]:
            if not tools:
                st.info(f"No tools available in the {category} category.")
                continue
                
            for tool in tools:
                with st.expander(f"{tool['name']} - {tool['description']}"):
                    # Tool details
                    st.markdown(f"**Name:** {tool['name']}")
                    st.markdown(f"**Description:** {tool['description']}")
                    st.markdown(f"**Category:** {tool['category']}")
                    
                    # Tool parameters
                    st.subheader("Parameters")
                    if "parameters" in tool and tool["parameters"]:
                        params_table = ""
                        for param_name, param_info in tool["parameters"].items():
                            param_type = param_info.get("type", "any")
                            param_description = param_info.get("description", "")
                            param_required = "Yes" if param_info.get("required", False) else "No"
                            params_table += f"| {param_name} | {param_type} | {param_required} | {param_description} |\n"
                            
                        if params_table:
                            st.markdown("| Name | Type | Required | Description |")
                            st.markdown("|------|------|----------|-------------|")
                            st.markdown(params_table)
                        else:
                            st.info("No parameters required.")
                    else:
                        st.info("No parameters required.")
                    
                    # Test tool
                    st.subheader("Test Tool")
                    
                    # Parameter inputs
                    param_values = {}
                    if "parameters" in tool and tool["parameters"]:
                        for param_name, param_info in tool["parameters"].items():
                            param_type = param_info.get("type", "string")
                            param_description = param_info.get("description", "")
                            
                            if param_type == "string":
                                param_values[param_name] = st.text_input(
                                    f"{param_name} ({param_description})",
                                    key=f"tool_{tool['name']}_{param_name}"
                                )
                            elif param_type == "integer" or param_type == "number":
                                param_values[param_name] = st.number_input(
                                    f"{param_name} ({param_description})",
                                    key=f"tool_{tool['name']}_{param_name}"
                                )
                            elif param_type == "boolean":
                                param_values[param_name] = st.checkbox(
                                    f"{param_name} ({param_description})",
                                    key=f"tool_{tool['name']}_{param_name}"
                                )
                            elif param_type == "array":
                                param_values[param_name] = st.text_area(
                                    f"{param_name} ({param_description}) - Enter one item per line",
                                    key=f"tool_{tool['name']}_{param_name}"
                                ).split("\n")
                            elif param_type == "object":
                                param_values[param_name] = st.text_area(
                                    f"{param_name} ({param_description}) - Enter JSON",
                                    key=f"tool_{tool['name']}_{param_name}"
                                )
                                try:
                                    if param_values[param_name]:
                                        param_values[param_name] = json.loads(param_values[param_name])
                                except json.JSONDecodeError:
                                    st.error(f"Invalid JSON for parameter {param_name}")
                    
                    # Execute button
                    if st.button("Execute Tool", key=f"execute_{tool['name']}"):
                        with st.spinner(f"Executing {tool['name']}..."):
                            try:
                                result = agent_core.execute_tool(tool["name"], param_values)
                                
                                # Display result
                                st.success("Tool executed successfully!")
                                st.json(result)
                                
                            except Exception as e:
                                st.error(f"Error executing tool: {str(e)}")
