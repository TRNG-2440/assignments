
from datetime import datetime
from exceptions import InvalidBookingError, BookingError
from booking_system import BookingSystem

def prompt_int(prompt_text):
    while True:
        try:
            raw = input(prompt_text).strip()
        except EOFError:
            return None
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def prompt_datetime(date_prompt, time_prompt):
    while True:
        try:
            date_str = input(date_prompt).strip()
            time_str = input(time_prompt).strip()
        except EOFError:
            raise InvalidBookingError("Input ended unexpectedly. Booking cancelled.")
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            print(" Invalid date/time format. Please use YYYY-MM-DD and HH:MM.\n")


def print_header():
    print("=" * 30)
    print("    Event Booking System")
    print("=" * 30)
    print()
    print("[1] Book an event")
    print("[2] Cancel a booking")
    print("[3] View a booking")
    print("[4] List upcoming bookings")
    print("[5] List bookings by host")
    print("[6] Quit")
    print()


def handle_book_event(system):
    print()
    try:
        name = input("Event name: ").strip()
        host = input("Host name: ").strip()
        start_dt = prompt_datetime("Start date (YYYY-MM-DD): ", "Start time (HH:MM): ")
        duration = prompt_int("Duration (minutes): ")
    except EOFError:
        print("\n InvalidBookingError: Input ended unexpectedly. Booking cancelled.")
        return
    except BookingError as exc:
        print(f"\n {type(exc).__name__}: {exc}")
        return

    if duration is None:
        print("\n InvalidBookingError: Duration is required.")
        return

    try:
        event = system.book_event(name, host, start_dt, duration)
        print("\n Booking confirmed!")
        print(f"   Booking ID : {event.booking_id}")
        print(f"   Event      : {event.name}")
        print(f"   Host       : {event.host}")
        print(f"   When       : {event.start_datetime.strftime('%Y-%m-%d')} at "
              f"{event.start_datetime.strftime('%H:%M')} ({event.duration_minutes} min)")
    except BookingError as exc:
        print(f"\n {type(exc).__name__}: {exc}")


def handle_cancel_booking(system):
    print()
    try:
        booking_id = input("Booking ID: ").strip()
    except EOFError:
        print("\n InvalidBookingError: Input ended unexpectedly.")
        return
    try:
        event = system.cancel_booking(booking_id)
        print(f"\n Booking {event.booking_id} (\"{event.name}\") has been cancelled.")
    except BookingError as exc:
        print(f"\n {type(exc).__name__}: {exc}")


def handle_view_booking(system):
    print()
    try:
        booking_id = input("Booking ID: ").strip()
    except EOFError:
        print("\n InvalidBookingError: Input ended unexpectedly.")
        return
    try:
        event = system.get_booking(booking_id)
        print("\nBooking Details")
        print("-" * 30)
        print(f"  Booking ID : {event.booking_id}")
        print(f"  Event      : {event.name}")
        print(f"  Host       : {event.host}")
        print(f"  Start      : {event.start_datetime.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Duration   : {event.duration_minutes} min")
        print(f"  End        : {event.end_datetime.strftime('%Y-%m-%d %H:%M')}")
    except BookingError as exc:
        print(f"\n {type(exc).__name__}: {exc}")


def handle_list_upcoming(system):
    print()
    upcoming = system.list_upcoming_bookings()
    print("Upcoming Bookings")
    print("-" * 30)
    if not upcoming:
        print("  No upcoming bookings found.")
    else:
        for event in upcoming:
            print(f"  {event}")
    print("-" * 30)
    print(f"{len(upcoming)} upcoming booking(s) found.")


def handle_list_by_host(system):
    print()
    try:
        host_name = input("Host name: ").strip()
    except EOFError:
        print("\n InvalidBookingError: Input ended unexpectedly.")
        return
    bookings = system.list_bookings_by_host(host_name)
    print(f"\nBookings for host '{host_name}'")
    print("-" * 30)
    if not bookings:
        print("  No bookings found for this host.")
    else:
        for event in bookings:
            print(f"  {event}")
    print("-" * 30)
    print(f"{len(bookings)} booking(s) found.")


def main():
    system = BookingSystem()

    while True:
        print_header()
        try:
            choice = input("> ").strip()
        except EOFError:
            print("\nGoodbye!")
            break
        print()

        if choice == "1":
            handle_book_event(system)
        elif choice == "2":
            handle_cancel_booking(system)
        elif choice == "3":
            handle_view_booking(system)
        elif choice == "4":
            handle_list_upcoming(system)
        elif choice == "5":
            handle_list_by_host(system)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 1-6.")

        print("\n" + "-" * 30 + "\n")


if __name__ == "__main__":
    main()
