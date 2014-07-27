import re

__author__ = 'Ryan'

from bs4 import BeautifulSoup
import grequests
import requests
import urlparse


class CaretagsUtils():
    LOGIN_URL = "http://care-tags.org/ucp.php?mode=login"
    THREADS_PER_PAGE = 25

    def __init__(self):
        self.is_logged_in = False

        # session will hold the cookies
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

    def get_all_forums(self):
        """
        Gets all forums

        :return: A list containing the urls of each forum
        """
        # Currently static.
        # TODO: Would be nice to make dynamic
        forumnums = [2, 3, 6]
        forumurls = []

        for num in forumnums:
            forumurls.append("http://care-tags.org/viewforum.php?f=" + str(num))

        return forumurls

    def get_all_threads(self, forum_url):
        """
        Gets all threads for a given forum

        :param forum_url: The url to get all threads from
        :return: A list of thread urls
        """
        page_urls = []
        thread_urls = []

        # Get number of pages
        soup = self.get_soup(forum_url)
        pagination = soup.find(class_="pagination")
        num_posts = int(pagination.text.split()[4])

        # Get all the pages
        for page_start in range(0, num_posts, self.THREADS_PER_PAGE):
            page_urls.append(forum_url + "&start=" + str(page_start))
        requests = (grequests.get(u) for u in page_urls)
        responses = grequests.map(requests, size=50)

        # Error check
        for response in responses:
            response.raise_for_status()
            assert(response.url in page_urls)
        assert(len(responses) == len(page_urls))

        # See if there are announcement threads and grab them.
        if len(soup.select("div.forumbg ul.topiclist.topics")) > 1:
            announcement_list =  soup.select("div.forumbg ul.topiclist.topics")[0]
            # For each topic (thread) get the url
            for li in announcement_list.find_all("li"):
                # Need to isolate the topic ID
                topic_url = li.find(class_="topictitle").get('href')
                parsed_topic_url = urlparse.urlparse(topic_url)
                topic_id = urlparse.parse_qs(parsed_topic_url.query)['t']

                # Create the url corresponding with that topic ID
                thread_url = str(forum_url + "&t=" + topic_id[0]).replace("forum", "topic")
                thread_urls.append(thread_url)

        for response in responses:
            # Make soup of the page
            soup = BeautifulSoup(response.text)

            # The main topic list will always be last one
            topic_list = soup.select("div.forumbg ul.topiclist.topics")[-1]

            # For each topic (thread) get the url
            # TODO: return topic title as well?
            for li in topic_list.find_all("li"):
                # Need to isolate the topic ID
                topic_url = li.find(class_="topictitle").get('href')
                parsed_topic_url = urlparse.urlparse(topic_url)
                topic_id = urlparse.parse_qs(parsed_topic_url.query)['t']
                thread_url = str(forum_url + "&t=" + topic_id[0]).replace("forum", "topic")
                thread_urls.append(thread_url)

        # Check that all thread urls were found
        try:
            assert(len(thread_urls) == num_posts)
        except AssertionError:
            print num_posts, len(thread_urls)

        # Return it
        return thread_urls

    def load_username_and_password(self):
        """
        Loads username and password from a file and returns it
        """
        with open('login','r') as f:
            username = f.readline().strip("\n")
            password = f.readline().strip("\n")
        return username, password

    def login_from_file(self):
        """
        Loads username and password from file, then logs in with it
        """
        username, password = self.load_username_and_password()
        self.login(username, password)

if __name__ == "__main__":
    utils = CaretagsUtils()
    username, password = utils.load_username_and_password()
    utils.login(username, password)
    forums = utils.get_all_forums()
    for forum in forums:
        utils.get_all_threads(forum)