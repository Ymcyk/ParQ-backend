import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import base64
import json

from .config import *

def get_token():
    credentials = "{0}:{1}".format(CLIENT_ID, SECRET)
    encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    header_params = {
            "Authorization": ("Basic {}".format(encode_credential)),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
                    }

    data = "grant_type=client_credentials".encode()

    request = Request(TOKEN_URL, data, header_params)
    response = urlopen(request).read()
    json_data = json.loads(response.decode("utf-8"))
    return json_data['access_token']

def get_payment_money(payment_id):
    token = get_token()
    # token = base64.b64encode(token.encode('utf-8')).decode('utf-8').replace("\n", "")
    req = Request('https://api.sandbox.paypal.com/v1/payments/payment/{}'.format(payment_id))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer {}'.format(token))
    res = urlopen(req).read()
    print(res)

