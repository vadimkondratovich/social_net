from typing import Dict
from abc import ABC, abstractmethod
from tortoise.exceptions import IntegrityError, ValidationError
from snet.utils.mixins import LogMixin


class BaseSerializer(ABC, LogMixin):
    __slots__ = ("data",)

    def __init__(self, data:Dict) -> None:
        self.data = data

    def is_valid(self):
        try:
            self.clean()
        except ValidationError:
            return False
        return True

    @abstractmethod
    def clean(self):
        "Validation method"

    def save(self):
        ...

    # def clean(self):
    #     raise NotImplementedError("Not implemented")


class UserSerializer(BaseSerializer):
    def clean(self):
        return super().clean()