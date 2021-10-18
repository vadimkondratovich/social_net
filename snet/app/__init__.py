import json
import snet
import argparse
import logging
import importlib
import logging.config as lconfig
from tortoise.contrib.aiohttp import register_tortoise
# import aiohttp_jinja2
# from jinja2 import FileSystemLoader
from aiohttp import web
from datetime import date
from typing import TypeVar
from snet.conf import settings
from snet.urls.route import Controller

Args = TypeVar("Args")
AiohttpApp = TypeVar("AiohttpApp")


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
            help="Run bg tasks.",
        )
        parser.add_argument(
            "-w",
            "--wait",
            dest="wait",
            action="store_true",
            help ="Run bg tasks.",
        )
        return parser.parse_known_args()[0], parser.parse_known_args()[1]

    @staticmethod
    def create_app() -> AiohttpApp:
        lconfig.dictConfig(settings.LOGGING)
        log = logging.getLogger(settings.LOGGER)
        app = web.Application(logger=log)
        app.middlewares.extend([importlib.import_module(m) for m in settings.MIDDLEWARES])
        app.on_startup.extend([importlib.import_module(m) for m in settings.STARTUP])
        app.on_shutdown.extend([importlib.import_module(m) for m in settings.SHUTDOWN])
        register_tortoise(app, config=settings.DATABASE, generate_schemas=True)
        Controller.entry_point(settings.ROOTURLS)
        for route in Controller.urls():
            app.router.add_route("*", route.path, route.handler, name=route.name)
        # aiohttp_jinja2.setup(
        #     app,
        #     loader=FileSystemLoader(
        #         [
        #             path / "templates"
        #             for path in (settings.BASE_DIR / "web").iterdir()
        #             if path.is_dir() and (path / "tempates").exists()
        #         ]
        #     )
        # )
        return app

    def __init__(self) -> None:
        self.arguments, self.vars = self.create_parser()
        self.app = self.create_app()
        self.run_args = {"print": False}
        self.run_args.update(host=self.arguments.host, port=self.arguments.port)

    def load(self):
        settings.DEBUG = True if self.arguments.debug else settings.DEBUG
        # if self.arguments.tasks:
        #     self.app["wait_tasks"] = self.arguments.wait
        #     for tm in settings.TASKS:
        #         importlib.import_module(tm)
        #     tasks = Tasks()
        #     self.app.cleanup_ctx.extend([task.run for task in tasks()])
        # else:
        #     self.app["wait_tasks"] = False
        for var in self.vars:
            if "=" in var:
                key, value = var.split("=")
                try:
                    settings[key.lower()] = json.loads(value)
                except json.JSONDecodeError:
                    settings[key.lower()] = value
            else:
                raise ValueError(f"Unrecognized arguments: {var}")
        return self

    def run(self):
        print("Social network is running.")
        print(self.run_args)
        try:
            web.run_app(self.app, **self.run_args)
        finally:
            print("\r", "Social network was killed.", sep="")


def run():
    SNetService().load().run()
