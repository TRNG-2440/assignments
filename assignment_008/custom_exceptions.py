from datetime import date, datetime
from uuid import UUID


class BookingError(Exception):
    """Base class for all custom exceptions raised by the booking system.

    Catching `BookingError` allows a caller to handle any booking-related
    failure without needing to know about every specific subclass.
    """

    pass


class TimeSlotTakenError(BookingError):
    """Raised when a requested time slot overlaps with an existing booking."""

    def __init__(self, event_name: str, start: datetime, end: datetime) -> None:
        """Initialize the error with details of the conflicting event.

        Args:
            event_name: The name of the event already occupying
                the requested time slot.
            start: The start datetime of the conflicting event.
            end: The end datetime of the conflicting event.
        """

        super().__init__(
            f"Time slot unavailable - Event: {event_name} already booked from {start} to {end}!"
        )


class BookingWindowExceededError(BookingError):
    """Raised when a booking is requested too far in advance."""

    def __init__(self, requested_date: date, max_allowed_date: date) -> None:
        """Initialize the error with the requested and maximum allowed dates.

        Args:
            requested_date: The date the user attempted to book.
            max_allowed_date: The latest date a booking is currently permitted.
        """
        super().__init__(
            f"Booking Window Exceeded - {requested_date} > {max_allowed_date}"
        )


class LateCancellationError(BookingError):
    """Raised when cancellation for a booking is attempted too late."""

    def __init__(
        self, event_name: str, start: datetime, cancellation_deadline: datetime
    ) -> None:
        """Initialize the error with details of the event and deadline.

        Args:
            event_name: The name of the event the user tried to cancel.
            start: The scheduled start datetime of the event.
            cancellation_deadline: The latest datetime by which the event
                could have been cancelled without penalty.
        """
        super().__init__(
            f"Event: {event_name} starting at {start} cannot be cancelled! "
            f"The cancellation deadline was {cancellation_deadline}"
        )


class EventNotFoundError(BookingError):
    """Raised when a non-existent booking ID or event is searched."""

    def __init__(self, booking_id: UUID) -> None:
        """Initialize the error with the booking ID that was not found.

        Args:
            booking_id: The booking ID that could not be located.
        """
        super().__init__(f"Booking id: {booking_id} does not exist!")


class InvalidBookingError(BookingError):
    """Raised for general booking validation failures.

    Examples include a start time in the past, a non-positive duration,
    or a missing required field.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidInputError(ValueError):
    """Raised when user-provided CLI input cannot be converted to the expected type."""

    def __init__(self, *args: object) -> None:
        """Initialize the error.

        Args:
            *args: Arguments forwarded to `ValueError.__init__`, typically a
                descriptive error message.
        """
        super().__init__(*args)
