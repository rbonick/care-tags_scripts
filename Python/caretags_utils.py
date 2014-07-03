import re

__author__ = 'Ryan'

from bs4 import BeautifulSoup
import grequests
import requests


class CaretagsUtils():
    LOGIN_URL = "http://care-tags.org/ucp.php?mode=login"

    def __init__(self):

        self.session = requests.Session()

    def login(self, username, password):
        """
        Logs a user into care-tags.org

        Should be run before any content-retrieval methods are attempted
        :param username: the username to use
        :param password: the password to use
        :return: Whether the login succeeded
        """
        # Create the login data and the request
        payload = {"username": username, "password": password, "autologin": "on", "login": "login"}
        response = self.session.post(self.LOGIN_URL, data=payload)
        if response.status_code != 200:
            response.raise_for_status()
        soup = BeautifulSoup(response.text)
        if soup.find(text=re.compile("Logout")):
            print username + " logged in successfully!"
            return True
        else:
            # TODO: better failure response (was it really a bad login?)
            print "Login failed. Perhaps check your login information is correct?"
            return False

if __name__ == "__main__":
    utils = CaretagsUtils()
    utils.login("pythonbot", "autonomous")