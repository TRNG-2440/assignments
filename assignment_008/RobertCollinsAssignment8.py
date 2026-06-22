from datetime import datetime, timedelta

class BookingError(Exception):
    """Base exception for all booking-related errors"""
    pass

class TimeSlotTakenError(BookingError):
    """Raised when a requested time slot is already booked"""
    def __init__(self, event_name, start_time, end_time, date):
        self.event_name = event_name
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        super().__init__(f"Time slot unavailable — \"{event_name}\" is already scheduled from {start_time} to {end_time} on {date}.")

class BookingWindowExceededError(BookingError):
    """Raised when booking too far in advance"""
    def __init__(self, requested_date, max_allowed_date):
        self.requested_date = requested_date
        self.max_allowed_date = max_allowed_date
        super().__init__(f"Requested date {requested_date} exceeds the maximum booking window. Bookings may not be made more than 90 days in advance (latest allowed: {max_allowed_date}).")

class LateCancellationError(BookingError):
    """Raised when cancelling within 24 hours of event"""
    def __init__(self, event_name, event_time, deadline):
        self.event_name = event_name
        self.event_time = event_time
        self.deadline = deadline
        super().__init__(f"Cannot cancel \"{event_name}\" — the event starts at {event_time} and the cancellation deadline has passed (cancellations must be made at least 24 hours in advance, deadline was {deadline}).")

class EventNotFoundError(BookingError):
    """Raised when booking ID doesn't exist"""
    def __init__(self, booking_id):
        self.booking_id = booking_id
        super().__init__(f"No event found with booking ID: {booking_id}")

class InvalidBookingError(BookingError):
    """Raised for general validation failures"""
    def __init__(self, message):
        super().__init__(message)

class Event:
    # Class variable to track the next booking number
    _next_id = 1
    
    def __init__(self, name, host, start_datetime, duration_minutes):
        self._name = name
        self._host = host
        self._start_datetime = start_datetime
        self._duration = duration_minutes
        self._end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        
        # Generate unique booking ID
        self._booking_id = f"BKG-{Event._next_id:04d}"
        Event._next_id += 1
    
    # Properties for encapsulation
    @property
    def booking_id(self):
        return self._booking_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def host(self):
        return self._host
    
    @property
    def start_datetime(self):
        return self._start_datetime
    
    @property
    def end_datetime(self):
        return self._end_datetime
    
    @property
    def duration(self):
        return self._duration
    
    def overlaps_with(self, other_event):
        """Check if this event overlaps with another event"""
        return (self._start_datetime < other_event.end_datetime and 
                other_event.start_datetime < self._end_datetime)
    
    def __str__(self):
        date_str = self._start_datetime.strftime("%Y-%m-%d")
        time_str = self._start_datetime.strftime("%H:%M")
        return f"[{self._booking_id}]  {date_str} {time_str}  |  {self._name} ({self._duration} min)  |  Host: {self._host}"
    
class BookingSystem:
    def __init__(self):
        self._bookings = []  # List to store all events
    
    def _is_time_slot_available(self, new_event):
        """Check if the time slot is available for a new event"""
        for existing_event in self._bookings:
            if new_event.overlaps_with(existing_event):
                # Check if it's the same day
                if new_event.start_datetime.date() == existing_event.start_datetime.date():
                    return False, existing_event
        return True, None
    
    def book_event(self, name, host, start_datetime, duration_minutes):
        """
        Book a new event after validating all rules.
        Returns the created Event object.
        """
        # Validation 1: Duration must be positive
        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0 minutes.")
        
        # Validation 2: Missing required fields (basic check)
        if not name or not host:
            raise InvalidBookingError("Event name and host name are required.")
        
        # Validation 3: Start time cannot be in the past
        now = datetime.now()
        if start_datetime < now:
            raise InvalidBookingError(f"Cannot book an event in the past. Start time {start_datetime.strftime('%Y-%m-%d %H:%M')} is before current time.")
        
        # Validation 4: Cannot book more than 90 days in advance
        max_date = now + timedelta(days=90)
        if start_datetime > max_date:
            raise BookingWindowExceededError(
                start_datetime.strftime("%Y-%m-%d"),
                max_date.strftime("%Y-%m-%d")
            )
        
        # Create the event temporarily to check for conflicts
        new_event = Event(name, host, start_datetime, duration_minutes)
        
        # Validation 5: Check for time slot conflicts
        is_available, conflicting_event = self._is_time_slot_available(new_event)
        if not is_available:
            raise TimeSlotTakenError(
                conflicting_event.name,
                conflicting_event.start_datetime.strftime("%H:%M"),
                conflicting_event.end_datetime.strftime("%H:%M"),
                conflicting_event.start_datetime.strftime("%Y-%m-%d")
            )
        
        # All validations passed, add the booking
        self._bookings.append(new_event)
        return new_event
    
    def cancel_booking(self, booking_id):
        """Cancel a booking by ID with 24-hour rule"""
        # Find the event
        event_to_cancel = None
        for event in self._bookings:
            if event.booking_id == booking_id:
                event_to_cancel = event
                break
        
        if event_to_cancel is None:
            raise EventNotFoundError(booking_id)
        
        # Check cancellation window (24 hours before event)
        now = datetime.now()
        hours_until_event = (event_to_cancel.start_datetime - now).total_seconds() / 3600
        
        if hours_until_event < 24 and hours_until_event > 0:
            deadline = event_to_cancel.start_datetime - timedelta(hours=24)
            raise LateCancellationError(
                event_to_cancel.name,
                event_to_cancel.start_datetime.strftime("%H:%M on %Y-%m-%d"),
                deadline.strftime("%H:%M on %Y-%m-%d")
            )
        elif hours_until_event <= 0:
            raise InvalidBookingError(f"Cannot cancel event \"{event_to_cancel.name}\" because it has already started or passed.")
        
        # Remove the booking
        self._bookings.remove(event_to_cancel)
        return event_to_cancel
    
    def view_booking(self, booking_id):
        """View a single booking by ID"""
        for event in self._bookings:
            if event.booking_id == booking_id:
                return event
        raise EventNotFoundError(booking_id)
    
    def list_upcoming_bookings(self):
        """Return all future events sorted chronologically"""
        now = datetime.now()
        upcoming = [event for event in self._bookings if event.start_datetime > now]
        return sorted(upcoming, key=lambda e: e.start_datetime)
    
    def list_bookings_by_host(self, host_name):
        """Return all events for a given host (case-insensitive)"""
        return [event for event in self._bookings 
                if event.host.lower() == host_name.lower()]
    
