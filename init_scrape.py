from bs4 import BeautifulSoup
import requests
from settings import *
import json
import sqlite3
import sys
from robobrowser import RoboBrowser

# Init database
conn = sqlite3.connect('listings.db')
c = conn.cursor()


def initialize():
    c.execute('''CREATE TABLE listings
                    (apply text, zipcode text, wages text, description text, education text)''')


def scrape():
    url = SEARCH_URL
    r = session.get(SEARCH_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    print(soup.prettify().encode('utf-8'))

    # Print the urls for each job listing.
    # Will need to implement stepping through these urls and scraping the
    # relevant data.
    listings = soup.find_all("dt")
    for l in listings:
        print(l)
        urls = l.find_all('a')
        for u in urls:
            job_url = u['href']
            print(BASE_URL + job_url)

if __name__ == '__main__':
    session = requests.Session()

    # Code for Illinois Jobs Link Login - TODO: Fix login issues. (Try utf-8
    # encoding??)

    # soup = BeautifulSoup(session.get(SEARCH_URL).content, "html.parser")
    # inputs = soup.find_all('input')
    # token = ''
    # for t in inputs:
    #     try:
    #         if t['name'] == 'authenticity_token':
    #             token = t['value']
    #             break
    #     except KeyError as e:
    #         pass
    # # print(soup.prettify().encode('utf-8'))
    # print(token)

    # login_data = dict(v_username=USER_NAME,
    #                   v_password=PASSWORD,
    #                   authenticity_token=token,
    #                   FormName=0,
    #                   fromlogin=1,
    #                   button='Log+in')
    # login_data['utf-8'] = '&#x2713;'

    # r = session.post(LOGIN_URL, data=login_data)

    # print(r.content)

    scrape()
