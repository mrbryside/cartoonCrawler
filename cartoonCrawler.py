# write by Sirawat Isaradej

import urllib2
import sys
import time
import re
import os
import requests
from bs4 import BeautifulSoup
import mysql.connector
import datetime
import pytz

mydb = mysql.connector.connect(
  host="localhost",
  user="mrbryside",
  passwd="b14121214",
  database="cartoonAPI"
)

cartoonID = 0
mycursor = mydb.cursor()
now = datetime.datetime.now(pytz.timezone('Asia/Bangkok'))

print("---------- Cartoon Crawler Start !!  ----------")
if not os.path.exists('/var/www/everygrams.ddns.net/cartoonAPI/public/onepiece'):
    os.system('sudo mkdir /var/www/everygrams.ddns.net/cartoonAPI/public/onepiece')   
# if not os.path.exists('/home/vagrant/sites/cartoonAPI/public/onepiece'):
#     os.system('sudo mkdir /home/vagrant/sites/cartoonAPI/public/onepiece') 
mycursor.execute("SELECT * FROM cartoons") 
myresult = mycursor.fetchall()
found = 0
foundID = 0
for x in myresult:
    if x[1] == "Onepiece":      
        found = 1
        foundID = x[0]

if found == 0 :
    sql = "INSERT INTO cartoons (cartoonName,created_at,updated_at) VALUES (%s,%s,%s)"
    val = ("Onepiece",now,now,)
    mycursor.execute(sql, val)
    
    mydb.commit()

    print(mycursor.rowcount, "update to databse success!")
    cartoonID = mycursor.lastrowid
elif found == 1:
    cartoonID = foundID
    
round = 1
while round <= 3 :
    
    if round == 1:
        req = requests.get('http://www.oremanga.com/77-1-One+Piece.html')
    elif round == 2:
        req = requests.get('http://www.oremanga.com/77-2-One+Piece.html')
    elif round == 3:
        req = requests.get('http://www.oremanga.com/77-3-One+Piece.html')


    html = req.content
    soup = BeautifulSoup(html, 'html.parser')
    cartoon_part = []
    count = 1
    print('read all part of onepiece...\n')
    for tag in soup.find_all('a',href=re.compile("^One.*")):
        cartoon_part.append('http://www.oremanga.com/'+tag['href'])
        print('save part :'+str(count))
        count+=1
    print('go to part and save image url...\n')
    count_2 = 1
    for part in cartoon_part:
        print('part :'+str(count_2))
        req = requests.get(part)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find("ul", {"id": "alphabet_detail"})
        count_image = 1
        part_name = re.search('\+\d+\-',part)
        part_name = re.sub("\D", "", part_name.group(0))
        
        if not os.path.exists('/var/www/everygrams.ddns.net/cartoonAPI/public/onepiece/'+part_name):
            os.system('sudo mkdir /var/www/everygrams.ddns.net/cartoonAPI/public/onepiece/'+part_name)  
        # if not os.path.exists('/home/vagrant/sites/cartoonAPI/public/onepiece/'+part_name):
        #     os.system('sudo mkdir /home/vagrant/sites/cartoonAPI/public/onepiece/'+part_name) 
        else:
            print('downloaded all break!')
            if part == cartoon_part[len(cartoon_part)]
                break
            else
                continue
        for tag in soup.find_all('img'):
            print('save image :'+str(count_image))
            f = open('/var/www/everygrams.ddns.net/cartoonAPI/public/onepiece/'+part_name+'/'+str(count_image), 'wb')
            # f = open('/home/vagrant/sites/cartoonAPI/public/onepiece/'+part_name+'/'+str(count_image), 'wb')
            f.write(urllib2.urlopen(tag['src']).read())
            f.close()

            count_image +=1
        print('part '+str(count_2)+' finished !')
        sql = "INSERT INTO cartoonlists (chapterID,cartoonPage,cartoonID,created_at,updated_at) VALUES (%s,%s,%s,%s,%s)"
        val = (part_name,count_image,cartoonID,now,now,)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "update to database success!!")
        count_2 +=1
    round+=1

print("---------- Finished !!  ----------")
sys.exit(0)

