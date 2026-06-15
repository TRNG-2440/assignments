from datetime import datetime, timedelta


class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start_time, end_time):
        self.event_name = event_name
        self.start_time = start_time
        self.end_time = end_time
        message = (
            f'Time slot unavailable — "{self.event_name}" is already scheduled '
            f'from {self.start_time.strftime("%H:%M")} to {self.end_time.strftime("%H:%M")} '
            f'on {self.start_time.strftime("%Y-%m-%d")}.'
        )
        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, latest_allowed_date):
        self.requested_date = requested_date
        self.latest_allowed_date = latest_allowed_date
        message = (
            f"Requested date {self.requested_date.strftime('%Y-%m-%d')} exceeds the maximum booking window. "
            f"Bookings may not be made more than 90 days in advance "
            f"(latest allowed: {self.latest_allowed_date.strftime('%Y-%m-%d')})."
        )
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event_name, event_start, cancellation_deadline):
        self.event_name = event_name
        self.event_start = event_start
        self.cancellation_deadline = cancellation_deadline
        message = (
            f'Cannot cancel "{self.event_name}" — the event starts at '
            f'{self.event_start.strftime("%H:%M")} on {self.event_start.strftime("%Y-%m-%d")} '
            f'and the cancellation deadline has passed '
            f'(cancellations must be made at least 24 hours in advance; deadline was '
            f'{self.cancellation_deadline.strftime("%Y-%m-%d %H:%M")}).'
        )
        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        self.booking_id = booking_id
        message = f"Booking ID {self.booking_id} was not found."
        super().__init__(message)


class InvalidBookingError(BookingError):
    def __init__(self, message):
        super().__init__(message)


class Event:
    booking_running_count = 1


    def __init__(self, event_name, start_datetime, duration_minutes, host_name):
        self.event_name = event_name
        self.start_datetime = start_datetime
        self.duration_minutes = duration_minutes
        self.host_name = host_name
        self.booking_id = self.create_booking_id()


    def create_booking_id(self):
        number = f"BKG-{Event.booking_running_count:04d}"
        Event.booking_running_count += 1
        return number


    def get_end_datetime(self):
        return self.start_datetime + timedelta(minutes=self.duration_minutes)


    def display_details(self):
        print(f"Booking ID : {self.booking_id}")
        print(f"Event      : {self.event_name}")
        print(f"Host       : {self.host_name}")
        print(
            f"When       : {self.start_datetime.strftime('%Y-%m-%d')} "
            f"at {self.start_datetime.strftime('%H:%M')} "
            f"({self.duration_minutes} min)"
        )


class BookingSystem:
    def __init__(self):
        self.events = {}


    def validate_booking(self, event_name, start_datetime, duration_minutes, host_name):
        if not event_name.strip():
            raise InvalidBookingError("Event name is required.")

        if not host_name.strip():
            raise InvalidBookingError("Host name is required.")

        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0 minutes.")

        now = datetime.now()

        if start_datetime < now:
            raise InvalidBookingError("A booking cannot be made in the past.")

        latest_allowed_datetime = now + timedelta(days=90)

        if start_datetime > latest_allowed_datetime:
            raise BookingWindowExceededError(start_datetime, latest_allowed_datetime)

        requested_end = start_datetime + timedelta(minutes=duration_minutes)

        for event in self.events.values():
            existing_start = event.start_datetime
            existing_end = event.get_end_datetime()

            if start_datetime.date() == existing_start.date():
                if start_datetime < existing_end and requested_end > existing_start:
                    raise TimeSlotTakenError(
                        event.event_name,
                        existing_start,
                        existing_end
                    )


    def book_event(self, event_name, start_datetime, duration_minutes, host_name):
        self.validate_booking(event_name, start_datetime, duration_minutes, host_name)

        new_event = Event(event_name, start_datetime, duration_minutes, host_name)
        self.events[new_event.booking_id] = new_event
        return new_event


    def cancel_booking(self, booking_id):
        if booking_id not in self.events:
            raise EventNotFoundError(booking_id)

        event = self.events[booking_id]
        cancellation_deadline = event.start_datetime - timedelta(hours=24)

        if datetime.now() > cancellation_deadline:
            raise LateCancellationError(
                event.event_name,
                event.start_datetime,
                cancellation_deadline
            )

        removed_event = self.events.pop(booking_id)
        return removed_event


    def view_booking(self, booking_id):
        if booking_id not in self.events:
            raise EventNotFoundError(booking_id)

        return self.events[booking_id]


    def list_upcoming_bookings(self):
        now = datetime.now()
        upcoming_events = []

        for event in self.events.values():
            if event.start_datetime > now:
                upcoming_events.append(event)

        upcoming_events.sort(key=lambda event: event.start_datetime)
        return upcoming_events


    def list_bookings_by_host(self, host_name):
        host_matches = []

        for event in self.events.values():
            if event.host_name.lower() == host_name.lower():
                host_matches.append(event)

        host_matches.sort(key=lambda event: event.start_datetime)
        return host_matches


