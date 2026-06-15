# Assignment 8 by Ariyan Shaikh

from datetime import datetime, timedelta
import random

# Custom Exceptions Hierarchy

class BookingError(Exception):
    """
    Base exception class that all other booking exceptions inherit from
    """
    pass

class TimeSlotTakenError(BookingError):
    """
    Raised when a requested time slot overlaps with an existing event
    """
    def __init__(self, conflict_name: str, start_time: datetime, end_time: datetime):
        date_str = start_time.strftime("%Y-%m-%d")
        start_str = start_time.strftime("%H:%M")
        end_str = end_time.strftime("%H:%M")
        super().__init__(
            f"Time slot unavailable — \"{conflict_name}\" is already scheduled from {start_str} to {end_str} on {date_str}."
        )

class BookingWindowExceededError(BookingError):
    """
    Raised when trying to book an event further than 90 days out
    """
    def __init__(self, requested_date: datetime, max_allowed_date: datetime):
        req_str = requested_date.strftime("%Y-%m-%d")
        max_str = max_allowed_date.strftime("%Y-%m-%d")
        super().__init__(
            f"Requested date {req_str} exceeds the maximum booking window. Bookings may not be made more than 90 days in advance (latest allowed: {max_str})."
        )

class LateCancellationError(BookingError):
    """
    Raised when trying to cancel an event less than 24 hours before it starts
    """
    def __init__(self, event_time: datetime, deadline_time: datetime):
        evt_str = event_time.strftime("%H:%M on %Y-%m-%d")
        super().__init__(
            f"Cannot cancel booking — the event starts at {evt_str} and the cancellation deadline has passed (cancellations must be made at least 24 hours in advance)."
        )

class EventNotFoundError(BookingError):
    """
    Raised when searching for a booking ID that does not exist
    """
    def __init__(self, booking_id: str):
        super().__init__(f"No booking found with ID: {booking_id}")

class InvalidBookingError(BookingError):
    """
    Raised for general validation errors like dates in the past or negative durations
    """
    pass


# Core Model and System Components

class Event:
    """
    Class to store details for a single event booking
    """
    def __init__(self, booking_id: str, name: str, start_time: datetime, duration: int, host_name: str):
        self.booking_id = booking_id
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.host_name = host_name
        self.end_time = start_time + timedelta(minutes=duration)

    def display_event_summary(self) -> None:
        """
        Prints out a short summary line for the customer menu lists
        """
        date_str = self.start_time.strftime("%Y-%m-%d")
        time_str = self.start_time.strftime("%H:%M")
        print(f"  [{self.booking_id}]  {date_str} {time_str}  |  {self.name} ({self.duration} min)  |  Host: {self.host_name}")


class BookingSystem:
    """
    Manages the list of events and applies business rule validations
    """
    def __init__(self):
        self.events = []

    def generate_booking_id(self) -> str:
        """
        Generates a unique random string booking ID
        """
        return f"BKG-{random.randint(1000, 9999)}"

    def book_event(self, name: str, host_name: str, start_time: datetime, duration: int) -> Event:
        """
        Checks validation rules and adds a new event to the schedule.
        Raises specific custom exceptions if rules are violated.
        """
        now = datetime.now()

        if duration <= 0:
            raise InvalidBookingError(f"Invalid duration: {duration} minutes. Must be greater than zero.")

        if start_time < now:
            raise InvalidBookingError("Cannot schedule an event in the past.")

        max_window = now + timedelta(days=90)
        if start_time > max_window:
            raise BookingWindowExceededError(start_time, max_window)

        new_end = start_time + timedelta(minutes=duration)

        # Look through all existing events to find overlapping time slots
        for existing in self.events:
            if start_time < existing.end_time and new_end > existing.start_time:
                raise TimeSlotTakenError(existing.name, existing.start_time, existing.end_time)

        bkg_id = self.generate_booking_id()
        new_event = Event(bkg_id, name, start_time, duration, host_name)
        self.events.append(new_event)
        return new_event

    def cancel_booking(self, booking_id: str) -> Event:
        """
        Cancels an event by ID if it is more than 24 hours away
        """
        target = self.view_booking(booking_id)
        now = datetime.now()

        deadline = target.start_time - timedelta(hours=24)
        if now > deadline:
            raise LateCancellationError(target.start_time, deadline)

        self.events.remove(target)
        return target

    def view_booking(self, booking_id: str) -> Event:
        """
        Finds a specific event by looking up its booking ID
        """
        for e in self.events:
            if e.booking_id.upper() == booking_id.upper():
                return e
        raise EventNotFoundError(booking_id)

    def list_upcoming_bookings(self) -> list:
        """
        Returns all future bookings sorted by their start date and time
        """
        now = datetime.now()
        upcoming = [e for e in self.events if e.start_time >= now]
        upcoming.sort(key=lambda x: x.start_time)
        return upcoming

    def list_bookings_by_host(self, host_name: str) -> list:
        """
        Returns a list of bookings for a specific host using a case-insensitive search
        """
        return [e for e in self.events if e.host_name.lower() == host_name.lower()]


