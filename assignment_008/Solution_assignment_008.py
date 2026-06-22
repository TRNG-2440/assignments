from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, event_name: str, start: datetime, end: datetime):
        date_str = start.strftime("%Y-%m-%d")
        start_str = start.strftime("%H:%M")
        end_str = end.strftime("%H:%M")
        super().__init__(
            f'Time slot unavailable — "{event_name}" is already scheduled '
            f"from {start_str} to {end_str} on {date_str}."
        )


class BookingWindowExceededError(BookingError):
    def __init__(self, requested: datetime, max_allowed: datetime):
        super().__init__(
            f"Requested date {requested.strftime('%Y-%m-%d')} exceeds the maximum "
            f"booking window. Bookings may not be made more than 90 days in advance "
            f"(latest allowed: {max_allowed.strftime('%Y-%m-%d')})."
        )


class LateCancellationError(BookingError):
    def __init__(self, event_start: datetime, deadline: datetime):
        super().__init__(
            f'Cannot cancel — the event starts at {event_start.strftime("%H:%M")} '
            f'on {event_start.strftime("%Y-%m-%d")} and the cancellation deadline '
            f"has passed (cancellations must be made at least 24 hours in advance, "
            f"deadline was {deadline.strftime('%Y-%m-%d %H:%M')})."
        )


class EventNotFoundError(BookingError):
    def __init__(self, booking_id: str):
        super().__init__(f"No booking found with ID '{booking_id}'.")


class InvalidBookingError(BookingError):
    pass


class Event:

    def __init__(self, booking_id: str, name: str, host: str,
                 start: datetime, duration_minutes: int):
        self.booking_id = booking_id
        self.name = name
        self.host = host
        self.start = start
        self.duration_minutes = duration_minutes

    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=self.duration_minutes)

    def display(self) -> str:
        return (
            f"  [{self.booking_id}]  {self.start.strftime('%Y-%m-%d %H:%M')}  |  "
            f"{self.name} ({self.duration_minutes} min)  |  Host: {self.host}"
        )


class BookingSystem:

    MAX_DAYS_AHEAD = 90
    CANCEL_HOURS_MINIMUM = 24
    _id_counter = 1000

    def __init__(self):
        self._bookings: dict[str, Event] = {}

    def _generate_id(self) -> str:
        BookingSystem._id_counter += 1
        return f"BKG-{BookingSystem._id_counter}"

    def _check_overlap(self, start: datetime, end: datetime) -> None:
        for event in self._bookings.values():
            if event.start.date() != start.date():
                continue
            if start < event.end and end > event.start:
                raise TimeSlotTakenError(event.name, event.start, event.end)

    def book(self, name: str, host: str,
             start: datetime, duration_minutes: int) -> Event:
        if not name.strip():
            raise InvalidBookingError("Event name cannot be empty.")
        if not host.strip():
            raise InvalidBookingError("Host name cannot be empty.")
        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be a positive number of minutes.")

        now = datetime.now()
        if start <= now:
            raise InvalidBookingError(
                f"Start time {start.strftime('%Y-%m-%d %H:%M')} is in the past."
            )

        max_allowed = now + timedelta(days=self.MAX_DAYS_AHEAD)
        if start > max_allowed:
            raise BookingWindowExceededError(start, max_allowed)

        end = start + timedelta(minutes=duration_minutes)
        self._check_overlap(start, end)

        booking_id = self._generate_id()
        event = Event(booking_id, name.strip(), host.strip(), start, duration_minutes)
        self._bookings[booking_id] = event
        return event

    def cancel(self, booking_id: str) -> Event:
        if booking_id not in self._bookings:
            raise EventNotFoundError(booking_id)

        event = self._bookings[booking_id]
        deadline = event.start - timedelta(hours=self.CANCEL_HOURS_MINIMUM)

        if datetime.now() > deadline:
            raise LateCancellationError(event.start, deadline)

        del self._bookings[booking_id]
        return event

    def view(self, booking_id: str) -> Event:
        if booking_id not in self._bookings:
            raise EventNotFoundError(booking_id)
        return self._bookings[booking_id]

    def list_upcoming(self) -> list[Event]:
        now = datetime.now()
        return sorted(
            [e for e in self._bookings.values() if e.start > now],
            key=lambda e: e.start,
        )

    def list_by_host(self, host: str) -> list[Event]:
        h = host.strip().lower()
        return sorted(
            [e for e in self._bookings.values() if e.host.lower() == h],
            key=lambda e: e.start,
        )


