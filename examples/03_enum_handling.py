"""
Enum Handling Example
=====================

This example demonstrates how PydanticVisualizer handles Enum types.
It shows:
- Using Enums in Pydantic models
- How Enums are visualized with special colors
- Enum value tables in the output
"""

from enum import Enum

from pydantic import BaseModel

from pydantic_visualizer import PydanticVisualizer


# Define Enums
class Role(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    MODERATOR = "moderator"


class Status(str, Enum):
    """Account status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class Priority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Define models using Enums
class User(BaseModel):
    """User model with role and status enums."""
    username: str
    email: str
    role: Role
    status: Status


class Task(BaseModel):
    """Task model with priority enum."""
    title: str
    description: str
    priority: Priority
    assigned_to: User


def main():
    # Create a visualizer instance
    visualizer = PydanticVisualizer()

    # Set the data model
    visualizer.set_datamodel(Task)

    # Print the Mermaid diagram code
    print("=" * 60)
    print("DIAGRAM WITH ENUMS - CODE")
    print("=" * 60)
    print(visualizer.mermaid)
    print()

    # Print enum tables - shows all enum values
    print("=" * 60)
    print("ENUM TABLES")
    print("=" * 60)
    print(visualizer.enum_markdown_tables)
    print()

    # Open the full diagram in browser
    print("=" * 60)
    print("Opening diagram with enums in browser...")
    print("=" * 60)
    visualizer.show()


if __name__ == "__main__":
    main()


