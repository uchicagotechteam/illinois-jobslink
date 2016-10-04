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

Once you've done this, `cd` into your project repo. Then run the following commands:
```
virtualenv env
env/scripts/activate
pip install -r requirements.txt
```

This will create a virtual environment so that any development you do will not be affected by the global system variables. Also, you will download all of the packages from `requirements.txt`, so that the code will actually run. If you install any new packages for code you have written, make sure to put them into `requirements.txt`. 
