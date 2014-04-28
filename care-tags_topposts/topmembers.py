from bs4 import BeautifulSoup
import requests
from operator import itemgetter


class TopMembers:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #Start session
        self.session = requests.Session()

    # Returns list containing top 10 users (sorted by post count) and their post count as a tuple
    def gettopposters(self, return_count):
        soup = self.__getbs("http://care-tags.org/memberlist.php?mode=&sk=d&sd=d#memberlist")
        postcountlist = []

        # Get number of members
        num_members = int(soup.find(class_="pagination").text.split()[0])  # Gets the thread count
        print num_members

        curr_members = 0
        while curr_members < num_members:
            print "Working, page", curr_members/25 + 1
            soup = self.__getbs("http://care-tags.org/memberlist.php?sk=d&sd=d&start=" + str(curr_members))

            memberlist = soup.find(id="memberlist").tbody
            for member in memberlist.children:
                if member.string is None:  # Gets rid of the newlines
                    # Store username and post count pair in the list
                    user = member.td.a.string
                    postcount = int(member.find(class_="posts").string)
                    postcountlist.append((user, postcount))
            curr_members += 25

        # Take the top 10 users
        return postcountlist[:return_count]

    # Returns list containing top 10 users (sorted by reputation) and their reputation as a tuple
    def mostreppedusers(self, return_count):
        soup = self.__getbs("http://care-tags.org/memberlist.php?mode=&sk=r&sd=d#memberlist")
        userreplist = []

        # Get number of members
        num_members = int(soup.find(class_="pagination").text.split()[0])  # Gets the thread count
        print num_members

        curr_members = 0
        while curr_members < num_members:
            print "Working, page", curr_members/25 + 1
            soup = self.__getbs("http://care-tags.org/memberlist.php?sk=r&sd=d&start=" + str(curr_members))

            memberlist = soup.find(id="memberlist").tbody
            for member in memberlist.children:
                if member.string is None:  # Get rid of newlines
                    # print member.prettify()
                    user = member.td.a.string
                    repcount = member.find_all(class_="posts")[1].string
                    userreplist.append((user, repcount))
            curr_members += 25

        # Take top 10 users
        return userreplist[:return_count]

    # Returns list containing top return_count users (sorted by rep per post count) in the form
    # (User, rep/post, posts, rep)
    def most_rep_per_post_users(self, return_count):
        users = []
        soup = self.__getbs("http://care-tags.org/memberlist.php")
        num_users = int(soup.find(class_ = "rightside pagination").text.split()[0])
        curr_user = 0
        while curr_user < num_users:
            print "Working, page", curr_user/25 + 1
            soup = self.__getbs("http://care-tags.org/memberlist.php?start=" + str(curr_user))
            body = soup.tbody
            for child in body.children:
                if child.string is None:
                    user = child.td.a.string
                    posts = int(child.find_all("td")[1].string)
                    rep = int(child.find_all("td")[3].string)
                    if posts > 0:
                        rep_per = float(rep)/float(posts)
                    else:
                        rep_per = -1.
                    users.append((user, rep_per, posts, rep))
            curr_user += 25
        users.sort(key=itemgetter(1), reverse=True)
        return users[:return_count]

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
    for poster in hakuna.gettopposters(10):
        print poster[0], poster[1]

    print "Top posters by reputation:"
    for poster in hakuna.mostreppedusers(10):
        print poster[0], poster[1]

    print "Top repped per post:"
    for poster in hakuna.most_rep_per_post_users(10):
        print poster[0], poster[1]