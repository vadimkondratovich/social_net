import argparse
import snet
from datetime import date
from typing import TypeVar
from snet.conf import settings

Args = TypeVar("Args")


class SNetService:
    @staticmethod
    def create_parser() -> Args:
        parser = argparse.ArgumentParser(
            prog="Social network.",
            description="Very cool social network.\n(c) Vadim Kondratovich {}".format(
                date.today().year
                ),
                add_help=False,
        )
        parser.add_argument(
            "-h",
            "--help",
            action="help",
            help="Print this message.",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            help="Current version.",
            version=f"Snet: {snet.__version__}",
        )
        parser.add_argument(
            "--host",
            dest="host",
            default="127.0.0.1",
            help="Network address.",
        )
        parser.add_argument(
            "--port",
            dest="port",
            default=8008,
            help="Network port.",
        )
        parser.add_argument(
            "-d",
            "--debug",
            dest="debug",
            action="store_true",
            help="Run application in DEBUG mode.",
        )
        parser.add_argument(
            "-t",
            "--tasks",
            dest="tasks",
            action="store_true",
            help="Run bg tasks",
        )
        parser.add_argument(
            "-w",
            "--wait",
            dest="wait",
            action="store_true",
            help ="Run bg tasks.",
        )
        return parser.parse_known_args()[0], parser.parse_known_args()[1]


    def __init__(self) -> None:
        self.arguments, self.vars = self.create_parser()

    def load(self):
        print(settings.DEBUG)
        return self

    def run(self):
        ...


def run():
    SNetService().load().run()
