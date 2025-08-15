"""
Service layer for business logic.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from .models import User, Task, Project, APIResponse
from .utils import setup_logging, validate_email, safe_get
from .api_client import APIClient


class UserService:
    """Service for user-related operations."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.users: Dict[int, User] = {}
        self._next_id = 1
    
    def create_user(self, name: str, email: str, metadata: Optional[Dict[str, Any]] = None) -> APIResponse:
        """
        Create a new user.
        
        Args:
            name: User's name
            email: User's email
            metadata: Additional user metadata
            
        Returns:
            APIResponse with user data or error
        """
        try:
            # Validate email
            if not validate_email(email):
                return APIResponse.error_response("Invalid email format", "INVALID_EMAIL")
            
            # Check if email already exists
            for user in self.users.values():
                if user.email == email:
                    return APIResponse.error_response("Email already exists", "EMAIL_EXISTS")
            
            # Create user
            user = User(
                id=self._next_id,
                name=name,
                email=email,
                metadata=metadata or {}
            )
            
            self.users[user.id] = user
            self._next_id += 1
            
            self.logger.info(f"Created user: {user.id} - {user.name}")
            return APIResponse.success_response(user.to_dict(), "User created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            return APIResponse.error_response("Failed to create user", "CREATE_ERROR")
    
    def get_user(self, user_id: int) -> APIResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            APIResponse with user data or error
        """
        try:
            user = self.users.get(user_id)
            if not user:
                return APIResponse.error_response("User not found", "USER_NOT_FOUND")
            
            return APIResponse.success_response(user.to_dict())
            
        except Exception as e:
            self.logger.error(f"Error getting user: {e}")
            return APIResponse.error_response("Failed to get user", "GET_ERROR")
    
    def update_user(self, user_id: int, **kwargs) -> APIResponse:
        """
        Update user information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            APIResponse with updated user data or error
        """
        try:
            user = self.users.get(user_id)
            if not user:
                return APIResponse.error_response("User not found", "USER_NOT_FOUND")
            
            # Update allowed fields
            allowed_fields = ['name', 'email', 'is_active', 'metadata']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(user, field, value)
            
            user.updated_at = datetime.now()
            
            self.logger.info(f"Updated user: {user_id}")
            return APIResponse.success_response(user.to_dict(), "User updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            return APIResponse.error_response("Failed to update user", "UPDATE_ERROR")
    
    def list_users(self, active_only: bool = False) -> APIResponse:
        """
        List all users.
        
        Args:
            active_only: Only return active users
            
        Returns:
            APIResponse with list of users
        """
        try:
            users = list(self.users.values())
            if active_only:
                users = [user for user in users if user.is_active]
            
            user_data = [user.to_dict() for user in users]
            return APIResponse.success_response(user_data)
            
        except Exception as e:
            self.logger.error(f"Error listing users: {e}")
            return APIResponse.error_response("Failed to list users", "LIST_ERROR")


class TaskService:
    """Service for task-related operations."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.tasks: Dict[int, Task] = {}
        self._next_id = 1
    
    def create_task(self, title: str, created_by: int, **kwargs) -> APIResponse:
        """
        Create a new task.
        
        Args:
            title: Task title
            created_by: ID of user creating the task
            **kwargs: Additional task fields
            
        Returns:
            APIResponse with task data or error
        """
        try:
            task = Task(
                id=self._next_id,
                title=title,
                created_by=created_by,
                **kwargs
            )
            
            self.tasks[task.id] = task
            self._next_id += 1
            
            self.logger.info(f"Created task: {task.id} - {task.title}")
            return APIResponse.success_response(task.to_dict(), "Task created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating task: {e}")
            return APIResponse.error_response("Failed to create task", "CREATE_ERROR")
    
    def get_task(self, task_id: int) -> APIResponse:
        """
        Get task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            APIResponse with task data or error
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                return APIResponse.error_response("Task not found", "TASK_NOT_FOUND")
            
            return APIResponse.success_response(task.to_dict())
            
        except Exception as e:
            self.logger.error(f"Error getting task: {e}")
            return APIResponse.error_response("Failed to get task", "GET_ERROR")
    
    def update_task(self, task_id: int, **kwargs) -> APIResponse:
        """
        Update task information.
        
        Args:
            task_id: Task ID
            **kwargs: Fields to update
            
        Returns:
            APIResponse with updated task data or error
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                return APIResponse.error_response("Task not found", "TASK_NOT_FOUND")
            
            # Update allowed fields
            allowed_fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'due_date', 'tags']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(task, field, value)
            
            task.updated_at = datetime.now()
            
            self.logger.info(f"Updated task: {task_id}")
            return APIResponse.success_response(task.to_dict(), "Task updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating task: {e}")
            return APIResponse.error_response("Failed to update task", "UPDATE_ERROR")
    
    def list_tasks(self, status: Optional[str] = None, assigned_to: Optional[int] = None) -> APIResponse:
        """
        List tasks with optional filtering.
        
        Args:
            status: Filter by status
            assigned_to: Filter by assigned user
            
        Returns:
            APIResponse with list of tasks
        """
        try:
            tasks = list(self.tasks.values())
            
            if status:
                tasks = [task for task in tasks if task.status == status]
            
            if assigned_to:
                tasks = [task for task in tasks if task.assigned_to == assigned_to]
            
            task_data = [task.to_dict() for task in tasks]
            return APIResponse.success_response(task_data)
            
        except Exception as e:
            self.logger.error(f"Error listing tasks: {e}")
            return APIResponse.error_response("Failed to list tasks", "LIST_ERROR")
    
    def get_overdue_tasks(self) -> APIResponse:
        """
        Get tasks that are overdue.
        
        Returns:
            APIResponse with list of overdue tasks
        """
        try:
            now = datetime.now()
            overdue_tasks = [
                task for task in self.tasks.values()
                if task.due_date and task.due_date < now and task.status not in ['completed', 'cancelled']
            ]
            
            task_data = [task.to_dict() for task in overdue_tasks]
            return APIResponse.success_response(task_data)
            
        except Exception as e:
            self.logger.error(f"Error getting overdue tasks: {e}")
            return APIResponse.error_response("Failed to get overdue tasks", "LIST_ERROR")


