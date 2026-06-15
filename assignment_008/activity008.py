import uuid
import datetime as dt
import re

class BookingError(Exception):
    """base booking error"""
    def __init__(self, message="a booking error has occurred"):
        super().__init__(message)

class TimeSlotTakenError(BookingError):
    """
    raised when a requested time slot is already booked. Should 
    include the conflicting event name and time in its message
    """
    def __init__(self, message="there is another event booked during that time"):
        super().__init__(message)

class BookingWindowExceededError(BookingError):
    """
    raised when a user attempts to book an event too far in advance 
    beyond a defined maximum window (e.g. 90 days). Should include 
    the requested date and the maximum allowed date in its message.
    """
    def __init__(self, message="event cannot be booked more than 90 days from today"):
        super().__init__(message)

class LateCancellationError(BookingError):
    """
    raised when a user attempts to cancel a booking within a restricted 
    window before the event (e.g. less than 24 hours). Should include 
    the event time and the cancellation deadline in its message.
    """
    def __init__(self, message="cannot cancel within 24h of event"):
        super().__init__(message)

class EventNotFoundError(BookingError):
    """
    raised when a lookup is performed for a 
    booking ID or event that does not exist
    """
    def __init__(self, message="No event found with that ID"):
        super().__init__(message)

class InvalidBookingError(BookingError):
    """
    raised for general validation failures such as a booking made 
    in the past, an invalid duration, or a missing required field.
    """
    def __init__(self, reason, message="Booking cannot be completed because"):
        super().__init__(f"{message} {reason}")

class Event:
    def __init__(self, event_name, start_date, start_time, dur, host_name):
        self.event_name = event_name
        self.start_date = start_date
        self.start_time = start_time
        self.duration = dur
        self.host_name = host_name
        self.booking_id = str(uuid.uuid1())

    def details(self):
        a = f"booking id  : {self.booking_id}\n"
        b = f"event       : {self.event_name}\n"
        c = f"host        : {self.host_name}\n"
        d = f"When        : {self.start_date} at {self.start_time} ({self.duration})\n"
        return a + b + c + d

class BookingSystem:
    def __init__(self):
        self.events = {}
        self.main_options = ["Book an event",
                             "Cancel a booking",
                             "View a booking",
                             "List upcoming bookings",
                             "List bookings by host"]
    

    
    def book_event(self):
        # may not start in the past
        # within 90 days from today
        # cannot overlap time range
        event_name = input("Event name: ")
        host_name = input("host name: ")
        start_date = dt.datetime.fromisoformat(input("start date (yyyy-mm-dd): "))
        start_time = dt.time.fromisoformat(input("start time (hh:mm): "))
        dur = dt.timedelta(minutes=int(input("duration (min): ")))

        missing = not bool(event_name and host_name and start_date and start_time and dur)

        if missing:
            raise InvalidBookingError("missing required field")
        if dur < dt.timedelta(minutes=0):
            raise InvalidBookingError("duration cannot be negative")
        if start_date < dt.datetime.today():
            raise InvalidBookingError("event cannot be booked before the current date")
        for event in self.events.values():
            # FIX need to solve converting time object and timedelta object
            if start_date == event.start_date:
                if start_time > event.start_time and start_time < convert_add_time(event.start_time, event.duration):
                    raise TimeSlotTakenError()
                if convert_add_time(start_time, dur) > event.start_time and convert_add_time(start_time, dur) < convert_add_time(event.start_time, event.duration):
                    raise TimeSlotTakenError()
                if event.start_time > start_time and event.start_time < convert_add_time(start_time, dur):
                    raise TimeSlotTakenError()
                if convert_add_time(event.start_time, event.duration) > start_time and convert_add_time(event.start_time, event.duration) < convert_add_time(start_time, dur):
                    raise TimeSlotTakenError()
        if start_date > dt.datetime.today() + dt.timedelta(days=90):
            raise BookingWindowExceededError()
        
        event = Event(event_name, start_date, start_time, dur, host_name)

        self.events[event.booking_id] = event

    def cancel_event(self):
        # cannot cancel within 24h
        id = input("booking id: ")
        try:
            event = self.events[id]
        except KeyError:
            raise EventNotFoundError()
        if dt.timedelta(days= dt.datetime.today() - event.start_date) < 1:
            raise LateCancellationError()

    def view_booking(self):
        # raise EventNotFoundError if event not found for ID
        id = input("booking id: ")
        try:
            event = self.events[id]
        except KeyError:
            raise EventNotFoundError()
        print(event.details())

    def list_upcoming(self):
        for event in self.events.values():
            if event.start_date > dt.datetime.today():
                print(event.details())

    def list_host(self):
        exp = input("host name: ")
        for event in self.events.values():
            if re.search(exp.lower(), event.host_name.lower()):
                print(event.details())

    def run(self):
        w = 31
        border = "=" * w + "\n"
        title = "Event Booking System"
        banner = f"{border}{title: ^{w}}\n{border}"
        print(banner)
        while True:
            print_menu(*self.main_options)
            user_selection = get_selection(len(self.main_options))
            match user_selection:
                case 1: # Book event
                    try:
                        self.book_event()
                    except BookingError as e:
                        print(e)
                case 2: # cancel booking
                    try:
                        self.cancel_event()
                    except BookingError as e:
                        print(e)
                case 3: # view booking
                    try:
                        self.view_booking()
                    except BookingError as e:
                        print(e)
                case 4: # list upcoming bookings
                    self.list_upcoming()
                case 5: # list bookings by host
                    try:
                        self.list_host()
                    except BookingError as e:
                        print(e)
                case 0: # exit
                    print("exiting...\nGoodbye")
                    return user_selection

def convert_add_time(time_ob=None, datetime_ob=None):
    return (dt.datetime.combine(dt.date(1,1,1),time_ob) + datetime_ob).time()

def print_menu(*args:str) -> None:
    w = 31
    """
    print main menu from list
    """
    print()
    for idx, item in enumerate(args, 1):
        print(f"[{idx}] {item:.>{w}}")
    print("[0]" + "." * (w-4) + " exit")

def get_selection(lim:int = 0) -> int:
    """
    get selection from user, return int within limit
    - repeat on ValueError
    """
    valid = False
    while not valid:
        try:
            sel = int(input(f"> "))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        print()
        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too high")
                valid = False
            case _:
                valid = True
    return sel

if __name__ == "__main__":
    bs = BookingSystem()
    bs.run()