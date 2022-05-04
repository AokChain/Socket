from .methods.general import General
from . import utils
from . import sio

def loop():
    bestblockhash = None

    while True:
        data = General.info()

        if data["error"]:
            continue

        if data["result"]["bestblockhash"] != bestblockhash:
            bestblockhash = data["result"]["bestblockhash"]

            sio.emit("block.update", utils.response({
                "height": data["result"]["blocks"],
                "hash": bestblockhash
            }), room="blocks")

        sio.sleep(3)
