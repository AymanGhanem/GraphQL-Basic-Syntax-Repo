import pandas as pd
users = None
actors_table = pd.read_csv("actors.csv", usecols=range(1,3))
messages = []
queues = []
movies_table = pd.read_csv("movies.csv", usecols=range(1,6))
movies_table.index = movies_table['id']
counter = 0