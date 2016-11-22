import sys
import os
import os.path
import requests
import json
import sqlite3
import re

from bs4 import BeautifulSoup
# from selenium import webdriver

from settings import *


# session needs to be global to maintain same session
session = requests.Session()

# Init Database
if(os.path.exists(DB)):
    os.remove(DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE listings
                (name text, id text, url text, company text, education text, average_hours text,
                 wage_type text, min_wages text, max_wages text, physical_address text,
                 contact_address text, company_description text, benefits text,
                 bool_internship_externship text, bool_permanent text, bool_overtime_available
                 text, bool_overtime_required text, bool_job_training text, bool_travel text,
                 bool_driving text)''')

def scrape():
    # Goes through all 40 pages of job listings, scrapes job url, name, and id
    # number
    # There are 40 pages of results, with 250 listings per page. There should
    # be more, but it's capped here.
    for n in range(1, 2): # When testing: use range(1, 2)
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

                # Step through to the job page.
                job_page = session.get(BASE_URL + job_url)
                # Make a new soup object to search the job page
                job_page_soup = BeautifulSoup(job_page.content, "html.parser")
                # Only get info from the job information section
                full_job_info = job_page_soup.find("div", class_='reviewform')
                # Three different div classes where job information is stored:
                job_info_1 = full_job_info.find_all("div", class_=re.compile(r'row attr-job*'))
                job_info_2 = full_job_info.find_all("div", class_='row ')
                job_info_3 = full_job_info.find_all("div", class_='row comparison')

                # The following is hard-coded to keep track of how many parameters are in each job_info_#
                job_attr = {}
                for job_detail in job_info_1:
                    # ex. say you have <div class='row attr-job-average_hours'>40</div> (not actually as clean as this)
                    # we can extract the substring that follows row attr-job- to get 'average_hours'
                    # the following code will add to the dictionary the following: {u'average_hours': u'40'}
                    # further down in c.execute(...) we'll add this data to the database file
                    job_attr[job_detail['class'][1][9:]] = job_detail.contents[1].contents[0]
                    print(job_detail['class'][1][9:])
                for job_detail in job_info_2:
                    # Has 1 OR 2 children
                    # If there's only 1 child, we should get the prev_sibling of the child as the description (?)
                    continue
                for job_detail in job_info_3:
                    # Has 4 children
                    continue

                print(job_attr)

                # there's also the "apply for this job" button (just a link), should we save it?

                # Need to scrape for description, zipcode, wages, education, etc and
                # put them into the DB. ---> Use above code as a model as well as what
                # we did in the scraping workshop.

                # Insert the job listing into the database (only the name and url
                # have been implemented at this point)
                # We want to scrape the following (and maybe more): job, id, url, apply, address, wages, salary, jobdescription, hours, contact, company, companydescription, experience, education, overtime, training, shift, insurance, childcare, 401k
                # Here we add 'average hours' to the database
                c.execute(
                    "INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (job_attr['title'], job_attr['display_id'], job_url, job_attr['company_name'],
                     job_attr['required_education_level_id'], job_attr['average_hours'],
                     job_attr['wage_type'], job_attr['wage_lower_bound'],
                     job_attr['wage_upper_bound'], job_attr['physical_address'],
                     job_attr['contact_address'], job_attr['company_work_description'],
                     job_attr['miscellaneous_benefits'], job_attr['internship_externship'],
                     job_attr['position_type'], job_attr['is_overtime_available'],
                     job_attr['is_overtime_required'], job_attr['on_the_job_training'],
                     job_attr['travel'], job_attr['driving_required']))
                # need to check miscellaneous_benefits
                # is_day_shift
                # is_evening_shift
                # is_night_shift
                # is_rotating_shift
                # is_split_shift
                # is_no_preference_shift
                # other_shift_schedules
            break # When testing, break here
        print(n)
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
    c.close()
