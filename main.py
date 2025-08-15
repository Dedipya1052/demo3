#!/usr/bin/env python3
"""
Main application entry point for Demo3.

This module provides a command-line interface for the Demo3 application,
allowing users to interact with the user, task, and project management system.
"""

import click
import json
from datetime import datetime
from src.config import Config
from src.services import UserService, TaskService, ProjectService
from src.utils import setup_logging, format_timestamp


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--log-file', type=str, help='Log file path')
def cli(debug, log_file):
    """Demo3 - A Complete Python Project Management System."""
    # Setup logging
    log_level = "DEBUG" if debug else Config.LOG_LEVEL
    setup_logging(level=log_level, log_file=log_file)
    
    # Validate configuration
    if not Config.validate():
        click.echo("❌ Configuration validation failed!")
        return


@cli.group()
def users():
    """Manage users."""
    pass


@users.command()
@click.option('--name', required=True, help='User name')
@click.option('--email', required=True, help='User email')
@click.option('--metadata', type=str, help='Additional metadata as JSON')
def create(name, email, metadata):
    """Create a new user."""
    try:
        metadata_dict = json.loads(metadata) if metadata else {}
    except json.JSONDecodeError:
        click.echo("❌ Invalid JSON format for metadata")
        return
    
    service = UserService()
    result = service.create_user(name=name, email=email, metadata=metadata_dict)
    
    if result.success:
        click.echo(f"✅ {result.message}")
        click.echo(f"User ID: {result.data['id']}")
    else:
        click.echo(f"❌ {result.message}")


@users.command()
@click.argument('user_id', type=int)
def get(user_id):
    """Get user by ID."""
    service = UserService()
    result = service.get_user(user_id)
    
    if result.success:
        user = result.data
        click.echo(f"👤 User Details:")
        click.echo(f"  ID: {user['id']}")
        click.echo(f"  Name: {user['name']}")
        click.echo(f"  Email: {user['email']}")
        click.echo(f"  Active: {user['is_active']}")
        click.echo(f"  Created: {user['created_at']}")
    else:
        click.echo(f"❌ {result.message}")


@users.command()
@click.option('--active-only', is_flag=True, help='Show only active users')
def list(active_only):
    """List all users."""
    service = UserService()
    result = service.list_users(active_only=active_only)
    
    if result.success:
        users = result.data
        if not users:
            click.echo("No users found.")
            return
        
        click.echo(f"👥 Users ({len(users)}):")
        for user in users:
            status = "✅" if user['is_active'] else "❌"
            click.echo(f"  {status} {user['id']}: {user['name']} ({user['email']})")
    else:
        click.echo(f"❌ {result.message}")


@cli.group()
def tasks():
    """Manage tasks."""
    pass


@tasks.command()
@click.option('--title', required=True, help='Task title')
@click.option('--description', help='Task description')
@click.option('--created-by', required=True, type=int, help='User ID of creator')
@click.option('--assigned-to', type=int, help='User ID of assignee')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high', 'urgent']), default='medium', help='Task priority')
@click.option('--due-date', help='Due date (YYYY-MM-DD)')
@click.option('--tags', help='Comma-separated tags')
def create(title, description, created_by, assigned_to, priority, due_date, tags):
    """Create a new task."""
    try:
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        tags_list = [tag.strip() for tag in tags.split(',')] if tags else []
    except ValueError:
        click.echo("❌ Invalid date format. Use YYYY-MM-DD")
        return
    
    service = TaskService()
    result = service.create_task(
        title=title,
        created_by=created_by,
        description=description,
        assigned_to=assigned_to,
        priority=priority,
        due_date=due_date_obj,
        tags=tags_list
    )
    
    if result.success:
        click.echo(f"✅ {result.message}")
        click.echo(f"Task ID: {result.data['id']}")
    else:
        click.echo(f"❌ {result.message}")


@tasks.command()
@click.argument('task_id', type=int)
def get(task_id):
    """Get task by ID."""
    service = TaskService()
    result = service.get_task(task_id)
    
    if result.success:
        task = result.data
        click.echo(f"📋 Task Details:")
        click.echo(f"  ID: {task['id']}")
        click.echo(f"  Title: {task['title']}")
        click.echo(f"  Description: {task['description'] or 'N/A'}")
        click.echo(f"  Status: {task['status']}")
        click.echo(f"  Priority: {task['priority']}")
        click.echo(f"  Assigned to: {task['assigned_to'] or 'Unassigned'}")
        click.echo(f"  Due date: {task['due_date'] or 'No due date'}")
        click.echo(f"  Tags: {', '.join(task['tags']) if task['tags'] else 'None'}")
    else:
        click.echo(f"❌ {result.message}")


@tasks.command()
@click.option('--status', help='Filter by status')
@click.option('--assigned-to', type=int, help='Filter by assigned user')
def list(status, assigned_to):
    """List tasks."""
    service = TaskService()
    result = service.list_tasks(status=status, assigned_to=assigned_to)
    
    if result.success:
        tasks = result.data
        if not tasks:
            click.echo("No tasks found.")
            return
        
        click.echo(f"📋 Tasks ({len(tasks)}):")
        for task in tasks:
            status_emoji = {
                'pending': '⏳',
                'in_progress': '🔄',
                'completed': '✅',
                'cancelled': '❌'
            }.get(task['status'], '❓')
            
            click.echo(f"  {status_emoji} {task['id']}: {task['title']} ({task['priority']})")
    else:
        click.echo(f"❌ {result.message}")


