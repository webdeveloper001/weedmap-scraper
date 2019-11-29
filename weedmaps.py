# -*- coding: utf-8 -*-
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')



csv.register_dialect('myDialect1',
	  quoting=csv.QUOTE_ALL,
	  skipinitialspace=True)





session = requests.Session()
session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


def get_storefront(lat, long, csv_writer):
    url = 'https://api-g.weedmaps.com/discovery/v1/listings?sort_by=position&filter%5Bany_retailer_services%5D%5B%5D=delivery&filter%5Blocation%5D=any&latlng={}%2C{}&page_size=100&page=1'

    r = session.get(url.format(latitude, longitude))
    print(url.format(latitude, longitude))
    data = json.loads(r.text)
    if 'data' in data:

        for one in data['data']['listings']:
            print(one['web_url'])
            business_name = one['name']
            state = one['state']
            city = one['city']
            r = session.get(one['web_url'] + '/about')
            soup = BeautifulSoup(r.text, features="html.parser")
            address = soup.find('p', class_='styled-components__AddressRow-sc-1k0lbjf-2')
            if address:
                address = address.text
            else:
                address = ''
            phone = soup.find('div', class_='styled-components__PhoneNumber-d53rlt-8')
            if phone:
                phone = phone.text
            else:
                phone = ''

            email = soup.find('div', class_='styled-components__Email-d53rlt-3')
            if email:
                email = email.text
            else:
                email = ''

            website = soup.find('div', class_='styled-components__Website-d53rlt-4')
            if website:
                website = website.text
            else:
                website = ''
            
            
            print(business_name,phone, email, website,  city, state, address)
            csv_writer.writerow([ business_name,phone, email, website,  city, state, address ])
            # if 'data' in json.loads(r.text):
            #     detail = json.loads(r.text)['data']['listing']
            # else:
            #     continue
            # if len(detail['licenses']) == 0:
            #     license_status = ''
            # else:
            #     license_status = detail['licenses'][0]['type']
            # csv_writer.writerow([detail['name'], detail['phone_number'], detail['email'], detail['website'], detail['state'], detail['city'], license_status, detail['license_type']])

            # print(detail['name'], detail['phone_number'], detail['email'], detail['website'], detail['state'], detail['city'], license_status, detail['license_type'])



url = 'https://weedmaps.com/dispensaries/in/united-states'
r = session.get(url)
soup = BeautifulSoup(r.text, features="html.parser")
states = soup.findAll('a', class_='region-subregions-tray__RegionLink-jf99ya-3')
flag = False
for state in states:

    if state.text != 'California':
        continue
    # if 'washington-dc' in state.attrs['href']:
    #     flag = True
    # if flag == False:
    #     continue

    url = 'https://weedmaps.com' + state.attrs['href']
    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    latitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[0]
    longitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[1]

    print(latitude, longitude)
    cities = soup.findAll('a', class_='region-subregions-tray__RegionLink-jf99ya-3')
    # if len(cities) == 0:
    #     latitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[0]
    #     longitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[1]
    #     get_storefront(latitude, longitude)

    for city in cities:
        
        # if city.text != 'Marin' and city.text != 'San Francisco' and city.text != 'San Jose' and city.text != 'Sacramento'  and city.text != 'Oakland':
        if city.text == 'Marin' or city.text == 'San Francisco' or city.text == 'San Jose' or city.text == 'Sacramento'  or city.text == 'Oakland':
            continue 

        write_file = open(state.text + '/' + city.text.replace('/', '_').strip() + '.csv', 'a')
        csv_writer = csv.writer(write_file, dialect='myDialect1')

        csv_writer.writerow(['Business name', 'Phone', 'Email', 'Website', 'State', 'City', 'Address'])

        print(city.attrs['href'])
        url = 'https://weedmaps.com' + city.attrs['href']
        r = session.get(url)
        latitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[0]
        longitude = r.text.split('"latitude":')[1].split(',"place_path"')[0].split(',"longitude":')[1]
        # print(url, latitude, longitude)
        get_storefront(latitude, longitude, csv_writer)



