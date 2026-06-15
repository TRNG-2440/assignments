"""
class Booking Error
    - parent/base class

    1. TimeSlotTakenError
        - time slot already booked
        - include conflicting event name + time

    2. BookingWindowExceededError
        - even booking too far in advance
        - include requested date and the max allowed date

    3. LateCancellationError
        - user tried to cancel within 24 hrs of reserved time
        - include time + cancellation deadline

    4. EventNotFoundError
        - event doesn't exist
    
    5. InvalidBookingError
        - general validation


event Class
    - bookable event (NOT plural!!)
    * event name
    * start datetime
    * duration
    * hostname
    * unique booking ID


main :

    1. create booking

    2. cancel booking

    3. view booking by ID

    4. list all upcoming bookings

    5. list bookings by host
"""


import datetime
import random
from time import sleep


class BookingError(Exception):
    pass

class TimeSlotTakenError(BookingError):
    def __init__(self, event_name, start_time, end_time, date):
        message = (f"Time slot unavailable {event_name} is already scheduled on {date.strftime('%Y-%m-%d')} from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}.")

        super().__init__(message)
    

class BookingWindowExceededError(BookingError):
    def __init__(self, requested_date, max_date):
        message = (f"Requested date {requested_date.strftime('%Y-%m-%d')} exceeds the maximum booking window. \nBookings cannot be made more than 60 days in advance. \nThe latest date you can book an event is {max_date.strftime('%Y-%m-%d')}")

        super().__init__(message)


class LateCancellationError(BookingError):
    def __init__(self, event_name, event_start, deadline):
        message = (f"Sorry! Cannot cancel '{event_name}' happening on {event_start.strftime("%Y-%m-%d")} at {event_start.strftime("%H:%M")} since the event starts in less than 24 hours. \nThe cancellation deadline was {deadline.strftime("%Y-%m-%d %H:%M")}")
    
        super().__init__(message)

class EventNotFoundError(BookingError):
    def __init__(self, booking_id):
        message = (f"Sorry! There is no booking found for id:{booking_id}")
        super().__init__(message)


class InvalidBookingError(BookingError):
    def __init__(self, reason):
        message = (f"Sorry! Invalid booking: {reason}")
        super().__init__(message)


class Event:
    def __init__(self, event_name, host_name, start_time, duration_min, booking_id):
        self.event_name = event_name
        self.host_name = host_name
        self.start_time = start_time
        self.duration_min = duration_min
        self.booking_id = booking_id
    
    def get_end_time(self):
        end = self.start_time + datetime.timedelta(minutes=self.duration_min)
        return end

    def __str__(self):
        return (f"[{self.booking_id}]  {self.start_time.strftime('%Y-%m-%d %H:%M')}  |  {self.event_name} ({self.duration_min} min)  |  Host: {self.host_name}")


    

class BookingSystem:
    MAX_DAYS = 60
    CANCEL_HOURS = 24

    def __init__(self):
        self.bookings = {}
        self.used_ids = set()
    
    def get_booking_id(self):
        while True:
            id = f"BID-{random.randint(1, 9999)}"
            if id not in self.used_ids:
                self.used_ids.add(id)
                return id

    def book_event(self, event_name, host_name, start_dt, duration):
        # make sure that there isn't a booking with that time already
        current = datetime.datetime.now()   # will need for checking validity

        if not event_name or not event_name.strip():
            raise InvalidBookingError("Event name cannot be empty!")
        
        if not host_name or not host_name.strip():
            raise InvalidBookingError("Host name cannot be empty!")

        if duration <= 0:
            raise InvalidBookingError("Invalid time duration! Please choose a positive number of minutes.")
        
        if start_dt <= current:
            raise InvalidBookingError(f"Start time {start_dt.strftime('%Y-%m-%d %H:%M')} is in the past")

        max_date = current + datetime.timedelta(days=self.MAX_DAYS)

        if start_dt > max_date:
            raise BookingWindowExceededError(start_dt.date(), max_date.date())
        
        end_dt = start_dt + datetime.timedelta(minutes=duration)
        
        for booking in self.bookings.values():
            if booking.start_time.date() == start_dt.date():
                if start_dt < booking.get_end_time() and booking.start_time < end_dt:
                    raise TimeSlotTakenError (booking.event_name, booking.start_time, booking.get_end_time(), start_dt.date())
                
        booking_id = self.get_booking_id()
        event = Event(event_name.strip(), host_name.strip(), start_dt, duration, booking_id)
        self.bookings[booking_id] = event

        return event
    
    def cancel_booking(self, booking_id):

        event = self.view_booking(booking_id)
        deadline = event.start_time  - datetime.timedelta(hours=self.CANCEL_HOURS)

        if datetime.datetime.now() > deadline:
            raise LateCancellationError(event.event_name, event.start_time, deadline)
        
        del self.bookings[booking_id]
        return event
    
    def view_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise EventNotFoundError(booking_id)
        
        return self.bookings[booking_id]
    
    def list_upcoming(self):
        now = datetime.datetime.now()

        upcoming = []

        for event in self.bookings.values():
            if event.start_time > now:
                upcoming.append(event)
        
        upcoming.sort(key=lambda e: e.start_time)
        return upcoming
    
    def list_by_host(self, host_name):
        results = []

        for event in self.bookings.values():
            if event.host_name.lower() == host_name.strip().lower():
                results.append(event)
        
        results.sort(key=lambda x: x.start_time)
        return results
    
