from bs4 import BeautifulSoup
import requests
from settings import *
import json


def main():
    requests.get("https://accounts.google.com/o/oauth2/auth?%s%s%s%s" %
                 ("client_id=%s&" % (CLIENT_ID),
                  "redirect_uri=http://localhost/&",
                  "scope=https://www.googleapis.com/auth/fusiontables&",
                  "response_type=code"))
    print(post_data())


def post_data():
    r = requests.post('https://www.googleapis.com/fusiontables/v2/tables/1UjAsnTg3R4-eJoRjEk3XLHrxQvCR09s6XKoOhswQ/columns?key=AIzaSyASH1rUfGB_L9VHQlbrvEXEeShnH5q7G10',
                      data=json.dumps({'name': 'Test', 'type': 'STRING'}))
    return r

if __name__ == '__main__':
    main()
