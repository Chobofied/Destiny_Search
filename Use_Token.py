import requests
import json
import Main_Token_Thread
import Destiny_test


CLIENT_ID = "37141"
api_key='afb7b0fcc0604ab49612af8de1b758f2'
CLIENT_SECRET='L6j-9vwZFv.uLcbx76o-o9JrEKSglu2Xz6lde45bYSA'

## See If Token Exists
try:
    file = open("token.txt")
    data = file.readlines()
    file.close()

#If Token doesnt exist, lets make a token
except FileNotFoundError:

    Main_Token_Thread.main()

    import os.path
    import time

    dir_path = os.path.dirname(os.path.realpath(__file__))
    while not os.path.exists(dir_path+'/token.txt'):
        time.sleep(1)


    #Need to add an await command here, or wait until 'File token.txt' is made

    file = open("token.txt")
    data = file.readlines()
    file.close()
    print("Made a New Tokens")


## Try and Refresh a Token, Time out error may have happend
try:
    access_token = data[0].strip('\n')
    refresh_token = data[1].strip('\n')

    url = 'https://www.bungie.net/Platform/App/OAuth/token/'

    #Refresh Token
    Rdata = {'grant_type': 'refresh_token',
             'refresh_token': refresh_token,
             'client_id': CLIENT_ID,
             'client_secret': CLIENT_SECRET}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    Rresponse = requests.request("POST", url, headers=headers, data=Rdata)

    if Rresponse.status_code != 200:

        import os.path
        import time

        os.remove("token.txt")
        Main_Token_Thread.main()



        dir_path = os.path.dirname(os.path.realpath(__file__))
        while not os.path.exists(dir_path + '/token.txt'):
            time.sleep(1)

        # Need to add an await command here, or wait until 'File token.txt' is made

        file = open("token.txt")
        data = file.readlines()
        file.close()
        print("Made a New Tokens")

        access_token = data[0].strip('\n')
        refresh_token = data[1].strip('\n')
    else:
        x=4
        access_token = json.loads(Rresponse.text)['access_token']
        refresh_token = json.loads(Rresponse.text)['refresh_token']
        f = open("token.txt", "w+")
        f.write(str(access_token) + "\n")
        f.write(str(refresh_token) + "\n")
        f.close()


    headers = {
        'X-API-Key': api_key,
        'Authorization': 'Bearer ' + access_token}

    url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"
    response2 = requests.request("GET", url2, headers=headers)

    x=4
    print(response2.content)


except ClientResponseError:
    print("Could Not Refresh, Lets Make a new Token")
    ##Failed to Refresh, Exit

if response2.status_code == 200:
    print('Goodness')
else:
    print('We need to recreate or refresh New Token')


Item=Destiny_test.main()

x=4

