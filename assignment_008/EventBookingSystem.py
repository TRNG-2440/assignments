import datetime
import string
import random

class BookingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, time):
        super().__init__(f"{event_name} at {time} is already booked.")

class BookingWindowExceededError(BookingError):
    def __init__(self, amount):
        super().__init__(f"Cannot book more than {amount} days in advance.")

class LateCancellationError(BookingError):
    def __init__(self):
        super().__init__(f"Cannot cancel less than 24 hours before your event.")

class EventNotFoundError(BookingError):
    def __init__(self):
        super().__init__("Event was not found.")

class InvalidBookingError(BookingError):
    def __init__(self, message):
        super().__init__(message)

class Event:
    def __init__(self, name, start, duration, host_name, id_number):
        self.name = name
        self.start = start
        self.duration = duration
        self.host_name = host_name
        self.id_number = id_number
        print(self.display_details())

    def display_details(self):
        return (f"Booking ID: {self.id_number}\nEvent: {self.name}\nHost: {self.host_name}\n"
                f"When: {self.start.date()} at {self.start.time()} ({self.duration} minutes)")
        

class BookingSystem: 
    events = []

    def book_event(self, name, start, duration, host_name): 
        id_number = self.random_id()
        if (not (name or start or duration or host_name)):
            raise InvalidBookingError ("An input field was not filled in.")
        if duration <= 0:
            raise InvalidBookingError ("Duration has to be a positive whole number greater than 0")
        if start.date() < datetime.date.today():
            raise InvalidBookingError ("Date needs to be in the future.")
        if (start > datetime.datetime.now() + datetime.timedelta(days=90)):
            raise BookingWindowExceededError (90)
        
        new_end = start + datetime.timedelta(minutes=duration)
        for event in self.events:
            end = event.start + datetime.timedelta(minutes=event.duration)
            if start < end and new_end > event.start:
                raise TimeSlotTakenError (event.name, event.start)
        
        self.events.append(Event(name, start, duration, host_name, id_number))

    def cancel_event(self, id_number):  
        event = self.find_booking(id_number)
        if event.start - datetime.timedelta(hours=24) < datetime.datetime.now():
            raise LateCancellationError
        
        self.events.remove(event)
        return event.name

    def find_booking(self, id_number): 
        for event in self.events:
            if (event.id_number == id_number):
                return event
            
        raise EventNotFoundError
            
    def list_upcoming(self): 
        sorted_events = sorted(self.events, key=lambda event: event.start)
        flag = 0
        for event in sorted_events:
            if (datetime.datetime.now() < event.start):
                flag = 1
                print(event.display_details())

        if (not flag):
            raise BookingError("No upcoming events: ")

    def list_by_host(self, host_name): 
        flag = 0
        for event in self.events:
            if (event.host_name.lower() == host_name.lower()):
                flag = 1
                print(event.display_details())

        if (not flag):
            raise BookingError(f"No events hosted by {host_name}")
                
    def random_id(self):
        chars = string.ascii_uppercase + string.digits
        new_id = ""
        try: 
            while True:
                for x in range (6):
                    new_id += random.choice(chars)
                self.find_booking(new_id)
        except EventNotFoundError:
            return new_id
                
booking_system = BookingSystem()

print ("Event Booking System\n")

def string_to_datetime(date_str, time_str):
    date_list = str.split(date_str, "-")
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    time_list = str.split(time_str, ":")
    hour = int(time_list[0])
    minute = int(time_list[1])
    return datetime.datetime(year, month, day, hour, minute)

def book_event(): # Exceptions!
    name = input("Event name: ")
    host_name = input("Host name: ")
    start_date_str = input("Start date (YYYY-MM-DD): ")
    start_time_str = input("Start time (HH:MM): ")
    start = string_to_datetime(start_date_str, start_time_str)
    duration = int(input("Duration (minutes): "))
    booking_system.book_event(name, start, duration, host_name)

def cancel_event(): 
    id_number = input("Enter the booking ID: ")
    print (f"{booking_system.cancel_event(id_number)} successfully cancelled!")

def view_booking(): 
    id_number = input("Enter the booking ID: ")
    print (booking_system.find_booking(id_number).display_details())

def list_upcoming(): 
    booking_system.list_upcoming()

def list_by_host():
    host = input("Enter the host name: ")
    booking_system.list_by_host(host)
    
while True:
    try: 
        print ("1. Book an event\n2. Cancel a booking\n3. View a booking\n4. List upcoming bookings\n" \
        "5. List bookings by host\n6. Quit")
        choice = input("Choose an option: ")

        match choice:
            case "1":
                book_event()
            case "2":
                cancel_event()
            case "3":
                view_booking()
            case "4":
                list_upcoming()
            case "5": 
                list_by_host()
            case "6":
                break
            case _:
                raise Exception ("Invalid Input")
            
    except TypeError:
        print("Input has to be a whole number.")
    except Exception as e:
        print(e)