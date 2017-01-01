import urllib
import urllib2
import base64
token_url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
client_id = 'ARRSMxRdTt_q6pD6LVOtFTztKKcRBpHfPq5G-UjarElLqrAW5S-PhTGlTE3_EOM4GvsHh8XCjIf4NHpQ'
client_secret = 'EJfeN50IWvCDz4hnZK31vjLa284dQJzjnlY1phwdzwNdYC-sE8ME11fF4TWEyWd60UMcTYySnG3GkKqa'

credentials = "%s:%s" % (client_id, client_secret)
encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

header_params = {
    "Authorization": ("Basic %s" % encode_credential),
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
param = {
    'grant_type': 'client_credentials',
}
data = urllib.urlencode(param)

request = urllib2.Request(token_url, data, header_params)
response = urllib2.urlopen(request).read()
print response
