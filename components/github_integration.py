import streamlit as st
import os
from typing import Dict, List, Any, Optional
from services.github_service import GitHubService
from services.code_analysis_service import CodeAnalysisService

def render_github_integration():
    """Render the GitHub integration interface"""
    # Create a header with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=100)
    with col2:
        st.markdown("<h1 class='main-header'>GitHub Integration</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subheader'>Connect and analyze GitHub repositories</p>", unsafe_allow_html=True)
    
    # Initialize GitHub service if not exists
    if 'github_service' not in st.session_state:
        st.session_state.github_service = GitHubService()
    
    # Authentication section
    st.subheader("GitHub Authentication")
    
    # Check if token is already set
    token_set = bool(st.session_state.github_service.token)
    
    if not token_set:
        with st.form("github_auth_form"):
            github_token = st.text_input(
                "GitHub Personal Access Token", 
                type="password",
                help="Create a token with 'repo' scope at https://github.com/settings/tokens"
            )
            submit_button = st.form_submit_button("Connect to GitHub")
            
            if submit_button and github_token:
                st.session_state.github_service.set_token(github_token)
                st.success("Successfully connected to GitHub!")
                st.rerun()
    else:
        st.success("✅ Connected to GitHub")
        if st.button("Disconnect"):
            st.session_state.github_service.set_token(None)
            st.rerun()
        
        # Repository section
        st.subheader("Repository Access")
        
        # Repository input
        col1, col2 = st.columns([3, 1])
        with col1:
            repo_url = st.text_input(
                "GitHub Repository URL",
                help="Example: https://github.com/username/repo"
            )
        with col2:
            connect_button = st.button("Connect to Repository")
        
        if connect_button and repo_url:
            # Parse owner and repo from URL
            try:
                parts = repo_url.strip("/").split("/")
                owner = parts[-2]
                repo = parts[-1]
                
                # Get repository info
                repo_info = st.session_state.github_service.get_repository(owner, repo)
                
                if "error" in repo_info:
                    st.error(f"Error connecting to repository: {repo_info['error']}")
                else:
                    st.session_state.current_repo = {
                        "owner": owner,
                        "name": repo,
                        "info": repo_info
                    }
                    st.success(f"Connected to {owner}/{repo}")
                    st.rerun()
            except Exception as e:
                st.error(f"Invalid repository URL: {str(e)}")
        
        # If repository is connected, show repository explorer
        if "current_repo" in st.session_state:
            render_repository_explorer()

def render_repository_explorer():
    """Render the repository explorer section"""
    owner = st.session_state.current_repo["owner"]
    repo = st.session_state.current_repo["name"]
    
    st.subheader(f"Repository: {owner}/{repo}")
    
    # Repository tabs
    tab1, tab2, tab3 = st.tabs(["Files", "Issues", "Pull Requests"])
    
    # Files tab
    with tab1:
        # Get repository structure
        structure = st.session_state.github_service.get_repository_structure(
            owner, repo
        )
        
        if isinstance(structure, list) and "error" in structure[0]:
            st.error(f"Error fetching repository structure: {structure[0]['error']}")
        else:
            # Display file tree
            st.write("Select a file to analyze:")
            
            # Create a simple file browser
            for item in structure:
                if item["type"] == "file" and item["name"].endswith((".py", ".js", ".java", ".cpp", ".c", ".go", ".rb")):
                    if st.button(f"📄 {item['name']}", key=f"file_{item['path']}"):
                        file_content = st.session_state.github_service.get_file_contents(
                            owner, repo, item["path"]
                        )
                        
                        if "error" in file_content:
                            st.error(f"Error fetching file: {file_content['error']}")
                        else:
                            st.session_state.current_file = {
                                "name": item["name"],
                                "path": item["path"],
                                "content": file_content.get("decoded_content", "")
                            }
                            st.rerun()
            
            # If a file is selected, show file content and analysis
            if "current_file" in st.session_state:
                render_file_analysis()
    
    # Issues tab
    with tab2:
        # Get issues
        issues = st.session_state.github_service.list_issues(owner, repo)
        
        if isinstance(issues, list) and issues and "error" in issues[0]:
            st.error(f"Error fetching issues: {issues[0]['error']}")
        else:
            # Create new issue section
            with st.expander("Create New Issue"):
                with st.form("new_issue_form"):
                    issue_title = st.text_input("Issue Title")
                    issue_body = st.text_area("Issue Description")
                    issue_labels = st.multiselect(
                        "Labels",
                        ["bug", "enhancement", "documentation", "question"]
                    )
                    
                    submit_issue = st.form_submit_button("Create Issue")
                    
                    if submit_issue and issue_title and issue_body:
                        result = st.session_state.github_service.create_issue(
                            owner, repo, issue_title, issue_body, issue_labels
                        )
                        
                        if "error" in result:
                            st.error(f"Error creating issue: {result['error']}")
                        else:
                            st.success("Issue created successfully!")
                            st.rerun()
            
            # Display existing issues
            st.subheader("Existing Issues")
            
            if not issues:
                st.info("No issues found in this repository.")
            else:
                for issue in issues:
                    with st.expander(f"#{issue['number']} - {issue['title']}"):
                        st.write(f"**Status:** {issue['state']}")
                        st.write(f"**Created by:** {issue['user']['login']}")
                        st.write(f"**Created at:** {issue['created_at']}")
                        st.markdown(issue['body'])
                        
                        # Display labels
                        if issue['labels']:
                            st.write("**Labels:**")
                            for label in issue['labels']:
                                st.markdown(f"- {label['name']}")
    
    # Pull Requests tab
    with tab3:
        # Get pull requests
        pull_requests = st.session_state.github_service.get_pull_requests(owner, repo)
        
        if isinstance(pull_requests, list) and pull_requests and "error" in pull_requests[0]:
            st.error(f"Error fetching pull requests: {pull_requests[0]['error']}")
        else:
            st.subheader("Pull Requests")
            
            if not pull_requests:
                st.info("No pull requests found in this repository.")
            else:
                for pr in pull_requests:
                    with st.expander(f"#{pr['number']} - {pr['title']}"):
                        st.write(f"**Status:** {pr['state']}")
                        st.write(f"**Created by:** {pr['user']['login']}")
                        st.write(f"**Created at:** {pr['created_at']}")
                        st.markdown(pr['body'])

