import sys
import os
import os.path
import requests
import json
import sqlite3

from bs4 import BeautifulSoup

from settings import *


import csv
# session needs to be global to maintain same session
session = requests.Session()

# Init Database
if(os.path.exists(DB)):
    os.remove(DB)
conn = sqlite3.connect(DB)
conn.text_factory = str
c = conn.cursor()
# c.execute('''CREATE TABLE listings
#                 (name text, id text, url text, apply text, zipcode text, wages text, description text, education text)''')
c.execute('''CREATE TABLE listings
                (name text, url text, location text, exp text, edu text, employment text, temp text, hours text, company text)''')


def scrape():
    # Goes through all 40 pages of job listings, scrapes job url, name, and id
    # number
    # There are 40 pages of results, with 250 listings per page. There should
    # be more, but it's capped here.
    for n in range(1, 3):  # should be 41
        # Changes the page= number
        page = PAGE_URL[:87] + str(n) + PAGE_URL[88:]
        r = session.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        listings = soup.find_all("dt")  # Finds all dt tags
        for l in listings:
            # Finds the a tag, which will have the name and the url
            urls = l.find_all('a')
            for u in urls:
                # The href part of the tag will have the url
                job_url = u['href']
                name = u.string    # The name will be in the string part of the a tag
                id_num = u.string[u.string.find('(') + 1:u.string.find(')')]

                # Step through to the job page.
                job_page = session.get(BASE_URL + job_url)

                job_soup = BeautifulSoup(job_page.content, "html.parser")

                # experience
                tags = job_soup.find_all(
                    'div', 'row attr-job-months_of_experience')
                exp = ""
                for t in tags:
                    children = t.contents
                    exp = children[1].contents[0]

                # education
                tags = job_soup.find_all(
                    'div', 'row attr-job-required_education_level_id')
                edu = ""
                for t in tags:
                    children = t.contents
                    edu = children[1].contents[0]

                # employment type
                tags = job_soup.find_all('div', 'row attr-job-employment_type')
                job_type = ""
                for t in tags:
                    children = t.contents
                    job_type = children[1].contents[0]

                # perm/temp
                tags = job_soup.find_all('div', 'row attr-job-position_type')
                pos_type = ""
                for t in tags:
                    children = t.contents
                    pos_type = children[1].contents[0]

                # hours
                tags = job_soup.find_all('div', 'row attr-job-average_hours')
                hours = ""
                for t in tags:
                    children = t.contents
                    hours = children[1].contents[0]

                # company
                tags = job_soup.find_all(
                    'div', 'row attr-job-company_name')
                comp = ""
                for t in tags:
                    children = t.contents
                    comp = children[1].contents[0]

                # # creds
                # tags = job_soup.find_all(
                #     'div', 'row attr-job-credential_description')
                # creds = ""
                # for t in tags:
                #     children = t.contents
                #     parts = children[1].contents
                #     print len(parts)

                # physical address
                tags = job_soup.find_all(
                    'div', class_='row attr-job-physical_address')
                for t in tags:
                    children = t.contents
                    address_parts = children[1]
                    parts = address_parts.contents
                    # import pdb
                    # pdb.set_trace()
                    parts = filter(
                        lambda s: 'br>' not in str(s) and '<br' not in str(s), parts)
                    location = ""
                    # print parts
                    for part in parts:
                        location += str(part) + ", "

                # print location
                # Need to scrape for description, zipcode, wages, education, etc and
                # put them into the DB. ---> Use above code as a model as well as what
                # we did in the scraping workshop.

                # Insert the job listing into the database (only the name and url
                # have been implemented at this point)
                # c.execute(
                #     "INSERT INTO listings VALUES (?, ?, ?, 'TODO', 'TODO', 'TODO', 'TODO', 'TODO');", (name, id_num, job_url))
                c.execute(
                    "INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?);", (name, BASE_URL + job_url, "\"" + location.encode('utf-8') + "\"", exp, edu, job_type, pos_type, hours, comp))
    conn.commit()


def login():
    # get html data for login page
    soup = BeautifulSoup(session.get(LOGIN_URL).content, "html.parser")
    # pulls login url from page, could change per session
    login = soup.find_all('form')[0]['action']

    login_data = dict(v_username=USER_NAME,
                      v_password=PASSWORD,
                      FormName='Form0',
                      fromlogin=1,
                      button='Log in')

    # logs in
    r = session.post(BASE_URL + login, data=login_data)


if __name__ == '__main__':
    login()
    scrape()

    # csvWriter = csv.writer(open("listings.csv", "w"))  # , delimiter='\t')

    # for row in c.execute('SELECT * FROM listings'):
    #     csvWriter.writerow([s.decode('utf-8', 'ignore') for s in row])

    c.close()
