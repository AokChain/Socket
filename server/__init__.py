from .models import Connection, Room
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import request
from flask import Flask
import flask_socketio
from pony import orm
from . import socket
import config

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = config.secret
sio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

from . import subscription

thread = None

@orm.db_session
def Connect():
    if not Connection.get(sid=request.sid):
        Connection(**{"sid": request.sid})

    global thread

    if thread is None:
        thread = sio.start_background_task(target=subscription.loop)

@orm.db_session
def Disconnect():
    if (connection := Connection.get(sid=request.sid)):
        for room in connection.rooms:
            flask_socketio.leave_room(room.name, connection.sid)
            room.delete()

        connection.delete()

@orm.db_session
def SubscribeBlocks():
    flask_socketio.join_room("blocks", request.sid)

    if (connection := Connection.get(sid=request.sid)):
        Room(**{"connection": connection, "name": "blocks"})

    return True

@orm.db_session
def UnsubscribeBlocks():
    flask_socketio.leave_room("blocks", request.sid)

    if (connection := Connection.get(sid=request.sid)):
        if (room := Room.get(name="blocks", connection=connection)):
            room.delete()

    return True


sio.on_event("connect", Connect)
sio.on_event("subscribe.blocks", SubscribeBlocks)
sio.on_event("unsubscribe.blocks", UnsubscribeBlocks)
sio.on_event("disconnect", Disconnect)

sio.on_event("general.info", socket.GetInfo)
sio.on_event("general.fee", socket.EstimateFee)
sio.on_event("general.tokens", socket.TokensList)
sio.on_event("address.unspent", socket.AddressUnspent)
sio.on_event("address.balance", socket.AddressBalance)
sio.on_event("address.history", socket.AddressHistory)
sio.on_event("address.mempool", socket.AddressMempool)
sio.on_event("address.mempool.raw", socket.AddressMempoolRaw)
sio.on_event("address.check", socket.CheckHistory)
sio.on_event("transaction.info", socket.TransactionInfo)
sio.on_event("transaction.broadcast", socket.Broadcast)
sio.on_event("transaction.batch", socket.TransactionBatch)
