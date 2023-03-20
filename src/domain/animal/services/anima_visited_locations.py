from datetime import datetime

from src.domain.animal.enums import LifeStatus
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.animal import Animal

from src.domain.animal.exceptions.animal_visited_location import \
    LocationPointEqualToChippingLocation, AnimalNowInThisPoint, NextOfPreviousEqualThisLocation, \
    UpdateToSameLocationPoint, UpdatedFirstPointToChippingPoint
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.values_objects.animal_visited_location import LocationPointID


def add_visited_location(animal: Animal, location_point_id: int):
    if animal.life_status.to_enum() == LifeStatus.DEAD:
        raise AnimalIsDead(animal.id.to_id())
    elif animal.chipping_location_id.to_id() == location_point_id:
        raise LocationPointEqualToChippingLocation(animal.id.to_id(), location_point_id)
    elif animal.visited_locations:
        if animal.visited_locations[-1].location_point_id.to_id() == location_point_id:
            raise AnimalNowInThisPoint(animal.id.to_id(), location_point_id)

    visited_location = AnimalVisitedLocation.create(location_point_id=LocationPointID(location_point_id),
                                                    animal_id=animal.id,
                                                    datetime_of_visit=datetime.utcnow())
    animal.update(visited_locations=[visited_location])


def change_visited_location(animal: Animal, visited_location_id: int, new_location_point_id: int) -> None:
    visited_location = animal.get_visited_location(visited_location_id)
    location_index = animal.visited_locations.index(visited_location)

    if visited_location.location_point_id.to_id() == new_location_point_id:
        raise UpdateToSameLocationPoint(animal.id.to_id(), visited_location.location_point_id.to_id())
    elif location_index != 0 and location_index != len(animal.visited_locations) - 1:

        next_element = animal.visited_locations[location_index + 1]
        previous_element = animal.visited_locations[location_index - 1]

        if next_element.location_point_id.to_id() == new_location_point_id:
            raise NextOfPreviousEqualThisLocation(animal.id.to_id(), visited_location.location_point_id.to_id())
        elif previous_element.location_point_id.to_id() == new_location_point_id:
            raise NextOfPreviousEqualThisLocation(animal.id.to_id(), visited_location.location_point_id.to_id())

    elif location_index == 0 and new_location_point_id == animal.chipping_location_id.to_id():
        raise UpdatedFirstPointToChippingPoint(animal.id.to_id(), visited_location.location_point_id.to_id())

    animal.visited_locations[location_index].update(location_point_id=LocationPointID(new_location_point_id))


def delete_visited_location(animal: Animal, visited_location_id: int) -> None:
    visited_location = animal.get_visited_location(visited_location_id)

    index_visited_location = animal.visited_locations.index(visited_location)

    if index_visited_location + 1 != len(animal.visited_locations):
        next_visited_location = animal.visited_locations[index_visited_location + 1]

        if index_visited_location == 0 and next_visited_location.location_point_id == animal.chipping_location_id:
            animal.visited_locations.remove(next_visited_location)
    animal.visited_locations.remove(visited_location)