class ProjectService:
    """Service for project-related operations."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.projects: Dict[int, Project] = {}
        self._next_id = 1
    
    def create_project(self, name: str, owner_id: int, **kwargs) -> APIResponse:
        """
        Create a new project.
        
        Args:
            name: Project name
            owner_id: ID of project owner
            **kwargs: Additional project fields
            
        Returns:
            APIResponse with project data or error
        """
        try:
            project = Project(
                id=self._next_id,
                name=name,
                owner_id=owner_id,
                **kwargs
            )
            
            self.projects[project.id] = project
            self._next_id += 1
            
            self.logger.info(f"Created project: {project.id} - {project.name}")
            return APIResponse.success_response(project.to_dict(), "Project created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating project: {e}")
            return APIResponse.error_response("Failed to create project", "CREATE_ERROR")
    
    def get_project(self, project_id: int) -> APIResponse:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            APIResponse with project data or error
        """
        try:
            project = self.projects.get(project_id)
            if not project:
                return APIResponse.error_response("Project not found", "PROJECT_NOT_FOUND")
            
            return APIResponse.success_response(project.to_dict())
            
        except Exception as e:
            self.logger.error(f"Error getting project: {e}")
            return APIResponse.error_response("Failed to get project", "GET_ERROR")
    
    def update_project(self, project_id: int, **kwargs) -> APIResponse:
        """
        Update project information.
        
        Args:
            project_id: Project ID
            **kwargs: Fields to update
            
        Returns:
            APIResponse with updated project data or error
        """
        try:
            project = self.projects.get(project_id)
            if not project:
                return APIResponse.error_response("Project not found", "PROJECT_NOT_FOUND")
            
            # Update allowed fields
            allowed_fields = ['name', 'description', 'status', 'start_date', 'end_date', 'members', 'settings']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(project, field, value)
            
            project.updated_at = datetime.now()
            
            self.logger.info(f"Updated project: {project_id}")
            return APIResponse.success_response(project.to_dict(), "Project updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating project: {e}")
            return APIResponse.error_response("Failed to update project", "UPDATE_ERROR")
    
    def list_projects(self, status: Optional[str] = None, owner_id: Optional[int] = None) -> APIResponse:
        """
        List projects with optional filtering.
        
        Args:
            status: Filter by status
            owner_id: Filter by owner
            
        Returns:
            APIResponse with list of projects
        """
        try:
            projects = list(self.projects.values())
            
            if status:
                projects = [project for project in projects if project.status == status]
            
            if owner_id:
                projects = [project for project in projects if project.owner_id == owner_id]
            
            project_data = [project.to_dict() for project in projects]
            return APIResponse.success_response(project_data)
            
        except Exception as e:
            self.logger.error(f"Error listing projects: {e}")
            return APIResponse.error_response("Failed to list projects", "LIST_ERROR")