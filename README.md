# DHS Project
Build Illinois Jobslink scraper, API, and front end for Illinois DHS. 


## Overview
+ Scrape the relevant information from [https://illinoisjoblink.illinois.gov/ada/r/search/jobs](https://illinoisjoblink.illinois.gov/ada/r/search/jobs). We will be using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Requests](http://docs.python-requests.org/en/master/).
  * Scrape `How To Apply`, `Education Level`, `Salary/Wages`, `Location`
  *  Python dictionaries, conditional and loop structures, HTTP methods, JSON.
  * Iron out authentication and login problems on Illinois Jobslink site.

+ Store in Google Fusion Tables and sqlite database
  * SQL queries helpful
  * Will need to solve OAuth2 troubles

+ [Derek Eder's Searcheable Map Template](http://derekeder.github.io/FusionTable-Map-Template/) will be used as the front end. 
  * Used before in Network9 Project for CPS
  * Bootstrap, JS stuff. 

+ Update Script that runs periodically (daily or weekly) and updates Google Fusion Tables and sqlite database. 
  * Will live on Heroku

## Teamwork

We will be using Git and GitHub for this project. To get started, fork the repository to your own account. Once forked, go to your repository and clone it to your local machine.
```
git clone /FORKED/REPO/URL
```

Make sure you make a new branch when you are implementing a new feature. Be sure to be working in the right branch when coding.

```
git checkout -b NEW_BRANCH_NAME
OR
git checkout EXISTING_BRANCH
```

Once you code, make sure you add your files and commit them. Push them to your forked repository when ready.

```
git add FILENAMES (or use -a {be careful!})
git commit -m "Insert commit message."
git push
```
Once you're done with your branch, be sure to send a pull request so I can merge your code with the existing project.

## Set Up
We will be using `pip` and `virtualenv` in this project. Make sure you have `pip` installed. If you downloaded Python via Anaconda, you are good to go. I'm not sure about other distributions.

To install `virtualenv`
```
pip install virtualenv
```

Once you've done this, `cd` into your project repo. Then run the following commands if you are on Windows.
```
virtualenv env
env/scripts/activate
pip install -r requirements.txt
```

If you're on MacOS, you'll run something like the following:
```
virtualenv env
env/bin/activate
pip install -r requirements.txt
```

This will create a virtual environment so that any development you do will not be affected by the global system variables. Also, you will download all of the packages from `requirements.txt`, so that the code will actually run. If you install any new packages for code you have written, make sure to put them into `requirements.txt`. 

## Branch: `init_scrape`
The `init_scrape` branch is the branch dedicated for the initial scrape. Our objectives/tasks for this branch are:

+ Login to `https://illinoisjoblink.illinois.gov/ada/r/search/jobs`
  
  So I made an account for this website as you can only get all of the information for each job posting by making an account. However, I have NOT yet figured out how to actually login with Python. There are some workarounds that we can try. This is kind of an advanced feature, and if you have a lot of experience, I'll be in touch.
   
+ Request `https://illinoisjoblink.illinois.gov/ada/r/search/jobs` (This is the FIRST page) and scrape it. 

  Like we did on `12 OCT 2016`, we are going to have to scrape the list of job postings on this page. If you inspect the page source and scroll down a TON to the job postings, you'll see HTML that looks like the following for ONE job posting:

  ```
  <dt>
    <a href="/ada/r/jobs/4324478">Insurance Sales Agent (4324478)</a>
    <div class="updated right">Last Updated: 2016-10-12</div>
    <!-- search score: 1.0 -->
  </dt>
  <dd>
    <div class="row">
        <div class="col_1">
            <b>Employer: </b>
            Combined Insurance
        </div>
        <div class="col_2">
            <b>Location: </b>
            <i>Belleville , IL</i>
        </div>
    </div>
    <div class="description"><p>Management Trainees needed for the Metro East Area. For those competitive individuals with a desire to achieve, come join a winning team. Offering insurance products including Disability, Accident &amp; Sickness, Whole Life, &amp; Medicare Supplement, Combined Insurance, established in 1922, is expanding its Management Trainee program. Opportunities available in two…</p></div>
  </dd>
  ```

  Notice how for each job posting we have a `<dt>` and `<dd>` tag that is associated with the job. The `<dt>` tag points to the name of the job name as well as the url of the webpage of that job. The `<dd>` tag has descriptions and stuff.

+ Step through the url for each job posting and scrape the job page
  
  So we're going to have to get the urls, which are located in the `<a>` tag under the `<dt>` tag. If you look in `init_scrape.py` you'll see the following code (as of 12 OCT 2016, 8:30 PM):

  ```
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
            id_num = u.string[u.string.find('(') + 1:u.string.find(')')]
  ```

  So we've gotten the url for each job posting, and we need to step through the url and scrape that page. We can request the url as follows and set up a `BeautifulSoup` object for that page.

  ```
  r = requests.get("INSERT_JOB_URL_HERE")
  job_soup = BeautifulSoup(r.content, "html.parser")
  ```
  We're going to step through the url because that page has more information than just the homepage of the website. 

  We're going to scrape information like `description`, `location`, `wages`, etc.

+ Insert the scraped data into sqlite and Google Fusion Tables.

  I'll go over this in a session. We'll be going over SQL statements and sqlite. Don't worry about this right now. 

  Fusion Tables is going to be difficult, but we'll figure it out.


+ Step through the ALL the pages of the search results. 
  
  If you look at the bottom of `https://illinoisjoblink.illinois.gov/ada/r/search/jobs`, you'll see there are a LOT of result pages. We're going to have to step through each of these, scrape for all of the job urls, and THEN step through all of those job urls. 

  But, wait, how are we going to go to next page? Python doesn't have a mouse to click `Next Page`, so what are we to do??


  `https://illinoisjoblink.illinois.gov/ada/r/search/jobs?is_subsequent_search=false&page=2&refiners=%7B%7D&status=Active`

  This is the url for the second webpage. Notice the very subtle `page=2` in the url. So what we can do is iterate through by changing the number from `page=2` to `page=3` to get the third page. If we want the `ith` page, we would do `'page=' + str(i)`.