class BookingSystem:
    def __init__(self):
        self._bookings = []  # List to store all events
    
    def _is_time_slot_available(self, new_event):
        """Check if the time slot is available for a new event"""
        for existing_event in self._bookings:
            if new_event.overlaps_with(existing_event):
                # Check if it's the same day
                if new_event.start_datetime.date() == existing_event.start_datetime.date():
                    return False, existing_event
        return True, None
    
    def book_event(self, name, host, start_datetime, duration_minutes):
        """
        Book a new event after validating all rules.
        Returns the created Event object.
        """
        # Validation 1: Duration must be positive
        if duration_minutes <= 0:
            raise InvalidBookingError("Duration must be greater than 0 minutes.")
        
        # Validation 2: Missing required fields (basic check)
        if not name or not host:
            raise InvalidBookingError("Event name and host name are required.")
        
        # Validation 3: Start time cannot be in the past
        now = datetime.now()
        if start_datetime < now:
            raise InvalidBookingError(f"Cannot book an event in the past. Start time {start_datetime.strftime('%Y-%m-%d %H:%M')} is before current time.")
        
        # Validation 4: Cannot book more than 90 days in advance
        max_date = now + timedelta(days=90)
        if start_datetime > max_date:
            raise BookingWindowExceededError(
                start_datetime.strftime("%Y-%m-%d"),
                max_date.strftime("%Y-%m-%d")
            )
        
        # Create the event temporarily to check for conflicts
        new_event = Event(name, host, start_datetime, duration_minutes)
        
        # Validation 5: Check for time slot conflicts
        is_available, conflicting_event = self._is_time_slot_available(new_event)
        if not is_available:
            raise TimeSlotTakenError(
                conflicting_event.name,
                conflicting_event.start_datetime.strftime("%H:%M"),
                conflicting_event.end_datetime.strftime("%H:%M"),
                conflicting_event.start_datetime.strftime("%Y-%m-%d")
            )
        
        # All validations passed, add the booking
        self._bookings.append(new_event)
        return new_event
    
    def cancel_booking(self, booking_id):
        """Cancel a booking by ID with 24-hour rule"""
        # Find the event
        event_to_cancel = None
        for event in self._bookings:
            if event.booking_id == booking_id:
                event_to_cancel = event
                break
        
        if event_to_cancel is None:
            raise EventNotFoundError(booking_id)
        
        # Check cancellation window (24 hours before event)
        now = datetime.now()
        hours_until_event = (event_to_cancel.start_datetime - now).total_seconds() / 3600
        
        if hours_until_event < 24 and hours_until_event > 0:
            deadline = event_to_cancel.start_datetime - timedelta(hours=24)
            raise LateCancellationError(
                event_to_cancel.name,
                event_to_cancel.start_datetime.strftime("%H:%M on %Y-%m-%d"),
                deadline.strftime("%H:%M on %Y-%m-%d")
            )
        elif hours_until_event <= 0:
            raise InvalidBookingError(f"Cannot cancel event \"{event_to_cancel.name}\" because it has already started or passed.")
        
        # Remove the booking
        self._bookings.remove(event_to_cancel)
        return event_to_cancel
    
    def view_booking(self, booking_id):
        """View a single booking by ID"""
        for event in self._bookings:
            if event.booking_id == booking_id:
                return event
        raise EventNotFoundError(booking_id)
    
    def list_upcoming_bookings(self):
        """Return all future events sorted chronologically"""
        now = datetime.now()
        upcoming = [event for event in self._bookings if event.start_datetime > now]
        return sorted(upcoming, key=lambda e: e.start_datetime)
    
    def list_bookings_by_host(self, host_name):
        """Return all events for a given host (case-insensitive)"""
        return [event for event in self._bookings 
                if event.host.lower() == host_name.lower()]
    
