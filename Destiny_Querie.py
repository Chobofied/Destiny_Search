import requests
import json
import Token_Creation
import Destiny_test
import os.path
import time


import SQL_DB

class Destiny_Session():

    #initial Data to use in Searches
    def __init__(self,User):
        #self.C_ID=User.C_ID
        #self.C_S=User.C_S
        self.api_key=User.api_key
        self.access_token=User.access_token
        self.baseurl='https://www.bungie.net/Platform/Destiny2/'
        self.membership_type='1'

        self.headers = {
            'X-API-Key': self.api_key,
            'Authorization': 'Bearer ' + self.access_token}

        self.Make_DB()

    def Make_DB(self):

        cur_dir = str(os.getcwd())+'\\SQL_DB'
        DB_Name='Destiny_Data.db'
        DB_Path=str(cur_dir)+'\\'+str(DB_Name)

        self.Destiny_DB=SQL_DB.sqllite_create.sqllite_db(DB_Path)


        create_itemhash_table = """
            CREATE TABLE IF NOT EXISTS itemhash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash INTEGER NOT NULL,
            name TEXT NOT NULL,
            jresp TEXT NOT NULL,
            UNIQUE(hash, jresp)
            );
            """
    
        self.Destiny_DB.execute_query(create_itemhash_table)

    #This gets the unqiue Bungie User_Name (Cross Play)
    def get_User_Data(self):
        headers = {
                'X-API-Key': self.api_key,
                'Authorization': 'Bearer ' + self.access_token}

        url2 = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"

        self.User_Data = requests.request("GET", url2, headers=headers)
        self.User_Data=json.loads(self.User_Data.text)

        self.user_name = self.User_Data['Response']['uniqueName']

        #For whatever reason, the # in the Bungie Unique name needs to be replaced with '%23' in order for the searches to work correctly
        self.user_name = self.user_name.replace('#', '%23')
        print(self.User_Data['Response']['uniqueName'])

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

        self.equiped_items=self.Char_Data['characterEquipment']['data'][str(self.Char_ID)]['items']

        #Empty Dictionary to be filled with infomation of the equiped items
        self.equiped={}

        # Loop Through all the equiped items and saves their results in a DB
        for item in self.equiped_items:
            self.entity_hash=item['itemHash']
            self.get_Item_Data()
        
        #self.entity_hash=self.Char_Data['characterEquipment']['data'][str(self.Char_ID)]['items'][0]['itemHash']
        #self.get_Item_Data()
        x=3       

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


    def add_sqllite(self):
        #path="C://Users//Taylo//OneDrive//Python//Projects//Destiny//Main1//SQL_DB//sqllite_test.db"
        
        #test_sql=SQL_DB.sqllite_create.sqllite_db(path)



        The_Name='RealSlimShady'
        try:
            self.Destiny_DB.cursor.execute("INSERT INTO itemhash (hash, jresp) VALUES (?,?)",(self.entity_hash, self.AA))
        except Exception as e:
            print( "<p>Error: %s</p>" % str(e) )
            print('This input already exists')

        self.Destiny_DB.connection.commit()

        X=1216130969

        self.Destiny_DB.cursor.execute("SELECT * FROM itemhash WHERE hash=(?)",('1216130969',))
        #self.Destiny_DB.execute_read_query("SELECT * FROM itemhash WHERE hash=(?)",(1216130969))
        result = self.Destiny_DB.cursor.fetchall()


        Select_Item="""SELECT * FROM itemhash
                        WHERE id=1;"""

        results=self.Destiny_DB.execute_read_query(Select_Item)

        for result in results:
                print(result)
                AA=json.loads(result[2])

        x=2

    
         




