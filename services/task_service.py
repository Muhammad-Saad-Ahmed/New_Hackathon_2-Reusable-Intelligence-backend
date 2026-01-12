"""
Service layer for managing Task business logic in the backend.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.database import Task, User
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    Service class for managing Task business logic.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the service with a database session.

        Args:
            db_session: The database session to use
        """
        self.db_session = db_session

    def create_task(self, user_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task for a user.

        Args:
            user_id: The ID of the user creating the task
            task_data: The task data to create

        Returns:
            The created Task object
        """
        # Create a new Task instance from the provided data
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            priority=task_data.priority
        )

        # Add the task to the session and commit
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)

        return task

    def get_task_by_id(self, user_id: str, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task for a user by its ID.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found and belongs to the user, None otherwise
        """
        # Query for the task that belongs to the specified user
        task = self.db_session.query(Task).filter(
            and_(Task.user_id == user_id, Task.id == task_id)
        ).first()

        return task

    def get_tasks_by_user(self, user_id: str,
                         status: Optional[str] = None,
                         priority: Optional[str] = None) -> List[Task]:
        """
        Retrieve all tasks for a specific user with optional filters.

        Args:
            user_id: The ID of the user
            status: Optional filter for task status ("completed", "incomplete", "all")
            priority: Optional filter for task priority ("high", "medium", "low")

        Returns:
            A list of Task objects for the user
        """
        # Start with a base query for tasks belonging to the user
        query = self.db_session.query(Task).filter(Task.user_id == user_id)

        # Apply status filter if provided
        if status:
            if status == "completed":
                query = query.filter(Task.completed == True)
            elif status == "incomplete":
                query = query.filter(Task.completed == False)

        # Apply priority filter if provided
        if priority:
            query = query.filter(Task.priority == priority)

        # Execute the query and return results
        tasks = query.all()

        return tasks

    def update_task(self, user_id: str, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task for a user.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to update
            task_data: The updated task data

        Returns:
            The updated Task object if successful, None if task doesn't exist or doesn't belong to user
        """
        # Get the existing task
        task = self.get_task_by_id(user_id, task_id)
        if not task:
            return None

        # Update the task with provided data
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Commit the changes and refresh the task
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)

        return task

    def delete_task(self, user_id: str, task_id: str) -> bool:
        """
        Delete a specific task for a user.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist or didn't belong to user
        """
        # Get the existing task
        task = self.get_task_by_id(user_id, task_id)
        if not task:
            return False

        # Delete the task
        self.db_session.delete(task)
        self.db_session.commit()

        return True

    def toggle_task_completion(self, user_id: str, task_id: str, completed: bool) -> Optional[Task]:
        """
        Toggle the completion status of a specific task for a user.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to update
            completed: The new completion status

        Returns:
            The updated Task object if successful, None if task doesn't exist or doesn't belong to user
        """
        # Get the existing task
        task = self.get_task_by_id(user_id, task_id)
        if not task:
            return None

        # Update the completion status
        task.completed = completed

        # Commit the changes and refresh the task
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)

        return task