from datetime import date


class InvalidDateRangeError(Exception):
    def __init__(
        self, start_date: date, end_date: date, detail="Invalid date range!"
    ) -> None:
        self.detail = detail
        self.start_date = start_date
        self.end_date = end_date


class UnauthorizedAccessError(Exception):
    def __init__(
        self,
        user_id: str,
        resource: str,
        resource_id: str,
        detail="User is not authorized for access!",
    ) -> None:
        self.detail = detail
        self.user_id = user_id
        self.resource = resource
        self.resource_id = resource_id


class ResourceNotFoundError(Exception):
    def __init__(
        self,
        resource: str,
        resource_id: str,
        detail="Resource not found!",
    ) -> None:
        self.detail = detail
        self.resource = resource
        self.resource_id = resource_id
