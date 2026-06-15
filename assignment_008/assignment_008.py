# dependencies
from datetime import datetime, timedelta

# base exception class for all booking related errors
class BookingError(Exception):
    pass

class TimeSlotTakenError(BookingError):
    def __init__(self, event_name: str, start: datetime, end: datetime) -> None:
        self.event_name = event_name
        self.start = start
        self.end = end
        message = (
            f'Time slot unavailable — "{event_name}" is already scheduled from '
            f'{start.strftime("%H:%M")} to {end.strftime("%H:%M")} on {start.strftime("%Y-%m-%d")}.'
        )
        super().__init__(message)

class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, latest_allowed) -> None:
        self.requested_date = requested_date
        self.latest_allowed = latest_allowed
        message = (
            f"Requested date {requested_date} exceeds the maximum booking window. "
            f"Bookings may not be made more than 90 days in advance "
            f"(latest allowed: {latest_allowed})."
        )
        super().__init__(message)

class LateCancellationError(BookingError):
    def __init__(self, event_name: str, start: datetime, deadline: datetime) -> None:
        self.event_name = event_name
        self.start = start
        self.deadline = deadline
        message = (
            f'Cannot cancel "{event_name}" — the event starts at {start.strftime("%H:%M")} '
            f'on {start.strftime("%Y-%m-%d")} and the cancellation deadline has passed '
            f"(cancellations must be made at least 24 hours in advance)."
        )
        super().__init__(message)

class EventNotFoundError(BookingError):
    def __init__(self, booking_id: str) -> None:
        self.booking_id = booking_id
        super().__init__(f"No booking found with ID {booking_id}.")

class InvalidBookingError(BookingError):
    pass

# Event class
class Event:
    def __init__(self, booking_id: str, name: str, start: datetime, duration: int, host: str) -> None:
        self.booking_id = booking_id
        self.name = name
        self.start = start
        self.duration = duration
        self.host = host

    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=self.duration)

    def details(self) -> None:
        print(
            f"  [{self.booking_id}]  {self.start.strftime('%Y-%m-%d %H:%M')}  |  "
            f"{self.name} ({self.duration} min)  |  Host: {self.host}"
        )

# BookingSystem class
class BookingSystem:
    MAX_WINDOW_DAYS = 90
    CANCELLATION_HOURS = 24

    def __init__(self) -> None:
        self.events = []
        # unique booking id counter, increasing by 1
        self.next_id = 1

    def generate_id(self) -> str:
        booking_id = f"BKG-{self.next_id:04d}"
        self.next_id += 1
        return booking_id

    def find_event(self, booking_id: str) -> Event:
        for event in self.events:
            if event.booking_id == booking_id:
                return event
        raise EventNotFoundError(booking_id)

    def book_event(self, name: str, start: datetime, duration: int, host: str) -> Event:
        if not name:
            raise InvalidBookingError("Event name is required.")
        if not host:
            raise InvalidBookingError("Host name is required.")
        if duration <= 0:
            raise InvalidBookingError("Duration must be a positive number of minutes.")

        now = datetime.now()
        if start < now:
            raise InvalidBookingError("Booking start time may not be in the past.")

        latest_allowed = (now + timedelta(days=self.MAX_WINDOW_DAYS)).date()
        if start.date() > latest_allowed:
            raise BookingWindowExceededError(start.date(), latest_allowed)

        new_end = start + timedelta(minutes=duration)
        for event in self.events:
            # overlap occurs when the two time ranges intersect
            if start < event.end and event.start < new_end:
                raise TimeSlotTakenError(event.name, event.start, event.end)

        event = Event(self.generate_id(), name, start, duration, host)
        self.events.append(event)
        return event

    def cancel_booking(self, booking_id: str) -> Event:
        event = self.find_event(booking_id)
        deadline = event.start - timedelta(hours=self.CANCELLATION_HOURS)
        if datetime.now() > deadline:
            raise LateCancellationError(event.name, event.start, deadline)
        self.events.remove(event)
        return event

    def view_booking(self, booking_id: str) -> Event:
        return self.find_event(booking_id)

    def list_upcoming(self):
        now = datetime.now()
        upcoming = [event for event in self.events if event.start > now]
        return sorted(upcoming, key=lambda event: event.start)

    def list_by_host(self, host: str):
        host = host.lower()
        matches = [event for event in self.events if event.host.lower() == host]
        return sorted(matches, key=lambda event: event.start)

# helper input functions for the CLI
def prompt_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def prompt_menu(message: str, low: int, high: int) -> int:
    while True:
        choice = prompt_int(message)
        if low <= choice <= high:
            return choice
        print("Invalid option. Try again.")

def prompt_datetime(date_message: str, time_message: str) -> datetime:
    while True:
        date_value = input(date_message)
        time_value = input(time_message)
        try:
            return datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date/time. Please use YYYY-MM-DD for the date and HH:MM for the time.")

def print_confirmation(event: Event) -> None:
    print("\nBooking confirmed!")
    print(f"   Booking ID : {event.booking_id}")
    print(f"   Event      : {event.name}")
    print(f"   Host       : {event.host}")
    print(f"   When       : {event.start.strftime('%Y-%m-%d')} at "
          f"{event.start.strftime('%H:%M')} ({event.duration} min)")

# main menu loop
system = BookingSystem()

while True:
    print("\n" + "=" * 30)
    print("    Event Booking System")
    print("=" * 30, "\n")
    print("[1] Book an event")
    print("[2] Cancel a booking")
    print("[3] View a booking")
    print("[4] List upcoming bookings")
    print("[5] List bookings by host")
    print("[6] Quit")

    option = prompt_menu("> ", 1, 6)

    match option:
        case 1:  # book an event
            name = input("Event name: ")
            host = input("Host name: ")
            start = prompt_datetime("Start date (YYYY-MM-DD): ", "Start time (HH:MM): ")
            duration = prompt_int("Duration (minutes): ")
            try:
                event = system.book_event(name, start, duration, host)
                print_confirmation(event)
            except BookingError as e:
                print(f"\nBookingError: {e}")

        case 2:  # cancel a booking
            booking_id = input("Booking ID: ")
            try:
                event = system.cancel_booking(booking_id)
                print(f'\nBooking "{event.name}" ({event.booking_id}) cancelled.')
            except BookingError as e:
                print(f"\nBookingError: {e}")

        case 3:  # view a booking
            booking_id = input("Booking ID: ")
            try:
                event = system.view_booking(booking_id)
                print("\nBooking Details")
                print("-" * 30)
                event.details()
            except BookingError as e:
                print(f"\nBookingError: {e}")

        case 4:  # list upcoming bookings
            upcoming = system.list_upcoming()
            print("\nUpcoming Bookings")
            print("-" * 30)
            if not upcoming:
                print("No upcoming bookings.")
            else:
                for event in upcoming:
                    event.details()
                print("-" * 30)
                print(f"{len(upcoming)} upcoming booking(s) found.")

        case 5:  # list bookings by host
            host = input("Host name: ")
            matches = system.list_by_host(host)
            print(f"\nBookings for {host}")
            print("-" * 30)
            if not matches:
                print("No bookings found for that host.")
            else:
                for event in matches:
                    event.details()
                print("-" * 30)
                print(f"{len(matches)} booking(s) found.")

        case 6:  # quit
            print("Goodbye!")
            break
