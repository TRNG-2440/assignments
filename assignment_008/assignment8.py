"""
Assignment 8
"""
from datetime import datetime, time


class BookingError(Exception):
    def __init__(self, message: str):
        self.message = message

class TimeSlotTakenError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class BookingWindowExceededError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class LateCancelledError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class EventNotFoundError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidBookingError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class Event:
    def __init__(self,
                 event_name: str,
                 host_name: str,
                 booking_id: str,
                 start: datetime,
                 duration_min: float,
                 ):
        self._event_name: str = event_name
        self._host_name: str = host_name
        self._booking_id: str = booking_id
        self._start: datetime = start
        self._duration_min: float = duration_min

class BookingSystem:

    def __init__(self):
        self._events: dict[str, Event] = {}
        self._advance_bookings_days: float = 90
        self._min_cancellation_time_days: float = 24

        self._next_id = 0

    def _generate_id(self) -> str:
        self._next_id += 1
        return "BK_" + str(self._next_id)

    def book_event(self, event: Event) -> Event:
        #TODO
        pass

    def cancel_event(self, booking_id: str) -> Event:
        #TODO
        pass

    def view_booking(self, booking_id: str) -> Event:
        #TODO
        pass

    def list_bookings(self) -> list[Event]:
        #TODO
        pass

    def books_by_host(self, host_id: str) -> list[Event]:
        #TODO
        pass

