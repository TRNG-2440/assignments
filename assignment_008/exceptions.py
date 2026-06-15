class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start, end):
        super().__init__(
            f'Time slot unavailable — "{event_name}" is already scheduled from {start} to {end}.'
        )


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_date):
        super().__init__(
            f"Requested date {requested_date} exceeds maximum booking window. "
            f"Latest allowed: {max_date}."
        )


class LateCancellationError(BookingError):
    def __init__(self, event_name, event_time, deadline):
        super().__init__(
            f'Cannot cancel "{event_name}" — event starts at {event_time}. '
            f"Cancellation deadline passed (must cancel before {deadline})."
        )


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        super().__init__(f"Booking ID {booking_id} not found.")


class InvalidBookingError(BookingError):
    def __init__(self, message):
        super().__init__(message)