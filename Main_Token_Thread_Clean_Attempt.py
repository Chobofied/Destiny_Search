from threading import *
import webbrowser
from flask import Flask
import requests
import json
from flask import request


#Stores Dummy Class Data to be filled in 
class App_Data:
    x=3
    Client_ID=1
    Client_Secret=1
    api_key = 'x'



app = Flask(__name__)

@app.route('/')
def homepage():
    text = '<a href="%s">Lets make a new Token for Destiny 2</a>'

    error = request.args.get('error', '')
    code = request.args.get('code', '')

    if code != '':
    
        #Session Data retrieved from class
        CLIENT_ID = App_Data.Client_ID
        CLIENT_SECRET=App_Data.Client_Secret
        api_key=App_Data.api_key

        print('Code Given from Bungie '+code)
        url = 'https://www.bungie.net/Platform/App/OAuth/token/'


        # Either Way Works
        # data='grant_type=authorization_code&code='+ code + '&client_id='+CLIENT_ID
        data = {'grant_type': 'authorization_code',
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret':CLIENT_SECRET}

        #Request Made to Bungie for Access Token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=data)


        access_token = json.loads(response.text)['access_token']
        refresh_token = json.loads(response.text)['refresh_token']

        #Save the Token to a text file
        f = open("token.txt", "w+")
        f.write(str(access_token) + "\n")
        f.write(str(refresh_token) + "\n")
        f.close()

        return 'The Access Token is '+access_token


    return text % make_authorization_url()

def make_authorization_url():
    CLIENT_ID = App_Data.Client_ID
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    #save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "reauth": 'true'}
              #"redirect_uri": REDIRECT_URI}
    # "state": state,
    # "redirect_uri": REDIRECT_URI,
    # "duration": "temporary",
    # "scope": "identity"}
    import urllib
    url = "https://www.bungie.net/en/oauth/authorize?" + urllib.parse.urlencode(params)
    return url

def runApp():
    app.run(debug=True, use_reloader=False, port=65011)


def main(User):

    #Bungie App Data
    App_Data.Client_ID=User.C_ID
    App_Data.Client_Secret=User.C_S
    App_Data.api_key=User.api_key

    #Start Thread for Flask App
    t1 = Thread(target=runApp).start()

    #Open Up new url to get code from Bungie for specific User input
    url = 'http://127.0.0.1:65011/'
    webbrowser.open(url, new=1)


if __name__ == '__main__':
    user='test'
    main(user)

