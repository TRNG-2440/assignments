from datetime import datetime, timedelta
from uuid import UUID, uuid4


class Event:
    """Represents a single bookable event with timing and host details."""

    def __init__(
        self,
        event_name: str,
        host_name: str,
        start_datetime: datetime,
        duration_in_minutes: int,
    ) -> None:
        """Initialize a new event.

        Args:
            booking_id: The unique, auto-generated identifier for this booking.
            event_name: The human-readable name of the event.
            host_name: The name of the person hosting the event.
            start_datetime: The datetime at which the event begins.
            duration_in_minutes: The length of the event, in minutes.
        """
        self.booking_id: UUID = uuid4()
        self.event_name: str = event_name
        self.host_name: str = host_name
        self.start_datetime: datetime = start_datetime
        self.duration_in_minutes: int = duration_in_minutes

    @property
    def end_datetime(self) -> datetime:
        """The datetime at which the event ends."""
        return self.start_datetime + timedelta(minutes=self.duration_in_minutes)

    def display_event_details(self) -> None:
        print("============================")
        print(f"Booking id: {self.booking_id}")
        print(f"Event: {self.event_name}")
        print(f"Host name: {self.host_name}")
        print(f"When: {self.start_datetime}")
        print("============================")
