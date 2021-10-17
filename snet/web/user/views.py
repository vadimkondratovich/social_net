import json
from aiohttp.web_exceptions import HTTPServiceUnavailable
from snet.utils.mixins import LogMixin
from aiohttp import web
from snet.web.root import views as rest
from snet.store.user_models import User
from tortoise.exceptions import IntegrityError, ValidationError

class Create(rest.BaseRestFull, LogMixin):
    async def post(self):
        try:
            data = await self.request.json()
        except json.JSONDecodeError as error:
            self._log.error(error.args[0])
            self._exlog.error(self._trace)
            return web.json_response(
                {"message": "INVALID DATA"},
                status=web.HTTPServiceUnavailable.status_code,
            )
        try:
            user = User(**data)
        except ValidationError:
            return web.json_response(
                {"message": "INVALID DATA"},
                status=web.HTTPServiceUnavailable.status_code,
                )
        try:
            await user.save()
        except IntegrityError:
            return web.json_response(
                {"message": "USER ALREADY EXISTS"},
                status=web.HTTPServiceUnavailable.status_code,
                )
        self._log.debug(data)
        return web.json_response(
            {"message": "CREATED", "user_id": user.id},
            status=HTTPServiceUnavailable.status_code,
            )
