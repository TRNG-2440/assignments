from datetime import datetime, timedelta

from event import Event
from exceptions import (
    TimeSlotTakenError,
    BookingWindowExceededError,
    LateCancellationError,
    EventNotFoundError,
    InvalidBookingError
)


class BookingSystem:

    def __init__(self):
        self.events = []


    # FIND EVENT
    def _find_event(self, booking_id):

        for event in self.events:
            if event.booking_id == booking_id:
                return event

        raise EventNotFoundError(booking_id)


    # OVERLAP CHECK
    def _is_overlap(self, new_event):

        for event in self.events:

            if event.start_datetime.date() == new_event.start_datetime.date():

                if (
                    new_event.start_datetime < event.end_datetime and
                    new_event.end_datetime > event.start_datetime
                ):
                    raise TimeSlotTakenError(
                        event.name,
                        event.start_datetime.strftime("%H:%M"),
                        event.end_datetime.strftime("%H:%M")
                    )

    
    # BOOK EVENT
    def book_event(self, name, host, start_dt, duration):

        if start_dt < datetime.now():
            raise InvalidBookingError("Cannot book an event in the past.")

        if duration <= 0:
            raise InvalidBookingError("Duration must be greater than 0.")

        max_date = datetime.now() + timedelta(days=90)

        if start_dt > max_date:
            raise BookingWindowExceededError(
                start_dt.date(),
                max_date.date()
            )

        new_event = Event(name, host, start_dt, duration)

        self._is_overlap(new_event)

        self.events.append(new_event)

        return new_event

   
    # CANCEL EVENT
    def cancel_booking(self, booking_id):

        event = self._find_event(booking_id)

        deadline = event.start_datetime - timedelta(hours=24)

        if datetime.now() > deadline:
            raise LateCancellationError(
                event.name,
                event.start_datetime,
                deadline
            )

        self.events.remove(event)

  
    # VIEW ONE
    def view_booking(self, booking_id):
        return self._find_event(booking_id)


    # UPCOMING BOOKINGS
    def list_upcoming(self):

        future_events = [
            e for e in self.events
            if e.start_datetime > datetime.now()
        ]

        return sorted(future_events, key=lambda x: x.start_datetime)


    # BY HOST
    def list_by_host(self, host_name):

        return [
            e for e in self.events
            if e.host.lower() == host_name.lower()
        ]