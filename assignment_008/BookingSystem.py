"""
In this activity, you will build a CLI event booking system with a 
strong emphasis on designing and using custom exceptions. You will practice:

Defining a custom exception hierarchy rooted in a shared base exception class
Raising exceptions with contextual data embedded in the message
Catching and handling specific exception types at the appropriate level
Separating validation logic from core application logic using exceptions
Core OOP concepts: classes, encapsulation, and composition
Working with the datetime module for date and time validation
"""

import datetime
import uuid

# --- Parent exception class ---

class BookingError(Exception):
  def __init__(self, message):
        super().__init__(message)

# --- Child expcetion classes ---

class TimeSlotTakenError(BookingError):
   def __init__(self, timeSlot):
      super().__init__(f"\nError - timeslot of {timeSlot} has already been booked\n")
      self.slot = timeSlot

class BookingWindowExceededError(BookingError):
   def __init__(self, date):
      super().__init__(f"\nError - Reserved date of {date} exceeds {datetime.datetime.now()} after 90 days\n")
      self.date = date

class LateCancellationError(BookingError):
   def __init__(self, message):
      super().__init__(message)
   
class EventNotFoundError(BookingError):
   def __init__(self, message):
        super().__init__(message)

class InvalidBookingError(BookingError):
   def __init__(self, message):
        super().__init__(message)

# ----------------- Classes ---------------------

class Event:
  def __init__(self, eventName, startDateTime, duration, hostName):
     
     self.eventName = eventName

     self.startDateTime = startDateTime

     self.duration = duration

     self.hostName = hostName

     self.bookingID = str(uuid.uuid4())

# -------------------------------------------------

class BookingSystem:
   
   def __init__(self):
      
      # Initialize event map
      self.EventMap = dict()
    
   # Book event
   def BookEvent(self, eventObj) -> str:
      
      # Execute if event date time is in the past
      if eventObj.startDateTime < datetime.datetime.now():
         raise InvalidBookingError(f'Error - Cannot book an event that is before {datetime.datetime.now()}\n')
      
      # Execute if event date booked time exceeds 90 days
      if eventObj.startDateTime > datetime.datetime.now() + datetime.timedelta(days=90):
         raise BookingWindowExceededError(eventObj.startDateTime)
      
      self.EventMap[eventObj.bookingID] = eventObj

      return eventObj.bookingID
   
   # Cancel event
   def CancelEvent(self, bookingID) -> None:
      
      # Determine if event is present
      if bookingID in self.EventMap:
         
         if datetime.datetime.now() > self.EventMap[bookingID].startDateTime - datetime.timedelta(hours=24):
            raise LateCancellationError("\nError - Cancellation window has closed")
         
         # Cancel event
         self.EventMap.pop(bookingID)

      else:
        raise EventNotFoundError(f"\nError - Booking ID {bookingID} not found\n")
      
   # View booked event
   def ViewBooking(self, bookingID) -> Event:
      
    if bookingID not in self.EventMap:
      raise EventNotFoundError(f"\nError - Booking ID {bookingID} not found\n")
    
    return self.EventMap[bookingID]
   
   # View all upcomming booking
   def UpComingBookings(self) -> list:
      
      # Declare list to collect upcomming events
      upcommingEvents = []

      # Traverse through all events
      for e in self.EventMap.values():
         if e.startDateTime > datetime.datetime.now():
            upcommingEvents.append(e)
      
      # Sort upcomming events
      def sort_key(event):
        return event.startDateTime

      upcommingEvents.sort(key=sort_key)

      return upcommingEvents
   
   # List booking by host
   def ListByHost(self, host) -> list:
        
        # Return event that is organized by a particular host
        return [ e for e in self.EventMap.values() if e.hostName.lower() == host.lower() ]

# Display booking menu
def Menu() -> str:
   
   print("==============================")
   print("    Event Booking System")
   print("==============================")
   print()
   print("[1] Book an event")
   print("[2] Cancel a booking")
   print("[3] View a booking")
   print("[4] List upcoming bookings")
   print("[5] List bookings by host")
   print("[6] Quit")
   
   return input('\nSelect Option: ')
   
def main():

  book = BookingSystem()

  while(True):

    match(Menu()):
       
       case "1":
          
          print("\n------------- Book Event -------------\n")

          eventName = input("Event name: ")
          hostName = input("Host name: ")
          date = input("Start date (YYYY-MM-DD): ")
          time = input("Start time (HH:MM): ")
          duration = int(input("Duration (minutes): "))

          print("\n--------------------------------------\n")

          bookingID = book.BookEvent(Event(eventName, datetime.datetime.strptime(f"{date} {time}","%Y-%m-%d %H:%M"), duration, hostName))

          print('✅ Booking Confirmed!')

          print(f"\nBooking ID: {bookingID}\n")

       case "2":

          # Prompt user to cancel event
          book.CancelEvent(input(f'\nPlease input bookID: ').strip())

          # Notify user event has been canceled
          print("\nBooking cancelled.\n")
        
       case "3":
           
          while(True):

            # Prompt user to view book
            event = book.ViewBooking(input(f'\nPlease input bookID: '))

            # Print booking details
            print("\n------------- Booking Details -------------\n")
            print(f"Booking ID : {event.bookingID}")
            print(f"Event      : {event.eventName}")
            print(f"Host       : {event.hostName}")
            print(f"When       : {event.startDateTime}")
            print(f"Duration   : {event.duration} minutes")
            print("\n-------------------------------------------\n")

            option = input("Would you like to view another booking (Y/N): ").strip()

            while option.lower() != "y" and option.lower() != "n":

              print("\nInvalid option, please re-enter\n")

              option = input("Would you like to view another booking (Y/N): ").strip()

            if option.lower() == "n":
              break

          
       case "4":
          
          # Produce list of upcoming bookings
          upcomingBookings = book.UpComingBookings()

          if len(upcomingBookings) == 0:
            print("No upcoming bookings found.")

          print("\n-------------------------- Upcoming Bookings --------------------------\n")
          # Display upcoming bookings
          for u in upcomingBookings:
             print(f'{u.bookingID} | {u.startDateTime} | {u.eventName} ({u.duration}) | Host: {u.hostName}\n')
          
          print("--------------------------------------------------------------------------------------\n")

          print(f"{len(upcomingBookings)} upcoming booking{'s' if len(upcomingBookings) > 1 else ''} found.")

       case "5":
          
          hostList = book.ListByHost(input(f'\nPlease input name of host: '))

          if(len(hostList) == 0):
             print('\nNo listings found.\n')
          
          else:
             
             print("\n-------------------------- Host Bookings --------------------------\n")
             
             # Traverse through host bookings
             for event in hostList:
                print(f'{event.bookingID} | {event.startDateTime} | {event.eventName} ({event.duration}) | Host: {event.hostName}')
             
             print("\n-----------------------------------------------------------------------\n")

       case "6":
          
          print('\nExiting program\n')
          break
       
       case _:
          
          print('\nInvalid option - please re-enter\n')
     

if __name__=="__main__":

  try:

    main()

  except ValueError as error:
    print(error)

  except BookingError as error:
    print(error)

  