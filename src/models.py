"""
Data models for the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class User:
    """User model."""
    
    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            is_active=data.get('is_active', True),
            metadata=data.get('metadata', {})
        )


@dataclass
class Task:
    """Task model."""
    
    id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, cancelled
    priority: str = "medium"  # low, medium, high, urgent
    assigned_to: Optional[int] = None
    created_by: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            assigned_to=data.get('assigned_to'),
            created_by=data['created_by'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            tags=data.get('tags', [])
        )


@dataclass
class Project:
    """Project model."""
    
    id: int
    name: str
    description: Optional[str] = None
    status: str = "active"  # active, completed, on_hold, cancelled
    owner_id: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    members: List[int] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'members': self.members,
            'settings': self.settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description'),
            status=data.get('status', 'active'),
            owner_id=data['owner_id'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            members=data.get('members', []),
            settings=data.get('settings', {})
        )


@dataclass
class APIResponse:
    """Standard API response model."""
    
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'error_code': self.error_code,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def success_response(cls, data: Any = None, message: str = "Success") -> 'APIResponse':
        """Create a success response."""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_response(cls, message: str, error_code: Optional[str] = None) -> 'APIResponse':
        """Create an error response."""
        return cls(success=False, message=message, error_code=error_code)