from bs4 import BeautifulSoup
from collections import defaultdict
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

    # Should be given the usernumber to retrieve
    # TODO: Support usernames
    # 
    # @Return: a list in the form [[username, posrep, negrep], ...]
    def parsehtml(self, usernum):
        
        pages = self.__gethtml(usernum)
        repdict = defaultdict(list)
        for page in pages:
            
            # Make some soup
            soup = BeautifulSoup(page)
               
            # Find the reputation list section
            repsection = soup.find(id="post-reputation-list")
           
            repsection.contents = [a for a in repsection.contents if a != "\n"]

            for child in repsection.children:
                if child.name == "ul":
                    continue
                user = child.find("a").string

                rep = child.find(class_ = "reputation-rating").contents[0]["title"].split()[1]

                repdict[user].append(rep)
        
        replist = []

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
        return True

    def __gettotalrep(self, tag):
        return int(tag.find("ul").find("li").text.split()[0])

    # Gets the html for a page
    def __gethtml(self, usernum):
        
        # Initial variables
        username = self.username
        password = self.password
        website = "http://care-tags.org/ucp.php?mode=login"
        
        # Start a session
        session = requests.Session()
        
        # Login with provided credentials
        payload = {"username": username, "password":password, 
                    "autologin":"on","login":"login"}
        response = session.post(website, data=payload)
        
        # Visit desired user's rep page
        response = session.get("http://care-tags.org/reputation.php?mode=details&u="+str(usernum)) 
        
        # Pull user's total rep
        bs = BeautifulSoup(response.text)
        totalrep = self.__gettotalrep(bs.find(id="post-reputation-list"))

        # Iterate through all rep pages
        pages = []
        urls = []
        repcount = 0 
        while repcount < totalrep:
            currentpage = "http://care-tags.org/reputation.php?&mode=details&u=" + str(usernum)+ "&start=" + str(repcount)
          
            # Store each page in a list
            response = session.get(currentpage)
            pages.append(response.text) 
            urls.append(response.url)
            repcount = repcount + 15

        return pages
