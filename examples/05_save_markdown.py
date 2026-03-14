"""
Save Markdown Example
=====================

This example demonstrates how to save diagrams as Markdown files.
It shows:
- Saving to a markdown file
- Controlling what to include (diagram, enums, descriptions)
- Specifying output folder
- Automatic filename generation
"""

from enum import StrEnum

from pydantic import BaseModel, Field

from pydantic_visualizer import PydanticVisualizer


# Define models
class Priority(StrEnum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Comment(BaseModel):
    """Comment on a task."""

    author: str = Field(description="Comment author")
    text: str = Field(description="Comment text")
    timestamp: str = Field(description="When the comment was made")


class Task(BaseModel):
    """Task model with priority and comments."""

    title: str = Field(description="Task title")
    description: str = Field(description="Detailed task description")
    priority: Priority = Field(description="Task priority level")
    completed: bool = Field(default=False, description="Whether task is completed")
    comments: list[Comment] = Field(default_factory=list, description="Task comments")


def main():
    # Create a visualizer instance
    visualizer = PydanticVisualizer()
    visualizer.set_datamodel(Task)

    print("Saving markdown files with different options...")
    print()

    # Example 1: Save everything (default)
    print("1. Saving complete markdown (diagram + enums + descriptions)...")
    visualizer.save_markdown(
        output_folder="./examples/output",
        include_diagram=True,
        include_enums=True,
        include_description=True,
    )
    print("   ✓ Saved to: ./output/employee_mermaid.md")
    print()


if __name__ == "__main__":
    main()
