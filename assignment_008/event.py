from datetime import timedelta


class Event:

    next_id = 1

    def __init__(self, name, host, start_datetime, duration_minutes):

        self.booking_id = f"BKG-{Event.next_id:04}"
        Event.next_id += 1

        self.name = name
        self.host = host
        self.start_datetime = start_datetime
        self.duration = duration_minutes

        self.end_datetime = start_datetime + timedelta(minutes=duration_minutes)

    def get_details(self):

        return (
            f"[{self.booking_id}] "
            f"{self.start_datetime.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.name} ({self.duration} min) | "
            f"Host: {self.host}"
        )