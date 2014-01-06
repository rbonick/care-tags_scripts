from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
import urllib
import urllib2
import cookielib
import re
import time
import requests

class RepReader:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        # Start a session
        self.session = requests.Session()
        
    # Should be given the usernumber to retrieve
    # TODO: Support usernames
    # 
    # @Return: a list in the form [[username, posrep, negrep], ...]
    def receivedrep(self, usernum):
        
        pages = self.__gethtml(usernum)
        repdict = defaultdict(list)
        
        # Iterate through each of the rep pages
        for page in pages:
            
            # Make some soup
            soup = BeautifulSoup(page)
               
            # Find the reputation list section
            repsection = soup.find(id="post-reputation-list")
            
            # Eliminate newlines
            repsection.contents = [a for a in repsection.contents if a != "\n"]
            # Go through all the rep sections
            for child in repsection.children:
                
                # Ignore the pages selection at the bottom
                if child.name == "ul":
                    continue

                # Parse user
                user = child.find("a").string

                # Parse rep
                rep = child.find(class_ = "reputation-rating").contents[0]["title"].split()[1]

                # Add to dictionary
                repdict[user].append(rep)
        
        # List to aggregate with
        replist = []

        # Iterate through dictionary and aggregate each user's reputation
        for usr, lst in repdict.iteritems():
            currlist = [usr]
            posrep = 0
            negrep = 0
            for rep in lst:
                if int(rep) > 0:
                    posrep = posrep + int(rep)
                elif int(rep) < 0:
                    negrep = negrep + int(rep)
            currlist.append(posrep)
            currlist.append(negrep)
            replist.append(currlist)

        return replist

    def __gettotalrep(self, tag):
        return int(tag.find("ul").find("li").text.split()[0])

    # Gets the html for a page
    def __gethtml(self, usernum):
        
        # Initial variables
        username = self.username
        password = self.password
        website = "http://care-tags.org/ucp.php?mode=login"
        
        # Login with provided credentials
        sess = self.session
        payload = {"username": username, "password":password, 
                    "autologin":"on","login":"login"}
        response = sess.post(website, data=payload)
        
        # Visit desired user's rep page
        response = sess.get("http://care-tags.org/reputation.php?mode=details&u="+str(usernum)) 
        
        # Pull user's total rep
        bs = BeautifulSoup(response.text)
        totalrep = self.__gettotalrep(bs.find(id="post-reputation-list"))

        # Iterate through all rep pages
        pages = []
        urls = []
        repcount = 0 
        while repcount < totalrep:
            # Gets each of the rep pages
            #
            # Server uses &start to pick where to display,
            # so use that to keep track of where we are
            currentpage = "http://care-tags.org/reputation.php?&mode=details&u=" + str(usernum)+ "&start=" + str(repcount)
          
            # Store each page in a list
            response = sess.get(currentpage)
            pages.append(response.text) 
            urls.append(response.url)
        
            # Increment count by max rep displayed on each page
            repcount = repcount + 15

        return pages

    # Should be given a usernumber to retrieve most repped post
    # TODO: Support usernames
    #
    # @Return: A list in the form of (post text, rep, url)
    def mostrepped(self, usernum):

        ## Get rep pages
        pages = self.__gethtml(usernum)
        postdict = defaultdict(list)

        # Iterate through each page
        for page in pages:

            # Make some soup
            soup = BeautifulSoup(page)

            # Get the list of rep on the page
            repsection = soup.find(id="post-reputation-list")

            repsection.contents = [a for a in repsection.contents if a != "\n"]

            # Iterate through rep
            for child in repsection.children:
                
                # Ignore the page navigation at the bottom of pages
                if child.name == "ul":
                    continue

                # Store rep
                rep = child.find(class_ = "reputation-rating").contents[0]["title"].split()[1]
                
                # Store post #
                try:
                    link = child.find_all("a")[1]
                    prestrip = link.string.split("[#p")[1]
                    postnum = prestrip.split("]")[0]
                    
                    # Add rep to the dictionary for that post number
                    postdict[postnum].append(rep)
                except:
                    continue                                
                
        ## Map rep in the form of (post #, rep)
        replist = []
        
        # Sum up the reps for each post and store in a list
        for postnum, replst in postdict.iteritems():
            postrep = 0
            for rep in replst:
                postrep = postrep + int(rep)
            replist.append((postnum, postrep))

        ## Find highest rep count
        replist.sort(key=itemgetter(1), reverse=True)
        mostrep = replist[0]            
        postnum = mostrep[0]

        ## Get associated post text
        # Make URL
        url = "http://care-tags.org/viewtopic.php?p="+postnum+"#p"+postnum
        
        # Get text of post
        response = self.session.get(url)
        page = BeautifulSoup(response.text)
        postdiv = page.find(id="p"+postnum)
        postcontent = postdiv.find(class_="content")
        txtlst = postcontent.contents
        text = "".join(x.string for x in txtlst if isinstance(x.string, unicode))
        
        # Return text and rep
        return [text, mostrep[1], url]
        