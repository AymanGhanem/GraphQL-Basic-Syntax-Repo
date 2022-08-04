import asyncio
from cmath import inf
from ariadne import convert_kwargs_to_snake_case, SubscriptionType

from database import queues

subscription = SubscriptionType()


@subscription.source("newMovie")
@convert_kwargs_to_snake_case
async def new_movie_source(obj, info, *_):
    queue = asyncio.Queue()
    queues.append(queue)
    try:
        while True:
            movie = await queue.get()
            queue.task_done()
            if(True):
                yield movie
    except asyncio.CancelledError:
        queues.remove(queue)
        raise


@subscription.field("newMovie")
@convert_kwargs_to_snake_case
async def new_movies_resolver(new_movie, info, **kwargs):
    return new_movie