def clear_console():
    print("\033[2J\033[H", end="", flush=True)


def main():
    booking_system = BookingSystem()

    print("------------------------------")
    print("     Event Booking System     ")
    print("------------------------------")


    while True:
        print("[1] Book an event")
        print("[2] Cancel a booking")
        print("[3] View a booking")
        print("[4] List upcoming bookings")
        print("[5] List bookings by host")
        print("[6] Quit")

        try:
            choice = int(input("\n> ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        print("-" * 30)

        if choice == 1:
            clear_console()

            event_name = input("\n\nEvent name: ").strip()
            host_name = input("Host name: ").strip()

            try:
                date = input("Start date (YYYY-MM-DD): ").strip()
                time = input("Start time (HH:MM): ").strip()
                start_dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                duration = int(input("Duration (min): ").strip())
            except ValueError as e:
                print(f"Input Error: {e}")
                print("-" * 30)
                continue

            try:
                event = booking_system.book_event(event_name, host_name, start_dt, duration)
                print(f"\nBooking confirmed!")
                print(f"   Booking ID : {event.booking_id}")
                print(f"   Event      : {event.event_name}")
                print(f"   Host       : {event.host_name}")
                print(f"   When       : {event.start_time.strftime('%Y-%m-%d')} at {event.start_time.strftime('%H:%M')} ({event.duration_min} min)")
            
            except BookingError as e:
                print(f"Unsuccessful booking: {e}")

        elif choice == 2:
            clear_console()

            booking_id = input("\n\nBooking ID: ").strip().upper()

            try:
                event = booking_system.cancel_booking(booking_id)
                print(f"'{event.event_name}' (id: {booking_id}) had been canceled!")
            except BookingError as e:
                print(f"Unsuccessful cancellation: {e}")
        
        elif choice == 3:
            clear_console()
            booking_id = input("\n\nBooking ID: ").strip().upper()

            try:
                event = booking_system.view_booking(booking_id)
                print(f"\n {event}")
            except BookingError as e:
                print(f"Error: {e}")


        elif choice == 4:
            clear_console()
            upcoming = booking_system.list_upcoming()
            print("Here are all the upcoming bookings:")
            print("-----------------------------------")

            if not upcoming:
                print("\nNo upcoming bookings!")
            else:
                for event in upcoming:
                    # [BKG-4821]  2025-06-15 09:00  |  Team Standup (30 min)  |  Host: Sarah Chen
                    print(f"{event}")
            
            print("-----------------------------------")
            print(f"{len(upcoming)} booking(s) coming up.")

        elif choice == 5:
            clear_console()
            host_name = input("Host name: ").strip()
            results = booking_system.list_by_host(host_name)
            
            print(f"Here are all the bookings for {host_name}:")
            print("-------------------------------------------")

            if not results:
                print(f"There are no booking found for {host_name}.")
            else:
                for event in results:
                    print(f"{event}")

            print("-------------------------------------------")
            print(f"{len(results)} booking(s) found for {host_name}.")

        elif choice == 6:
            # clear_console()

            print("\n\nGoodbye!")
            sleep(3)
            break
        
        else:
            print(f"'{choice}' if not a valid option. Please enter a number from 1-6.")



if __name__ == "__main__":
    main()