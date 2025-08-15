"""
Unit tests for data models.
"""

import pytest
from datetime import datetime
from src.models import User, Task, Project, APIResponse


class TestUser:
    """Test User model."""
    
    def test_user_creation(self):
        """Test user creation with required fields."""
        user = User(id=1, name="John Doe", email="john@example.com")
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert user.updated_at is None
    
    def test_user_to_dict(self):
        """Test user to dictionary conversion."""
        user = User(id=1, name="John Doe", email="john@example.com")
        user_dict = user.to_dict()
        
        assert user_dict['id'] == 1
        assert user_dict['name'] == "John Doe"
        assert user_dict['email'] == "john@example.com"
        assert user_dict['is_active'] is True
        assert 'created_at' in user_dict
        assert user_dict['updated_at'] is None
    
    def test_user_from_dict(self):
        """Test user creation from dictionary."""
        user_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': None,
            'is_active': True,
            'metadata': {'role': 'admin'}
        }
        
        user = User.from_dict(user_data)
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert user.metadata == {'role': 'admin'}


class TestTask:
    """Test Task model."""
    
    def test_task_creation(self):
        """Test task creation with required fields."""
        task = Task(id=1, title="Test Task", created_by=1)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.created_by == 1
        assert task.status == "pending"
        assert task.priority == "medium"
        assert task.assigned_to is None
        assert isinstance(task.created_at, datetime)
        assert task.updated_at is None
    
    def test_task_to_dict(self):
        """Test task to dictionary conversion."""
        task = Task(
            id=1,
            title="Test Task",
            created_by=1,
            description="Test description",
            status="in_progress",
            priority="high"
        )
        task_dict = task.to_dict()
        
        assert task_dict['id'] == 1
        assert task_dict['title'] == "Test Task"
        assert task_dict['description'] == "Test description"
        assert task_dict['status'] == "in_progress"
        assert task_dict['priority'] == "high"
        assert 'created_at' in task_dict
    
    def test_task_from_dict(self):
        """Test task creation from dictionary."""
        task_data = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test description',
            'status': 'completed',
            'priority': 'high',
            'assigned_to': 2,
            'created_by': 1,
            'created_at': '2023-01-01T00:00:00',
            'updated_at': None,
            'due_date': None,
            'tags': ['urgent', 'frontend']
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.status == "completed"
        assert task.priority == "high"
        assert task.assigned_to == 2
        assert task.tags == ['urgent', 'frontend']


class TestProject:
    """Test Project model."""
    
    def test_project_creation(self):
        """Test project creation with required fields."""
        project = Project(id=1, name="Test Project", owner_id=1)
        
        assert project.id == 1
        assert project.name == "Test Project"
        assert project.owner_id == 1
        assert project.status == "active"
        assert project.description is None
        assert isinstance(project.created_at, datetime)
        assert project.updated_at is None
    
    def test_project_to_dict(self):
        """Test project to dictionary conversion."""
        project = Project(
            id=1,
            name="Test Project",
            owner_id=1,
            description="Test description",
            status="completed"
        )
        project_dict = project.to_dict()
        
        assert project_dict['id'] == 1
        assert project_dict['name'] == "Test Project"
        assert project_dict['description'] == "Test description"
        assert project_dict['status'] == "completed"
        assert project_dict['owner_id'] == 1
        assert 'created_at' in project_dict
    
    def test_project_from_dict(self):
        """Test project creation from dictionary."""
        project_data = {
            'id': 1,
            'name': 'Test Project',
            'description': 'Test description',
            'status': 'active',
            'owner_id': 1,
            'created_at': '2023-01-01T00:00:00',
            'updated_at': None,
            'start_date': None,
            'end_date': None,
            'members': [1, 2, 3],
            'settings': {'visibility': 'public'}
        }
        
        project = Project.from_dict(project_data)
        
        assert project.id == 1
        assert project.name == "Test Project"
        assert project.status == "active"
        assert project.owner_id == 1
        assert project.members == [1, 2, 3]
        assert project.settings == {'visibility': 'public'}


class TestAPIResponse:
    """Test APIResponse model."""
    
    def test_success_response(self):
        """Test success response creation."""
        data = {"message": "Success"}
        response = APIResponse.success_response(data, "Operation successful")
        
        assert response.success is True
        assert response.data == data
        assert response.message == "Operation successful"
        assert response.error_code is None
        assert isinstance(response.timestamp, datetime)
    
    def test_error_response(self):
        """Test error response creation."""
        response = APIResponse.error_response("Something went wrong", "ERROR_001")
        
        assert response.success is False
        assert response.data is None
        assert response.message == "Something went wrong"
        assert response.error_code == "ERROR_001"
        assert isinstance(response.timestamp, datetime)
    
    def test_response_to_dict(self):
        """Test response to dictionary conversion."""
        response = APIResponse.success_response({"id": 1}, "Created")
        response_dict = response.to_dict()
        
        assert response_dict['success'] is True
        assert response_dict['data'] == {"id": 1}
        assert response_dict['message'] == "Created"
        assert response_dict['error_code'] is None
        assert 'timestamp' in response_dict