def render_file_analysis():
    """Render file content and analysis"""
    file = st.session_state.current_file
    
    st.subheader(f"File: {file['name']}")
    
    # Display file content
    with st.expander("File Content", expanded=True):
        st.code(file['content'], language=get_language_from_filename(file['name']))
    
    # Analyze button
    if st.button("Analyze Code", type="primary"):
        with st.spinner("Analyzing code..."):
            # Initialize code analysis service if not exists
            if 'code_analysis_service' not in st.session_state:
                st.session_state.code_analysis_service = CodeAnalysisService()
            
            # Get analysis results
            analysis = st.session_state.code_analysis_service.analyze_code(file['content'])
            metrics = st.session_state.code_analysis_service.get_code_metrics(file['content'])
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Code Smells", "Best Practices", "Suggestions"])
            
            # Overview tab
            with tab1:
                st.subheader("Code Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Lines of Code", metrics['loc'])
                with col2:
                    st.metric("Classes", metrics['classes'])
                with col3:
                    st.metric("Functions", metrics['functions'])
                with col4:
                    st.metric("Imports", metrics['imports'])
                
                st.subheader("Complexity Analysis")
                st.progress(min(analysis['complexity_score'] / 20, 1.0))
                st.write(f"Complexity Score: {analysis['complexity_score']}")
            
            # Code Smells tab
            with tab2:
                st.subheader("Detected Code Smells")
                if analysis['code_smells']:
                    for smell in analysis['code_smells']:
                        with st.expander(f"{smell['type']} at line {smell['location']}"):
                            st.write(smell['message'])
                            
                            # Add option to create issue from code smell
                            if st.button(f"Create Issue for this Code Smell", key=f"issue_{smell['location']}"):
                                owner = st.session_state.current_repo["owner"]
                                repo = st.session_state.current_repo["name"]
                                
                                issue_title = f"Code Smell: {smell['type']} in {file['name']}"
                                issue_body = f"**File:** {file['path']}\n\n**Location:** Line {smell['location']}\n\n**Issue:** {smell['message']}"
                                
                                result = st.session_state.github_service.create_issue(
                                    owner, repo, issue_title, issue_body, ["bug", "code-quality"]
                                )
                                
                                if "error" in result:
                                    st.error(f"Error creating issue: {result['error']}")
                                else:
                                    st.success("Issue created successfully!")
                else:
                    st.success("No code smells detected!")
            
            # Best Practices tab
            with tab3:
                st.subheader("Best Practices Analysis")
                if analysis['best_practices']:
                    for violation in analysis['best_practices']:
                        with st.expander(f"Issue at line {violation['location']}"):
                            st.write(violation['message'])
                            
                            # Add option to create issue from best practice violation
                            if st.button(f"Create Issue for this Violation", key=f"violation_{violation['location']}"):
                                owner = st.session_state.current_repo["owner"]
                                repo = st.session_state.current_repo["name"]
                                
                                issue_title = f"Best Practice Violation in {file['name']}"
                                issue_body = f"**File:** {file['path']}\n\n**Location:** Line {violation['location']}\n\n**Issue:** {violation['message']}"
                                
                                result = st.session_state.github_service.create_issue(
                                    owner, repo, issue_title, issue_body, ["enhancement", "code-quality"]
                                )
                                
                                if "error" in result:
                                    st.error(f"Error creating issue: {result['error']}")
                                else:
                                    st.success("Issue created successfully!")
                else:
                    st.success("All best practices are followed!")
            
            # Suggestions tab
            with tab4:
                st.subheader("Improvement Suggestions")
                if analysis['suggestions']:
                    for suggestion in analysis['suggestions']:
                        st.info(suggestion)
                else:
                    st.success("No immediate improvements suggested!")

def get_language_from_filename(filename: str) -> str:
    """Get the programming language based on file extension"""
    extension = filename.split('.')[-1].lower()
    
    language_map = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'html': 'html',
        'css': 'css',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'cs': 'csharp',
        'go': 'go',
        'rb': 'ruby',
        'php': 'php',
        'swift': 'swift',
        'kt': 'kotlin',
        'rs': 'rust',
        'sh': 'bash',
        'md': 'markdown',
        'json': 'json',
        'xml': 'xml'
    }