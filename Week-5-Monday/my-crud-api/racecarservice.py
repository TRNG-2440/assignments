import uuid
from typing import Optional, Any
from uuid import UUID
from models import Racecar, RacecarCreate

class RacecarService:
    def __init__(self):
        self._current_next_id = 0
        self.data: dict[int, Racecar] = {}

    def _create_id(self) -> int:
        self._current_next_id += 1
        return self._current_next_id

    def create_trip(self, new_racecar: RacecarCreate) -> Racecar:
        new_id: int = self._create_id()
        new_values: dict[str, Any] = new_racecar.model_dump(exclude_none=True)
        new_values["id"] = new_id
        new_racecar: Racecar = Racecar.model_validate(new_values)
        self.data[new_racecar.id] = new_racecar
        return new_racecar

    def get_racecar(self) -> list[Racecar]:
        return list(self.data.values())

    def get_racecar(self, racecar_id: int) -> Optional[Racecar]:
        return self.data.get(racecar_id)

    def delete_trip(self, racecar_id: UUID) -> Optional[Racecar]:
        """

        :param trip_id:
        :raises TripNotFoundError: Trip not found
        :return:
        """
        trip: Racecar = self.get_racecar(trip_id)
        trips: list[Trip] = self.get_trips()
        trips.remove(trip)
        self.save_trips(trips)
        return trip

    def update_racecar(self, trip_update: TripUpdate) -> Trip:
        """
        Updates the trip with the non-null params of trip_update or raises TripNotFoundError if there is no trip with the specified id
        :param trip_update:
        :raises TripNotFoundError: Trip not found
        :return: the updated trip
        """
        to_update: Trip = self.get_trip(trip_update.id)

        new_values: dict[str, Any] = trip_update.model_dump(
            mode="python", exclude_none=True
        )
        # merge the values
        to_update = to_update.model_validate(
            to_update.model_dump(mode="python") | new_values
        )

        self.delete_trip(to_update.id)
        return self.save_trip(to_update)
