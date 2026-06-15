import random
from datetime import datetime, timedelta

class BookingError(Exception):
    pass

class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start_date, end_date):
        msg = f'Time slot unavailable, {event_name}\'s timeframe is already taken from {start_date.strftime("%H:%M")} to {end_date.strftime("%H:%M")} on {start_date.strftime("%Y-%m-%d")}.'
        super().__init__(msg)

class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_date):
        msg = f'Requested date {requested_date.strftime("%Y-%m-%d")} exceeds the maximum booking window ending at {max_date.strftime("%Y-%m-%d")}.'
        super().__init__(msg)

class LateCancellationError(BookingError):
    def __init__(self, event_name, start_datetime, deadline):
        msg = f'Cannot cancel "{event_name}", the event starts at {start_datetime.strftime("%Y-%m-%d %H:%M")} and the deadline ({deadline.strftime("%Y-%m-%d %H:%M")}) has passed.'
        super().__init__(msg)

class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        msg = f'Booking with ID {booking_id} not found'
        super().__init__(msg)

class InvalidBookingError(BookingError):
    pass


class Event:
    def __init__(self, name, host, start_datetime, duration_minutes):
        self.booking_id = f"BKG-{random.randint(1000, 9999)}"
        self.name = name
        self.host = host
        self.start_datetime = start_datetime
        self.duration_minutes = duration_minutes

    @property
    def end_datetime(self):
        return self.start_datetime + timedelta(minutes=self.duration_minutes)

    def __str__(self):
        return f"[{self.booking_id}] {self.start_datetime.strftime('%Y-%m-%d %H:%M')} | {self.name} ({self.duration_minutes} min) | Host: {self.host}"
    
class BookingSystem:
    def __init__(self):
        self.bookings = {}

    def book_event(self, name, host, start_datetime, duration_minutes):
        now = datetime.now()

        end = start_datetime + timedelta(minutes=duration_minutes)

        if duration_minutes <= 0:
            raise InvalidBookingError("Booking duration must be greater than zero minutes.")

        if start_datetime < now:
            raise InvalidBookingError("Cannot book an event in the past.")
            
        max_allowed_date = now + timedelta(days=90)
        if start_datetime > max_allowed_date:
            raise BookingWindowExceededError(start_datetime, max_allowed_date)
            
        for booking in self.bookings.values():
            if start_datetime < booking.end_datetime and end > booking.start_datetime:
                    
                raise TimeSlotTakenError(booking.name, start_datetime, end)
                
        event = Event(name, host, start_datetime, duration_minutes)
        self.bookings[event.booking_id] = event
            
        return event
        
    def cancel_event(self, eid):
        if eid not in self.bookings.keys():
            raise EventNotFoundError(eid)

        deadline = self.bookings[eid].start_datetime - timedelta(hours = 24)

        if datetime.now() > deadline:
            raise LateCancellationError(self.bookings[eid].name, self.bookings[eid].start_datetime, deadline)
            
        del self.bookings[eid]

    def view_bookings(self):
        now = datetime.now()
        
        upcoming = [e for e in self.bookings.values() if e.start_datetime > now]
        sorted_events = sorted(upcoming, key=lambda e: e.start_datetime)

        return sorted_events
    
    def view_event(self, eid):
        if eid not in self.bookings:
            raise EventNotFoundError(eid)
        
        return self.bookings[eid]

    def list_by_host(self, host_name):
        matches = [e for e in self.bookings.values() if e.host.lower() == host_name.lower()]
        
        return sorted(matches, key=lambda e: e.start_datetime)
    
def main():

    booker = BookingSystem()
    print('''
==============================
    Event Booking System
==============================
''')
    while True:
        choice = input('''
[1] Book an event
[2] Cancel a booking
[3] View a booking
[4] List upcoming bookings
[5] List bookings by host
[6] Quit
                
> ''')
        match choice:
            case "1":
                name = input("Enter the name of the event")
                host = input("Enter the name of the host")
                date = input("Enter the starting date (format: YYYY-MM-DD)")
                time = input("Enter the starting time (format: HH:MM)")
                try:
                    start_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                    duration = int(input("Enter the duration of the event in minutes: "))                
                except:
                    print("Invalid input! Ensure your date, time, and duration are formatted correctly!")
                    continue

                try:
                    new_event = booker.book_event(name, host, start_date, duration)
                    print("\nBooking confirmed!")
                    print(new_event)
                except BookingError as e:
                    print(f"\n {type(e).__name__}: {e}")
            case "2":
                eid = input("Input the id of the event you'd like to cancel.")
                booker.cancel_event(eid)
            case "3":
                eid = input("Input the id of the event you'd like to view.")

                print(booker.view_event(eid))
            case "4":
                upcoming = booker.view_bookings()
                print("--- Upcoming Bookings ---")
                if not upcoming:
                    print("No upcoming events!")
                else:
                    for e in upcoming:
                        print(e)
            case "5":
                name = input("Type in the name of the host")

                host_e = booker.list_by_host(name)

                if not host_e:
                    print("No events found for this host!")
                else:
                    for e in host_e:
                        print(e)
            case "6":
                print("Bye!  Have a good time")
                break

main()