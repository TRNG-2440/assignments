from datetime import datetime, timedelta

# Menu options Dicts
main_menu_text ="========================\n" \
                "  Event Booking System  \n" \
                "========================\n"
main_menu_options = {0: "Quit", \
                     1: "Book an event", \
                     2: "Cancel a booking", \
                     3: "View a booking", \
                     4: "List upcoming bookings", \
                     5: "List bookings by host"}


###################################
# Custom items to help with Menus #
###################################

class MenuMachine():
    def __printOptions(self, menu_dict:dict):
        for key in menu_dict:
            print(f"[{key}] {menu_dict[key]}")
    
    def __validateUserInput(self, user_input, options:dict):
        try:
            user_input = int(user_input)
            return user_input in options
        except ValueError:
            return False

    def menu_with_input(self, menu_title:str, menu_dict:dict):
        while True:
            print(menu_title)
            self.__printOptions(menu_dict)
            user_in = input(f"\n>")
            hasUserInputValidOption = self.__validateUserInput(user_in, menu_dict)
            if hasUserInputValidOption == True:
                return int(user_in)
            else:
                print("Please input a valid option from the menu.")

###################################
# Required Classes for Assignment #
###################################

class BookingError(Exception):
    pass


class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start_time, end_time):
        message = (
            f"Time slot taken: '{event_name}' "
            f"({start_time} - {end_time}) conflicts with an existing booking."
        )
        super().__init__(message)
        self.event_name = event_name
        self.start_time = start_time
        self.end_time = end_time


class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_allowed_date):
        message = (
            f"Booking window exceeded: requested {requested_date}, "
            f"but latest allowed date is {max_allowed_date}."
        )
        super().__init__(message)
        self.requested_date = requested_date
        self.max_allowed_date = max_allowed_date


class LateCancellationError(BookingError):
    def __init__(self, event_start_time, cancellation_deadline):
        message = (
            f"Late cancellation: event starts at {event_start_time}. "
            f"Cancellation deadline was {cancellation_deadline}."
        )
        super().__init__(message)
        self.event_start_time = event_start_time
        self.cancellation_deadline = cancellation_deadline


class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        message = f"Event not found: booking ID '{booking_id}' does not exist."
        super().__init__(message)
        self.booking_id = booking_id


class InvalidBookingError(BookingError):
    def __init__(self, reason):
        message = f"Invalid booking: {reason}"
        super().__init__(message)
        self.reason = reason

class Event:
    def __init__(
        self,
        booking_id: str,
        event_name: str,
        start_time: datetime,
        duration_minutes: int,
        host_name: str
    ):
        if not event_name or not host_name:
            raise InvalidBookingError("Event name and host name are required")

        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0 minutes")

        if start_time < datetime.now():
            raise InvalidBookingError("Event cannot be scheduled in the past")

        self.booking_id = booking_id
        self.event_name = event_name
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.host_name = host_name

    def getEndTime(self) -> datetime:
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def toDict(self):
        return {
            "Booking ID": self.booking_id,
            "Event Name": self.event_name,
            "Host": self.host_name,
            "Start Time": self.start_time,
            "End Time": self.getEndTime(),
            "Duration (min)": self.duration_minutes
        }

    def __repr__(self):
        return (
            f"Event({self.booking_id}, {self.event_name}, "
            f"{self.start_time}, {self.duration_minutes}min, {self.host_name})"
        )