# CLI Driver Application Interface

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input("> "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
            return selection
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")


if __name__ == "__main__":
    system = BookingSystem()

    while True:
        print()
        print("=" * 30)
        print(f'{"Event Booking System":^30}')
        print("=" * 30)
        print("[1] Book an event")
        print("[2] Cancel a booking")
        print("[3] View a booking")
        print("[4] List upcoming bookings")
        print("[5] List bookings by host")
        print("[6] Quit")
        
        choice = get_selection(6)

        match choice:
            case 6:
                print("Goodbye!")
                break

            case 1:
                print("\n--- Book an Event ---")
                name = input("Event name: ").strip()
                host = input("Host name: ").strip()
                date_str = input("Start date (YYYY-MM-DD): ").strip()
                time_str = input("Start time (HH:MM): ").strip()
                
                try:
                    duration = int(input("Duration (minutes): "))
                    start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                    
                    confirmed = system.book_event(name, host, start_dt, duration)
                    
                    print("\n Booking confirmed!")
                    print(f'{"Booking ID":<14}: {confirmed.booking_id}')
                    print(f"{"Event":<14}: {confirmed.name}")
                    print(f"{"Host":<14}: {confirmed.host_name}")
                    print(f"{"When":<14}: {confirmed.start_time.strftime('%Y-%m-%d at %H:%M')} ({confirmed.duration} min)")
                    
                except ValueError:
                    print("\n Input Error: Duration must be an integer, and date/time must follow the correct format.")
                except BookingError as be:
                    print(f"\n BookingError: {be}")

            case 2:
                print("\n--- Cancel a Booking ---")
                b_id = input("Booking ID: ").strip()
                try:
                    removed = system.cancel_booking(b_id)
                    print(f"\n Successfully cancelled booking \"{removed.name}\" ({removed.booking_id}).")
                except BookingError as be:
                    print(f"\n BookingError: {be}")

            case 3:
                print("\n--- View Booking Details ---")
                b_id = input("Booking ID: ").strip()
                try:
                    target = system.view_booking(b_id)
                    print(f"\nBooking Records Found:")
                    print(f"  ID: {target.booking_id} | {target.name}")
                    print(f"  Host: {target.host_name}")
                    print(f"  Time: {target.start_time.strftime('%Y-%m-%d %H:%M')} to {target.end_time.strftime('%H:%M')}")
                    print(f"  Duration: {target.duration} minutes")
                except BookingError as be:
                    print(f"\n BookingError: {be}")

            case 4:
                print("\nUpcoming Bookings")
                print("-" * 30)
                upcoming_list = system.list_upcoming_bookings()
                for evt in upcoming_list:
                    evt.display_event_summary()
                print("-" * 30)
                print(f"{len(upcoming_list)} upcoming booking(s) found.")

            case 5:
                print("\n--- Search Bookings by Host ---")
                h_name = input("Host name: ").strip()
                host_list = system.list_bookings_by_host(h_name)
                print(f"\nBookings hosted by '{h_name}':")
                print("-" * 30)
                if not host_list:
                    print("  No records encountered for this host name.")
                for evt in host_list:
                    evt.display_event_summary()
                print("-" * 30)