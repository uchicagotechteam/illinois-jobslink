import sys
import os
import os.path
import requests
import json
import sqlite3

from bs4 import BeautifulSoup
from selenium import webdriver

from settings import *


# Init Database
if(os.path.exists(DB)):
    os.remove(DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE listings
                (name text, id text, url text, apply text, zipcode text, wages text, description text, education text)''')


def setupAndLogin(URL):
    # Will need to install Chrome Webdriver via homebrew
    browser = webdriver.Chrome()
    browser.get('https://illinoisjoblink.illinois.gov/ada/skillmatch/skl_login.cfm')
    username_field = browser.find_element_by_name("v_username")
    password_field = browser.find_element_by_name("v_password")
    login_button = browser.find_element_by_name("button") # Not great but only button on page
    #print username_field, password_field, login_button
    username_field.send_keys(USER_NAME)
    password_field.send_keys(PASSWORD)
    login_button.click()
    browser.find_element_by_name('continue').click()
    # browser.find_element_by_xpath("//input[@name='question' and @value='1']").click()
    # browser.find_element_by_name('Continue5').click()
    return browser

def scrape():
    url1 = 'https://illinoisjoblink.illinois.gov/ada/r/search/jobs?is_subsequent_search=false&page=1&per_page=250&refiners=%7B%7D&status=Active&utf8=%E2%9C%93'
    url_base = 'https://illinoisjoblink.illinois.gov'
    browser = setupAndLogin(LOGIN_URL)
    # Goes through all 40 pages of job listings, scrapes job url, name, and id
    # number
    # There are 40 pages of results, with 250 listings per page. There should
    # be more, but it's capped here.
    for n in range(1, 41):
        page = url1[:87] + str(n) + url1[88:]   # Changes the page= number
        browser.get(page)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # So user can see what's going on for testing
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        listings = soup.find_all("dt")  # Finds all dt tags
        for l in listings:
            # Finds the a tag, which will have the name and the url
            urls = l.find_all('a')
            for u in urls:
                # The href part of the tag will have the url
                job_url = u['href']
                name = u.string     # The name will be in the string part of the a tag
                id_num = u.string[u.string.find('(') + 1:u.string.find(')')]

                browser.get(url_base + job_url)


                # Insert the job listing into the database (only the name and url
                # have been implemented at this point)
                c.execute(
                    "INSERT INTO listings VALUES (?, ?, ?, 'TODO', 'TODO', 'TODO', 'TODO', 'TODO');", (name, id_num, job_url))
            # Need to scrape for description, zipcode, wages, education, etc and
            # put them into the DB. ---> Use above code as a model as well as what
            # we did in the scraping workshop.
    conn.commit()

if __name__ == '__main__':
    session = requests.Session()

    # Code for Illinois Jobs Link Login - TODO: Fix login issues. (Try utf-8
    # encoding??)

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

    # scrape()

    # Print our entries in the database
    for row in c.execute('SELECT * FROM listings'):
        print row

    c.close()
