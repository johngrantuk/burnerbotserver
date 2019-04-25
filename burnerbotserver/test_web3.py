from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from django.core.exceptions import ValidationError
import json
import hashlib
from .models import UserDetail
from eth_account import Account
from web3 import Web3
from . import crypto
import dotenv
import os

class Web3TestCase(TestCase):

    # load environment variables from .env
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)

    def test_account(self):

        acct = Account.create()
        # print(acct.privateKey)
        # print(acct.address)
        #self.assertEqual(False, True)

    def test_balance(self):
        username = hashlib.sha256("jguk#9008".encode('utf-8')).hexdigest()
        hash = hashlib.sha256("thisisthehahd".encode('utf-8')).hexdigest()
        privatekey = os.getenv("PRIVATEKEY")
        address = os.getenv("ADDRESS")
        load = UserDetail(username=username, address=address, private_key=privatekey, hash=hash)
        load.save()

        web3 = Web3(Web3.HTTPProvider("https://dai.poa.network"))

        senderInfo = crypto.getUserAddress(username)
        self.assertEqual(senderInfo['status'], 'ok')
        self.assertEqual(senderInfo['address'], address)

        senderBalance = web3.eth.getBalance(Web3.toChecksumAddress(senderInfo['address']))
        isBalance = (senderBalance > 0)
        self.assertEqual(isBalance, True)

        senderInfo = crypto.getUserInfo(username, hash)            # hash would come from discord input
        self.assertEqual(senderInfo['status'], 'ok')
        self.assertEqual(senderInfo['address'], address)
        self.assertEqual(senderInfo['username'], username)
        self.assertEqual(senderInfo['privatekey'], privatekey)

        rx_username = hashlib.sha256("test_receiver".encode('utf-8')).hexdigest()
        rx_Info = crypto.getUserAddress(rx_username)

        self.assertEqual(rx_Info['status'], 'no-user')

        rx_wallet = Account.create()
        rx_hash = hashlib.sha256("test_hadsh".encode('utf-8')).hexdigest()

        load = UserDetail(username=rx_username, address=rx_wallet.address, private_key=rx_wallet.privateKey, hash=rx_hash)
        load.save()

        rx_balance = web3.eth.getBalance(Web3.toChecksumAddress(rx_wallet.address))

        # send dai
        result = crypto.sendDai(senderInfo['address'], senderInfo['privatekey'], rx_wallet.address, '0.001')

        print(rx_username)
        print(rx_wallet.address)
        print(rx_wallet.privateKey)
        print(result['txn_receipt'])

        senderBalance2 = web3.eth.getBalance(Web3.toChecksumAddress(senderInfo['address']))
        rx_balance2 = web3.eth.getBalance(Web3.toChecksumAddress(rx_wallet.address))

        self.assertEqual(result['status'], 'added')
        self.assertEqual(senderBalance2, senderBalance - web3.toWei('0.001', 'ether') -  web3.toWei('0.000021', 'ether'))
        self.assertEqual(rx_balance2, rx_balance + web3.toWei('0.001', 'ether'))