@tasks.command()
def overdue():
    """List overdue tasks."""
    service = TaskService()
    result = service.get_overdue_tasks()
    
    if result.success:
        tasks = result.data
        if not tasks:
            click.echo("No overdue tasks found.")
            return
        
        click.echo(f"⚠️  Overdue Tasks ({len(tasks)}):")
        for task in tasks:
            click.echo(f"  ⚠️  {task['id']}: {task['title']} (Due: {task['due_date']})")
    else:
        click.echo(f"❌ {result.message}")


@cli.group()
def projects():
    """Manage projects."""
    pass


@projects.command()
@click.option('--name', required=True, help='Project name')
@click.option('--description', help='Project description')
@click.option('--owner-id', required=True, type=int, help='User ID of project owner')
@click.option('--start-date', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD)')
def create(name, description, owner_id, start_date, end_date):
    """Create a new project."""
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        click.echo("❌ Invalid date format. Use YYYY-MM-DD")
        return
    
    service = ProjectService()
    result = service.create_project(
        name=name,
        owner_id=owner_id,
        description=description,
        start_date=start_date_obj,
        end_date=end_date_obj
    )
    
    if result.success:
        click.echo(f"✅ {result.message}")
        click.echo(f"Project ID: {result.data['id']}")
    else:
        click.echo(f"❌ {result.message}")


@projects.command()
@click.argument('project_id', type=int)
def get(project_id):
    """Get project by ID."""
    service = ProjectService()
    result = service.get_project(project_id)
    
    if result.success:
        project = result.data
        click.echo(f"📁 Project Details:")
        click.echo(f"  ID: {project['id']}")
        click.echo(f"  Name: {project['name']}")
        click.echo(f"  Description: {project['description'] or 'N/A'}")
        click.echo(f"  Status: {project['status']}")
        click.echo(f"  Owner ID: {project['owner_id']}")
        click.echo(f"  Start date: {project['start_date'] or 'Not set'}")
        click.echo(f"  End date: {project['end_date'] or 'Not set'}")
        click.echo(f"  Members: {len(project['members'])}")
    else:
        click.echo(f"❌ {result.message}")


@projects.command()
@click.option('--status', help='Filter by status')
@click.option('--owner-id', type=int, help='Filter by owner')
def list(status, owner_id):
    """List projects."""
    service = ProjectService()
    result = service.list_projects(status=status, owner_id=owner_id)
    
    if result.success:
        projects = result.data
        if not projects:
            click.echo("No projects found.")
            return
        
        click.echo(f"📁 Projects ({len(projects)}):")
        for project in projects:
            status_emoji = {
                'active': '🟢',
                'completed': '✅',
                'on_hold': '⏸️',
                'cancelled': '❌'
            }.get(project['status'], '❓')
            
            click.echo(f"  {status_emoji} {project['id']}: {project['name']} ({project['status']})")
    else:
        click.echo(f"❌ {result.message}")


@cli.command()
def info():
    """Show application information."""
    click.echo(f"🚀 {Config.APP_NAME} v{Config.APP_VERSION}")
    click.echo(f"📅 Started at: {format_timestamp()}")
    click.echo(f"🔧 Debug mode: {'Enabled' if Config.DEBUG else 'Disabled'}")
    click.echo(f"🌐 API Base URL: {Config.API_BASE_URL}")
    click.echo(f"⏱️  API Timeout: {Config.API_TIMEOUT}s")
    click.echo(f"📝 Log Level: {Config.LOG_LEVEL}")


@cli.command()
def demo():
    """Run a demonstration of the application."""
    click.echo("🎭 Running Demo3 demonstration...")
    
    # Create services
    user_service = UserService()
    task_service = TaskService()
    project_service = ProjectService()
    
    # Create demo users
    click.echo("\n👥 Creating demo users...")
    user1 = user_service.create_user("Alice Johnson", "alice@example.com")
    user2 = user_service.create_user("Bob Smith", "bob@example.com")
    
    if user1.success and user2.success:
        user1_id = user1.data['id']
        user2_id = user2.data['id']
        click.echo(f"✅ Created users: Alice (ID: {user1_id}), Bob (ID: {user2_id})")
        
        # Create demo project
        click.echo("\n📁 Creating demo project...")
        project = project_service.create_project(
            "Website Redesign",
            owner_id=user1_id,
            description="Redesign company website with modern UI/UX"
        )
        
        if project.success:
            project_id = project.data['id']
            click.echo(f"✅ Created project: Website Redesign (ID: {project_id})")
            
            # Create demo tasks
            click.echo("\n📋 Creating demo tasks...")
            task1 = task_service.create_task(
                "Design Homepage",
                created_by=user1_id,
                assigned_to=user2_id,
                priority="high",
                description="Create new homepage design mockups"
            )
            
            task2 = task_service.create_task(
                "Implement Navigation",
                created_by=user1_id,
                assigned_to=user1_id,
                priority="medium",
                description="Build responsive navigation component"
            )
            
            if task1.success and task2.success:
                click.echo(f"✅ Created tasks: Design Homepage (ID: {task1.data['id']}), Implement Navigation (ID: {task2.data['id']})")
                
                # List everything
                click.echo("\n📊 Current state:")
                users_result = user_service.list_users()
                tasks_result = task_service.list_tasks()
                projects_result = project_service.list_projects()
                
                if users_result.success:
                    click.echo(f"👥 Users: {len(users_result.data)}")
                if tasks_result.success:
                    click.echo(f"📋 Tasks: {len(tasks_result.data)}")
                if projects_result.success:
                    click.echo(f"📁 Projects: {len(projects_result.data)}")
                
                click.echo("\n🎉 Demo completed successfully!")
            else:
                click.echo("❌ Failed to create demo tasks")
        else:
            click.echo("❌ Failed to create demo project")
    else:
        click.echo("❌ Failed to create demo users")


if __name__ == '__main__':
    cli()