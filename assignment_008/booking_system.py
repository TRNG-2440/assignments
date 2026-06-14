
from datetime import datetime, timedelta
from exceptions import LateCancellationError, InvalidBookingError, BookingWindowExceededError, TimeSlotTakenError, EventNotFoundError
import itertools


class Event:
    """single bookable event."""

    _id_counter = itertools.count(1)

    def __init__(self, name, start_datetime, duration_minutes, host):
        self.booking_id = f"BKG-{next(Event._id_counter):06d}" #0 padded id
        self.name = name
        self.start_datetime = start_datetime
        self.duration_minutes = duration_minutes
        self.host = host

    @property
    def end_datetime(self):
        return self.start_datetime + timedelta(minutes=self.duration_minutes)

    def overlaps_with(self, other_start, other_end):
        return self.start_datetime < other_end and other_start < self.end_datetime

    def __str__(self):
        return (
            f"[{self.booking_id}]  "
            f"{self.start_datetime.strftime('%Y-%m-%d %H:%M')}  |  "
            f"{self.name} ({self.duration_minutes} min)  |  Host: {self.host}"
        )

class BookingSystem:
    """Manages creation, cancellation, and lookup of events."""

    MAX_BOOKING_WINDOW_DAYS = 90
    CANCELLATION_WINDOW_HOURS = 24

    def __init__(self):
        self.events = {}  # booking_id -> Event

    def _validate_new_booking(self, start_datetime, duration_minutes, name, host):
        now = datetime.now()

        if not name or not name.strip():
            raise InvalidBookingError("Event name is required and cannot be empty.")

        if not host or not host.strip():
            raise InvalidBookingError("Host name is required and cannot be empty.")

        if duration_minutes <= 0:
            raise InvalidBookingError(
                f"Invalid duration: {duration_minutes} minutes. "
                f"Duration must be a positive number of minutes."
            )

        if start_datetime < now:
            raise InvalidBookingError(
                f"Cannot book an event in the past "
                f"(requested: {start_datetime.strftime('%Y-%m-%d %H:%M')}, "
                f"current time: {now.strftime('%Y-%m-%d %H:%M')})."
            )

        max_allowed_date = now + timedelta(days=self.MAX_BOOKING_WINDOW_DAYS)
        if start_datetime > max_allowed_date:
            raise BookingWindowExceededError(start_datetime, max_allowed_date)

    def _check_for_conflicts(self, start_datetime, duration_minutes):
        new_end = start_datetime + timedelta(minutes=duration_minutes)
        for event in self.events.values():
            if event.start_datetime.date() == start_datetime.date():
                if event.overlaps_with(start_datetime, new_end):
                    raise TimeSlotTakenError(
                        event.name,
                        event.start_datetime,
                        event.end_datetime,
                        event.start_datetime,
                    )


    def book_event(self, name, host, start_datetime, duration_minutes):
        """Validate and create a new booking. Returns the created Event."""
        self._validate_new_booking(start_datetime, duration_minutes, name, host)
        self._check_for_conflicts(start_datetime, duration_minutes)

        event = Event(name, start_datetime, duration_minutes, host)
        self.events[event.booking_id] = event
        return event

    def cancel_booking(self, booking_id):
        event = self.get_booking(booking_id)

        deadline = event.start_datetime - timedelta(hours=self.CANCELLATION_WINDOW_HOURS)
        if datetime.now() > deadline:
            raise LateCancellationError(event.name, event.start_datetime, deadline)

        del self.events[booking_id]
        return event

    def get_booking(self, booking_id):
        if booking_id not in self.events:
            raise EventNotFoundError(booking_id)
        return self.events[booking_id]

    def list_upcoming_bookings(self):
        now = datetime.now()
        upcoming = [e for e in self.events.values() if e.start_datetime >= now]
        return sorted(upcoming, key=lambda e: e.start_datetime)

    def list_bookings_by_host(self, host_name):
        target = host_name.strip().lower()
        matches = [e for e in self.events.values() if e.host.strip().lower() == target]
        return sorted(matches, key=lambda e: e.start_datetime)


