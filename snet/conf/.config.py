import pathlib
import sys, os

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()
DEBUG = True

LOG_DIR = BASE_DIR.parent.absolute() / ".log"

if not LOG_DIR.exists():
    os.makedirs(LOG_DIR)

MIDDLEWARES = []
STARTUP = []
SHUTDOWN = []
TASKS = []
DATABASE = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "127.0.0.1",
                "port": 5432,
                "user": "snet",
                "password": "Kakoy to parol",
                "database": "snet_data",
                "minsize": 50,
                "maxsize": 90 if DEBUG else 190, 
            }
        }
    },
    "apps": {
        #
    },
    "timezone": "UTC",
}

LOGGING = {
    "version": 1,
}