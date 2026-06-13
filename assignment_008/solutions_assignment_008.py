from datetime import datetime, timedelta

class BookingError(Exception):
    pass

class TimeSlotTakenError(BookingError):
    pass

class BookingWindowExceededError(BookingError):
    pass

class LateCancellationError(BookingError):
    pass

class EventNotFoundError(BookingError):
    pass

class InvalidBookingError(BookingError):
    pass

class Event:
    def __init__(self, booking_id, event_name, start_date, duration, host_name):
        self.booking_id = booking_id
        self.event_name = event_name
        self.start_date = start_date
        self.duration = duration
        self.host_name = host_name

class BookingSystem:
    def __init__(self):
        self.booking_id = 0
        self.bookings = []

    def IDGenerator(self):
        self.booking_id += 1
        return self.booking_id
    
    def BookEvent(self):
        event = []

        print("")
        name = input("Event Name: ")
        if name == "": raise InvalidBookingError("Fields cannot be empty.") 

        host = input("Host name: ")
        if host == "": raise InvalidBookingError("Fields cannot be empty.") 

        start = input("Start date (YYYY-MM-DD): ")
        if start == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            datetime.strptime(start, "%Y-%m-%d")
        except ValueError:
            raise InvalidBookingError("Start date needs to be in the format YYYY-MM-DD.")
        time = input("Start time (HH:MM): ")
        if time == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            raise InvalidBookingError("Start time needs to be in the format HH:MM.")    
        start_time = datetime.strptime(f"{start} {time}", "%Y-%m-%d %H:%M")
        if start_time < datetime.today(): raise InvalidBookingError("Time cannot be in the past.")

        duration = input("Duration (minutes): ")
        if duration == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            d = int(duration)
        except ValueError:
            raise InvalidBookingError("Duration must be in minutes.")
        if d <= 0: raise InvalidBookingError("Duration must be greater than 0.")

        end_time = start_time + timedelta(minutes=d)
        for e in self.bookings:
            e_d = int(e[4])
            e_end = e[3] + timedelta(minutes=e_d)
            if start_time < e_end and end_time > e[3]:
                raise TimeSlotTakenError(f"Conflict event ({e[1]} at {e[3].strftime('%Y-%m-%d %H:%M')} to {e_end.strftime('%Y-%m-%d %H:%M')}).") 

        event.append(self.IDGenerator())
        event.append(name)
        event.append(host)
        event.append(start_time)
        event.append(d)
        self.bookings.append(event)

        print("\nBooking confimed!")
        print(f"Booking ID : {event[0]}")
        print(f"Event Name : {event[1]}")
        print(f"Host Name  : {event[2]}")
        print(f"When       : {event[3].year}-{event[3].month:02d}-{event[3].day:02d} at {event[3].hour:02d}:{event[3].minute:02d} ({event[4]} min)")
        
    def CancelEvent(self):
        pass

    def ViewBooking(self):
        pass

    def ListUpcomingBookings(self):
        pass

    def ListBookingByHost(self):
        pass

def CLIMenu():
    booking_system = BookingSystem()
    bk_errors = BookingError()

    while True:
        print("==============================")
        print("     Event Booking System     ")
        print("==============================")
        print(" [1] Book an event")
        print(" [2] Cancel a booking")
        print(" [3] View a booking")
        print(" [4] List upcoming bookings")
        print(" [5] List bookings by host")
        print(" [6] Quit")
        inp = input("Enter an option to proceed (1, 2, 3, 4, 5, or 6): ")

        match inp:
            case "1":
                try:
                    booking_system.BookEvent()
                except (InvalidBookingError, TimeSlotTakenError) as e:
                    print(f"Error: {e}")
            case "6":
                print("Exiting now.")
                break

CLIMenu()