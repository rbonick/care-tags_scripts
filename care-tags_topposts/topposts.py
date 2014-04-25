from bs4 import BeautifulSoup
import requests
from operator import itemgetter
import time


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
        threadurls = []

        soup = self.__getbs(forumurl)
        pagination = soup.find(class_="pagination")
        numposts = int(pagination.text.split()[4])  # Gets the thread count
        currpost = 0
        while currpost < numposts:
            print "Working..."
            soup = self.__getbs(forumurl + "&start=" + str(currpost))
            postlists = soup.find_all(class_="topiclist topics")
            if len(postlists) > 1:
                # Handle announcements (only once)
                if currpost is 0:
                    for li in postlists[0].children:
                        if li.string is None:
                            # This jumble grabs the first link (the relative link) and splits along = and & signs
                            # This allows the forum number and topic number to be extracted and put into a standard link
                            stringsplit = li.dl.dt.a["href"].replace("=", "*").replace("&", "*").split("*")
                            threadurls.append("http://care-tags.org/viewtopic.php?f=" + stringsplit[1] +
                                              "&t=" + stringsplit[3])
                postlists = postlists[1]
            else:
                postlists = postlists[0]

            for li in postlists.children:
                if li.string is None:
                    # This jumble grabs the first link (the relative link) and splits along = and & signs
                    # This allows the forum number and topic number to be extracted and put into a standard link
                    stringsplit = li.dl.dt.a["href"].replace("=", "*").replace("&", "*").split("*")
                    threadurls.append("http://care-tags.org/viewtopic.php?f=" + stringsplit[1] +
                                      "&t=" + stringsplit[3])
            currpost += 25

        return threadurls

    # Returns all posts for a given thread in the form (Post url, poster, reputation)
    def getposts(self, threadurl):
        allposts = []
        soup = self.__getbs(threadurl)
        pagination = soup.find(class_="pagination").text.split()
        # If there are unread posts, pagination[0] is "First", so you need pagination[4] instead
        try:
            numposts = int(pagination[0])
        except:
            numposts = int(pagination[4])
        currpost = 0
        while currpost < numposts:
            print "Working..."
            soup = self.__getbs(threadurl + "&start=" + str(currpost))
            threadposts = soup.find_all(class_="post")
            for threadpost in threadposts:
                # Extract username
                try:
                    user = threadpost.div.dl.dt.find_all("a")
                except:  # If user is banned/no longer exists it won't work so just break
                    # TODO: Fix so it still works with banned users
                    break
                # If no avatar then it's the first element, otherwise the second element
                try:
                    if len(user) is 1:
                        user = user[0].string
                    elif len(user) is 2:
                        user = user[1].string
                    else:
                        break
                except:
                    print "FAILED"
                    print threadurl + "&start=" + str(currpost)
                    print threadpost.prettify()
                    print user
                    user = "FAILED SOMEHOW"

                # Extract post id and generate its permalink
                postid = threadpost["id"]
                posturl = threadurl + "&start=" + str(currpost) + "#" + postid

                # Extract rep of the post
                postrep = int(threadpost.find(title="Post reputation").a.string)

                allposts.append((posturl, user, postrep))
            currpost += 30

        return allposts

    def gettopposts(self, numposts):
        forums = self.getforums()
        threads = []
        posts = []

        exclusions = ["http://care-tags.org/viewtopic.php?f=2&t=8"]

        for forum in forums:
            for thread in self.getthreads(forum):
                threads.append(thread)

        for thread in threads:
            if thread not in exclusions:
                currposts = self.getposts(thread)
                for post in currposts:
                    posts.append(post)

        posts.sort(key=itemgetter(2), reverse=True)

        topposts = posts[:numposts]
        return topposts

    def gettopwaywt(self, numposts):
        waywturl = "http://care-tags.org/viewtopic.php?f=2&t=8"
        posts = self.getposts(waywturl)

        posts.sort(key=itemgetter(2), reverse=True)

        topposts = posts[:numposts]
        return topposts

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
    starttime = time.time()
    hakuna = TopPosts("pythonbot", "autonomous")
    forums = hakuna.getforums()
    threads = []
    posts = []

    for forum in forums:
        for thread in hakuna.getthreads(forum):
            threads.append(thread)
    #
    # for i, thread in enumerate(threads):
    #     print (str(i) + ": " + thread)
    for thread in threads:
        currposts = hakuna.getposts(thread)
        for post in currposts:
            posts.append(post)
    posts.sort(key=itemgetter(2), reverse=True)

    top10posts = posts[:10]
    for post in top10posts:
        print post

    print "Runtime: " + str(time.time() - starttime)