import requests
import json
import Token_Creation
import Destiny_test
import os.path
import time

from Destiny_Querie import Destiny_Session

import SQL_DB



class Destiny_Data():
    def __init__(self,token_file,CLIENT_ID,CLIENT_SECRET,api_key):
        self.C_ID=CLIENT_ID
        self.C_S=CLIENT_SECRET
        self.api_key=api_key
        self.token_file=token_file
        self.get_token()

    def Make_token(self):
        Token_Creation.main(self)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        while not os.path.exists(dir_path+'/'+self.token_file):
            time.sleep(1)

        file = open(self.token_file)
        self.data = file.readlines()
        file.close()
        print("Made a New Tokens")
        

    def get_token(self):
        try:
            file = open(self.token_file)
            self.data = file.readlines()
            file.close()

        #If token file cannot be found, lets make a new one
        except FileNotFoundError:
            #We need to make a Token
            self.Make_token()


        ## Try and Refresh a Token, Time out error may have happend
        try:
            self.access_token = self.data[0].strip('\n')
            self.refresh_token = self.data[1].strip('\n')

            url = 'https://www.bungie.net/Platform/App/OAuth/token/'

            #Refresh Token
            Rdata = {'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token,
                    'client_id': self.C_ID,
                    'client_secret': self.C_S}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            Rresponse = requests.request("POST", url, headers=headers, data=Rdata)


            
            if Rresponse.status_code == 200:
                # Extract the token codes
                x=4
                self.access_token = json.loads(Rresponse.text)['access_token']
                self.refresh_token = json.loads(Rresponse.text)['refresh_token']
                f = open(token_file, "w+")
                f.write(str(self.access_token) + "\n")
                f.write(str(self.refresh_token) + "\n")
                f.close()


            else:
                #If there is an error trying to refresh the token, lets make a brand new one
                import os.path
                import time

                Main_Token_Thread_Clean_Attempt.main()

                dir_path = os.path.dirname(os.path.realpath(__file__))

                # Waits until token.txt file is created
                # Need to add an async await command here instead, or wait until 'File token.txt' is made
                while not os.path.exists(dir_path + '/'+self.token_file):
                    time.sleep(1)

                file = open(self.token_file)
                data = file.readlines()
                file.close()
                print("Made a New Tokens")

                self.access_token = self.data[0].strip('\n')
                self.refresh_token = self.data[1].strip('\n')

        except ClientResponseError:
                print("Could Not Refresh, Lets Make a new Token")
                os.remove(token_file)
                self.Make_token()
          
    def get_User_Data(self):
        headers = {
                'X-API-Key': self.api_key,
                'Authorization': 'Bearer ' + self.access_token}

        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"

        self.User_Data = requests.request("GET", url2, headers=headers)
        self.User_Data=json.loads(self.User_Data.text)
        print(self.User_Data['Response']['uniqueName'])
               

def Main_Routine(token_file,CLIENT_ID,CLIENT_SECRET,api_key):
    #token_file="token.txt"
    User=Destiny_Data(token_file,CLIENT_ID,CLIENT_SECRET,api_key)
    User.get_User_Data()

    Session=Destiny_Session(User)
    Session.get_User_Data()
    Session.get_Player_Summary()
    Session.get_Char_Data()
    

    x=4


if __name__ == '__main__':

    ## User Inputs
    token_file="token.txt"
    CLIENT_ID = "37141"
    api_key='afb7b0fcc0604ab49612af8de1b758f2'
    CLIENT_SECRET='L6j-9vwZFv.uLcbx76o-o9JrEKSglu2Xz6lde45bYSA'
    Main_Routine(token_file,CLIENT_ID,CLIENT_SECRET,api_key)
    

