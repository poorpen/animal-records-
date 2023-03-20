from dataclasses import dataclass

from src.domain.animal.exceptions.common import BaseAnimalDomainException


@dataclass
class AnimalIsDead(BaseAnimalDomainException):
    animal_id: int

    def message(self):
        return f'У животного с animal_id {self.animal_id} life_status = "DEAD"'


@dataclass
class AttemptToResurrectAnimal(BaseAnimalDomainException):
    animal_id: int

    def message(self):
        return f'Попытка изменить у животного с animal_id {self.animal_id} статус с "DEAD" на "ALIVE"'


@dataclass
class ChippingLocationEqualFirstLocation(BaseAnimalDomainException):
    animal_id: int
    chipping_location: int

    def message(self):
        return f'Новая точка чипирования c location_id {self.chipping_location} у животного с animal_id {self.animal_id}' \
               f'совпадает с первой посещенной точкой'
