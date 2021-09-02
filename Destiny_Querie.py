import requests
import json
import Token_Creation
import Destiny_test
import os.path
import time

class Destiny_Session():
    def __init__(self,User):
        self.C_ID=User.C_ID
        self.C_S=User.C_S
        self.api_key=User.api_key
        self.access_token=User.access_token
        self.baseurl='https://www.bungie.net/Platform/Destiny2/'
        self.membership_type='1'

        self.headers = {
            'X-API-Key': self.api_key,
            'Authorization': 'Bearer ' + self.access_token}

    def get_User_Data(self):
        headers = {
                'X-API-Key': self.api_key,
                'Authorization': 'Bearer ' + self.access_token}

        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"

        self.User_Data = requests.request("GET", url2, headers=headers)
        self.User_Data=json.loads(self.User_Data.text)

        self.user_name = self.User_Data['Response']['uniqueName']
        self.user_name = self.user_name.replace('#', '%23')
        print(self.User_Data['Response']['uniqueName'])

    def get_Player_Summary(self):
        url=self.baseurl + 'SearchDestinyPlayer/' + self.membership_type + '/' + self.user_name + '/'
       

        response = requests.get(url, headers = self.headers)
        self.Player_Summary=json.loads(response.content)['Response'][0]
        self.membershipId=self.Player_Summary['membershipId']
        x=4

    def get_Char_Data(self):
        #components='200,205'
        components='201'
        url=self.baseurl + self.membership_type + '/' + 'Profile/' + self.membershipId + '/?components=' + components
        response = requests.get(url, headers = self.headers)
        response=json.loads(response.content)['Response']
        x=3        