from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from Event import Event
from custom_exceptions import (
    BookingWindowExceededError,
    EventNotFoundError,
    InvalidBookingError,
    LateCancellationError,
    TimeSlotTakenError,
)

# Maximum number of days in advance a booking may be made
MAX_BOOKING_WINDOW_DAYS = 90

# Minimum number of hours before an event's start that a cancellation is allowed
CANCELLATION_WINDOW_HOURS = 24


class BookingSystem:
    def __init__(self) -> None:
        # Maps booking_id -> Event for fast lookup
        self.bookings: dict[UUID, Event] = {}

    def book_event(self, event: Event) -> None:
        if not event.event_name or not event.event_name.strip():
            raise InvalidBookingError("Event name is required!")

        if not event.host_name or not event.host_name.strip():
            raise InvalidBookingError("Event host name is required!")

        if event.start_datetime < datetime.now():
            raise InvalidBookingError("Start time cannot be in the past!")

        if event.duration_in_minutes <= 0:
            raise InvalidBookingError("Event duration must be positive!")

        if event.start_datetime > datetime.now() + timedelta(
            days=MAX_BOOKING_WINDOW_DAYS
        ):
            raise BookingWindowExceededError(
                event.start_datetime,
                datetime.now() + timedelta(days=MAX_BOOKING_WINDOW_DAYS),
            )

        self._check_booking_conflict(event)
        self.bookings[event.booking_id] = event
        print("Booking confirmed!")
        event.display_event_details()

    def _get_upcoming_events(self) -> List[Event]:
        bookings: List[Event] = list(self.bookings.values())
        return sorted(bookings, key=lambda event: event.start_datetime)

    def _check_booking_conflict(self, event: Event) -> None:
        bookings: List[Event] = self._get_upcoming_events()

        lo: int = 0
        hi: int = len(bookings) - 1
        while lo <= hi:
            mid: int = lo + (hi - lo) // 2
            booking: Event = bookings[mid]
            if (
                booking.start_datetime <= event.end_datetime
                and event.start_datetime <= booking.end_datetime
            ):
                # overlapping intervals
                raise TimeSlotTakenError(
                    booking.event_name, booking.start_datetime, booking.end_datetime
                )
            elif booking.end_datetime < event.start_datetime:
                lo = mid + 1
            else:
                hi = mid - 1

    def cancel_booking(self, booking_id: UUID) -> None:
        if booking_id not in self.bookings:
            raise EventNotFoundError(booking_id)

        booking: Event = self.bookings[booking_id]
        cancellation_deadline: datetime = booking.start_datetime - timedelta(
            hours=CANCELLATION_WINDOW_HOURS
        )
        if cancellation_deadline < datetime.now():
            raise LateCancellationError(
                booking.event_name, booking.start_datetime, cancellation_deadline
            )
        del self.bookings[booking_id]
        print(f"Cancelled event for booking id: {booking_id} successfully!")