def parse_datetime(date_str, time_str):
    """Helper function to parse date and time strings into a datetime object"""
    try:
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise InvalidBookingError("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

def main():
    system = BookingSystem()
    
    while True:
        print("\n" + "="*30)
        print("    Event Booking System")
        print("="*30)
        print("\n[1] Book an event")
        print("[2] Cancel a booking")
        print("[3] View a booking")
        print("[4] List upcoming bookings")
        print("[5] List bookings by host")
        print("[6] Quit")
        
        choice = input("\n> ").strip()
        
        match choice:
            case "1":
                print("\n--- Book an Event ---")
                try:
                    name = input("Event name: ").strip()
                    host = input("Host name: ").strip()
                    date_str = input("Start date (YYYY-MM-DD): ").strip()
                    time_str = input("Start time (HH:MM): ").strip()
                    
                    try:
                        duration = int(input("Duration (minutes): ").strip())
                    except ValueError:
                        raise InvalidBookingError("Duration must be a valid number.")
                    
                    start_datetime = parse_datetime(date_str, time_str)
                    
                    # Book the event
                    event = system.book_event(name, host, start_datetime, duration)
                    
                    print(f"\n✅ Booking confirmed!")
                    print(f"   Booking ID : {event.booking_id}")
                    print(f"   Event      : {event.name}")
                    print(f"   Host       : {event.host}")
                    print(f"   When       : {event.start_datetime.strftime('%Y-%m-%d at %H:%M')} ({event.duration} min)")
                    
                except BookingError as e:
                    print(f"\n❌ {e}")
                except Exception as e:
                    print(f"\n❌ An unexpected error occurred: {e}")
            
            case "2":
                print("\n--- Cancel a Booking ---")
                try:
                    booking_id = input("Booking ID: ").strip().upper()
                    cancelled_event = system.cancel_booking(booking_id)
                    print(f"\n✅ Successfully cancelled: {cancelled_event.name}")
                    
                except BookingError as e:
                    print(f"\n❌ {e}")
                except Exception as e:
                    print(f"\n❌ An unexpected error occurred: {e}")
            
            case "3":
                print("\n--- View a Booking ---")
                try:
                    booking_id = input("Booking ID: ").strip().upper()
                    event = system.view_booking(booking_id)
                    print(f"\n📅 Event Details:")
                    print(f"   Booking ID: {event.booking_id}")
                    print(f"   Event: {event.name}")
                    print(f"   Host: {event.host}")
                    print(f"   Start: {event.start_datetime.strftime('%Y-%m-%d %H:%M')}")
                    print(f"   Duration: {event.duration} minutes")
                    print(f"   End: {event.end_datetime.strftime('%Y-%m-%d %H:%M')}")
                    
                except BookingError as e:
                    print(f"\n❌ {e}")
                except Exception as e:
                    print(f"\n❌ An unexpected error occurred: {e}")
            
            case "4":
                print("\n--- Upcoming Bookings ---")
                upcoming = system.list_upcoming_bookings()
                if not upcoming:
                    print("\nNo upcoming bookings found.")
                else:
                    print("\n" + "-"*30)
                    for event in upcoming:
                        print(f"  {event}")
                    print("-"*30)
                    print(f"\n{len(upcoming)} upcoming booking(s) found.")
            
            case "5":
                print("\n--- List Bookings by Host ---")
                host_name = input("Host name: ").strip()
                bookings = system.list_bookings_by_host(host_name)
                
                if not bookings:
                    print(f"\nNo bookings found for host: {host_name}")
                else:
                    print(f"\nBookings for {host_name}:")
                    print("-"*30)
                    for event in sorted(bookings, key=lambda e: e.start_datetime):
                        print(f"  {event}")
                    print("-"*30)
                    print(f"\n{len(bookings)} booking(s) found.")
            
            case "6":
                print("\nGoodbye!")
                break
            
            case _:
                print("\n❌ Please select one of the options provided in the menu (1-6).")

if __name__ == "__main__":
    main()