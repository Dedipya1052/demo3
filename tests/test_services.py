"""
Unit tests for service layer.
"""

import pytest
from datetime import datetime, timedelta
from src.services import UserService, TaskService, ProjectService
from src.models import APIResponse


class TestUserService:
    """Test UserService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = UserService()
    
    def test_create_user_success(self):
        """Test successful user creation."""
        result = self.service.create_user("John Doe", "john@example.com")
        
        assert result.success is True
        assert result.data['name'] == "John Doe"
        assert result.data['email'] == "john@example.com"
        assert result.data['id'] == 1
        assert result.message == "User created successfully"
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        result = self.service.create_user("John Doe", "invalid-email")
        
        assert result.success is False
        assert result.error_code == "INVALID_EMAIL"
        assert "Invalid email format" in result.message
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        # Create first user
        self.service.create_user("John Doe", "john@example.com")
        
        # Try to create second user with same email
        result = self.service.create_user("Jane Doe", "john@example.com")
        
        assert result.success is False
        assert result.error_code == "EMAIL_EXISTS"
        assert "Email already exists" in result.message
    
    def test_get_user_success(self):
        """Test successful user retrieval."""
        # Create user first
        create_result = self.service.create_user("John Doe", "john@example.com")
        user_id = create_result.data['id']
        
        # Get user
        result = self.service.get_user(user_id)
        
        assert result.success is True
        assert result.data['id'] == user_id
        assert result.data['name'] == "John Doe"
    
    def test_get_user_not_found(self):
        """Test user retrieval for non-existent user."""
        result = self.service.get_user(999)
        
        assert result.success is False
        assert result.error_code == "USER_NOT_FOUND"
    
    def test_list_users(self):
        """Test listing users."""
        # Create some users
        self.service.create_user("John Doe", "john@example.com")
        self.service.create_user("Jane Doe", "jane@example.com")
        
        result = self.service.list_users()
        
        assert result.success is True
        assert len(result.data) == 2
        assert result.data[0]['name'] == "John Doe"
        assert result.data[1]['name'] == "Jane Doe"
    
    def test_list_users_active_only(self):
        """Test listing only active users."""
        # Create users
        self.service.create_user("John Doe", "john@example.com")
        self.service.create_user("Jane Doe", "jane@example.com")
        
        # Deactivate one user
        self.service.update_user(1, is_active=False)
        
        result = self.service.list_users(active_only=True)
        
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]['name'] == "Jane Doe"


class TestTaskService:
    """Test TaskService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = TaskService()
    
    def test_create_task_success(self):
        """Test successful task creation."""
        result = self.service.create_task("Test Task", created_by=1)
        
        assert result.success is True
        assert result.data['title'] == "Test Task"
        assert result.data['created_by'] == 1
        assert result.data['status'] == "pending"
        assert result.data['priority'] == "medium"
        assert result.data['id'] == 1
    
    def test_create_task_with_all_fields(self):
        """Test task creation with all optional fields."""
        due_date = datetime.now() + timedelta(days=7)
        result = self.service.create_task(
            title="Complex Task",
            created_by=1,
            description="A complex task description",
            assigned_to=2,
            priority="high",
            due_date=due_date,
            tags=["urgent", "frontend"]
        )
        
        assert result.success is True
        assert result.data['title'] == "Complex Task"
        assert result.data['description'] == "A complex task description"
        assert result.data['assigned_to'] == 2
        assert result.data['priority'] == "high"
        assert result.data['tags'] == ["urgent", "frontend"]
    
    def test_get_task_success(self):
        """Test successful task retrieval."""
        # Create task first
        create_result = self.service.create_task("Test Task", created_by=1)
        task_id = create_result.data['id']
        
        # Get task
        result = self.service.get_task(task_id)
        
        assert result.success is True
        assert result.data['id'] == task_id
        assert result.data['title'] == "Test Task"
    
    def test_get_task_not_found(self):
        """Test task retrieval for non-existent task."""
        result = self.service.get_task(999)
        
        assert result.success is False
        assert result.error_code == "TASK_NOT_FOUND"
    
    def test_update_task_success(self):
        """Test successful task update."""
        # Create task first
        create_result = self.service.create_task("Original Title", created_by=1)
        task_id = create_result.data['id']
        
        # Update task
        result = self.service.update_task(
            task_id,
            title="Updated Title",
            status="in_progress",
            priority="high"
        )
        
        assert result.success is True
        assert result.data['title'] == "Updated Title"
        assert result.data['status'] == "in_progress"
        assert result.data['priority'] == "high"
    
    def test_list_tasks(self):
        """Test listing tasks."""
        # Create some tasks
        self.service.create_task("Task 1", created_by=1)
        self.service.create_task("Task 2", created_by=1)
        self.service.create_task("Task 3", created_by=2)
        
        result = self.service.list_tasks()
        
        assert result.success is True
        assert len(result.data) == 3
    
    def test_list_tasks_with_filters(self):
        """Test listing tasks with filters."""
        # Create tasks
        self.service.create_task("Task 1", created_by=1, assigned_to=2)
        self.service.create_task("Task 2", created_by=1, assigned_to=3)
        self.service.create_task("Task 3", created_by=2, assigned_to=2)
        
        # Filter by assigned_to
        result = self.service.list_tasks(assigned_to=2)
        
        assert result.success is True
        assert len(result.data) == 2
        assert all(task['assigned_to'] == 2 for task in result.data)
    
    def test_get_overdue_tasks(self):
        """Test getting overdue tasks."""
        # Create tasks with different due dates
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)
        
        self.service.create_task("Overdue Task", created_by=1, due_date=past_date)
        self.service.create_task("Future Task", created_by=1, due_date=future_date)
        self.service.create_task("Completed Overdue", created_by=1, due_date=past_date, status="completed")
        
        result = self.service.get_overdue_tasks()
        
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]['title'] == "Overdue Task"


