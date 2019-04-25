from .models import UserDetail
from web3 import Web3
import time

def getUserAddress(username):

    print('Getting Address For User: ' + username)
    userinfo = UserDetail.objects.filter(username=username)

    if(len(userinfo) == 1):
        # print('User Exists')
        responseData = {
            'status': 'ok',
            'username': userinfo[0].username,
            'address': userinfo[0].address
        }
    else:
        # print('User Not Exists')
        responseData = {
            'status': 'no-user'
        }

    return responseData

def getUserInfo(username, hash):
    userinfo = UserDetail.objects.filter(username=username, hash=hash)

    if(len(userinfo) == 1):
        responseData = {
            'status': 'ok',
            'username': userinfo[0].username,
            'address': userinfo[0].address,
            'privatekey': userinfo[0].private_key
        }
    else:
        responseData = {
            'status': 'cheeky-monkey'
        }

    return responseData

def sendDai(SenderAddress, PrivateKey, DestinationAddress, EthAmount):
    w3 = Web3(Web3.HTTPProvider("https://dai.poa.network"))

    amount_in_wei = w3.toWei(EthAmount, 'ether')

    nonce = w3.eth.getTransactionCount(SenderAddress)

    txn_dict = {
        'to': DestinationAddress,
        'value': amount_in_wei,
        'gas': 21000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    }

    signed_txn = w3.eth.account.signTransaction(txn_dict, PrivateKey)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    txn_receipt = None
    count = 0
    while txn_receipt is None and (count < 50):

        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

        # print(txn_receipt)

        time.sleep(1)

    if txn_receipt is None:
        print('Transaction FAILED!!!!!!!!')
        return {'status': 'failed', 'error': 'timeout'}

    print('Alrighty then!!')
    return {'status': 'added', 'txn_receipt': txn_receipt}
