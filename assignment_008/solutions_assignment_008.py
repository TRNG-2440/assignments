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

class EventFullError(BookingError):
    pass

def LogError(e):
    with open("booking_errors.log", "a") as file:
        file.write(f"{datetime.now()}, {type(e).__name__}, {e}\n")
    
class Event:
    def __init__(self, booking_id, event_name, host_name, start_date, duration, capacity):
        self.booking_id = booking_id
        self.event_name = event_name
        self.host_name = host_name
        self.start_date = start_date
        self.duration = duration
        self.capacity = capacity
        self.curr_cap = capacity
class BookingSystem:
    def __init__(self):
        self.booking_id = 0
        self.bookings = []
        
    def IDGenerator(self):
        self.booking_id += 1
        return str(self.booking_id)
    
    def BookEvent(self):
        # event name validation
        name = input("Event Name: ")
        if name == "": raise InvalidBookingError("Fields cannot be empty.") 

        # host name validation
        host = input("Host name: ")
        if host == "": raise InvalidBookingError("Fields cannot be empty.") 

        # start time validation
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

        # start time must be in future
        if start_time < datetime.today(): raise InvalidBookingError("Time cannot be in the past.")

        # start time can't be >90 days in advance
        allowed_max = datetime.today() + timedelta(days=90)
        if start_time > allowed_max: raise BookingWindowExceededError(f"Date {start_time} not allowed. Dates up to {allowed_max} are allowed.")

        # duration validation
        duration = input("Duration (minutes): ")
        if duration == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            d = int(duration)
        except ValueError:
            raise InvalidBookingError("Duration must be in minutes.")
        if d <= 0: raise InvalidBookingError("Duration must be greater than 0.")

        # no conflicting events
        end_time = start_time + timedelta(minutes=d)
        for e in self.bookings:
            e_end = e.start_date + timedelta(minutes=int(e.duration))
            if start_time < e_end and end_time > e.start_date:
                raise TimeSlotTakenError(f"Conflict event ({e.event_name} at {e.start_date.strftime('%Y-%m-%d %H:%M')} to {e_end.strftime('%Y-%m-%d %H:%M')}).") 

        # capacity validation
        cap = input("Capacity: ")
        if cap == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            c = int(cap)
        except ValueError:
            raise InvalidBookingError("Capacity must be a number.")
        if c <= 0: raise InvalidBookingError("Capacity must be greater than 0.")

        event = Event(self.IDGenerator(), name, host, start_time, d, c)
        self.bookings.append(event)

        print("\nBooking confirmed!")
        print(f"Booking ID : {event.booking_id}")
        print(f"Event Name : {event.event_name}")
        print(f"Host Name  : {event.host_name}")
        print(f"When       : {event.start_date.year}-{event.start_date.month:02d}-{event.start_date.day:02d} at {event.start_date.hour:02d}:{event.start_date.minute:02d} ({event.duration} min)")
        print(f"Capacity   : {event.curr_cap}/{event.capacity} available")
        print("")

    def BookExisting(self):
        inp = input("Enter booking ID: ")
        print("")
        if not self.bookings: raise EventNotFoundError("No events available.")

        for event in self.bookings:
            if event.booking_id == inp:
                if event.curr_cap - 1 < 0:
                    raise EventFullError(f"Event with booking ID {event.booking_id} is full. Unable to book.")
                elif event.start_date < datetime.today():
                    raise EventNotFoundError(f"Event has already passed.")
                else: 
                    event.curr_cap -= 1
                    print(f"Event with booking ID {event.booking_id} is now at {event.curr_cap}/{event.capacity} available capacity.\n")
                    return
        raise EventNotFoundError("Booking ID does not match any future events.")
    
    def BookRecurring(self):
        # check 1st and compare all existing until 1st < exsting.
        # if 1st < existing: switch to 2nd and compare, then move on and repeat.
        # if current booking time is an overlap, raise error (exits)
        # if all existing has been gone through or we are at the nth recurring entry, exit and add to booking
        
        # recurring validation
        rec = input("How many times will this event occur: ")
        if rec == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            r = int(rec)
        except ValueError:
            raise InvalidBookingError("Number must be a whole number.")
        if r <= 0: raise InvalidBookingError("Number must be greater than 0.")
        
        # start time validation
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

        # start time must be in future
        if start_time < datetime.today(): raise InvalidBookingError("Time cannot be in the past.")

        # start time can't be >90 days in advance
        allowed_max = datetime.today() + timedelta(days=90)
        if start_time > allowed_max: raise BookingWindowExceededError(f"Date {start_time} not allowed. Dates up to {allowed_max} are allowed.")

        # duration validation
        duration = input("Duration (minutes): ")
        if duration == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            d = int(duration)
        except ValueError:
            raise InvalidBookingError("Duration must be in minutes.")
        if d <= 0: raise InvalidBookingError("Duration must be greater than 0.")
        
        # create recurring dates
        dates = []
        for i in range(r):
            date = start_time + timedelta(weeks=i)
            if date > allowed_max:
                raise BookingWindowExceededError(f"Recurring date {start_time} not allowed. Dates up to {allowed_max} are allowed.")
            dates.append(date)
            
        # no conflicting events, check every recurring against existing
        for date in dates:
            for e in self.bookings:
                e_end = e.start_date + timedelta(minutes=int(e.duration))
                curr_end = date + timedelta(minutes=d)
                
                if date < e_end and curr_end > e.start_date:
                    raise TimeSlotTakenError(f"Conflict event ({e.event_name} at {e.start_date.strftime('%Y-%m-%d %H:%M')} to {e_end.strftime('%Y-%m-%d %H:%M')}).")             
        
        # event name validation
        name = input("Event Name: ")
        if name == "": raise InvalidBookingError("Fields cannot be empty.") 
        name += " (Recurring)"

        # host name validation
        host = input("Host name: ")
        if host == "": raise InvalidBookingError("Fields cannot be empty.") 

        # capacity validation
        cap = input("Capacity: ")
        if cap == "": raise InvalidBookingError("Fields cannot be empty.") 
        try:
            c = int(cap)
        except ValueError:
            raise InvalidBookingError("Capacity must be a number.")
        if c <= 0: raise InvalidBookingError("Capacity must be greater than 0.")

        for date in dates:
            event = Event(self.IDGenerator(), name, host, date, d, c)
            self.bookings.append(event)
        
            print("\nBooking confirmed!")
            print(f"Booking ID : {event.booking_id}")
            print(f"Event Name : {event.event_name}")
            print(f"Host Name  : {event.host_name}")
            print(f"When       : {event.start_date.year}-{event.start_date.month:02d}-{event.start_date.day:02d} at {event.start_date.hour:02d}:{event.start_date.minute:02d} ({event.duration} min)")
            print(f"Capacity   : {event.curr_cap}/{event.capacity} available")
            print("")
    
    def CancelEvent(self):
        inp = input("Enter booking ID: ")
        print("")
        if not self.bookings: raise EventNotFoundError("No events available.")
        
        # must be <24 hrs before event start
        for event in self.bookings:
            if event.booking_id == inp:
                allowed_max = event.start_date - timedelta(hours=24)
                if datetime.today() > allowed_max: raise LateCancellationError(f"Cancellation for {event.event_name} at {event.start_date} not allowed. Cancellations until {allowed_max} are allowed.")

                self.bookings.remove(event)
                print(f"Successfully cancelled event with booking ID: {inp}\n")
                return
        raise EventNotFoundError("Booking ID does not match any future events.")

    def ViewBooking(self):
        inp = input("Enter booking ID: ")
        print("")
        if not self.bookings: raise EventNotFoundError("No events available.")
        for event in self.bookings:
            if event.booking_id == inp:
                if event.start_date < datetime.today():
                    raise EventNotFoundError(f"Event has already passed.")
                print(f"Booking ID : {event.booking_id}")
                print(f"Event Name : {event.event_name}")
                print(f"Host Name  : {event.host_name}")
                print(f"When       : {event.start_date.year}-{event.start_date.month:02d}-{event.start_date.day:02d} at {event.start_date.hour:02d}:{event.start_date.minute:02d} ({event.duration} min)")
                print(f"Capacity   : {event.curr_cap}/{event.capacity} available")
                return
        raise EventNotFoundError("Booking ID does not match any future events.")

    def ListUpcomingBookings(self):
        if not self.bookings: raise EventNotFoundError("No events available.")
        counter = 0
        ordered = sorted(self.bookings, key=lambda x: x.start_date)
        for event in ordered:
            if event.start_date > datetime.today():
                counter += 1
                print(f"{counter}. Booking ID : {event.booking_id}")
                print(f"   Event Name : {event.event_name}")
                print(f"   Host Name  : {event.host_name}")
                print(f"   When       : {event.start_date.year}-{event.start_date.month:02d}-{event.start_date.day:02d} at {event.start_date.hour:02d}:{event.start_date.minute:02d} ({event.duration} min)")
                print(f"   Capacity   : {event.curr_cap}/{event.capacity} available")
                print("")
        if counter == 0: raise EventNotFoundError("No events available.")
        else: print(f"{counter} events found after today's date.")

    def ListBookingByHost(self):
        inp = input("Enter host name: ")
        print("")
        if not self.bookings: raise EventNotFoundError("No events available.")
        counter = 0
        for event in self.bookings:
            if event.host_name.lower() == inp.lower():
                counter += 1
                print(f"{counter}. Booking ID : {event.booking_id}")
                print(f"   Event Name : {event.event_name}")
                print(f"   Host Name  : {event.host_name}")
                print(f"   When       : {event.start_date.year}-{event.start_date.month:02d}-{event.start_date.day:02d} at {event.start_date.hour:02d}:{event.start_date.minute:02d} ({event.duration} min)")
                print(f"   Capacity   : {event.curr_cap}/{event.capacity} available")
                print("")
        if counter == 0: raise EventNotFoundError("Host name does not match any future events.")
        else: print(f"{counter} events found under {inp}.")
        
def CLIMenu():   
    booking_system = BookingSystem()

    while True:
        print("==============================")
        print("     Event Booking System     ")
        print("==============================")
        print(" [1] Book an event")
        print(" [2] Book an existing event")
        print(" [3] Book a recurring event")
        print(" [4] Cancel a booking")
        print(" [5] View a booking")
        print(" [6] List upcoming bookings")
        print(" [7] List bookings by host")
        print(" [8] Quit")
        inp = input("Enter an option to proceed (1, 2, 3, 4, 5, 6, 7, or 8): ")
        print("")
        
        match inp:
            case "1":
                try:
                    booking_system.BookEvent()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "2":
                try:
                    booking_system.BookExisting()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "3":
                try:
                    booking_system.BookRecurring()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "4":
                try:
                    booking_system.CancelEvent()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "5":
                try:
                    booking_system.ViewBooking()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "6":
                try:
                    booking_system.ListUpcomingBookings()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "7":
                try:
                    booking_system.ListBookingByHost()
                except BookingError as e:
                    LogError(e)
                    print(f"Error: {e}")
            case "8":
                print("Exiting now.")
                break

CLIMenu()