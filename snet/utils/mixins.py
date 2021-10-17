import logging
from snet.conf import settings


class LogMixin():
    _log = logging.getLogger(settings.LOGGER)
    _except_log = logging.getLogger(settings.EXCEPLOGGER)

    @property
    def _log(self)

