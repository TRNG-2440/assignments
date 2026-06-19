"""
Endpoint definitions.
"""
# dependencies
from fastapi import APIRouter, Depends
from auth import get_current_user

# API data is of personal nature for each user
# apply authentication to all routes present
