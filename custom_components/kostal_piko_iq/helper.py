import base64
import hashlib
import hmac
import json
import os
import random
import requests
import string

from Crypto.Cipher import AES

"""
Inspired by https://github.com/ITTV-tools/kostalplenticorepy

Accessing RESTful API of Kostal PIKO IQ / Plenticore Plus and even Plenticore inverters.
"""
class KostalRestClient:
    def __init__(self, host, password):
        self.host = host
        self.password = password

    def randomString(self, stringLength):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    def getUrl(self, path):
        return "http://" + self.host + "/api/v1" + path

    def login(self):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        nonce = base64.b64encode(
            self.randomString(12).encode('utf-8')).decode('utf-8')
        response = requests.post(
            self.getUrl("/auth/start"),
            data=json.dumps({"username": "user", "nonce": nonce}),
            headers=headers,
            timeout=10)
        response = json.loads(response.text)

        nonce_resp = response['nonce']
        transaction_id = response['transactionId']
        rounds = response['rounds']
        salt = response['salt']
        salt_base64 = base64.b64decode(salt)

        msg = "n=user,r=" + nonce + ",r=" + nonce_resp + ",s=" + \
              salt + ",i=" + str(rounds) + ",c=biws,r=" + nonce_resp

        pw_hash = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'),
                                      salt_base64, rounds)
        client_key = hmac.new(pw_hash, "Client Key".encode('utf-8'),
                              hashlib.sha256).digest()
        client_key_hash = hashlib.sha256(client_key).digest()
        client_hmac = hmac.new(client_key_hash, msg.encode('utf-8'),
                               hashlib.sha256).digest()

        proof = base64.b64encode(
            bytes(a ^ b for (a, b) in zip(client_key, client_hmac))).decode('utf-8')
        response = requests.post(
            self.getUrl("/auth/finish"),
            data=json.dumps({"transactionId": transaction_id, "proof": proof}),
            headers=headers,
            timeout=10)
        response = json.loads(response.text)

        token = response['token']

        session_key = hmac.new(
            client_key_hash, "Session Key".encode('utf-8'), hashlib.sha256)
        session_key.update(msg.encode('utf-8'))
        session_key.update(client_key)
        protocol_key = session_key.digest()
        random_number = os.urandom(16)

        cipher = AES.new(protocol_key, AES.MODE_GCM, random_number)
        cipher, authtag = cipher.encrypt_and_digest(token.encode('utf-8'))

        response = requests.post(
            self.getUrl("/auth/create_session"),
            data=json.dumps({
                "transactionId": transaction_id,
                "iv": base64.b64encode(random_number).decode('utf-8'),
                "tag": base64.b64encode(authtag).decode("utf-8"),
                "payload": base64.b64encode(cipher).decode('utf-8')
            }),
            headers=headers,
            timeout=10)
        response = json.loads(response.text)

        session_id = response['sessionId']

        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'authorization': "Session " + session_id
        }
        response = requests.get(url=self.getUrl("/auth/me"),
                                headers=self.headers)
        response = json.loads(response.text)
        if not response['authenticated']:
            raise Exception(response)

    def getProcessdata(self, moduleid, processdata):
        datareq = [{"moduleid": moduleid, "processdataids": processdata}]
        datareq = json.dumps(datareq)
        response = requests.post(url=self.getUrl("/processdata"),
                                 data=datareq,
                                 headers=self.headers,
                                 timeout=10)
        response = json.loads(response.text)
        return response[0]['processdata']
