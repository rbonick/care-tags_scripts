from bs4 import BeautifulSoup
import requests
from operator import itemgetter

class TopMembers:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #Start session
        self.session = requests.Session()

    # Returns list containing top 10 users (sorted by post count) and their post count
    def gettopposters(self):
        soup = self.__getbs("http://care-tags.org/memberlist.php?mode=&sk=d&sd=d#memberlist")
        postcountlist = []
        top10 = []

        memberlist = soup.find(id="memberlist").tbody
        for member in memberlist.children:
            if member.string is None: # Gets rid of the newlines
                # Store username and post count pair in the list
                user = member.td.a.string
                postcount = int(member.find(class_="posts").string)
                postcountlist.append((user, postcount))

        # Take the top 10 users
        postcountlist.sort(key=itemgetter(1), reverse=True)
        for i in range(10):
            usercount = postcountlist[i]
            print "User: " + usercount[0] + "   Posts: " + str(usercount[1])

        top10 = postcountlist[:10]

        return top10




    def __getbs(self, url):
        # Initial variables
        username = self.username
        password = self.password
        website = "http://care-tags.org/ucp.php?mode=login"

        # Login with provided credentials
        sess = self.session
        payload = {"username": username, "password":password,
            "autologin":"on","login":"login"}
        response = sess.post(website, data=payload)

        # Visit desired url
        response = sess.get(url)

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

    hakuna = TopMembers("pythonbot", "autonomous")
    hakuna.gettopposters()