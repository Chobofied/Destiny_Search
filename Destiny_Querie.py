import requests
import json
import Token_Creation
import Destiny_test
import os.path
import time


import SQL_DB

import SQL_DB.Queries.Select as Sel
import SQL_DB.Queries.create as Cr

class Destiny_Session():

    #initial Data to use in Searches
    def __init__(self,api_key,access_token):
 
        self.api_key=api_key
        self.access_token=access_token
        self.baseurl='https://www.bungie.net/Platform/Destiny2/'
        self.membership_type='1'

        if self.access_token==None:
             self.headers = {
                'X-API-Key': self.api_key}
        else:
            self.headers = {
                'X-API-Key': self.api_key,
                'Authorization': 'Bearer ' + self.access_token}

        self.Make_DB()

    def Make_DB(self):

        cur_dir = str(os.getcwd())+'\\SQL_DB'
        DB_Name='Destiny_Data.db'
        DB_Path=str(cur_dir)+'\\'+str(DB_Name)

        #Initiates the Database, creates one if it doesnt already exist
        self.Destiny_DB=SQL_DB.sqllite_create.sqllite_db(DB_Path)

        #Makes the SQL Tables
        self.Destiny_DB.execute_query(Cr.create_itemhash_table)
        self.Destiny_DB.execute_query(Cr.create_users_table)
        self.Destiny_DB.execute_query(Cr.create_KDR_table)

        

    #This gets the unqiue Bungie User_Name (Cross Play)
    def get_User_Name(self):

        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"

        self.User_Data = requests.request("GET", url2, headers=self.headers)
        self.User_Data=json.loads(self.User_Data.text)

        self.user_name = self.User_Data['Response']['uniqueName']

        #For whatever reason, the # in the Bungie Unique name needs to be replaced with '%23' in order for the searches to work correctly
        self.user_name = self.user_name.replace('#', '%23')
        print(self.User_Data['Response']['uniqueName'])

        self.Destiny_DB.cursor.execute("INSERT INTO users (username) VALUES (?)",(self.user_name,))
        self.Destiny_DB.connection.commit()


    #This gets general Player information (membership ID, ect)
    def get_Player_Summary(self):
        url=self.baseurl + 'SearchDestinyPlayer/' + self.membership_type + '/' + self.user_name + '/'
       

        response = requests.get(url, headers = self.headers)
        self.Player_Summary=json.loads(response.content)['Response'][0]
        self.membershipId=self.Player_Summary['membershipId']
        x=4

    #This looks up specific information about the character (What items they have equipped) depending on the component selected. Some are public and some are private (needs Access Key)
    # See https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html for a list of components that can be quiered 
    
    def get_Char_Data(self):
        #components='200,205'
        components='200,201,205'
        url=self.baseurl + self.membership_type + '/' + 'Profile/' + self.membershipId + '/?components=' + components
        response = requests.get(url, headers = self.headers)
        self.Char_Data=json.loads(response.content)['Response']
        self.Char_ID=list(self.Char_Data['characterEquipment']['data'].keys())[0]

        self.equiped_hash=self.Char_Data['characterEquipment']['data'][str(self.Char_ID)]['items']

        #Empty Dictionary to be filled with infomation of the equiped items
        self.equiped={}

        # Loop Through all the equiped items and saves their results in a DB
        for item in self.equiped_hash:
            self.entity_hash=item['itemHash']
            self.get_Item_Data()
        
        x=5       

    def get_Item_Data(self):
        #Lets make an SQL Database  here, if it doesnt exist, then request it from Bungie

        # Tries to look for entity hash data in 'itemhash' table from 'Destiny_Data.db'
        try:
            self.Destiny_DB.cursor.execute("SELECT * FROM itemhash WHERE hash=(?)",(str(self.entity_hash),))
            result_STRING = self.Destiny_DB.cursor.fetchall()
            self.result_JSON=json.loads(result_STRING[0][3])['Response']

        # If there is an error looking up the item hash data, creates a new one by sending a request to Bungie'
        except Exception as e:
            print( "<p>Error: %s</p>" % str(e) )

            # Sends Item Hash Request to Bungie and formats to a dictionary (JSON)
            url= self.baseurl + 'Manifest/' + 'DestinyInventoryItemDefinition' + '/' + str(self.entity_hash)
            result_STRING = requests.get(url, headers = self.headers).text
            self.result_JSON = json.loads(result_STRING)['Response']

            # Inserts Item Hash results into an SQLlite DB to be queried later
            self.Destiny_DB.cursor.execute("INSERT INTO itemhash (hash, name, jresp) VALUES (?,?,?)",(self.entity_hash,self.result_JSON['displayProperties']['name'], result_STRING))
            self.Destiny_DB.connection.commit()

        finally:
            #Gets the Item Name and image URL
            item_name=self.result_JSON['displayProperties']['name']
            image_url='https://www.bungie.net'+self.result_JSON['displayProperties']['icon']

            #Adds the item name and image url to the equiped item dictionary
            self.equiped[str(self.entity_hash)]=[item_name,image_url]

            #Request Bungie for the image and save it locally
            img_data = requests.get(image_url).content
            cur_dir = str(os.getcwd())+'\\SQL_DB\\images\\'

            with open(cur_dir+item_name+'.jpg', 'wb') as handler:
                handler.write(img_data)

    def get_historical_stats(self):

       
        activity_modes='None'
        query_string = '?modes=' + activity_modes
        url=self.baseurl+self.membership_type+ '/Account/' + self.membershipId + '/Character/' + self.Char_ID + '/Stats/' + query_string

        response = requests.get(url, headers = self.headers)
        self.hist_Data=json.loads(response.content)['Response']
        self.KDR=self.hist_Data['allPvP']['allTime']['killsDeathsRatio']['basic']['displayValue']
        x=4

        #Adds KDR for user
        ##TO DO-- user_ID is currently hardcoded, need to fix

        try:
            self.Destiny_DB.cursor.execute("INSERT INTO KDR (KDR, user_id) VALUES (?,?)",(self.KDR,'1',))
            self.Destiny_DB.connection.commit()

        #If the User is alreay in the Database, lets update it with the latest value
        except Exception as e:
            print( "<p>Error: %s</p>" % str(e) )
            self.Destiny_DB.cursor.execute("UPDATE KDR SET KDR = (?) WHERE user_id = 1;",(self.KDR,))
            self.Destiny_DB.connection.commit()

  


