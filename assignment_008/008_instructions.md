# Python Coding Activity 8 - Event Booking System

## Objective

In this activity, you will build a CLI event booking system with a strong emphasis on designing and using **custom exceptions**. You will practice:

- Defining a custom exception hierarchy rooted in a shared base exception class
- Raising exceptions with contextual data embedded in the message
- Catching and handling specific exception types at the appropriate level
- Separating validation logic from core application logic using exceptions
- Core OOP concepts: classes, encapsulation, and composition
- Working with the `datetime` module for date and time validation

---

## Instructions

You will build a system that allows users to create events, book time slots, and manage cancellations. Business rule violations must be communicated exclusively through custom exceptions — not bare `if/else` returns or print statements inside your logic classes.

1. Define a base exception class called `BookingError` that all other custom exceptions in this project inherit from. This ensures callers can catch either a specific exception or any booking-related error with a single `except` clause.

2. Define the following custom exceptions, each as a subclass of `BookingError`. Each exception should store and display relevant contextual data in its message:
   - `TimeSlotTakenError` — raised when a requested time slot is already booked. Should include the conflicting event name and time in its message.
   - `BookingWindowExceededError` — raised when a user attempts to book an event too far in advance beyond a defined maximum window (e.g. 90 days). Should include the requested date and the maximum allowed date in its message.
   - `LateCancellationError` — raised when a user attempts to cancel a booking within a restricted window before the event (e.g. less than 24 hours). Should include the event time and the cancellation deadline in its message.
   - `EventNotFoundError` — raised when a lookup is performed for a booking ID or event that does not exist.
   - `InvalidBookingError` — raised for general validation failures such as a booking made in the past, an invalid duration, or a missing required field.

<!-- 3. Create an `Event` class to represent a single bookable event. It should store at minimum: an event name, a start datetime, a duration, a host name, and a unique booking ID. You will need to import the `datetime` module. -->

4. Create a `BookingSystem` class that manages all events and exposes the following operations:
   <!-- - **Book an event** — accepts event details, validates them, and adds the event if no conflicts exist. Must raise appropriate custom exceptions for all invalid states. -->
   <!-- - **Cancel a booking** — accepts a booking ID and cancels the event if it exists and the cancellation window allows it. -->
   <!-- - **View a booking** — looks up and returns a single event by booking ID. -->
   <!-- - **List all upcoming bookings** — returns all future events in chronological order. -->
   <!-- - **List bookings by host** — returns all events associated with a given host name. -->

5. Validation rules your `BookingSystem` must enforce via custom exceptions:
   <!-- - A new booking may not start in the past. -->
   <!-- - A new booking may not be scheduled more than 90 days in advance. -->
   <!-- - A new booking may not overlap with an existing booking (same day, overlapping time range). -->
   <!-- - A cancellation requested within 24 hours of the event start must raise `LateCancellationError`. -->
   <!-- - Any lookup by booking ID that finds no match must raise `EventNotFoundError`. -->

<!-- 6. Booking IDs should be auto-generated and unique. You may use any strategy you like to generate them. -->

<!-- 7. Build a CLI menu loop that allows users to: create a booking, cancel a booking, view a booking by ID, list all upcoming bookings, and list bookings by host. All exceptions should be caught at the CLI layer and displayed as clean, user-friendly error messages — the user should never see a raw Python traceback. -->

---

## Example Interaction

```
==============================
    Event Booking System
==============================

[1] Book an event
[2] Cancel a booking
[3] View a booking
[4] List upcoming bookings
[5] List bookings by host
[6] Quit

> 1

Event name: Team Standup
Host name: Sarah Chen
Start date (YYYY-MM-DD): 2025-06-15
Start time (HH:MM): 09:00
Duration (minutes): 30

✅ Booking confirmed!
   Booking ID : BKG-4821
   Event      : Team Standup
   Host       : Sarah Chen
   When       : 2025-06-15 at 09:00 (30 min)

------------------------------

> 1

Event name: Sprint Planning
Host name: Marcus Lee
Start date (YYYY-MM-DD): 2025-06-15
Start time (HH:MM): 09:15
Duration (minutes): 60

❌ BookingError: Time slot unavailable — "Team Standup" is already scheduled from 09:00 to 09:30 on 2025-06-15.

------------------------------

> 1

Event name: Q4 Kickoff
Host name: Sarah Chen
Start date (YYYY-MM-DD): 2025-10-01
Start time (HH:MM): 14:00
Duration (minutes): 90

❌ BookingError: Requested date 2025-10-01 exceeds the maximum booking window. Bookings may not be made more than 90 days in advance (latest allowed: 2025-09-08).

------------------------------

> 2

Booking ID: BKG-4821

❌ BookingError: Cannot cancel "Team Standup" — the event starts at 09:00 on 2025-06-15 and the cancellation deadline has passed (cancellations must be made at least 24 hours in advance).

------------------------------

> 4

Upcoming Bookings
------------------------------
  [BKG-4821]  2025-06-15 09:00  |  Team Standup (30 min)  |  Host: Sarah Chen
  [BKG-5033]  2025-06-17 13:00  |  Design Review (60 min) |  Host: Marcus Lee
  [BKG-5101]  2025-06-20 10:00  |  1:1 Check-in (30 min)  |  Host: Sarah Chen
------------------------------
3 upcoming booking(s) found.
```

> ***NOTE: Examples shown are for illustrative purposes, functionality related to raised exceptions, accepted bookings, cancellations, etc... should adhere to the instructions and requirements presented in these instructions.***

---

## Requirements Checklist

- [x] A base `BookingError` exception class exists and all custom exceptions inherit from it
- [x] `TimeSlotTakenError` includes the conflicting event name and time range in its message
- [x] `BookingWindowExceededError` includes the requested date and the latest allowed date in its message (can't be scheduled more than 90 days in advance)
- [x] `LateCancellationError` includes the event start time and cancellation deadline in its message
- [x] `EventNotFoundError` is raised for any lookup using an unrecognized booking ID
- [x] `InvalidBookingError` is raised for bookings with a start time in the past
- [x] `InvalidBookingError` is raised for any other general validation failure (e.g. zero or negative duration)
- [ ] The `BookingSystem` class raises exceptions for all invalid states rather than returning error strings
- [x] Overlap detection correctly identifies conflicts for events on the same day with overlapping time ranges
- [x] Booking IDs are auto-generated and unique across all bookings in the session
- [x] Cancellation within 24 hours of the event raises `LateCancellationError`
- [x] Listing upcoming bookings returns only future events, sorted chronologically
- [x] Listing by host name is case-insensitive
- [ ] All exceptions are caught at the CLI layer and displayed as readable messages — no raw tracebacks reach the user
- [ ] The CLI handles non-numeric menu input and malformed dates/times without crashing

---

## Stretch Goals

- **Exception Logging** — When any `BookingError` is raised and caught, append a log entry to a `booking_errors.log` file with a timestamp, the exception type, and its message. This pairs custom exceptions naturally with File I/O.

- **Recurring Bookings** — Add support for creating a recurring event (e.g. weekly for N weeks). Each occurrence should be validated and booked individually — if any occurrence conflicts, a `TimeSlotTakenError` should be raised identifying which occurrence failed and no bookings from that batch should be saved (all-or-nothing).

- **Capacity Support** — Add an optional `capacity` attribute to events. Introduce a new `EventFullError` (subclass of `BookingError`) raised when an event is fully booked. Update the CLI to allow multiple attendees to book the same event up to its capacity.