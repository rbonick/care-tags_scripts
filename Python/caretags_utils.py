import re

__author__ = 'Ryan'

from bs4 import BeautifulSoup
import grequests
import requests


class CaretagsUtils():
    LOGIN_URL = "http://care-tags.org/ucp.php?mode=login"

    def __init__(self):
        self.is_logged_in = False
        self.session = requests.Session()

    def login(self, username, password):
        """
        Logs a user into care-tags.org

        Should be run before any content-retrieval methods are attempted
        :param username: the username to use
        :param password: the password to use
        :return: Whether the login succeeded
        """
        # Create the login data
        payload = {"username": username, "password": password, "autologin": "on", "login": "login"}

        # Send the login request
        response = self.session.post(self.LOGIN_URL, data=payload)

        # Raise an exception if an HTTP error occurred
        response.raise_for_status()

        # Look through the response data to see if the user was successfully logged in
        soup = BeautifulSoup(response.text)
        if soup.find(text=re.compile("Logout \[.*\]")):
            print username + " logged in successfully!"
            self.is_logged_in = True
            return True
        else:
            # TODO: better failure response (was it really a bad login?)
            print "Login failed. Perhaps check your login information is correct?"
            return False

    def get_soup(self, url):
        """
        Gets a BeautifulSoup object corresponding to the html of the url.

        :param url: The url to make Soup from
        :return: A BeautifulSoup object for the web page
        """
        # TODO: verify that the response text corresponds to html (as opposed to JSON or something)
        # Send a GET request for the url
        response = self.session.get(url)

        # If an error was returned, raise an exception
        response.raise_for_status()

        # Otherwise return the souped up (haha) version of the html
        return BeautifulSoup(response.text)


if __name__ == "__main__":
    utils = CaretagsUtils()
    utils.login("pythonbot", "autonomous")