"""
The creating and editing method of the review object of the API
"""

from api.lib import BaseType, validate, report
from api.models.review import Review


class Type(BaseType):
    id: int = None
    title: str = None
    data: str = None

@validate(Type)
async def handle(request, data):
    """ Save """

    # Get

    new = False

    if data.id:
        review = Review.get(ids=data.id, fields={})
    else:
        review = Review(
            user=request.user.id,
        )
        new = True

    # Change fields
    review.title = data.title # TODO: checking if add
    review.data = data.data # TODO: checking if add

    # Save
    review.save()

    # Report
    await report.request("New review", {
        'review': review.id,
        'title': review.title,
        'data': review.data,
        'user': request.user.id,
        'token': request.token,
    })

    # Processing
    cont = None
    if data.data and data.data != review.data:
        cont = review.data

    # Response
    return {
        'id': review.id,
        'data': cont,
        'new': new,
    }
