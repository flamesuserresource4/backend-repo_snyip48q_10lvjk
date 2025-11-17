"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# HVAC Maintenance Lead schema
class Lead(BaseModel):
    """
    Leads captured from the AC Maintenance marketing site.
    Collection name: "lead"
    """
    name: str = Field(..., description="Contact person full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    company: Optional[str] = Field(None, description="Company or property name")
    location: Optional[str] = Field(None, description="City/Area of the site")
    unit_types: Optional[List[str]] = Field(None, description="Split, Ducted, VRF, Package, etc.")
    units_count: Optional[int] = Field(None, ge=0, description="Approximate number of units")
    capacity_tonnage: Optional[str] = Field(None, description="Range like 1–50 TR/BtuH")
    preferred_interval: Optional[str] = Field(None, description="Monthly, Quarterly, Bi-Annual, Annual")
    pain_points: Optional[List[str]] = Field(None, description="Selected pain points")
    message: Optional[str] = Field(None, description="Additional context or notes")
