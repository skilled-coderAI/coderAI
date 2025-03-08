import streamlit as st
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Project:
    name: str
    description: str
    created_at: datetime
    status: str
    tasks: List[dict]
    collaborators: List[str]
    repository_url: Optional[str] = None

class ProjectManagement:
    def __init__(self):
        if 'projects' not in st.session_state:
            st.session_state.projects = []

    def create_project(self, name: str, description: str, repository_url: str = None):
        """Create a new project"""
        project = Project(
            name=name,
            description=description,
            created_at=datetime.now(),
            status='active',
            tasks=[],
            collaborators=[],
            repository_url=repository_url
        )
        st.session_state.projects.append(project)
        return project

    def add_task(self, project_name: str, task: dict):
        """Add a task to a project"""
        for project in st.session_state.projects:
            if project.name == project_name:
                project.tasks.append(task)
                return True
        return False

    def add_collaborator(self, project_name: str, collaborator: str):
        """Add a collaborator to a project"""
        for project in st.session_state.projects:
            if project.name == project_name:
                project.collaborators.append(collaborator)
                return True
        return False

    def update_project_status(self, project_name: str, status: str):
        """Update project status"""
        for project in st.session_state.projects:
            if project.name == project_name:
                project.status = status
                return True
        return False

    def render_project_dashboard(self):
        """Render the project management dashboard"""
        st.title('Project Management Dashboard')

        # Create new project section
        with st.expander('Create New Project'):
            project_name = st.text_input('Project Name')
            project_desc = st.text_area('Project Description')
            repo_url = st.text_input('Repository URL (optional)')
            
            if st.button('Create Project'):
                if project_name and project_desc:
                    self.create_project(project_name, project_desc, repo_url)
                    st.success(f'Project {project_name} created successfully!')
                else:
                    st.error('Please fill in required fields')

        # Display existing projects
        if st.session_state.projects:
            for project in st.session_state.projects:
                with st.expander(f'Project: {project.name}'):
                    st.write(f'Description: {project.description}')
                    st.write(f'Status: {project.status}')
                    st.write(f'Created: {project.created_at.strftime("%Y-%m-%d %H:%M")}')
                    
                    # Tasks section
                    st.subheader('Tasks')
                    for task in project.tasks:
                        st.write(f"- {task['title']}: {task['status']}")
                    
                    # Add new task
                    task_title = st.text_input('New Task Title', key=f'task_{project.name}')
                    if st.button('Add Task', key=f'add_task_{project.name}'):
                        if task_title:
                            self.add_task(project.name, {
                                'title': task_title,
                                'status': 'pending',
                                'created_at': datetime.now()
                            })
                            st.success('Task added successfully!')
                    
                    # Collaborators section
                    st.subheader('Collaborators')
                    st.write(', '.join(project.collaborators) if project.collaborators else 'No collaborators yet')
                    
                    # Add collaborator
                    new_collaborator = st.text_input('Add Collaborator', key=f'collab_{project.name}')
                    if st.button('Add', key=f'add_collab_{project.name}'):
                        if new_collaborator:
                            self.add_collaborator(project.name, new_collaborator)
                            st.success(f'Added {new_collaborator} to the project')
                    
                    # Update project status
                    new_status = st.selectbox(
                        'Update Status',
                        ['active', 'on hold', 'completed'],
                        key=f'status_{project.name}'
                    )
                    if st.button('Update Status', key=f'update_status_{project.name}'):
                        self.update_project_status(project.name, new_status)
                        st.success('Project status updated successfully!')
        else:
            st.info('No projects created yet. Create your first project above!')