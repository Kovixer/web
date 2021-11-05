"""
The API
"""

import asyncio
import time

from api.lib import get_network, get_language, report
from api.methods import call
from api.methods.account.online import get_user
from api.background import background


class Request():
    """ Request container """

    def __init__(self, ip, socket, token, network, locale, sio=None):
        self.timestamp = time.time()
        self.ip = ip
        self.socket = socket
        self.token = token
        self.network = get_network(network)
        self.locale = get_language(locale)
        self.user = get_user(token, socket)
        self.sio = sio


class API():
    """ API """

    def __init__(self, sio=None):
        self.sio = sio

        # Background processes
        asyncio.create_task(background(sio))

    async def method(
        self,
        name,
        data=None,
        ip=None,
        socket=None,
        token=None,
        network=0,
        locale=0,
    ):
        """ Call API method """

        if socket is None and token is None:
            await report.warning("There is no socket id and token", {
                'method': name,
            })

        if not data:
            data = {}

        # print(name, data, ip, socket, token, network, locale)

        request = Request(ip, socket, token, network, locale, self.sio)

        # # Action tracking
        # Action(
        #     title=name,
        #     data=data,
        #     request=request,
        # }.save()

        # API method
        return await call(name, request, data)
