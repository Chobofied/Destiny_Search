import requests
import json
import Main_Token_Thread_Clean_Attempt
import Destiny_test

class Destiny_Data():
    def __init__(self,token_file,CLIENT_ID,CLIENT_SECRET,api_key):
        self.C_ID=CLIENT_ID
        self.C_S=CLIENT_SECRET
        self.api_key=api_key
        self.get_token(token_file)
        


    def get_token(self,token_file):
        try:
            file = open(token_file)
            self.data = file.readlines()
            file.close()
        except FileNotFoundError:
            #We need to make a Token

            Main_Token_Thread_Clean_Attempt.main(self)

            import os.path
            import time

            dir_path = os.path.dirname(os.path.realpath(__file__))
            while not os.path.exists(dir_path+'/token.txt'):
                time.sleep(1)

            file = open("token.txt")
            self.data = file.readlines()
            file.close()
            print("Made a New Tokens")

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


            #If there is an error trying to refresh the token, lets make a brand new one
            if Rresponse.status_code != 200:

                import os.path
                import time

                os.remove("token.txt")

                Main_Token_Thread_Clean_Attempt.main()

                dir_path = os.path.dirname(os.path.realpath(__file__))
                while not os.path.exists(dir_path + '/token.txt'):
                    time.sleep(1)

                # Need to add an await command here, or wait until 'File token.txt' is made

                file = open("token.txt")
                data = file.readlines()
                file.close()
                print("Made a New Tokens")

                self.access_token = self.data[0].strip('\n')
                self.refresh_token = self.data[1].strip('\n')
            else:
                x=4
                self.access_token = json.loads(Rresponse.text)['access_token']
                self.refresh_token = json.loads(Rresponse.text)['refresh_token']
                f = open("token.txt", "w+")
                f.write(str(self.access_token) + "\n")
                f.write(str(self.refresh_token) + "\n")
                f.close()
        except ClientResponseError:
                print("Could Not Refresh, Lets Make a new Token")
                ##Failed to Refresh, Exit


            
    def get_User_Data(self):
        headers = {
                'X-API-Key': self.api_key,
                'Authorization': 'Bearer ' + self.access_token}


        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"

        self.User_Data = requests.request("GET", url2, headers=headers)
        self.User_Data=json.loads(self.User_Data.text)
        print(self.User_Data['Response']['uniqueName'])
        x=4
        

       
        
       


def Main_Routine(token_file,CLIENT_ID,CLIENT_SECRET,api_key):
    token_file="token.txt"
    User=Destiny_Data(token_file,CLIENT_ID,CLIENT_SECRET,api_key)
    User.get_User_Data()
    x=4


if __name__ == '__main__':

    ## User Inputs
    token_file="token.txt"
    CLIENT_ID = "37141"
    api_key='afb7b0fcc0604ab49612af8de1b758f2'
    CLIENT_SECRET='L6j-9vwZFv.uLcbx76o-o9JrEKSglu2Xz6lde45bYSA'
    Main_Routine(token_file,CLIENT_ID,CLIENT_SECRET,api_key)
