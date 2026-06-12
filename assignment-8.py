import datetime as dt
import uuid


class BookingError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.message = message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class TimeSlotTakenError(BookingError):
    def __init__(self, message: str) -> None:

        super().__init__(message)


class BookingWindowExceededError(BookingError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, message: str) -> None:

        super().__init__(message)


class EventNotFoundError(BookingError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidBookingError(BookingError):
    def __init__(self, message: str) -> None:

        super().__init__(message)


class Event:

    def __init__(
        self, name: str, start: dt.datetime, duration: dt.timedelta, host: str) -> None:
        self.name = name
        self.start = start
        self.duration = duration
        self.host = host
        self.booking_id: str = str(uuid.uuid4())

    def __str__(self) -> str:

        return f"{self.name} on {self.start.date()} at {self.start.time()} for {self.duration} hosted by {self.host} (Booking ID: {self.booking_id})"


class BookingSystem:

    def __init__(self) -> None:
        self.events: dict[str, Event] = {}

    def bookEvent(self) -> None:
        print("Enter Details\n" + "-" * 13)
        name = input("Event name: ").strip()

        host = input("Host name: ").strip()
        date_str = input("Start date (YYYY-MM-DD): ").strip()
        time_str = input("Start time (HH:MM): ").strip()

        try:
            duration_mins = int(input("Duration (minutes): ").strip())

            start_datetime = dt.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            duration_timedelta = dt.timedelta(minutes=duration_mins)
            end_datetime = start_datetime + duration_timedelta

            if start_datetime < dt.datetime.now():

                raise InvalidBookingError("Cannot book an event in the past.")

            for existing_event in self.events.values():
                exist_start = existing_event.start

                exist_end = existing_event.start + existing_event.duration

                if (start_datetime < exist_end and end_datetime > exist_start):
                    raise TimeSlotTakenError(f"Time slot conflicts with existing event: '{existing_event.name}'.")

            new_event = Event(name, start_datetime, duration_timedelta, host)
            self.events[new_event.booking_id] = new_event

            print(f"\nEvent sucessfully created!\n{new_event}")

        except ValueError as e:
            raise InvalidBookingError(f"Please fix the input format: {e}")

    def cancelEvent(self) -> None:

        booking_id = input("Please enter the Booking ID to cancel: ").strip()

        if booking_id not in self.events:
            raise EventNotFoundError(f"No event has been found with that Booking ID: {booking_id}")

        event = self.events[booking_id]
        time_until_event = event.start - dt.datetime.now()

        if time_until_event < dt.timedelta(hours=2):
            raise LateCancellationError(f"Cannot cancel '{event.name}'. Less than 2 hours notice remaining.")

        del self.events[booking_id]
        print(f"Successfully cancelled event: {event.name}")

    def viewBooking(self) -> None:
        booking_id = input("Enter Booking ID to lookup: ").strip()

        if booking_id not in self.events:
            raise EventNotFoundError(f"No event has been found with Booking ID: {booking_id}")

        print(f"\nFound the Booking Details:\n{self.events[booking_id]}")

    def listUpcoming(self) -> None:
        now = dt.datetime.now()
        upcoming = [e for e in self.events.values() if e.start >= now]

        if not upcoming:
            print("\nNo upcoming events scheduled.")
            return

        print("\n=== UPCOMING EVENTS ===")
        for event in sorted(upcoming, key=lambda x: x.start):
            print(event)

    def list_by_host(self) -> None:
        host_name = input("Enter host name: ").strip().lower()
        matches = [e for e in self.events.values() if e.host.lower() == host_name]

        if not matches:
            print(f"\nNo events found hosted by: {host_name}")
            return

        print(f"\n=== EVENTS HOSTED BY {host_name.upper()} ===")
        for event in matches:
            print(event)


def main():
    system = BookingSystem()
    is_running = True

    print("-" * 30)
    print("Event Booking System")
    print("-" * 30)

    while is_running:
        print("\n[1] Create a Booking")
        print("[2] Cancel a Booking")
        print("[3] View a Booking by ID")
        print("[4] List All Upcoming Bookings")
        print("[5] List Bookings by Host")
        print("[6] Quit")

        choice = input("\n> ").strip()

        try:
            match choice:
                case "1":
                    system.bookEvent()
                case "2":
                    system.cancelEvent()
                case "3":
                    system.viewBooking()
                case "4":
                    system.listUpcoming()
                case "5":
                    system.list_by_host()
                case "6":
                    print("\nGoodbye!")
                    is_running = False
                case _:
                    print("Please select a valid option")

        except BookingError as e:
            print(f"\n{e}")
        except Exception as e:
            print(f"\nAn unexpected structural error has occured!  {e}")


if __name__ == "__main__":
    main()