class BookingSystem():
    def __init__(self):
        self.bookings = []
        self.current_id = 1

    def _generateBookingId(self):
        booking_id = f"BK-{self.current_id:05d}"
        self.current_id += 1
        return booking_id

    def _findBooking(self, booking_id: str):
        for event in self.bookings:
            if event.booking_id == booking_id:
                return event
        raise EventNotFoundError(booking_id)

    def _checkOverlap(self, new_event: Event):
        new_start = new_event.start_time
        new_end = new_event.getEndTime()

        for event in self.bookings:
            existing_start = event.start_time
            existing_end = event.getEndTime()

            if new_start < existing_end and new_end > existing_start:
                raise TimeSlotTakenError(
                    event.event_name,
                    existing_start,
                    existing_end
                )

    def bookEvent(self, event_name, start_time, duration_minutes, host_name):
        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0")

        if start_time < datetime.now():
            raise InvalidBookingError("Event cannot start in the past")

        max_date = datetime.now() + timedelta(days=90)
        if start_time > max_date:
            raise BookingWindowExceededError(start_time, max_date)

        temp_event = Event(
            self._generateBookingId(),
            event_name,
            start_time,
            duration_minutes,
            host_name
        )

        self._checkOverlap(temp_event)

        self.bookings.append(temp_event)
        return temp_event

    def cancelBooking(self, booking_id: str):
        event = self._findBooking(booking_id)

        cancellation_deadline = event.start_time - timedelta(hours=24)

        if datetime.now() > cancellation_deadline:
            raise LateCancellationError(event.start_time, cancellation_deadline)

        self.bookings.remove(event)
        return True

    def viewBooking(self, booking_id: str):
        return self._findBooking(booking_id)

    def listUpcomingBookings(self):
        now = datetime.now()
        upcoming = [b for b in self.bookings if b.start_time > now]
        return sorted(upcoming, key=lambda x: x.start_time)

    def listBookingsByHost(self, host_name: str):
        host_name = host_name.lower()
        return [
            b for b in self.bookings
            if b.host_name.lower() == host_name
        ]

# This will be main
def runTheBooker():
    menu = MenuMachine()
    system = BookingSystem()

    while True:
        choice = menu.menu_with_input(main_menu_text, main_menu_options)
        if choice == 0:
            break
        
        elif choice == 1: # Book an event
            try:
                event_name = input("Event Name: ").strip()
                host_name = input("Host Name: ").strip()
                start_raw = input("Start Time (YYYY-MM-DD HH:MM): ").strip()
                try:
                    start_time = datetime.strptime(start_raw, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD HH:MM")
                    continue
                duration_raw = input("Duration (minutes): ").strip()
                if not duration_raw.isdigit():
                    print("Duration must be a number.")
                    continue
                duration_minutes = int(duration_raw)

                event = system.bookEvent(
                    event_name,
                    start_time,
                    duration_minutes,
                    host_name
                )

                print("\nBooking confirmed:")
                for k, v in event.toDict().items():
                    print(f"{k}: {v}")

            except BookingError as e:
                print(f"\nBooking error: {e}")

        elif choice == 2: # Cancel a booking
            try:
                booking_id = input("Enter Booking ID to cancel: ").strip()
                if not booking_id:
                    print("Booking ID is required.")
                    continue
                result = system.cancelBooking(booking_id)
                if result:
                    print(f"\nBooking '{booking_id}' cancelled successfully.")
            except BookingError as e:
                print(f"\nCancellation error: {e}")

        elif choice == 3: # View a booking
            try:
                booking_id = input("Enter Booking ID: ").strip()
                if not booking_id:
                    print("Booking ID is required.")
                    continue
                event = system.viewBooking(booking_id)
                print("\nBooking Details:")
                for k, v in event.toDict().items():
                    print(f"{k}: {v}")
            except BookingError as e:
                print(f"\nLookup error: {e}")

        elif choice == 4: # List upcoming bookings
            upcoming = system.listUpcomingBookings()

            if not upcoming:
                print("\nNo upcoming bookings found.")
                continue

            print("\nUpcoming Bookings:")
            for event in upcoming:
                print("-" * 40)
                for k, v in event.toDict().items():
                    print(f"{k}: {v}")

        elif choice == 5: # List bookings by host
            host_name = input("Enter Host Name: ").strip()

            if not host_name:
                print("Host name is required.")
                continue

            bookings = system.listBookingsByHost(host_name)

            if not bookings:
                print(f"\nNo bookings found for host '{host_name}'.")
                continue

            print(f"\nBookings for host '{host_name}':")
            for event in bookings:
                print("-" * 40)
                for k, v in event.toDict().items():
                    print(f"{k}: {v}")
                    
                    
runTheBooker()