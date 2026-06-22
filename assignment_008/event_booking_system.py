from datetime import datetime, timedelta


# custom exceptions

# base exception class for all booking related errors
class BookingError(Exception):
    pass


# error when event overlaps w an existing booking
class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start_time, end_time):
        super().__init__(
            f'Time slot unavailable — "{event_name}" is already scheduled '
            f'from {start_time} to {end_time}.'
        )


# error when booking is more than 90 days in advance
class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_date):
        super().__init__(
            f"Requested date {requested_date} exceeds the maximum booking "
            f"window. Latest allowed date is {max_date}."
        )


# error when trying to cancel too close to event start
class LateCancellationError(BookingError):
    def __init__(self, event_name, event_time, deadline):
        super().__init__(
            f'Cannot cancel "{event_name}" — the event starts at '
            f'{event_time} and the cancellation deadline '
            f'({deadline}) has passed.'
        )


# error when booking id does not exist
class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        super().__init__(
            f"Booking ID '{booking_id}' was not found."
        )


# error when general validation errors
class InvalidBookingError(BookingError):
    def __init__(self, message):
        super().__init__(message)


# event class
class Event:

    def __init__(
        self,
        booking_id,
        event_name,
        start_datetime,
        duration,
        host_name
    ):
        self.booking_id = booking_id
        self.event_name = event_name
        self.start_datetime = start_datetime
        self.duration = duration
        self.host_name = host_name

    # calc when event ends
    @property
    def end_datetime(self):
        return self.start_datetime + timedelta(
            minutes=self.duration
        )

    # displays event details
    def display_details(self):
        print(f"\nBooking ID : {self.booking_id}")
        print(f"Event      : {self.event_name}")
        print(f"Host       : {self.host_name}")
        print(
            f"When       : "
            f"{self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
        )
        print(f"Duration   : {self.duration} minutes")


# booking system class
class BookingSystem:

    def __init__(self):
        self.events = {}
        self.next_id = 1000

    # generates unique booking ids
    def generate_booking_id(self):
        booking_id = f"BKG-{self.next_id}"
        self.next_id += 1
        return booking_id

    # creates a new booking
    def book_event(
        self,
        event_name,
        host_name,
        start_datetime,
        duration
    ):

        # req fields validation
        if not event_name.strip():
            raise InvalidBookingError(
                "Event name cannot be empty."
            )

        if not host_name.strip():
            raise InvalidBookingError(
                "Host name cannot be empty."
            )

        # duration validation
        if duration <= 0:
            raise InvalidBookingError(
                "Duration must be greater than zero."
            )

        # cannot book in the past
        if start_datetime < datetime.now():
            raise InvalidBookingError(
                "Bookings cannot be made in the past."
            )

        # cannot exceed 90 day booking window
        max_date = datetime.now() + timedelta(days=90)

        if start_datetime > max_date:
            raise BookingWindowExceededError(
                start_datetime.date(),
                max_date.date()
            )

        # calcs ending time of new booking
        new_end = start_datetime + timedelta(
            minutes=duration
        )

        # checks for overlapping bookings
        for event in self.events.values():

            if (
                start_datetime < event.end_datetime
                and new_end > event.start_datetime
            ):
                raise TimeSlotTakenError(
                    event.event_name,
                    event.start_datetime.strftime(
                        "%H:%M"
                    ),
                    event.end_datetime.strftime(
                        "%H:%M"
                    )
                )

        # create booking
        booking_id = self.generate_booking_id()

        event = Event(
            booking_id,
            event_name,
            start_datetime,
            duration,
            host_name
        )

        self.events[booking_id] = event

        return event

    # cancel an existing booking
    def cancel_booking(self, booking_id):

        if booking_id not in self.events:
            raise EventNotFoundError(
                booking_id
            )

        event = self.events[booking_id]

        cancellation_deadline = (
            event.start_datetime
            - timedelta(hours=24)
        )

        if datetime.now() > cancellation_deadline:
            raise LateCancellationError(
                event.event_name,
                event.start_datetime.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                cancellation_deadline.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

        del self.events[booking_id]

    # view a booking by id
    def view_booking(self, booking_id):

        if booking_id not in self.events:
            raise EventNotFoundError(
                booking_id
            )

        return self.events[booking_id]

    # lists future bookings sorted chronologically
    def list_upcoming_bookings(self):

        upcoming = [
            event
            for event in self.events.values()
            if event.start_datetime > datetime.now()
        ]

        return sorted(
            upcoming,
            key=lambda event: event.start_datetime
        )

    # lists bookings for a specific host
    def list_bookings_by_host(
        self,
        host_name
    ):

        return [
            event
            for event in self.events.values()
            if event.host_name.lower()
            == host_name.lower()
        ]


# CLI meny system
system = BookingSystem()

while True:

    print("Event Booking System")
    print("[1] Book an event")
    print("[2] Cancel a booking")
    print("[3] View a booking")
    print("[4] List upcoming bookings")
    print("[5] List bookings by host")
    print("[6] Quit")

    choice = input("\nSelect an option: ")

    try:

        # book event
        if choice == "1":

            event_name = input(
                "Event name: "
            )

            host_name = input(
                "Host name: "
            )

            date_input = input(
                "Start date (YYYY-MM-DD): "
            )

            time_input = input(
                "Start time (HH:MM): "
            )

            duration = int(
                input(
                    "Duration (minutes): "
                )
            )

            start_datetime = datetime.strptime(
                f"{date_input} {time_input}",
                "%Y-%m-%d %H:%M"
            )

            event = system.book_event(
                event_name,
                host_name,
                start_datetime,
                duration
            )

            print("\nBooking confirmed!")

            event.display_details()

        # cancel booking
        elif choice == "2":

            booking_id = input(
                "Booking ID: "
            )

            system.cancel_booking(
                booking_id
            )

            print(
                "\nBooking cancelled."
            )

        # view booking
        elif choice == "3":

            booking_id = input(
                "Booking ID: "
            )

            event = system.view_booking(
                booking_id
            )

            event.display_details()

        # upcming bookings
        elif choice == "4":

            bookings = (
                system.list_upcoming_bookings()
            )

            if not bookings:
                print(
                    "\nNo upcoming bookings."
                )

            else:

                print(
                    "\nUpcoming Bookings"
                )
                print("-" * 50)

                for event in bookings:

                    print(
                        f"[{event.booking_id}] "
                        f"{event.start_datetime.strftime('%Y-%m-%d %H:%M')} | "
                        f"{event.event_name} | "
                        f"Host: {event.host_name}"
                    )

        # booking by host
        elif choice == "5":

            host_name = input(
                "Host name: "
            )

            bookings = (
                system.list_bookings_by_host(
                    host_name
                )
            )

            if not bookings:
                print(
                    "\nNo bookings found."
                )

            else:

                for event in bookings:
                    event.display_details()

        # exit
        elif choice == "6":

            print(
                "\nGoodbye!"
            )

            break

        else:
            print(
                "\nPlease enter a valid option."
            )

    # catch invalid dates or times
    except ValueError:
        print(
            "\nInvalid date, time, or number format."
        )

    # catch all custom booking exceptions
    except BookingError as e:
        print(f"\n {e}")

    # catch anything unexpected
    except Exception:
        print(
            "\nUnexpected error occurred."
        )