"""
Complex Relationships Example
==============================

This example demonstrates how PydanticVisualizer handles complex model relationships.
It shows:
- Self-referencing models (recursive relationships)
- Multiple levels of nesting
- Lists of nested models
- Optional relationships
- Mixed relationship types in one diagram
"""

from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field

from pydantic_visualizer import PydanticVisualizer


# Define complex models with various relationship types
class ProjectStatus(StrEnum):
    """Project status enumeration."""

    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Skill(BaseModel):
    """A skill that a team member can have."""

    name: str = Field(description="Skill name")
    level: int = Field(description="Proficiency level (1-5)", ge=1, le=5)


class TeamMember(BaseModel):
    """Team member with skills and optional manager (self-referencing)."""

    name: str = Field(description="Team member name")
    email: str = Field(description="Email address")
    role: str = Field(description="Job role")
    skills: list[Skill] = Field(default_factory=list, description="List of skills")
    manager: Optional["TeamMember"] = Field(None, description="Direct manager (optional)")


class Task(BaseModel):
    """A task within a project."""

    title: str = Field(description="Task title")
    description: str = Field(description="Task description")
    assigned_to: TeamMember | None = Field(None, description="Assigned team member")
    estimated_hours: float = Field(description="Estimated hours to complete")
    completed: bool = Field(default=False, description="Completion status")


class Milestone(BaseModel):
    """Project milestone with associated tasks."""

    name: str = Field(description="Milestone name")
    description: str = Field(description="Milestone description")
    tasks: list[Task] = Field(default_factory=list, description="Tasks in this milestone")
    due_date: str = Field(description="Due date (ISO format)")


class Project(BaseModel):
    """
    Main project model with complex nested relationships.

    This model demonstrates:
    - Enum fields (status)
    - List of nested models (team, milestones)
    - Optional nested model (lead)
    - Multiple levels of nesting (Project -> Milestone -> Task -> TeamMember -> Skill)
    """

    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    status: ProjectStatus = Field(description="Current project status")
    team: list[TeamMember] = Field(default_factory=list, description="Project team members")
    lead: TeamMember | None = Field(None, description="Project lead (optional)")
    milestones: list[Milestone] = Field(default_factory=list, description="Project milestones")
    budget: float = Field(description="Project budget in USD")


def main():
    # Create a visualizer instance
    visualizer = PydanticVisualizer()

    # Set the complex data model
    visualizer.set_datamodel(Project)

    print("=" * 60)
    print("COMPLEX RELATIONSHIPS DIAGRAM")
    print("=" * 60)
    print()
    print("This diagram shows:")
    print("  • Self-referencing model (TeamMember.manager)")
    print("  • Multiple levels of nesting (4 levels deep)")
    print("  • Lists of nested models (team, milestones, tasks, skills)")
    print("  • Optional relationships (lead, assigned_to, manager)")
    print("  • Enum integration (ProjectStatus)")
    print()

    print("=" * 60)
    print("RELATIONSHIP LEGEND")
    print("=" * 60)
    print("Solid line (-->)  : Required relationship")
    print("Dashed line (..)  : Optional relationship")
    print("Arrow (>)         : Single object")
    print("Star (*)          : List/collection")
    print("Dashed border     : Optional nested model")
    print()

    # Print the Mermaid diagram code
    print("=" * 60)
    print("MERMAID DIAGRAM CODE")
    print("=" * 60)
    print(visualizer.mermaid)
    print()

    # Open in browser
    print("=" * 60)
    print("Opening complex diagram in browser...")
    print("=" * 60)
    visualizer.show()


if __name__ == "__main__":
    main()
