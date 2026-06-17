import random
from datetime import datetime, timedelta


class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, existing_name, start_time, end_time, date):
        message = (
            f'Time slot unavailable — "{existing_name}" is already scheduled '
            f"from {start_time} to {end_time} on {date}."
        )
        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_allowed_date):
        message = (
            f"Requested date {requested_date} exceeds the maximum booking window. "
            f"Bookings may not be made more than 90 days in advance "
            f"(latest allowed: {max_allowed_date})."
        )
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event_name, event_time, deadline):
        message = (
            f'Cannot cancel "{event_name}" — the event starts at '
            f"{event_time} and the cancellation deadline has passed "
            f"(cancellations must be made before {deadline})."
        )
        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        message = f'No booking found with ID "{booking_id}".'
        super().__init__(message)


class InvalidBookingError(BookingError):
    def __init__(self, reason):
        message = f"Invalid booking: {reason}"
        super().__init__(message)


class Event:
    def __init__(self, name, start_datetime, duration_minutes, host_name, booking_id):
        self.name = name
        self.start_datetime = start_datetime
        self.duration_minutes = duration_minutes
        self.host_name = host_name
        self.booking_id = booking_id

    def end_datetime(self):
        return self.start_datetime + timedelta(minutes=self.duration_minutes)

    def __str__(self):
        start_str = self.start_datetime.strftime("%Y-%m-%d at %H:%M")
        return (
            f"[{self.booking_id}]  {self.name}\n"
            f"   Host : {self.host_name}\n"
            f"   When : {start_str} ({self.duration_minutes} min)"
        )


class BookingSystem:
    MAX_DAYS_AHEAD = 90
    CANCEL_HOURS_BEFORE = 24

    def __init__(self):
        self.bookings = {}

    def _make_booking_id(self):
        while True:
            candidate = f"BKG-{random.randint(1000, 9999)}"
            if candidate not in self.bookings:
                return candidate

    def _check_overlap(self, new_start, new_end):
        for event in self.bookings.values():
            if new_start < event.end_datetime() and new_end > event.start_datetime:
                return event
        return None

    def book_event(self, name, start_datetime, duration_minutes, host_name):
        now = datetime.now()

        if not name or not name.strip():
            raise InvalidBookingError("Event name cannot be empty.")

        if not host_name or not host_name.strip():
            raise InvalidBookingError("Host name cannot be empty.")

        if duration_minutes <= 0:
            raise InvalidBookingError(
                f"Duration must be greater than 0 minutes (got {duration_minutes})."
            )

        if start_datetime < now:
            raise InvalidBookingError(
                f"Start time {start_datetime.strftime('%Y-%m-%d %H:%M')} is in the past."
            )

        max_date = now + timedelta(days=self.MAX_DAYS_AHEAD)
        if start_datetime > max_date:
            raise BookingWindowExceededError(
                start_datetime.strftime("%Y-%m-%d"),
                max_date.strftime("%Y-%m-%d")
            )

        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        conflict = self._check_overlap(start_datetime, end_datetime)

        if conflict is not None:
            raise TimeSlotTakenError(
                conflict.name,
                conflict.start_datetime.strftime("%H:%M"),
                conflict.end_datetime().strftime("%H:%M"),
                conflict.start_datetime.strftime("%Y-%m-%d")
            )

        booking_id = self._make_booking_id()
        new_event = Event(name.strip(), start_datetime, duration_minutes, host_name.strip(), booking_id)
        self.bookings[booking_id] = new_event
        return new_event

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise EventNotFoundError(booking_id)

        event = self.bookings[booking_id]
        now = datetime.now()
        cancellation_deadline = event.start_datetime - timedelta(hours=self.CANCEL_HOURS_BEFORE)

        if now >= cancellation_deadline:
            raise LateCancellationError(
                event.name,
                event.start_datetime.strftime("%H:%M on %Y-%m-%d"),
                cancellation_deadline.strftime("%Y-%m-%d at %H:%M")
            )

        del self.bookings[booking_id]
        return event

    def view_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise EventNotFoundError(booking_id)
        return self.bookings[booking_id]

    def list_upcoming(self):
        now = datetime.now()
        upcoming = [e for e in self.bookings.values() if e.start_datetime > now]
        upcoming.sort(key=lambda e: e.start_datetime)
        return upcoming

    def list_by_host(self, host_name):
        search = host_name.strip().lower()
        results = [e for e in self.bookings.values() if e.host_name.lower() == search]
        results.sort(key=lambda e: e.start_datetime)
        return results


