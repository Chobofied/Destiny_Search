import requests
import json


CLIENT_ID = "37141"

REDIRECT_URI = "http://localhost:65010/reddit_callback2"
api_key='afb7b0fcc0604ab49612af8de1b758f2'
CLIENT_SECRET='L6j-9vwZFv.uLcbx76o-o9JrEKSglu2Xz6lde45bYSA'

## See If File Exists
try:
    file = open("token.txt")
    data = file.readlines()
except ClientResponseError:
    print("Could not refresh tokens")
    ##MAke a token
    #sys.exit(-1)

## Try and Refresh Token
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



except ClientResponseError:
    print("Could Not Refresh, Lets Make a new Token")
    ##Failed to Refresh, Exit

if response2.status_code == 200:
    print('Goodness')
else:
    print('We need to recreate or refresh New Token')




# open the data file
file = open("token.txt")
# read the file as a list
data = file.readlines()

access_token=data[0].strip('\n')
refresh_token=data[1].strip('\n')
# close the file
file.close()

headers = {
            'X-API-Key': api_key,
            'Authorization': 'Bearer ' + access_token}

url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"
response2 = requests.request("GET", url2, headers=headers)

x=3
print(data)