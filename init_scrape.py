from bs4 import BeautifulSoup
import requests
from settings import *
import json
import sqlite3
import sys
import os
from robobrowser import RoboBrowser

# Init Database
os.remove(DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE listings
                (name text, url text, apply text, zipcode text, wages text, description text, education text)''')


def scrape():
    url = SEARCH_URL
    r = session.get(SEARCH_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup.prettify().encode('utf-8'))

    # Print the urls for each job listing.
    # Will need to implement stepping through these urls and scraping the
    # relevant data.
    listings = soup.find_all("dt")  # Finds all dt tags (elements in the list)
    for l in listings:
        # Finds the a tag, which will have the name and the url
        urls = l.find_all('a')
        for u in urls:
            job_url = u['href']  # The href part of the tag will have the url
            name = u.string  # The name will be in the string part of the a tag

            # Insert the job listing into the database (only the name and url
            # have been implemented at this point)
            c.execute(
                "INSERT INTO listings VALUES (?, ?, 'TODO', 'TODO', 'TODO', 'TODO', 'TODO');", (name, job_url))

    conn.commit()

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

    # Print our entries in the database
    for row in c.execute('SELECT * FROM listings'):
        print row

    c.close()
