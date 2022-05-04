from .methods.transaction import Transaction
from .methods.general import General
from .methods.address import Address
from .methods.token import Token
from . import utils

def GetInfo():
    return General.info()

def EstimateFee():
    return General.fee()

def AddressUnspent(address=None, amount=0, token="AOK"):
    return Address.unspent(address, amount, token)

def AddressBalance(address=None):
    return Address.balance(address)

def AddressHistory(address=None):
    return Address.history(address)

def AddressMempool(address=None):
    return Address.mempool(address)

def AddressMempoolRaw(address=None):
    return Address.mempool(address, True)

def TransactionInfo(thash=None):
    return Transaction.info(thash)

def Broadcast(raw=None):
    return Transaction.broadcast(raw)

def CheckHistory(addresses=[]):
    return Address.check(addresses)

def TransactionBatch(hashes=[]):
    result = []
    for thash in hashes:
        result.append(Transaction.info(thash))

    return utils.response(result)

def TokensList(offset=0, count=50, search=""):
    return Token.list(offset, count, search)
