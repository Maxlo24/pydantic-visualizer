"""
Basic Usage Example
===================

This example demonstrates the most basic usage of PydanticVisualizer.
It shows how to:
- Define a simple Pydantic model
- Create a visualizer instance
- Set the data model
- Visualize it in the browser
"""

from pydantic import BaseModel

from pydantic_visualizer import PydanticVisualizer


# Define a simple Pydantic model
class Product(BaseModel):
    """A simple product model."""

    name: str
    price: float
    in_stock: bool
    description: str


def main():
    # Create a visualizer instance
    visualizer = PydanticVisualizer()

    # Set the data model to visualize
    visualizer.set_datamodel(Product)

    # Print the Mermaid diagram code
    print("=" * 60)
    print("MERMAID DIAGRAM CODE")
    print("=" * 60)
    print(visualizer.mermaid)
    print()

    # Open the diagram in your browser
    print("=" * 60)
    print("Opening diagram in browser...")
    print("=" * 60)
    visualizer.show()


if __name__ == "__main__":
    main()
