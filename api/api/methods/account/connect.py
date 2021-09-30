"""
The connect socket of the account object of the API
"""

from ...lib import report


# pylint: disable=unused-argument
async def handle(this, request, data):
    """ Connect """

    await report.debug('IN', request.socket)
