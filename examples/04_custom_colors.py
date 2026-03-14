"""
Custom Colors Example
=====================

This example demonstrates how to customize the colors used in the diagram.
It shows:
- Setting custom colors for objects, lists, and enums
- How different colors help distinguish element types
- Using hex color codes for customization
"""

from enum import Enum

from pydantic import BaseModel

from pydantic_visualizer import PydanticVisualizer


# Define models
class Category(str, Enum):
    """Product category."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"


class Tag(BaseModel):
    """Product tag."""
    name: str
    color: str


class Product(BaseModel):
    """Product with tags and category."""
    name: str
    price: float
    category: Category
    tags: list[Tag]


def main():
    print("=" * 60)
    print("CUSTOM COLORS EXAMPLE")
    print("=" * 60)
    print()

    # Create visualizer with grayscale colors
    print("Monochrome theme.")
    visualizer_mono = PydanticVisualizer(
        object_color="#F5F5F5",  # Light gray for objects
        list_color="#E0E0E0",     # Medium gray for lists
        enum_color="#BDBDBD",     # Darker gray for enums
        html_color="#90CAF9"      # Darker blue for html

    )
    visualizer_mono.set_datamodel(Product)
    visualizer_mono.show()
    print("   ✓ Opened in browser with monochrome theme")

    print("=" * 60)
    print("Compare the different color themes in your browser!")
    print("=" * 60)


if __name__ == "__main__":
    main()


