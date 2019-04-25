from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from django.core.exceptions import ValidationError
import json
import hashlib
from .models import UserDetail


class ServerTestCase(TestCase):

    username = hashlib.sha256("jguk#9008".encode('utf-8')).hexdigest()
    address = hashlib.sha256("sfjklasdflkdjfklj".encode('utf-8')).hexdigest()
    private_key = hashlib.sha256("sfdxcvlkjxvlkj".encode('utf-8')).hexdigest()
    hash = hashlib.sha256("98a7wsdakjfhag0u".encode('utf-8')).hexdigest()

    def test_register_need_post(self):
        # Register must be a POST

        client = Client()
        response = client.get('/register/')
        self.assertEqual(response.status_code, 404)


    def test_get_user_info_not_exist(self):
        # If user data is requested with wrong hash then we give nothing away
        user = hashlib.sha256("jguk#9008".encode('utf-8')).hexdigest()

        client = Client()
        response = client.get('/userInfo/' + user + '/testhash/')

        data = json.loads(response.content)

        self.assertEqual(data['status'], 'cheeky-monkey')

    def test_get_user_address_not_exist(self):
        # If user data is requested with wrong hash then we give nothing away
        user = hashlib.sha256("jguk#9008".encode('utf-8')).hexdigest()

        client = Client()
        response = client.get('/userAddress/' + user + '/')

        data = json.loads(response.content)

        self.assertEqual(data['status'], 'no-user')

    def test_add_new_unregistered_user(self):
        # Adds a new user who hasn't been registered before
        # This should be improved security wise

        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(len(userRecord), 0, "Should be no intial user")

        data = {
            'username': self.username,
            'address': self.address,
            'privatekey': self.private_key,
            'hash': self.hash
        }
        dum = json.dumps(data)
        client = Client()

        response = client.post('/register/', dum, content_type='application/json')

        data = json.loads(response.content)

        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(data['status'], 'user-added')
        self.assertEqual(len(userRecord), 1, "Should user added")
        self.assertEqual(userRecord[0].username, self.username)
        self.assertEqual(userRecord[0].address, self.address)
        self.assertEqual(userRecord[0].private_key, self.private_key)
        self.assertEqual(userRecord[0].hash, self.hash)

        response = client.get('/userAddress/' + self.username + '/')
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['username'], self.username)
        self.assertEqual(data['address'], self.address)


    def test_false_update_user(self):
        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(len(userRecord), 0, "Should be no intial user")

        data = {
            'username': self.username,
            'address': self.address,
            'privatekey': self.private_key,
            'hash': self.hash
        }
        dum = json.dumps(data)
        client = Client()

        response = client.post('/register/', dum, content_type='application/json')

        data = json.loads(response.content)
        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(data['status'], 'user-added')
        self.assertEqual(len(userRecord), 1, "Should user added")

        data = {
            'username': self.username,
            'address': 'newaddr',
            'privatekey': 'newkey',
            'hash': 'wrong'
        }
        dum = json.dumps(data)
        client = Client()

        response = client.post('/register/', dum, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'cheeky-monkey')

        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(len(userRecord), 1, "Should user added")
        self.assertEqual(userRecord[0].username, self.username)
        self.assertEqual(userRecord[0].address, self.address)
        self.assertEqual(userRecord[0].private_key, self.private_key)
        self.assertEqual(userRecord[0].hash, self.hash)

    def test_ok_update_user(self):
        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(len(userRecord), 0, "Should be no intial user")

        data = {
            'username': self.username,
            'address': self.address,
            'privatekey': self.private_key,
            'hash': self.hash
        }
        dum = json.dumps(data)
        client = Client()

        response = client.post('/register/', dum, content_type='application/json')

        data = json.loads(response.content)
        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(data['status'], 'user-added')
        self.assertEqual(len(userRecord), 1, "Should user added")

        data = {
            'username': self.username,
            'address': 'newaddr',
            'privatekey': 'newkey',
            'hash': self.hash
        }
        dum = json.dumps(data)
        client = Client()

        response = client.post('/register/', dum, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'user-updated')

        userRecord = UserDetail.objects.filter(username=self.username)
        self.assertEqual(len(userRecord), 1, "Should user added")
        self.assertEqual(userRecord[0].username, self.username)
        self.assertEqual(userRecord[0].address, 'newaddr')
        self.assertEqual(userRecord[0].private_key, 'newkey')
        self.assertEqual(userRecord[0].hash, self.hash)

    def test_get_user_info_fails_wronghash(self):

        incorrecthash = hashlib.sha256("thisiswrong".encode('utf-8')).hexdigest()

        client = Client()

        data = {
            'username': self.username,
            'address': self.address,
            'privatekey': self.private_key,
            'hash': self.hash
        }
        dum = json.dumps(data)

        response = client.post('/register/', dum, content_type='application/json')
        response = client.get('/userInfo/' + self.username + '/' + incorrecthash + '/')

        data = json.loads(response.content)

        self.assertEqual(data['status'], 'cheeky-monkey')


    def test_get_user_info_ok(self):
        client = Client()
        data = {
            'username': self.username,
            'address': self.address,
            'privatekey': self.private_key,
            'hash': self.hash
        }
        dum = json.dumps(data)

        response = client.post('/register/', dum, content_type='application/json')
        response = client.get('/userInfo/' + self.username + '/' + self.hash + '/')

        data = json.loads(response.content)

        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['privatekey'], self.private_key)
        self.assertEqual(data['address'], self.address)
        self.assertEqual(data['username'], self.username)
