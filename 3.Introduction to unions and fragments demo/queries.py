from ariadne import ObjectType, convert_kwargs_to_snake_case, UnionType

from database import shows_table, counter


import random

query = ObjectType("Query")
show = ObjectType("Show")
ticket_union = UnionType("Ticket")
vip_ticket = ObjectType("VipTicket")
ord_ticket = ObjectType("OrdTicket")

@ticket_union.type_resolver
def resolve_ticket_union_type(obj, *_):
    # print("------------------interface type resolver------------------------")
    global counter
    counter += 1
    print(f"Counter == {counter}.")
    if(obj.get('expire_at', None)):
        return "OrdTicket"
    elif(obj.get('num', None) or obj.get('row', None)):
        return "VipTicket"

@query.field("allShows")
@convert_kwargs_to_snake_case
async def resolve_all_shows(obj, info):
    print("-------------All Shows Query------------------")
    global counter
    counter = 1
    print(f"Counter == {counter}.")
    shows_list = []
    for index, value in shows_table.iterrows():
        obj = {
            'name': shows_table.iloc[index, 1],
            'date': shows_table.iloc[index, 0]
        }
        shows_list.append(obj)
    return shows_list

@show.field("tickets")
@convert_kwargs_to_snake_case
async def resolve_tickets(obj, info):
    print("-------------tickets field resolver------------------")
    global counter
    tickets_list = []
    counter += 1
    print(f"Counter == {counter}.")
    tickets_rows = shows_table[shows_table['names'] == obj['name']]
    for index, row in tickets_rows.iterrows():
        ticket_string = row.iloc[2]
        tickets_list.extend(ticket_string.split(','))
    objects = []
    for ticket in tickets_list:
        obj = ticket.split('*')
        if( random.random()> 0.5):
            ticket_obj = {
                "id": ticket,
                "expire_at": f"{random.randint(1,28)}-{random.randint(1,12)}-{random.randint(2024,2026)}"
            }
            objects.append(ticket_obj)
        else:
            ticket_obj = {
                "id": ticket,
                "num": random.randint(1,10),
                "row": random.randint(1,3),
            }
            objects.append(ticket_obj)
    return objects

@vip_ticket.field("show")
@convert_kwargs_to_snake_case
async def resolve_vip_tickets(obj, info):
    print("-------------show field resolver------------------")
    global counter
    counter += 1
    print(f"Counter == {counter}.")
    parts_obj = obj['id'].split("*")
    return {'name': parts_obj[0], 'date': parts_obj[2]}

@ord_ticket.field("show")
@convert_kwargs_to_snake_case
async def resolve_ord_tickets(obj, info):
    print("-------------show field resolver------------------")
    global counter
    counter += 1
    print(f"Counter == {counter}.")
    parts_obj = obj['id'].split("*")
    return {'name': parts_obj[0], 'date': parts_obj[2]}