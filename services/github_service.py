from typing import Dict, List, Any, Optional
import requests
import base64
from datetime import datetime

class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHub service
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.headers["Accept"] = "application/vnd.github.v3+json"
    
    def set_token(self, token: str) -> None:
        """Set or update the GitHub token
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.headers["Authorization"] = f"token {token}"
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information
        
        Returns:
            Dictionary containing user information
        """
        response = requests.get(f"{self.base_url}/user", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get user info: {response.status_code}"}
    
    def list_repositories(self) -> List[Dict[str, Any]]:
        """List repositories for the authenticated user
        
        Returns:
            List of repositories
        """
        response = requests.get(f"{self.base_url}/user/repos", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Failed to list repositories: {response.status_code}"}]
    
    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository information
        """
        response = requests.get(f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get repository: {response.status_code}"}
    
    def get_file_contents(self, owner: str, repo: str, path: str, ref: str = "main") -> Dict[str, Any]:
        """Get file contents from a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path within the repository
            ref: Branch or commit reference
            
        Returns:
            File content and metadata
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            content = response.json()
            if content.get("encoding") == "base64" and content.get("content"):
                # Decode base64 content
                decoded_content = base64.b64decode(content["content"]).decode("utf-8")
                content["decoded_content"] = decoded_content
            return content
        else:
            return {"error": f"Failed to get file contents: {response.status_code}"}
    
    def list_issues(self, owner: str, repo: str, state: str = "open") -> List[Dict[str, Any]]:
        """List issues for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            
        Returns:
            List of issues
        """
        response = requests.get(
            f"{self.base_url}/repos/{owner}/{repo}/issues",
            headers=self.headers,
            params={"state": state}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Failed to list issues: {response.status_code}"}]
    
    def create_issue(self, owner: str, repo: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a new issue
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body
            labels: List of labels to apply
            
        Returns:
            Created issue information
        """
        data = {
            "title": title,
            "body": body
        }
        
        if labels:
            data["labels"] = labels
        
        response = requests.post(
            f"{self.base_url}/repos/{owner}/{repo}/issues",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            return {"error": f"Failed to create issue: {response.status_code}"}
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "open") -> List[Dict[str, Any]]:
        """List pull requests for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state (open, closed, all)
            
        Returns:
            List of pull requests
        """
        response = requests.get(
            f"{self.base_url}/repos/{owner}/{repo}/pulls",
            headers=self.headers,
            params={"state": state}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Failed to list pull requests: {response.status_code}"}]
    
    def get_repository_structure(self, owner: str, repo: str, path: str = "", ref: str = "main") -> List[Dict[str, Any]]:
        """Get repository file structure
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Directory path within the repository
            ref: Branch or commit reference
            
        Returns:
            List of files and directories
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Failed to get repository structure: {response.status_code}"}]