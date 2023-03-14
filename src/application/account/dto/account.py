from typing import List
from dataclasses import dataclass

from src.application.common.dto.base import DTO
from src.application.common.dto.id_validator import IDValidator


@dataclass
class AccountID(DTO, IDValidator):
    id: int

@dataclass
class BaseAccountDTO(DTO):
    first_name: str
    last_name: str
    email: str


@dataclass
class SearchParametersDTO(BaseAccountDTO):
    limit: int
    offset: int


@dataclass
class CreateAccountDTO(BaseAccountDTO):
    password: str
    ...


@dataclass
class UpdateAccountDTO(BaseAccountDTO, AccountID):
    password: str


@dataclass
class AccountDTO(BaseAccountDTO):
    id: int


@dataclass
class AccountDTOs(DTO):
    accounts: List[AccountDTO]
