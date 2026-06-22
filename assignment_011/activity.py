from enum import Enum

class Activity(str, Enum):
    STARTING = "starting"
    PLANTING = "planting"
    HARVESTING = "harvesting"
    MAINTENANCE = "maintenance"
    OBSERVATION = "observation"