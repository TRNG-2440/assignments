from enum import Enum

class Activity(str, Enum):
    STARTING = "Starting"
    PLANTING = "Planting"
    HARVESTING = "Harvesting"
    MAINTENANCE = "Maintenance"
    OBSERVATION = "Observation"