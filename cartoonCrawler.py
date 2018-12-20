# write by Sirawat Isaradej

import urllib2
import sys
import time
import re
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui

print("---------- Cartoon Crawler Start !!  ----------")
display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()
round = 1
while round <= 3 :
    
    if round == 1:
        driver.get('http://www.oremanga.com/77-1-One+Piece.html')
    elif round == 2:
        driver.get('http://www.oremanga.com/77-2-One+Piece.html')
    elif round == 3:
        driver.get('http://www.oremanga.com/77-3-One+Piece.html')


    html = driver.page_source
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
        driver.get(part)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find("ul", {"id": "alphabet_detail"})
        count_image = 1
        part_name = re.search('\+\d+\-',part)
        part_name = re.sub("\D", "", part_name.group(0))
        
        if not os.path.exists(part_name):
            os.system('sudo mkdir /var/www/'+part_name)   
        else:
            print('downloaded all break!')
            break
        for tag in soup.find_all('img'):
            print('save image :'+str(count_image))
            f = open('/var/www/'+part_name+'/'+str(count_image), 'wb')
            f.write(urllib2.urlopen(tag['src']).read())
            f.close()

            count_image +=1
        print('part '+str(count_2)+' finished !')
        count_2 +=1
    round+=1

print('kill google chrome...')
os.system("sudo pkill chrome")
driver.quit()
print('killed!!')
print("---------- Finished !!  ----------")
sys.exit(0)

