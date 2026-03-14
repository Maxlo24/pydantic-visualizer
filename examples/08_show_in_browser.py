"""
Show in Browser Example
=======================

This example demonstrates the show() function that opens diagrams directly
in your web browser without saving intermediate files.

It shows:
- Opening diagrams directly in the browser
- No need to manually save HTML files
- Temporary file handling
- Quick visualization for development and testing
"""

from enum import Enum

from pydantic import BaseModel, Field

from pydantic_visualizer import PydanticVisualizer


# Define example models
class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Product(BaseModel):
    """Product in an order."""
    name: str = Field(description="Product name")
    sku: str = Field(description="Stock keeping unit")
    price: float = Field(description="Unit price")
    quantity: int = Field(description="Quantity ordered")


class ShippingAddress(BaseModel):
    """Shipping address information."""
    street: str = Field(description="Street address")
    city: str = Field(description="City")
    state: str = Field(description="State/Province")
    postal_code: str = Field(description="Postal/ZIP code")
    country: str = Field(description="Country")


class Customer(BaseModel):
    """Customer information."""
    name: str = Field(description="Customer full name")
    email: str = Field(description="Email address")
    phone: str | None = Field(None, description="Phone number (optional)")


class Order(BaseModel):
    """
    Complete order model.
    
    Represents a customer order with products, shipping, and status tracking.
    """
    order_id: str = Field(description="Unique order identifier")
    customer: Customer = Field(description="Customer who placed the order")
    products: list[Product] = Field(description="List of ordered products")
    shipping_address: ShippingAddress = Field(description="Where to ship the order")
    status: OrderStatus = Field(description="Current order status")
    total_amount: float = Field(description="Total order amount in USD")
    notes: str | None = Field(None, description="Additional order notes")


def main():
    print("=" * 60)
    print("SHOW IN BROWSER EXAMPLE")
    print("=" * 60)
    print()

    # Create a visualizer instance
    visualizer = PydanticVisualizer()
    visualizer.set_datamodel(Order)

    print("Opening diagram in your default web browser...")
    print()
    print("Features of the show() method:")
    print("  ✓ No intermediate files saved")
    print("  ✓ Opens directly in browser")
    print("  ✓ Temporary file auto-cleanup")
    print("  ✓ Perfect for quick visualization")
    print("  ✓ Great for development and testing")
    print()

    # Example 1: Show everything (default)
    print("1. Opening complete diagram (diagram + enums + descriptions)...")
    visualizer.show()
    print("   ✓ Browser should open with the full diagram")
    print()

    input("Press Enter to continue to the next example...")
    print()

    # Example 2: Show only the diagram
    print("2. Opening diagram only (no enums or descriptions)...")
    visualizer.show(
        include_diagram=True,
        include_enums=False,
        include_description=False
    )
    print("   ✓ Browser should open with just the diagram")
    print()

    input("Press Enter to continue to the next example...")
    print()

    # Example 3: Show diagram with descriptions but no enums
    print("3. Opening diagram with descriptions (no enum tables)...")
    visualizer.show(
        include_diagram=True,
        include_enums=False,
        include_description=True
    )
    print("   ✓ Browser should open with diagram and descriptions")
    print()

    print("=" * 60)
    print("COMPARISON: show() vs save_html()")
    print("=" * 60)
    print()
    print("show():")
    print("  • Quick visualization")
    print("  • No files to manage")
    print("  • Perfect for development")
    print("  • Temporary file auto-cleanup")
    print()
    print("save_html():")
    print("  • Permanent file")
    print("  • Can be shared")
    print("  • Version control friendly")
    print("  • Documentation purposes")
    print()

    print("=" * 60)
    print("TIP: Use show() during development, save_html() for docs!")
    print("=" * 60)


if __name__ == "__main__":
    main()