class TestProjectService:
    """Test ProjectService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ProjectService()
    
    def test_create_project_success(self):
        """Test successful project creation."""
        result = self.service.create_project("Test Project", owner_id=1)
        
        assert result.success is True
        assert result.data['name'] == "Test Project"
        assert result.data['owner_id'] == 1
        assert result.data['status'] == "active"
        assert result.data['id'] == 1
    
    def test_create_project_with_all_fields(self):
        """Test project creation with all optional fields."""
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=30)
        
        result = self.service.create_project(
            name="Complex Project",
            owner_id=1,
            description="A complex project description",
            start_date=start_date,
            end_date=end_date,
            members=[1, 2, 3],
            settings={"visibility": "public"}
        )
        
        assert result.success is True
        assert result.data['name'] == "Complex Project"
        assert result.data['description'] == "A complex project description"
        assert result.data['members'] == [1, 2, 3]
        assert result.data['settings'] == {"visibility": "public"}
    
    def test_get_project_success(self):
        """Test successful project retrieval."""
        # Create project first
        create_result = self.service.create_project("Test Project", owner_id=1)
        project_id = create_result.data['id']
        
        # Get project
        result = self.service.get_project(project_id)
        
        assert result.success is True
        assert result.data['id'] == project_id
        assert result.data['name'] == "Test Project"
    
    def test_get_project_not_found(self):
        """Test project retrieval for non-existent project."""
        result = self.service.get_project(999)
        
        assert result.success is False
        assert result.error_code == "PROJECT_NOT_FOUND"
    
    def test_update_project_success(self):
        """Test successful project update."""
        # Create project first
        create_result = self.service.create_project("Original Name", owner_id=1)
        project_id = create_result.data['id']
        
        # Update project
        result = self.service.update_project(
            project_id,
            name="Updated Name",
            status="completed",
            description="Updated description"
        )
        
        assert result.success is True
        assert result.data['name'] == "Updated Name"
        assert result.data['status'] == "completed"
        assert result.data['description'] == "Updated description"
    
    def test_list_projects(self):
        """Test listing projects."""
        # Create some projects
        self.service.create_project("Project 1", owner_id=1)
        self.service.create_project("Project 2", owner_id=1)
        self.service.create_project("Project 3", owner_id=2)
        
        result = self.service.list_projects()
        
        assert result.success is True
        assert len(result.data) == 3
    
    def test_list_projects_with_filters(self):
        """Test listing projects with filters."""
        # Create projects
        self.service.create_project("Project 1", owner_id=1, status="active")
        self.service.create_project("Project 2", owner_id=1, status="completed")
        self.service.create_project("Project 3", owner_id=2, status="active")
        
        # Filter by status
        result = self.service.list_projects(status="active")
        
        assert result.success is True
        assert len(result.data) == 2
        assert all(project['status'] == "active" for project in result.data)
        
        # Filter by owner
        result = self.service.list_projects(owner_id=1)
        
        assert result.success is True
        assert len(result.data) == 2
        assert all(project['owner_id'] == 1 for project in result.data)