# --------------------------------------------------------


def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Error: Please enter a valid whole number.")


def get_date_string(prompt):
    while True:
        date_text = input(prompt).strip()

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Error: Please enter a valid date in YYYY-MM-DD format.")


def get_time_string(prompt):
    while True:
        time_text = input(prompt).strip()

        try:
            datetime.strptime(time_text, "%H:%M")
            return time_text
        except ValueError:
            print("Error: Please enter a valid time in HH:MM format.")


def build_start_datetime():
    start_date = get_date_string("Start date (YYYY-MM-DD): ")
    start_time = get_time_string("Start time (HH:MM): ")
    return datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")


# --------------------------------------------------------


def create_booking_cli(system):
    try:
        event_name = input("Event name: ").strip()
        host_name = input("Host name: ").strip()
        start_datetime = build_start_datetime()
        duration_minutes = get_int("Duration (minutes): ")

        booking = system.book_event(event_name, start_datetime, duration_minutes, host_name)

        print("✅ Booking confirmed!")
        booking.display_details()

    except BookingError as e:
        print(f"❌ BookingError: {e}")


def cancel_booking_cli(system):
    try:
        booking_id = input("Booking ID: ").strip()
        cancelled_event = system.cancel_booking(booking_id)

        print("✅ Booking cancelled successfully.")
        cancelled_event.display_details()

    except BookingError as e:
        print(f"❌ BookingError: {e}")


def view_booking_cli(system):
    try:
        booking_id = input("Booking ID: ").strip()
        event = system.view_booking(booking_id)

        print("-" * 30)
        event.display_details()
        print("-" * 30)

    except BookingError as e:
        print(f"❌ BookingError: {e}")


def list_upcoming_cli(system):
    events = system.list_upcoming_bookings()

    print("Upcoming Bookings")
    print("-" * 30)

    if not events:
        print("No upcoming bookings found.")
        return

    for event in events:
        print(
            f"[{event.booking_id}] "
            f"{event.start_datetime.strftime('%Y-%m-%d %H:%M')} | "
            f"{event.event_name} ({event.duration_minutes} min) | "
            f"Host: {event.host_name}"
        )

    print("-" * 30)
    print(f"{len(events)} upcoming booking(s) found.")


def list_by_host_cli(system):
    host_name = input("Host name: ").strip()
    events = system.list_bookings_by_host(host_name)

    print(f'Bookings for host: {host_name}')
    print("-" * 30)

    if not events:
        print("No bookings found for that host.")
        return

    for event in events:
        print(
            f"[{event.booking_id}] "
            f"{event.start_datetime.strftime('%Y-%m-%d %H:%M')} | "
            f"{event.event_name} ({event.duration_minutes} min)"
        )

    print("-" * 30)
    print(f"{len(events)} booking(s) found.")

def main():
    system = BookingSystem()

    while True:
        print("\n" + "=" * 30)
        print("Event Booking System")
        print("=" * 30)
        print("[1] Book an event")
        print("[2] Cancel a booking")
        print("[3] View a booking")
        print("[4] List upcoming bookings")
        print("[5] List bookings by host")
        print("[6] Quit")

        choice = input("> ").strip()

        if choice == "1":
            create_booking_cli(system)

        elif choice == "2":
            cancel_booking_cli(system)

        elif choice == "3":
            view_booking_cli(system)

        elif choice == "4":
            list_upcoming_cli(system)

        elif choice == "5":
            list_by_host_cli(system)

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Error: Invalid menu choice.")


if __name__ == "__main__":
    main()