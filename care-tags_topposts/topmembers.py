from bs4 import BeautifulSoup
import requests


class TopMembers:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #Start session
        self.session = requests.Session()

    # Returns list containing top 10 users (sorted by post count) and their post count as a tuple
    def gettopposters(self):
        soup = self.__getbs("http://care-tags.org/memberlist.php?mode=&sk=d&sd=d#memberlist")
        postcountlist = []

        memberlist = soup.find(id="memberlist").tbody
        for member in memberlist.children:
            if member.string is None:  # Gets rid of the newlines
                # Store username and post count pair in the list
                user = member.td.a.string
                postcount = int(member.find(class_="posts").string)
                postcountlist.append((user, postcount))

        # Take the top 10 users
        return postcountlist[:10]

    # Returns list containing top 10 users (sorted by reputation) and their reputation as a tuple
    def mostreppedusers(self):
        soup = self.__getbs("http://care-tags.org/memberlist.php?mode=&sk=r&sd=d#memberlist")
        userreplist = []

        memberlist = soup.find(id="memberlist").tbody
        for member in memberlist.children:
            if member.string is None:  # Get rid of newlines
                # print member.prettify()
                user = member.td.a.string
                repcount = member.find_all(class_="posts")[1].string
                userreplist.append((user, repcount))

        # Take top 10 users
        return userreplist[:10]

    def __getbs(self, url):
        # Initial variables
        username = self.username
        password = self.password
        website = "http://care-tags.org/ucp.php?mode=login"

        # Login with provided credentials
        sess = self.session
        payload = {"username": username, "password": password,
                   "autologin": "on", "login": "login"}
        sess.post(website, data=payload)

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
    print "Top posters by post count:"
    for poster in hakuna.gettopposters():
        print str(poster[0]) + " " + str(poster[1])

    print "Top posters by reputation:"
    for poster in hakuna.mostreppedusers():
        print str(poster[0]) + " " + str(poster[1])