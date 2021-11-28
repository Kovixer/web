"""
Sockets
"""

import requests


LINK = 'http://api:5000/'


# Online users

@sio.on('connect')
async def connect(sid, request, data):
    """ Connect socket """
    requests.post(LINK, json={
        'method': 'account.connect',
        'socket': sid,
    })
    # await api.method(
    #     'account.connect',
    #     ip=request['asgi.scope']['client'][0],
    #     socket=sid,
    # )

@sio.on('online')
async def online(sid, data):
    """ Socket about online user """
    requests.post(LINK, json={
        'method': 'account.online',
        'params': data,
        'socket': sid,
    })
    # await api.method(
    #     'account.online',
    #     data,
    #     socket=sid,
    # )

@sio.on('disconnect')
async def disconnect(sid):
    """ Disconnect socket """
    requests.post(LINK, json={
        'method': 'account.disconnect',
        'socket': sid,
    })
    # await api.method(
    #     'account.disconnect',
    #     socket=sid,
    # )
