# Illinois JobsLink Project
Build Illinois Jobslink scraper, API, and front end. 


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

You will also need to make sure you set your upstream repository correctly. To do that do the following:

```
git remote add upstream https://github.com/uchicagotechteam/illinois-jobslink.git
```

Then you will need to create and pull the branches themselves, as follows:

```
git checkout -b init_scrape
git checkout init_scrape
git pull upstream init_scrape

git checkout -b api
git checkout api
git pull upstream api
```

You'll be ready to code now! Make sure you are in the right branch by using `git checkout <BRANCH_NAME>`. 

Once you code, make sure you add your files and commit them. Push them to your forked repository when ready.

```
git add FILENAMES (or use -a {be careful!})
git commit -m "Insert commit message."
git push origin <BRANCH_NAME>
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

## Team: `Scrape`
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

## Team: `Backend`

+ Write to Google Fusion Tables (OAuth)
  
  To use the searcheable map template developed by Derek Eder, we need to store all of our data on Google Fusion Tables. So we will need to write our data from our SQL database to a Google Fusion Table. We can do this through the Google API found: [https://developers.google.com/fusiontables/docs/v1/using](https://developers.google.com/fusiontables/docs/v1/using). 

  I've done some preliminary digging around and coding, and I think I'm on to something. Checkout the `oauth.py` file under the `oauth` branch. Furthermore, checkout the following links:

  [Handling OAauth 2.0 Authentication](https://developers.google.com/identity/protocols/OAuth2WebServer)
  [Fusion Tables API](https://developers.google.com/fusiontables/)
  [More Fusion Tables API](https://developers.google.com/resources/api-libraries/documentation/fusiontables/v1/python/latest/index.html)
  [SQL and Fusion Tables](https://developers.google.com/fusiontables/docs/v2/sql-reference)

  There is some setup that is needed to start testing locally. FOLLOW THE STEPS IN [Handling OAauth 2.0 Authentication](https://developers.google.com/identity/protocols/OAuth2WebServer). You will need to setup credentials and other stuff at the [Google API Developer Console](https://console.developers.google.com/). Once you follow the steps, you need to make sure that in the following code found in `oauth.py`

  ```

@app.route('/callback')
def callback():
    flow = client.flow_from_clientsecrets(
        'client_secret_911503641744-hn8pinmojgfi1n4poh2n8ssk48bu8idn.apps.googleusercontent.com.json',
        scope='https://www.googleapis.com/auth/fusiontables',
        redirect_uri='http://localhost:5000/callback')

    flow.params['access_type'] = 'offline'

    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('index'))
  ```

  that you insert your own `client_secrets.json` file. MAKE SURE YOU DON'T PUSH THE JSON FILE TO GITHUB. THAT'S REALLY BAD! 

  Also, make sure you make your own personal Fusion Table and in the following spot: 

  ```
  ft_service = build('fusiontables', 'v2', http_auth)
    ft_service.query().sql(
        sql="INSERT INTO 1WOu6DaHenRNNXIWHkNWjGf66sUCnfl5fLQHhHOwt (col0) VALUES ('TODO');").execute()
    tables = ft_service.table().list().execute()
    return json.dumps(tables)
  ```

  you put in the `table_id` for your Fusion Table. Now make sure you have a column called `col0`, and this SQL statement will put a `TODO` value in that column!

  This is the basis for how writing to Fusion Table will be. Instead of `TODO`, we will query our database and write whatever we get back into the Fusion Table. 

  There are a few things we still need to figure out though. 
  + We will need to update old entries with either new information or deleting really old listings.
  + How do we set up the Flask framework so that we can automate the write on a daily or weekly basis? 
  + How do we get prolonged access to the user's data? There is something called a `refresh` token, but I haven't figured it out yet. 

+ Endpoints
  
  Our data is stored in a `sqlite` database, which will be served via an API built on Flask. If we look in the `api` branch, there is `api.py` file that has all of the Flask code (well really basic stuff) in it. We can instantiate it as follows. (Make sure you have all of the correct packages installed i.e. `pip install requsts`, `pip install flask`, and other packages).
  ```
  (env) PS D:\Projects\TechTeam\illinois-jobslink> python api.py
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 115-448-509
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

  This indicates that our server is running. We can then go to our favorite browser and type into the browser bar `http://127.0.0.1:5000/`. 

  You should get an error at this point, because in `api.py` we haven't written what should be done when the `/` endpoint is called. BUT we do have `/jobs` endpoint defined. So we can type in `http://127.0.0.1:5000/jobs` and we should see something pop up! It should look something like this 

  ```
  {
    "jobs": ""
  }
  ```

  So far this is empty since we haven't actually returned any of the job listings, but it should eventually come back with a list of all the jobs that fit our parameters.

  Jobs can be filtered via the url and a query string. If we type in 
  ```
  http://127.0.0.1:5000/jobs?name=ferret
  ```
  we can filter all of the jobs with the name `ferret`. This won't actually work since we haven't written the code to actually do it. We can chain together parameters with the `&` character as follows

  ```
  http://127.0.0.1:5000/jobs?name=ferret&id=007
  ```

  So we will be using this paradigm. A user can filter what jobs they want by using this query string, and its our job to only grab the jobs in the database that fit the parameters. Some more info about [query strings](https://en.wikipedia.org/wiki/Query_string).

  We will be servicing the requests through SQL statements, and you can find model code in `api.py` that does this. 

  Another thing to think about is whether we want to add more endpoints or functionality so that users can ask for data in different and more complex ways. 

+ Update
  
  We are going to have to solve how to update our database with new jobs and removing old jobs. We will be doing this with SQL statements again and probably periodically (daily or weekly?). [SQL](http://www.w3schools.com/sql/) commands and syntax.

## Team: Frontend

+ Searchable Map Template
  
  We will be using [Derek Eder's Searcheable Map Template](http://derekeder.github.io/FusionTable-Map-Template/) for our mapping purposes. He has GREAT documentation so check his page out. 

  We really have free range on how we want to design the map, so you guys have a lot of creative freedom.

+ Analytics
  
  I think it might be cool to do some of our own analytics on this data. We can use R as well as Python with `matplotlib` and `pandas`.

  You should start to think about what trends, relationships we want to look at and how we can describe these graphically.

+ D3

  [D3](https://d3js.org/) is a REALLY cool visualization library written in JavaScript. I don't have much experience at all but I think we can make some cool looking graphics. This team will work with the Analytics team closely.