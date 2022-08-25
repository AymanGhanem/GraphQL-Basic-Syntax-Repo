from ariadne import ObjectType, convert_kwargs_to_snake_case

from database import movies_table, actors_table, counter

query = ObjectType("Query")
actor = ObjectType("Actor")
movie = ObjectType("Movie")

@query.field("allMovies")
@convert_kwargs_to_snake_case
async def resolve_all_movies(obj, info):
    # print("---------------Movies Query----------------")
    counter = 1
    movies_list = []
    for index in range(1,len(movies_table)+1):
        rows_index = 'mov-' + str(index)
        movie = {
            'id': movies_table.loc[rows_index, 'id'],
            'title': movies_table.loc[rows_index, 'title'],
            'rating': movies_table.loc[rows_index, 'rating'],
            'available': bool(movies_table.loc[rows_index, 'available']),
        }
        movies_list.append(movie)
    # print("Before exiting all movies query resolver the counter is : ", counter)
    return movies_list

@query.field("allActors")
@convert_kwargs_to_snake_case
async def resolve_all_actors(obj, info):
    # print("------------------Actors Query----------------")
    counter = 1
    resulted_actors = []
    for index in range(0, len(actors_table)):
        obj = {
            'id': actors_table.iloc[index, 0],
            'name': actors_table.iloc[index, 1]
        }
        resulted_actors.append(obj)
    # print("Before exiting all actors query resolver the counter is : ", counter)
    return resulted_actors

@movie.field("actors")
@convert_kwargs_to_snake_case
async def resolve_actors(obj, info):
    # print("------------------actors----------------")
    global counter
    counter += 1
    resulted_actors = []
    actors_string = movies_table.loc[obj['id'], 'actors']
    actors_list = [actor.strip() for actor in actors_string.split(',')]
    for actor in actors_list:
        actor_objects = actors_table[actors_table['names'] == actor]
        obj = {
            'id': actor_objects.iloc[0,0],
            'name': actor_objects.iloc[0,1]
        }
        resulted_actors.append(obj)
    # print("Before exiting  actors field resolver the counter is : ", counter)
    return resulted_actors

@actor.field("movies")
@convert_kwargs_to_snake_case
async def resolve__movies(obj, info):
    global counter
    counter += 1
    # print("********************Hi********************")
    movies_obj_list = []
    actor_name = obj['name']
    for index in range(1,len(movies_table)+1):
        movie_row = movies_table[movies_table['id'] == 'mov-' + str(index)]
        movie_actors = movie_row.iloc[0,2]
        movie_id = movie_row.iloc[0,0]
        movie_actors_list = [actor.strip() for actor in movie_actors.split(',')]
        if(actor_name in movie_actors_list):
            obj = {
                'id': movies_table.loc[movie_id, 'id'],
                'title': movies_table.loc[movie_id, 'title'],
                'rating': movies_table.loc[movie_id, 'rating'],
                'available': bool(movies_table.loc[movie_id, 'available']),
            }
            movies_obj_list.append(obj)
    # print("Before exiting movies field resolver the counter is : ", counter)
    return movies_obj_list