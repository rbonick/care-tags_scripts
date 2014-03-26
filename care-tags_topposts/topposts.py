from bs4 import BeautifulSoup
import requests


class TopPosts:
    def __init__(self, username, password):
        #Store username and password
        self.username = username
        self.password = password

        # Start session
        self.session = requests.Session()

        # Login
        website = "http://care-tags.org/ucp.php?mode=login"

        # Use given credentials
        sess = self.session
        payload = {"username": username, "password": password,
                   "autologin": "on", "login": "login"}
        sess.post(website, data=payload)

    # Returns urls for all forums
    def getforums(self):
        # Currently static.  Would be nice to make dynamic
        forumnums = [2, 3, 6]
        forumurls = []

        for num in forumnums:
            forumurls.append("http://care-tags.org/viewforum.php?f=" + str(num))

        return forumurls

    # Returns urls for all threads within a given forum
    def getthreads(self, forumurl):
        soup = self.__getbs(forumurl)
        pagination = soup.find(class_="pagination")
        numposts = pagination.text.split()[4]  # Gets the thread count

        # print soup.prettify()

    def __getbs(self, url):
        # Visit desired url
        response = self.session.get(url)

        # Pull page
        bs = BeautifulSoup(response.text)

        return bs

if __name__ == "__main__":
    # from optparse import OptionParser
    # import sys
    #
    # parser = OptionParser()
    #
    # usage = "Usage: %prog -u <USERNAME> -p <PASSWORD> -n <USERNUMBER TO DISPLAY>"
    # parser = OptionParser(usage)
    #
    # parser.add_option(
    #     "-u",
    #     "--username",
    #     dest="user",
    #     help="Needs a username to login with",
    #     default=None)
    #
    # parser.add_option(
    #     "-p",
    #     "--password",
    #     dest="pw",
    #     help="Need the password to login user",
    #     default=None)
    #
    # parser.add_option(
    #         "-n",
    #         "--number",
    #         dest="usernum",
    #         help="The user number to look up",
    #         type="int",
    #         default=2)
    #
    # if not len(sys.argv) == 7:
    #     parser.print_help()
    #     sys.exit()
    #
    # (options, args) = parser.parse_args()

    hakuna = TopPosts("pythonbot", "autonomous")

    forums = hakuna.getforums()
    hakuna.getthreads(forums[1])
