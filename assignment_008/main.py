from datetime import datetime

from booking_system import BookingSystem
from exceptions import BookingError


def parse_datetime():

    date_str = input("Start date (YYYY-MM-DD): ")
    time_str = input("Start time (HH:MM): ")

    return datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M"
    )


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

        choice = input("\nPlease select an option: ")

        try:

            # BOOK
            if choice == "1":

                name = input("Event name: ")
                host = input("Host name: ")

                start_dt = parse_datetime()

                duration = int(input("Duration (minutes): "))

                event = system.book_event(
                    name,
                    host,
                    start_dt,
                    duration
                )

                print("\n Booking confirmed!")
                print(event.get_details())

            # CANCEL
            elif choice == "2":

                if len(system.events) == 0:
                    print("\nNo bookings found.")
                    continue

                booking_id = input("Booking ID: ")

                system.cancel_booking(booking_id)

                print(f"Booking {booking_id} cancelled.")

            # VIEW
            elif choice == "3":

                if len(system.events) == 0:
                    print("\nNo bookings found.")
                    continue

                booking_id = input("Booking ID: ")

                event = system.view_booking(booking_id)

                print(event.get_details())

            # UPCOMING 
            elif choice == "4":

                events = system.list_upcoming()

                print("\nUpcoming Bookings")
                print("------------------------------")

                for e in events:
                    print(e.get_details())

                print(f"\n{len(events)} upcoming booking(s).")

            # BY HOST
            elif choice == "5":

                if len(system.events) == 0:
                    print("\nNo bookings found.")
                    continue

                host = input("Host name: ")

                events = system.list_by_host(host)

                for e in events:
                    print(e.get_details())

            # QUIT
            elif choice == "6":
                print("\nYou are now leaving the Event Booking System, Goodbye!\n")
                break

            else:
                print("Invalid menu option.")

        except BookingError as e:
            print(f"\n BookingError: {e}")

        except ValueError:
            print("\n Invalid input format (check numbers/dates).")


if __name__ == "__main__":
    main()