def prompt_date(prompt: str) -> str:
    return input(prompt).strip()

def parse_datetime(date_str: str, time_str: str) -> datetime:
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def prompt_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("  Invalid input — please enter a whole number.")
        return None

def divider() -> None:
    print("-" * 30)

def header(title: str) -> None:
    print("=" * 30)
    print(f"    {title}")
    print("=" * 30)


def cli_book(system: BookingSystem) -> None:
    name = input("Event name: ").strip()
    host = input("Host name: ").strip()
    date_str = input("Start date (YYYY-MM-DD): ").strip()
    time_str = input("Start time (HH:MM): ").strip()
    duration = prompt_int("Duration (minutes): ")

    if duration is None:
        return

    try:
        start = parse_datetime(date_str, time_str)
    except ValueError:
        print("  Invalid date or time format.")
        return

    try:
        event = system.book(name, host, start, duration)
        print(f"\n✅ Booking confirmed!")
        print(f"   Booking ID : {event.booking_id}")
        print(f"   Event      : {event.name}")
        print(f"   Host       : {event.host}")
        print(f"   When       : {event.start.strftime('%Y-%m-%d')} at "
              f"{event.start.strftime('%H:%M')} ({event.duration_minutes} min)")
    except BookingError as e:
        print(f"\n❌ BookingError: {e}")


def cli_cancel(system: BookingSystem) -> None:
    booking_id = input("Booking ID: ").strip().upper()
    try:
        event = system.cancel(booking_id)
        print(f"\n✅ Booking '{event.name}' ({booking_id}) has been cancelled.")
    except BookingError as e:
        print(f"\n❌ BookingError: {e}")


def cli_view(system: BookingSystem) -> None:
    booking_id = input("Booking ID: ").strip().upper()
    try:
        event = system.view(booking_id)
        print()
        print(event.display())
    except BookingError as e:
        print(f"\n❌ BookingError: {e}")


def cli_list_upcoming(system: BookingSystem) -> None:
    events = system.list_upcoming()
    print("\nUpcoming Bookings")
    divider()
    if not events:
        print("  No upcoming bookings.")
    else:
        for event in events:
            print(event.display())
    divider()
    print(f"{len(events)} upcoming booking(s) found.")


def cli_list_by_host(system: BookingSystem) -> None:
    host = input("Host name: ").strip()
    events = system.list_by_host(host)
    print(f"\nBookings for '{host}'")
    divider()
    if not events:
        print("  No bookings found for this host.")
    else:
        for event in events:
            print(event.display())
    divider()
    print(f"{len(events)} booking(s) found.")


def main() -> None:
    system = BookingSystem()

    while True:
        print()
        header("Event Booking System")
        print()
        print("  [1] Book an event")
        print("  [2] Cancel a booking")
        print("  [3] View a booking")
        print("  [4] List upcoming bookings")
        print("  [5] List bookings by host")
        print("  [6] Quit")

        choice = input("\n> ").strip()
        print()

        if choice == "1":
            cli_book(system)
        elif choice == "2":
            cli_cancel(system)
        elif choice == "3":
            cli_view(system)
        elif choice == "4":
            cli_list_upcoming(system)
        elif choice == "5":
            cli_list_by_host(system)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("  Invalid option — choose 1 through 6.")

        print()
        divider()


if __name__ == "__main__":
    main()