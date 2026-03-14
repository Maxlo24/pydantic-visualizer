"""
Example: Adding Multiple Models with Overlapping Submodels

This example demonstrates how to use the add_model() method to visualize
multiple independent models in the same diagram. It shows how models that
share common submodels are handled correctly without duplication.
"""

from pydantic import BaseModel, Field
from pydantic_visualizer import PydanticVisualizer
from enum import StrEnum


# Shared submodel used by multiple models
class Address(BaseModel):
    """Address information"""

    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")
    postal_code: str = Field(description="Postal/ZIP code")


class ContactInfo(BaseModel):
    """Contact information"""

    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    address: Address = Field(description="Physical address")


# First main model - User
class User(BaseModel):
    """User account information"""

    id: int = Field(description="Unique user identifier")
    username: str = Field(description="Username for login")
    full_name: str = Field(description="User's full name")
    contact: ContactInfo = Field(description="User contact details")


# Second main model - Company (also uses Address)
class Company(BaseModel):
    """Company information"""

    name: str = Field(description="Company name")
    registration_number: str = Field(description="Business registration number")
    headquarters: Address = Field(description="Company headquarters address")
    billing_address: Address = Field(description="Billing address")


# Third main model - Store (uses both Address and ContactInfo)
class Store(BaseModel):
    """Physical store location"""

    store_id: int = Field(description="Store identifier")
    name: str = Field(description="Store name")
    location: Address = Field(description="Store location")
    contact: ContactInfo = Field(description="Store contact information")


class Status(StrEnum):
    """Account status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class Product(BaseModel):
    """A simple product model."""

    name: str
    price: float
    in_stock: bool
    description: str
    status: Status


def main():
    # Create visualizer
    visualizer = PydanticVisualizer()

    # Set the first model
    visualizer.set_datamodel(User)
    print(f"After set_datamodel(User): Title = '{visualizer.title}'")

    # Add the second model (shares Address with User through ContactInfo)
    visualizer.add_model(Company)
    print(f"After add_model(Company): Title = '{visualizer.title}'")

    # Add the third model (shares both Address and ContactInfo)
    visualizer.add_model(Store)
    print(f"After add_model(Store): Title = '{visualizer.title}'")

    visualizer.add_model(Product)
    print(f"After add_model(Product): Title = '{visualizer.title}'")

    print("\n" + "=" * 60)
    print("Note: Address and ContactInfo appear only once in the diagram")
    print("even though they are used by multiple models!")
    print("=" * 60)

    # Display in browser
    print("\n✓ Opening diagram in browser...")
    visualizer.show()


if __name__ == "__main__":
    main()

# Made with Bob
