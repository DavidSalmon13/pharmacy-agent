from pydantic import BaseModel
from dataclasses import dataclass
from typing import List

"""
Data models used by the pharmacy agent.

These classes define the structure of medications, stock records,
prescription requirements, and users in the synthetic database.
"""
# @dataclass
class Medication(BaseModel):
    name: str
    active_ingredient: str
    dosage_text: str
    prescription_required: bool

@dataclass
class Stock(BaseModel):
    name: str
    quantity: int

@dataclass
class Prescription(BaseModel):
    name: str
    required: bool

@dataclass
class User:
    name: str
    email: str
    age: int
    medications: List[str]  # List of medication names the user has been