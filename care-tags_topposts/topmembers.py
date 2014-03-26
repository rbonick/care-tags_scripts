from bs4 import BeautifulSoup
import requests

class TopMembers:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #Start session
        self.session = requests.Session()

    def gettopposters(self):
        print "hi"