def Main_Routine(api_key,access_token,user_name):

    
    Session=Destiny_Session(api_key,access_token)
    
    # If a User Token is not provided, Need to enter Bungie Unique Name Manually
    if access_token!=None:
        Session.get_User_Name()
    else:
        Session.user_name=user_name
        Session.user_name = Session.user_name.replace('#', '%23')
    Session.get_Player_Summary()
    Session.get_Char_Data()
    Session.get_historical_stats()
    x=4


if __name__ == '__main__':

    #Only Requiered if access token is not given
    user_name='Chobofied#0631'

    api_key='afb7b0fcc0604ab49612af8de1b758f2'
    access_token='COi/AxKGAgAghWkYJYcSS/EzMsCLL2xevEEMJVsHiENKOJ4gB17MFkbgAAAAjyu8M86RWPZ6NOZ0mAia1c3s8UqyDyxyzh+vZybr5OtIneVAmBF2iuwHvm3jHGUvsfqGJWRTmbA7c4r3PFWSh7jFBqWkfRvzNfbyvHkajZti68WLa6slHRcHPIjTWpQjYqPPnJTCyizOrarbr86pPcIJMiTo7b9FK+f/s+tgBt/skb39WRBYORert17fZOar/J7qjIu1xKMyC1LfYXEEUuAXgXZ/++0DQ+ySzHYCIUrW3au3elAgTCNnWO79yw2sx688mWi1IxYD4lv28puXpLCLSJ8SmkgPoG4BYIwuaN8='

    Main_Routine(api_key,access_token,user_name)
    
    
         




