from bs4 import BeautifulSoup
import requests
from operator import itemgetter
import time
import grequests



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
        forumurls = []

        soup = self.__getbs(forumurl)
        pagination = soup.find(class_="pagination")
        numposts = int(pagination.text.split()[4])  # Gets the thread count
        currpost = 0
        while currpost < numposts:
            forumurls.append(forumurl + "&start=" + str(currpost))
            currpost += 25
        for response in self.__getallbs(forumurls):
            postlists = response.find_all(class_="topiclist topics")
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
        return threadurls

    # Returns all posts for a given thread in the form (Post url, poster, reputation)
    def getposts(self, threadurl):
        allposts = []
        pageurls = []

        soup = self.__getbs(threadurl)
        pagination = soup.find(class_="pagination").text.split()
        # If there are unread posts, pagination[0] is "First", so you need pagination[4] instead
        try:
            numposts = int(pagination[0])
        except:
            numposts = int(pagination[4])
        currpost = 0
        while currpost < numposts:
            pageurls.append(threadurl + "&start=" + str(currpost))
            # print "Working, page", currpost/30 + 1, "of", numposts/30 + 1
            # soup = self.__getbs(threadurl + "&start=" + str(currpost))
            # threadposts = soup.find_all(class_="post")
            # for threadpost in threadposts:
            #     # Extract username
            #     try:
            #         user = threadpost.div.dl.dt.find_all("a")
            #     except:  # If user is banned/no longer exists it won't work so just break
            #         # TODO: Fix so it still works with banned users
            #         break
            #     # If no avatar then it's the first element, otherwise the second element
            #     try:
            #         if len(user) is 1:
            #             user = user[0].string
            #         elif len(user) is 2:
            #             user = user[1].string
            #         else:
            #             break
            #     except:
            #         print "FAILED"
            #         print threadurl + "&start=" + str(currpost)
            #         print threadpost.prettify()
            #         print user
            #         user = "FAILED SOMEHOW"
            #
            #     # Extract post id and generate its permalink
            #     postid = threadpost["id"]
            #     posturl = threadurl + "&start=" + str(currpost) + "#" + postid
            #
            #     # Extract rep of the post
            #     postrep = int(threadpost.find(title="Post reputation").a.string)
            #
            #     allposts.append((posturl, user, postrep))
            currpost += 30
        for response in self.__getallbs(pageurls):
            threadposts = response.find_all(class_="post")
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
                postrep = int(threadpost.find(title="Post reputation").string)

                allposts.append((posturl, user, postrep))
        return allposts

    def gettopposts(self, numposts):
        forums = self.getforums()
        threads = []
        posts = []

        exclusions = ["http://care-tags.org/viewtopic.php?f=2&t=8"]

        for i, forum in enumerate(forums):
            print "Working, forum", i+1, "out of", len(forums)
            for thread in self.getthreads(forum):
                threads.append(thread)

        for i, thread in enumerate(threads):
            print "Working, thread", i+1, "out of", len(threads)
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

    def __getallbs(self, urls):
        '''
        Given a list of urls, returns list of Beautiful Soups
        made from the text associated with each page
        '''
        soups = []
        rs = (grequests.get(u) for u in urls if u[0] is 'h')
        for i, response in enumerate(grequests.map(rs, size=100)):
            print "On", i
            if response is not None:
                soups.append(BeautifulSoup(response.text))
        return soups

if __name__ == "__main__":
    starttime = time.time()
    hakuna = TopPosts("pythonbot", "autonomous")
    forums = hakuna.getforums()
    threads = []
    posts = []

    print "Getting forums"
    for forum in forums:
        for thread in hakuna.getthreads(forum):
            threads.append(thread)
    #
    # for i, thread in enumerate(threads):
    #     print (str(i) + ": " + thread)
    print "Getting threads/posts"
    for thread in threads:
        currposts = hakuna.getposts(thread)
        for post in currposts:
            posts.append(post)
    posts.sort(key=itemgetter(2), reverse=True)

    top10posts = posts[:10]
    for post in top10posts:
        print post

    print "Runtime: " + str(time.time() - starttime)