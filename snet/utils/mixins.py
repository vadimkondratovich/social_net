import logging
import traceback
from snet.conf import settings


class LogMixin():
    _log = logging.getLogger(settings.LOGGER)
    _except_log = logging.getLogger(settings.EXCEPTLOGGER)

    @property
    def _log(self):
        return self._log

    @property
    def _exlog(self):
        return self._except_log

    @property
    def _trace(self):
        return traceback.format_exc()

