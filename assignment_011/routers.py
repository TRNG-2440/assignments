"""
Endpoint definitions.
"""
# dependencies
from fastapi import APIRouter, Depends

# API data is of personal nature for each user
# apply authentication to all routes present