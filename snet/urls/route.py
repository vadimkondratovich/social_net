import importlib
import traceback
from typing import Union, TypeVar, Generator
from collections import namedtuple


View = TypeVar("View")


__all__ = ("Controller", "ControllerError")

Route = namedtuple("Route", "path, handler, name")

class ControllerError(Exception):
    """Controller exception."""


class Controller:
    """Url controller."""

    _urlpatterns = set()
    _sub_path = ""

    @classmethod
    def add(cls, path: str, handler: View, name: str) -> None:
        """[summary]

        Args:
            path (str): [description]
            handler (View): [description]
            name (str): [description]
        """        
        cls._urlpatterns.add(Route("".join((cls._sub_path, path)), handler, name))

    @classmethod
    def include(cls, path: str, module: str) -> None:
        """[summary]

        Args:
            path (str): [description]
            module (str): [description]
        """

        old_sub_path = cls._sub_path
        cls._sub_path += path
        try:
            importlib.import_module(module)
        except Exception:
            raise ConnectionError(
                "Import {!r} from {!r}:/n{}".format(
                    path, module, traceback.format_exc()
                )
            )
        cls._sub_path = old_sub_path
    
    @classmethod
    def get(cls, name: str) -> Union[Route, None]:
        """[summary]

        Args:
            name (str): [description]

        Returns:
            Union[Route, None]: [description]
        """
        for route in cls._urlpatterns:
            if route.name == name:
                return route
        return None

    
    @classmethod
    def entry_point(cls, module: str) -> None:
        """[summary]

        Args:
            module (str): [description]
        """
        try:
            importlib.import_module(module)
        except Exception:
            raise ConnectionError(
                "Import {!r}:\n{}".format(module, traceback.format_exc())
            )

    @classmethod
    def urls(cls) -> Generator:
        """[summary]

        Yields:
            Generator: [description]
        """
        for route in cls._urlpatterns:
            yield route                