from typing import Optional
from uuid import UUID

from BookingSystem import BookingSystem
from Event import Event
from utils import parse_start_datetime, try_cast_to_int


def print_main_menu() -> None:
    """Print the main menu options to the console."""
    print("==============================")
    print("    Event Booking System")
    print("==============================")
    print("[1] Book an event")
    print("[2] Cancel a booking")
    print("[3] View a booking")
    print("[4] List upcoming bookings")
    print("[5] List bookings by host")
    print("[6] Quit")


if __name__ == "__main__":
    # Shared booking system instance used across all menu actions
    booking_system: BookingSystem = BookingSystem()

    while True:
        print_main_menu()

        try:
            choice: Optional[int] = try_cast_to_int("\n> ")
        except Exception as e:
            print(e)
            continue

        match choice:
            case 1:
                try:
                    event_name: str = input("Event name: ")
                    host_name: str = input("Host name: ")
                    start_date: str = input("Start date (YYYY-MM-DD): ")
                    start_time: str = input("Start time (HH:MM): ")
                    duration_in_minutes: Optional[int] = try_cast_to_int(
                        "Duration (minutes): "
                    )
                    if duration_in_minutes:
                        event: Event = Event(
                            event_name,
                            host_name,
                            parse_start_datetime(start_date, start_time),
                            duration_in_minutes,
                        )
                        booking_system.book_event(event)
                except Exception as e:
                    print(e)
            case 2:
                try:
                    booking_id: UUID = UUID(input("Enter booking id to cancel: "))
                    booking_system.cancel_booking(booking_id)
                except Exception as e:
                    print(e)
            case 3:
                try:
                    booking_id: UUID = UUID(input("Enter booking id to view details: "))
                    booking_system.view_booking(booking_id)
                except Exception as e:
                    print(e)
            case 4:
                pass
            case 5:
                pass
            case 6:
                # Exit the application
                break
            case _:
                print("Invalid choice! Try again...")
