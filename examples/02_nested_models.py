"""
Nested Models Example
=====================

This example demonstrates how PydanticVisualizer handles nested Pydantic models.
It shows:
- Models containing other models as fields
- Optional nested models
- How relationships are automatically detected and visualized
"""


from pydantic import BaseModel

from pydantic_visualizer import PydanticVisualizer


# Define nested models
class Address(BaseModel):
    """Address information."""
    street: str
    city: str
    country: str
    postal_code: str


class Company(BaseModel):
    """Company information."""
    name: str
    industry: str
    address: Address


class User(BaseModel):
    """User with nested address and optional company."""
    name: str
    email: str
    age: int
    address: Address
    company: Company | None = None


def main():
    # Create a visualizer instance
    visualizer = PydanticVisualizer()

    # Set the data model - it will automatically detect nested models
    visualizer.set_datamodel(User)

    # Print the Mermaid diagram code
    print("=" * 60)
    print("NESTED MODELS DIAGRAM CODE")
    print("=" * 60)
    print(visualizer.mermaid)
    print()

    # The diagram will show:
    # - User class with its fields
    # - Address class (used by both User and Company)
    # - Company class (optional relationship)
    # - Relationships between them
    # - Dashed lines for optional relationships

    print("=" * 60)
    print("Opening diagram in browser...")
    print("=" * 60)
    visualizer.show()


if __name__ == "__main__":
    main()


