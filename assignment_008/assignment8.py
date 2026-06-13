"""
Assignment 8
"""
from datetime import datetime, time, date, timedelta

from assignments.shared.menu import Menu


class BookingError(Exception):
    def __init__(self, message: str):
        self.message = message

class TimeSlotTakenError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class BookingWindowExceededError(BookingError):
    def __init__(self, message: str):
        super().__init__(message)

class LateCanceliationError(BookingError):
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

    def display_str(self) -> str:
        return (f"Name: {self._event_name}"
                f"\nHost: {self._host_name}"
                f"\nBooking ID: {self._booking_id}"
                f"\nStart: {self._start}"
                f"\nDuration: {self._duration_min} (min)"
                )

    def get_event_name(self) -> str:
        return self._event_name

    def get_host_name(self):
        return self._host_name

    def get_start(self) -> datetime:
        return self._start

    def get_duration(self) -> float:
        return self._duration_min

class BookingSystem:

    def __init__(self):
        self._events: dict[str, Event] = {}
        self._advance_bookings_days: float = 90
        self._min_cancellation_time_days: float = 13

        self._next_id = 0

    def _generate_id(self) -> str:
        self._next_id += 1
        return "BK_" + str(self._next_id)

    def book_event(self, event_name: str, host_name: str, start: datetime, duration_min: float) -> Event:
        if start < datetime.now():
            raise InvalidBookingError(f"Start time {start} is in the past and invalid")

        if duration_min <= 0:
            raise InvalidBookingError(f"Duration min {duration_min} is invalid")

        if event_name == "":
            raise InvalidBookingError("Event name is invalid")

        if host_name == "":
            raise InvalidBookingError("Host name is invalid")

        if start - datetime.now() > timedelta(days=self._advance_bookings_days):
            raise BookingWindowExceededError(f"Start time {start} is too fare in advance. Maximum booking: {self._advance_bookings_days} days")

        end: datetime = start + timedelta(minutes=duration_min)
        for event in self._events.values():
            event_start: datetime = event.get_start()
            event_end: datetime = event_start + timedelta(minutes=duration_min)

            #TODO double check logic
            if start < event_start < end or start < event_end < end:
                raise TimeSlotTakenError(f"Conflict for an event starting at {start} and running {duration_min} minutes. "
                                         f"Conflicts with {event.get_event_name()} at {event_start} running for {event.get_duration()} minutes")

        new_id: str = self._generate_id()
        new_event: Event = Event(event_name, host_name, new_id, start, duration_min)
        self._events[new_id] = new_event
        return new_event


    def cancel_event(self, booking_id: str) -> Event:
        if booking_id not in self._events:
            raise EventNotFoundError(f"Booking ID {booking_id} not found")
        event: Event = self._events[booking_id]

        if datetime.now() + timedelta(days=self._min_cancellation_time_days) > event.get_start():
            raise LateCanceliationError(f"Cannot cancel {event.get_event_name()}, it starts at {event.get_start()} which is less than the minimum cancel time of {self._min_cancellation_time_days} day")

        del self._events[booking_id]
        return event

    def view_booking(self, booking_id: str) -> Event:
        if booking_id not in self._events:
            raise EventNotFoundError(f"Booking ID {booking_id} not found")
        return self._events[booking_id]

    def list_bookings(self) -> list[Event]:
        return sorted(self._events.values(), key=lambda event: event.get_start())

    def bookings_by_host(self, host_name: str) -> list[Event]:
        return [event for event in self.list_bookings() if host_name == event.get_host_name()]


class BookingMenu(Menu):

    def __init__(self, booking_system:BookingSystem):
        super().__init__({
            "Book an event": self.book_event,
            "Cancel a booking": self.cancel_booking,
            "View a booking": self.view_booking,
            "List upcoming bookings": self.list_bookings,
            "List bookings by host": self.list_bookings_by_host,
        }, add_quit=True)
        self.booking_system: BookingSystem = booking_system

    def book_event(self) -> None:
        event_name: str = Menu.get_str("Event Name: ")
        host_name: str = Menu.get_str("Host Name: ")
        start_date: date = Menu.get_date("Start Date (YYYY-MM-DD): ")
        start_time: time = Menu.get_time("Start Time (HH:MM): ")
        duration_min: float = Menu.get_positive_float("Duration (minutes): ")

        start: datetime = datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute)

        try:
            event: Event = self.booking_system.book_event(event_name, host_name, start, duration_min)
            print("Booked Event!")
            print(event.display_str())
        except BookingError as e:
            print(f"Error: {e.message}")

    def cancel_booking(self) -> None:
        print("Cancel Booking")
        event_id: str = Menu.get_str("Booking ID: ")
        try:
            event: Event = self.booking_system.cancel_event(event_id)
            print("Canceled Event:")
            print(event.display_str())
        except BookingError as e:
            print(f"Error: {e.message}")

        pass

    def view_booking(self) -> None:
        print("View Booking")
        event_id: str = Menu.get_str("Booking ID: ")
        try:
            event: Event = self.booking_system.view_booking(event_id)
            print(event.display_str())
        except BookingError as e:
            print(f"Error: {e.message}")

    def list_bookings(self) -> None:
        if len(self.booking_system.list_bookings()) == 0:
            print("No Bookings")
            return

        print(Menu.MINOR_DIVIDER)

        for event in self.booking_system.list_bookings():
            print(event.display_str())
            print(Menu.MINOR_DIVIDER)

    def list_bookings_by_host(self) -> None:
        host_name: str = Menu.get_str("Host Name: ")
        results: list[Event] = self.booking_system.bookings_by_host(host_name)
        if len(results) == 0:
            print(f"No Bookings found for {host_name}")
            return

        print(Menu.MINOR_DIVIDER)

        for event in results:
            print(event.display_str())
            print(Menu.MINOR_DIVIDER)



if __name__ == "__main__":
    system: BookingSystem = BookingSystem()
    BookingMenu(system).start()
