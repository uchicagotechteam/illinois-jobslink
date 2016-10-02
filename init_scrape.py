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
    listings = soup.find_all("dt")
    # for l in listings:
    #     print(l)
    #     urls = l.find_all('a')
    #     for u in urls:
    #         job_url = u['href']
    #         print(BASE_URL + job_url)

if __name__ == '__main__':
    session = requests.Session()
    soup = BeautifulSoup(session.get(SEARCH_URL).content, "html.parser")
    inputs = soup.find_all('input')
    token = ''
    for t in inputs:
        try:
            if t['name'] == 'authenticity_token':
                token = t['value']
                break
        except KeyError as e:
            pass
    # print(soup.prettify().encode('utf-8'))
    print(token)

    login_data = dict(v_username=USER_NAME,
                      v_password=PASSWORD,
                      authenticity_token=token,
                      commit='Log In')
    login_data['utf-8'] = '&#x2713;'

    r = session.post(LOGIN_URL, data=login_data)

    print(r.content)

    # r = session.get(
    #     'https://illinoisjoblink.illinois.gov/ada/mn_loginstatistics_dsp.cfm')

    # soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify().encode('utf-8'))

    # browser = RoboBrowser(history=True)
    # browser.open(SEARCH_URL)
    # forms = browser.get_forms()
    # print(forms)
    # login_form = forms[1]  # Hardcoded LOL
    # login_form['v_username'] = USER_NAME
    # login_form['v_password'] = PASSWORD
    # browser.submit_form(login_form)

    # print(browser.parsed)
    # scrape()
