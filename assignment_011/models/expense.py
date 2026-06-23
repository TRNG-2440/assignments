from enum import StrEnum


class ExpenseCategory(StrEnum):
    HOUSING = "housing"
    ENTERTAINMENT = "entertainment"
    TRANSPORT = "transport"
    MEDICAL = "medical"
    DEBT = "debt"
    INSURANCE = "insurance"
    FOOD = "food"
    HOUSEHOLD_SUPPLIES = "household supplies"
    PERSONAL = "personal grooming"
    EDUCATION = "education"
    OTHER = "other"