def print_separator():
    print("-" * 30)


def print_header():
    print("=" * 30)
    print("    Event Booking System")
    print("=" * 30)


def print_menu():
    print()
    print("[1] Book an event")
    print("[2] Cancel a booking")
    print("[3] View a booking")
    print("[4] List upcoming bookings")
    print("[5] List bookings by host")
    print("[6] Quit")
    print()


def get_datetime_from_user():
    date_str = input("Start date (YYYY-MM-DD): ").strip()
    time_str = input("Start time (HH:MM): ").strip()
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date or time format. Please use YYYY-MM-DD and HH:MM.")
        return None


def get_duration_from_user():
    raw = input("Duration (minutes): ").strip()
    try:
        return int(raw)
    except ValueError:
        print("Duration must be a whole number (e.g. 30).")
        return None


def do_book_event(system):
    print()
    name = input("Event name: ").strip()
    host = input("Host name: ").strip()

    start_dt = get_datetime_from_user()
    if start_dt is None:
        return

    duration = get_duration_from_user()
    if duration is None:
        return

    try:
        event = system.book_event(name, start_dt, duration, host)
        print()
        print("Booking confirmed.")
        print(f"   Booking ID : {event.booking_id}")
        print(f"   Event      : {event.name}")
        print(f"   Host       : {event.host_name}")
        print(f"   When       : {event.start_datetime.strftime('%Y-%m-%d at %H:%M')} ({event.duration_minutes} min)")
    except BookingError as e:
        print(f"Error: {e}")


def do_cancel_booking(system):
    print()
    booking_id = input("Booking ID: ").strip().upper()
    try:
        event = system.cancel_booking(booking_id)
        print(f'Booking "{event.name}" ({event.booking_id}) has been cancelled.')
    except BookingError as e:
        print(f"Error: {e}")


def do_view_booking(system):
    print()
    booking_id = input("Booking ID: ").strip().upper()
    try:
        event = system.view_booking(booking_id)
        print()
        print(event)
    except BookingError as e:
        print(f"Error: {e}")


def do_list_upcoming(system):
    upcoming = system.list_upcoming()
    print()
    print("Upcoming Bookings")
    print_separator()

    if not upcoming:
        print("  No upcoming bookings found.")
    else:
        for event in upcoming:
            start_str = event.start_datetime.strftime("%Y-%m-%d %H:%M")
            print(
                f"  [{event.booking_id}]  {start_str}  |  "
                f"{event.name} ({event.duration_minutes} min)  |  "
                f"Host: {event.host_name}"
            )

    print_separator()
    print(f"{len(upcoming)} upcoming booking(s) found.")


def do_list_by_host(system):
    print()
    host = input("Host name: ").strip()
    results = system.list_by_host(host)

    print()
    print(f"Bookings for: {host}")
    print_separator()

    if not results:
        print(f'  No bookings found for host "{host}".')
    else:
        for event in results:
            start_str = event.start_datetime.strftime("%Y-%m-%d %H:%M")
            print(
                f"  [{event.booking_id}]  {start_str}  |  "
                f"{event.name} ({event.duration_minutes} min)"
            )

    print_separator()
    print(f"{len(results)} booking(s) found.")


def main():
    system = BookingSystem()
    print_header()

    while True:
        print_menu()
        choice = input("> ").strip()

        if choice == "1":
            do_book_event(system)
        elif choice == "2":
            do_cancel_booking(system)
        elif choice == "3":
            do_view_booking(system)
        elif choice == "4":
            do_list_upcoming(system)
        elif choice == "5":
            do_list_by_host(system)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

        print_separator()


if __name__ == "__main__":
    main()