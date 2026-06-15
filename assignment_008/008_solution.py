from datetime import datetime, timedelta


class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, event, requested_start=None):
        start = event.start_datetime.strftime("%H:%M")
        end = event.end_datetime().strftime("%H:%M")
        event_date = event.start_datetime.strftime("%Y-%m-%d")

        if requested_start:
            requested = requested_start.strftime("%Y-%m-%d at %H:%M")
            message = (
                f'Time slot unavailable for {requested} — "{event.name}" '
                f"is already scheduled from {start} to {end} on {event_date}."
            )
        else:
            message = (
                f'Time slot unavailable — "{event.name}" is already scheduled '
                f"from {start} to {end} on {event_date}."
            )

        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, latest_allowed_date):
        message = (
            f"Requested date {requested_date} exceeds the maximum booking window. "
            f"Bookings may not be made more than 90 days in advance "
            f"(latest allowed: {latest_allowed_date})."
        )
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event):
        event_time = event.start_datetime.strftime("%H:%M on %Y-%m-%d")
        deadline = (event.start_datetime - timedelta(hours=24)).strftime("%H:%M on %Y-%m-%d")

        message = (
            f'Cannot cancel "{event.name}" — the event starts at {event_time} '
            f"and the cancellation deadline has passed. "
            f"Cancellations must be made at least 24 hours in advance. "
            f"Deadline was {deadline}."
        )
        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        super().__init__(f"Booking ID {booking_id} was not found.")


class InvalidBookingError(BookingError):
    pass


class EventFullError(BookingError):
    def __init__(self, event):
        super().__init__(f'"{event.name}" is fully booked. Capacity: {event.capacity}.')


class Event:
    next_id = 1

    def __init__(self, name, start_datetime, duration, host_name, capacity=1):
        self.booking_id = self.generate_id()
        self.name = name
        self.start_datetime = start_datetime
        self.duration = duration
        self.host_name = host_name
        self.capacity = capacity
        self.attendees = []

    @classmethod
    def generate_id(cls):
        booking_id = f"BKG-{cls.next_id:04d}"
        cls.next_id += 1
        return booking_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise InvalidBookingError("Event name is required.")
        self._name = value.strip()

    @property
    def host_name(self):
        return self._host_name

    @host_name.setter
    def host_name(self, value):
        if not value.strip():
            raise InvalidBookingError("Host name is required.")
        self._host_name = value.strip()

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        value = int(value)

        if value <= 0:
            raise InvalidBookingError("Duration must be greater than 0.")

        self._duration = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        value = int(value)

        if value <= 0:
            raise InvalidBookingError("Capacity must be greater than 0.")

        self._capacity = value

    def end_datetime(self):
        return self.start_datetime + timedelta(minutes=self.duration)

    def add_attendee(self, attendee_name):
        if not attendee_name.strip():
            raise InvalidBookingError("Attendee name is required.")

        if len(self.attendees) >= self.capacity:
            raise EventFullError(self)

        self.attendees.append(attendee_name.strip())

    def display_details(self):
        return (
            f"[{self.booking_id}] "
            f"{self.start_datetime.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.name} ({self.duration} min) | "
            f"Host: {self.host_name} | "
            f"Attendees: {len(self.attendees)}/{self.capacity}"
        )


class BookingSystem:
    MAX_BOOKING_DAYS = 90
    CANCELLATION_HOURS = 24

    def __init__(self):
        self.events = {}

    def book_event(self, name, start_datetime, duration, host_name, capacity=1):
        event = Event(name, start_datetime, duration, host_name, capacity)
        self.validate_event(event)
        self.events[event.booking_id] = event
        return event

    def book_recurring_event(self, name, start_datetime, duration, host_name, capacity, weeks):
        weeks = int(weeks)

        if weeks <= 0:
            raise InvalidBookingError("Number of weeks must be greater than 0.")

        new_events = []

        for week in range(weeks):
            occurrence_start = start_datetime + timedelta(weeks=week)
            event = Event(name, occurrence_start, duration, host_name, capacity)
            self.validate_event(event)
            new_events.append(event)

        for event in new_events:
            self.events[event.booking_id] = event

        return new_events

    def validate_event(self, event):
        now = datetime.now()
        latest_allowed = now + timedelta(days=self.MAX_BOOKING_DAYS)

        if event.start_datetime < now:
            raise InvalidBookingError("Booking cannot start in the past.")

        if event.start_datetime > latest_allowed:
            requested_date = event.start_datetime.strftime("%Y-%m-%d")
            latest_allowed_date = latest_allowed.strftime("%Y-%m-%d")
            raise BookingWindowExceededError(requested_date, latest_allowed_date)

        for existing_event in self.events.values():
            if self.events_overlap(event, existing_event):
                raise TimeSlotTakenError(existing_event, event.start_datetime)

    def events_overlap(self, event1, event2):
        same_day = event1.start_datetime.date() == event2.start_datetime.date()

        if not same_day:
            return False

        return (
            event1.start_datetime < event2.end_datetime()
            and event1.end_datetime() > event2.start_datetime
        )

    def cancel_booking(self, booking_id):
        event = self.view_booking(booking_id)
        deadline = event.start_datetime - timedelta(hours=self.CANCELLATION_HOURS)

        if datetime.now() > deadline:
            raise LateCancellationError(event)

        del self.events[event.booking_id]
        return event

    def view_booking(self, booking_id):
        booking_id = booking_id.strip().upper()

        if booking_id not in self.events:
            raise EventNotFoundError(booking_id)

        return self.events[booking_id]

    def list_upcoming_bookings(self):
        now = datetime.now()
        upcoming = []

        for event in self.events.values():
            if event.start_datetime > now:
                upcoming.append(event)

        return sorted(upcoming, key=lambda event: event.start_datetime)

    def list_bookings_by_host(self, host_name):
        host_name = host_name.lower().strip()
        results = []

        for event in self.events.values():
            if event.host_name.lower() == host_name:
                results.append(event)

        return sorted(results, key=lambda event: event.start_datetime)

    def add_attendee_to_event(self, booking_id, attendee_name):
        event = self.view_booking(booking_id)
        event.add_attendee(attendee_name)
        return event


