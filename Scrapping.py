import requests
from bs4 import BeautifulSoup
from firebase import firebase
import random
firebase = firebase.FirebaseApplication('https://pesdatabase-d2d99.firebaseio.com/')

def player_scrap(link):
    url = link #Getting url from the link passed as paramater

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    #Making a SOUP Object

    playerMainTable = soup.find('table',{'class':'player'}) #Fining Player Table (More than one table present in website)

    tr1 = playerMainTable.findAll('tr') #Finding all Rows
    allTables = tr1[0].find_all('table') #Get all table inside the first table row
    
    main_dict = {} #Dictionary to push to firebse

    for tables in allTables:
        dict = {} #Sub dict, to create dictionaries of dictionaries

        all_rows = tables.find_all('tr')
        #find all rows in sub table

        for i in all_rows:
            try:
                lable = i.find('th') 
                value = i.find('td')

                #Saving data according to structure of website

                print(lable.text, " ", value.text)

                dict[lable.text] = value.text #Put value into dict
                #result = firebase.put('/'+unique_num,lable.text,value.text)
            except:
                break
            main_dict.update(dict)
    result = firebase.post('/players',main_dict) ##POST IN FIREBASE
    print(result)



url = 'http://pesdb.net/pes2019/' #BASE URL

source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, "html.parser")

#CONVERTING WEBSITE CODE TO BS4 OBJECT

tables = soup.find('table',{'class': 'players'}) #Find all tables with class name 'players'

tr = tables.find_all("tr") #FINDING ALL ROWS in TABLE and Storing them in tr

for t in tr:
    td = t.find_all("td") 
    row = []
    c = 0
    for i in td:
        row.append(i.text) #GETTING EACH PLAYER
        if (c == 1):
            link = i.a.get('href')[1:] #LINK OF DETAILS OF EACH PLAYER
            player_scrap("http://pesdb.net/pes2019"+link) # Appending at the end of base url to jump to next page
        c = c + 1
    print(row)

