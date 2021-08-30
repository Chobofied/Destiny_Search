import requests
import json
import Main_Token_Thread
import Destiny_test

def identify_item(item,api_key):
    ##item_instance_id = item['itemInstanceId']
    item_hash = str(item['itemHash'])

    baseurl = 'https://bungie.net/Platform/Destiny2/'
    #entity_type = 'DestinyStatDefinition'
    entity_type ='DestinyInventoryItemDefinition'

    item_url=baseurl + 'Manifest/' + entity_type + '/' + item_hash
    #item_url = get_entity_definition_url(item_hash, 'DestinyInventoryItemDefinition', my_api_key)
    my_headers = {"X-API-Key": api_key}
    response = requests.get(item_url, headers=my_headers)
    return response.json()



    #item_summary = destiny2_api_public(item_url, my_api_key)


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



# Create a list of active Destiny 2 items for character
char_id,user_id,char_items,Item=Destiny_test.main()

item_data=[]
for item in char_items:
    #identify_item(char_items[0], api_key)
    item_data.append(identify_item(item,api_key))




#Trying to get vault Data Here!! May need to change to get to Char vs Get Profile
# %%GetProfile
# Component types include: 100 profiles; 200 characters; 201 non-equipped items (need oauth);
# 205: CharacterEquipment: what they currently have equipped. All can see this
#See https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html#schema_Destiny-DestinyComponentType
#Need to make this 201 to see vault items



#components = '200,205'
#https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html#schema_Destiny-DestinyComponentType
components = '201'

membership_type='1'
baseurl = 'https://www.bungie.net/Platform/Destiny2/'


char_url=baseurl + membership_type + '/' + 'Profile/' + user_id +'/Character/'+ char_id+ '/?components=' + components
#char_url=baseurl + membership_type + '/' + 'Profile/' + user_id +'/Character/'+ char_id+ '/'
#char_url=baseurl + membership_type + '/' + 'Profile/' + user_id +'/Character/'+ char_id+ '/?components=CharacterInventories'

#my_headers = {"X-API-Key": api_key}


my_headers = {
    'X-API-Key': api_key,
    'Authorization': 'Bearer ' + access_token}

response2 = requests.request("GET", char_url, headers=my_headers).json()

char_data=response2['Response']['inventory']['data']['items']

item_data=[]
count=1
for item in char_data:
    #item_ident.append(identify_item(item, api_key))
    count=count+1
    print(count)
    item_data.append(identify_item(item,api_key))



character_summary = requests.get(char_url, headers = my_headers)
character_summary=character_summary.json()
character_items = character_summary['Response']['equipment']['data']['items']  #
first_item = character_items[0]

x=4

