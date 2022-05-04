from datetime import datetime
from pony import orm

db = orm.Database("sqlite", "../socket.db", create_db=True)

class Connection(db.Entity):
    _table_ = "socket_connections"

    created = orm.Optional(datetime, default=datetime.utcnow)
    sid = orm.Required(str)

    rooms = orm.Set("Room")

class Room(db.Entity):
    _table_ = "socket_rooms"

    connection = orm.Required("Connection")
    name = orm.Required(str)


db.generate_mapping(create_tables=True)
