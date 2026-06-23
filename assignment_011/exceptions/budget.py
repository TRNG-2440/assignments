from datetime import date


class InvalidDateRangeError(Exception):
    def __init__(
        self, start_date: date, end_date: date, detail="Invalid date range!"
    ) -> None:
        self.detail = detail
        self.start_date = start_date
        self.end_date = end_date
