
class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, conflicting_event_name, conflict_start, conflict_end, date):
        self.conflicting_event_name = conflicting_event_name
        self.conflict_start = conflict_start
        self.conflict_end = conflict_end
        self.date = date
        message = (
            f'Time slot unavailable — "{conflicting_event_name}" is already '
            f'scheduled from {conflict_start.strftime("%H:%M")} to '
            f'{conflict_end.strftime("%H:%M")} on {date.strftime("%Y-%m-%d")}.'
        )
        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_allowed_date):
        self.requested_date = requested_date
        self.max_allowed_date = max_allowed_date
        message = (
            f'Requested date {requested_date.strftime("%Y-%m-%d")} exceeds the '
            f'maximum booking window. Bookings may not be made more than 90 days '
            f'in advance (latest allowed: {max_allowed_date.strftime("%Y-%m-%d")}).'
        )
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event_name, event_start, cancellation_deadline):
        self.event_name = event_name
        self.event_start = event_start
        self.cancellation_deadline = cancellation_deadline
        message = (
            f'Cannot cancel "{event_name}" — the event starts at '
            f'{event_start.strftime("%H:%M")} on {event_start.strftime("%Y-%m-%d")} '
            f'and the cancellation deadline has passed (cancellations must be made '
            f'at least 24 hours in advance; deadline was '
            f'{cancellation_deadline.strftime("%Y-%m-%d %H:%M")}).'
        )
        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        self.booking_id = booking_id
        message = f'No event found with booking ID "{booking_id}".'
        super().__init__(message)


class InvalidBookingError(BookingError):
    def __init__(self, message):
        super().__init__(message)

