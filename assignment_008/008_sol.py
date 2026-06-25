#Assignment 8 Solution
#Alex Tran
# Python Booking Event System




from datetime import datetime, timedelta
import uuid


#Define exceptions and errors


#Set the errors we can expect to encounter

class BookingError(Exception):
    """Base class for all booking-related errors."""
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, conflicting_event, requested_start):
        message = (
            f'Time slot unavailable — "{conflicting_event.name}" is already scheduled '
            f'from {conflicting_event.start_time.strftime("%H:%M")} '
            f'to {conflicting_event.end_time.strftime("%H:%M")} '
            f'on {conflicting_event.start_time.strftime("%Y-%m-%d")}.'
        )
        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, latest_allowed_date):
        message = (
            f"Requested date {requested_date.strftime('%Y-%m-%d')} exceeds the maximum "
            f"booking window. Latest allowed: {latest_allowed_date.strftime('%Y-%m-%d')}."
        )
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event):
        deadline = event.start_time - timedelta(hours=24)
        message = (
            f'Cannot cancel "{event.name}" — the event starts at '
            f'{event.start_time.strftime("%H:%M")} on {event.start_time.strftime("%Y-%m-%d")} '
            f'and the cancellation deadline has passed. Deadline was '
            f'{deadline.strftime("%Y-%m-%d %H:%M")}.'
        )
        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        super().__init__(f"No booking found with ID: {booking_id}")


class InvalidBookingError(BookingError):
    pass


#Event Class to be booked in the system
class Event:
    def __init__(self, name, start_time, duration_minutes, host_name):
        self.name = name
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.host_name = host_name
        self.booking_id = self.generate_booking_id()

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def generate_booking_id(self):
        return "BKG-" + str(uuid.uuid4())[:4].upper()

    def __str__(self):
        return (
            f"[{self.booking_id}] {self.start_time.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.name} ({self.duration_minutes} min) | Host: {self.host_name}"
        )


#Booking Systems Class

class BookingSystem:
    def __init__(self):
        self.bookings = {}

    #book event
    def book_event(self, name, start_time, duration_minutes, host_name):
        self.validate_booking(name, start_time, duration_minutes, host_name)

        new_event = Event(name, start_time, duration_minutes, host_name)
        self.bookings[new_event.booking_id] = new_event

        return new_event
    
    #validation method
    def validate_booking(self, name, start_time, duration_minutes, host_name):
        now = datetime.now()

        if not name.strip():
            raise InvalidBookingError("Event name is required.")

        if not host_name.strip():
            raise InvalidBookingError("Host name is required.")

        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0 minutes.")

        if start_time < now:
            raise InvalidBookingError("Booking cannot start in the past.")

        latest_allowed = now + timedelta(days=90)

        if start_time > latest_allowed:
            raise BookingWindowExceededError(start_time, latest_allowed)

        new_end_time = start_time + timedelta(minutes=duration_minutes)

        for event in self.bookings.values():
            same_day = event.start_time.date() == start_time.date()

            overlaps = start_time < event.end_time and new_end_time > event.start_time

            if same_day and overlaps:
                raise TimeSlotTakenError(event, start_time)

    #Cancel booking
    def cancel_booking(self, booking_id):
        event = self.view_booking(booking_id)

        if datetime.now() > event.start_time - timedelta(hours=24):
            raise LateCancellationError(event)

        del self.bookings[booking_id]
        return event
    
    #view booking
    def view_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise EventNotFoundError(booking_id)

        return self.bookings[booking_id]
    
    #list upcoming bookings
    def list_upcoming_bookings(self):
        now = datetime.now()

        upcoming = [
            event for event in self.bookings.values()
            if event.start_time > now
        ]

        return sorted(upcoming, key=lambda event: event.start_time)

    def list_bookings_by_host(self, host_name):
        results = [
            event for event in self.bookings.values()
            if event.host_name.lower() == host_name.lower()
        ]

        return sorted(results, key=lambda event: event.start_time)


# ==============================
# CLI Helper Functions
# ==============================

def get_start_datetime():
    date_input = input("Start date (YYYY-MM-DD): ")
    time_input = input("Start time (HH:MM): ")

    try:
        return datetime.strptime(date_input + " " + time_input, "%Y-%m-%d %H:%M")
    except ValueError:
        raise InvalidBookingError("Invalid date or time format.")


def print_booking(event):
    print(f"Booking ID : {event.booking_id}")
    print(f"Event      : {event.name}")
    print(f"Host       : {event.host_name}")
    print(
        f"When       : {event.start_time.strftime('%Y-%m-%d at %H:%M')} "
        f"({event.duration_minutes} min)"
    )


# ==============================
# CLI Menu
# ==============================

def main():
    system = BookingSystem()

    while True:
        print("\n==============================")
        print("    Event Booking System")
        print("==============================")
        print("[1] Book an event")
        print("[2] Cancel a booking")
        print("[3] View a booking")
        print("[4] List upcoming bookings")
        print("[5] List bookings by host")
        print("[6] Quit")

        choice = input("> ")

        try:
            if choice == "1":
                name = input("Event name: ")
                host = input("Host name: ")
                start_time = get_start_datetime()

                try:
                    duration = int(input("Duration (minutes): "))
                except ValueError:
                    raise InvalidBookingError("Duration must be a number.")

                event = system.book_event(name, start_time, duration, host)

                print("\n✅ Booking confirmed!")
                print_booking(event)

            elif choice == "2":
                booking_id = input("Booking ID: ").strip().upper()
                event = system.cancel_booking(booking_id)

                print(f"\n✅ Booking cancelled: {event.name}")

            elif choice == "3":
                booking_id = input("Booking ID: ").strip().upper()
                event = system.view_booking(booking_id)

                print("\nBooking Details")
                print("------------------------------")
                print_booking(event)

            elif choice == "4":
                bookings = system.list_upcoming_bookings()

                print("\nUpcoming Bookings")
                print("------------------------------")

                if not bookings:
                    print("No upcoming bookings found.")
                else:
                    for event in bookings:
                        print(event)

                    print(f"{len(bookings)} upcoming booking(s) found.")

            elif choice == "5":
                host = input("Host name: ")
                bookings = system.list_bookings_by_host(host)

                print("\nBookings by Host")
                print("------------------------------")

                if not bookings:
                    print("No bookings found for this host.")
                else:
                    for event in bookings:
                        print(event)

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid menu option. Please choose 1-6.")

        except BookingError as error:
            print(f"\n❌ BookingError: {error}")


if __name__ == "__main__":
    main()