def log_booking_error(error):
    with open("booking_errors.log", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} | {type(error).__name__} | {error}\n")


def get_text(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("Error: Input cannot be empty.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a whole number.")


def get_optional_int(prompt, default):
    text = input(prompt).strip()

    if not text:
        return default

    try:
        return int(text)
    except ValueError:
        print(f"Invalid input. Using default value of {default}.")
        return default


def get_start_datetime():
    while True:
        try:
            start_date = get_text("Start date (YYYY-MM-DD): ")
            start_time = get_text("Start time (HH:MM): ")
            return datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Error: Date or time format is invalid.")


def print_booking(event):
    print(f"Booking ID : {event.booking_id}")
    print(f"Event      : {event.name}")
    print(f"Host       : {event.host_name}")
    print(f"When       : {event.start_datetime.strftime('%Y-%m-%d at %H:%M')} ({event.duration} min)")
    print(f"Capacity   : {len(event.attendees)}/{event.capacity}")


def print_bookings(events):
    if not events:
        print("No bookings found.")
        return

    for event in events:
        print(event.display_details())

    print(f"{len(events)} booking(s) found.")


def book_event_menu(system):
    try:
        name = get_text("Event name: ")
        host_name = get_text("Host name: ")
        start_datetime = get_start_datetime()
        duration = get_int("Duration (minutes): ")
        capacity = get_optional_int("Capacity (press Enter for 1): ", 1)

        event = system.book_event(name, start_datetime, duration, host_name, capacity)

        print()
        print("Booking confirmed!")
        print_booking(event)

    except BookingError as error:
        log_booking_error(error)
        print(f"BookingError: {error}")


def book_recurring_event_menu(system):
    try:
        name = get_text("Event name: ")
        host_name = get_text("Host name: ")
        start_datetime = get_start_datetime()
        duration = get_int("Duration (minutes): ")
        capacity = get_optional_int("Capacity (press Enter for 1): ", 1)
        weeks = get_int("Repeat weekly for how many weeks? ")

        events = system.book_recurring_event(
            name,
            start_datetime,
            duration,
            host_name,
            capacity,
            weeks
        )

        print()
        print(f"{len(events)} recurring booking(s) confirmed.")

        for event in events:
            print(event.display_details())

    except BookingError as error:
        log_booking_error(error)
        print(f"BookingError: {error}")


def cancel_booking_menu(system):
    try:
        booking_id = get_text("Booking ID: ")
        event = system.cancel_booking(booking_id)

        print(f'Booking "{event.name}" has been canceled.')

    except BookingError as error:
        log_booking_error(error)
        print(f"BookingError: {error}")


def view_booking_menu(system):
    try:
        booking_id = get_text("Booking ID: ")
        event = system.view_booking(booking_id)

        print()
        print_booking(event)

    except BookingError as error:
        log_booking_error(error)
        print(f"BookingError: {error}")


def list_upcoming_menu(system):
    print()
    print("Upcoming Bookings")
    print("------------------------------")
    print_bookings(system.list_upcoming_bookings())


def list_by_host_menu(system):
    host_name = get_text("Host name: ")

    print()
    print(f"Bookings for {host_name}")
    print("------------------------------")
    print_bookings(system.list_bookings_by_host(host_name))


def add_attendee_menu(system):
    try:
        booking_id = get_text("Booking ID: ")
        attendee_name = get_text("Attendee name: ")

        event = system.add_attendee_to_event(booking_id, attendee_name)

        print(f"{attendee_name} added to {event.name}.")
        print(f"Capacity: {len(event.attendees)}/{event.capacity}")

    except BookingError as error:
        log_booking_error(error)
        print(f"BookingError: {error}")


def main():
    system = BookingSystem()

    while True:
        print()
        print("==============================")
        print("    Event Booking System")
        print("==============================")
        print("[1] Book an event")
        print("[2] Book a recurring event")
        print("[3] Cancel a booking")
        print("[4] View a booking")
        print("[5] List upcoming bookings")
        print("[6] List bookings by host")
        print("[7] Add attendee to event")
        print("[8] Quit")

        choice = input("> ").strip()

        if choice == "1":
            book_event_menu(system)

        elif choice == "2":
            book_recurring_event_menu(system)

        elif choice == "3":
            cancel_booking_menu(system)

        elif choice == "4":
            view_booking_menu(system)

        elif choice == "5":
            list_upcoming_menu(system)

        elif choice == "6":
            list_by_host_menu(system)

        elif choice == "7":
            add_attendee_menu(system)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()