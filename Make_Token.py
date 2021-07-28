CLIENT_ID = "37141"
# CLIENT_SECRET = "IHuCXKBZe__SQP7bfAeBZllBRCnuhA"
# http://localhost:65010/
REDIRECT_URI = "http://localhost:65010/reddit_callback2"
api_key='afb7b0fcc0604ab49612af8de1b758f2'
api_key='afb7b0fcc0604ab49612af8de1b758f2'
CLIENT_SECRET='L6j-9vwZFv.uLcbx76o-o9JrEKSglu2Xz6lde45bYSA'

# AA=requests.get('https://www.bungie.net', params='en/OAuth/Authorize')

from flask import Flask
import requests
import json

"""
try token

try refresh


"""

app = Flask(__name__)


@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'

    # test
    error = request.args.get('error', '')
    code = request.args.get('code', '')

    #token='CO6wAxKGAgAgERb56w/nq+YTDalgzcW8VDiuIwPH6kL64gGV1J9E4JvgAAAA36a2QbvmYXH9ujUt9XLxG9XKQIxSTJmyNI8TZ2P3dAqzj8DViW/oFARJrq0FYgbyToSN3OlMKYs6kOs16Bo5PNZBOmqoBT7WFiQk9RNmugBwpUwBEPbKKdxE0NDz0oOWwxMGwgexQVR5gsD+LK6b4ct6B7nfq+ub6AfblRBlH73iQjZY4iLbTAh0tNd6vwAaEfTMAESbSB1jLkKi6MImNvuA6Tkr92ZwTKavN4/taxjc3pPA7V+03CcL0YDSBXNj3wm1yPrGwdzGRJ6AVFU9yt+kDSZfcjhMcYEXjYrP5vY='

    if code != '':
        print(code)

        CLIENT_ID = '37141'
        url = 'https://www.bungie.net/Platform/App/OAuth/token/'
        api_key = 'afb7b0fcc0604ab49612af8de1b758f2'


        # Either Way Works
        # data='grant_type=authorization_code&code='+ code + '&client_id='+CLIENT_ID
        data = {'grant_type': 'authorization_code',
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret':CLIENT_SECRET}

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # headers={'Content-Type':'application/x-www-form-urlencoded'}

        # response = requests.request("POST", url, headers=headers, data=payload)
        response = requests.request("POST", url, headers=headers, data=data)

        access_token = json.loads(response.text)['access_token']
        refresh_token = json.loads(response.text)['refresh_token']

        f = open("token.txt", "w+")
        f.write(str(access_token) + "\n")
        f.write(str(refresh_token) + "\n")
        f.close()


        headers = {
            'X-API-Key': api_key,
            'Authorization': 'Bearer ' + access_token}

        #data = {'grant_type': 'authorization_code',
        #        'code': token,
        #        'client_id': CLIENT_ID,
        #        'client_secret':CLIENT_SECRET}


        url3 = "https://www.bungie.net/Platform/User/ReadBasicUserProfile/"
        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"
        response2 = requests.request("GET", url2, headers=headers)


        B = json.loads(response2.content)

        x=3

        Rdata = {'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET}

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        Rresponse = requests.request("POST", url,headers=headers, data=Rdata)

        return access_token

    return text % make_authorization_url()


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    #save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "redirect_uri": REDIRECT_URI}
    # "state": state,
    # "redirect_uri": REDIRECT_URI,
    # "duration": "temporary",
    # "scope": "identity"}
    import urllib
    url = "https://www.bungie.net/en/oauth/authorize?" + urllib.parse.urlencode(params)
    return url


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.


from flask import abort, request,redirect


if __name__ == '__main__':
    app.run(debug=True, port=65011)
    x=4