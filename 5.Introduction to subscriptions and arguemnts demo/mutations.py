import random
import pandas as pd
from ariadne import ObjectType, convert_kwargs_to_snake_case

from database import counter, actors_table, queues

mutation = ObjectType("Mutation")

@mutation.field("createMovie")
@convert_kwargs_to_snake_case
async def resolve_create_movie(obj, info, title, actors = ["Angelina Jolie"], available= False):
    movies_table = movies_table = pd.read_csv("movies.csv", usecols=range(1,6))
    actors_table = pd.read_csv("actors.csv", usecols=range(1,3))
    actors_list = []
    for index, row in actors_table.iterrows():
        print(actors_table.iloc[index,1])
        actors_list.append(actors_table.iloc[index,1])
    for in_actor in actors:
        if(in_actor in actors_list):
            print(in_actor)
        else:
            last_row = movies_table.tail(1)
            last_id = int(last_row.iloc[0][0].split('-')[1]) + 1
            dictionary = {
            "id": "actor-" + str(last_id),
            "names": in_actor
            }
            actors_table = actors_table.append(dictionary, ignore_index= True)
            actors_table.to_csv("actors.csv")
    rating_list = ["ONE_STAR", "TWO_STARS", "THREE_STARS", "FOUR_STARS", "FIVE_STARS"]
    last_row = movies_table.tail(1)
    last_id = int(last_row.iloc[0][0].split('-')[1]) + 1
    dictionary = {
        "id": "mov-" + str(last_id),
        "title": title,
        "actors": str(' , '.join(actors)),
        "available": available,
        "rating": random.choice(rating_list)
    }
    movies_table = movies_table.append(dictionary, ignore_index= True)
    movies_table.to_csv("movies.csv")
    for queue in queues:
        await queue.put(dictionary)
    print(movies_table)
    return {"success": True, "errors": []}