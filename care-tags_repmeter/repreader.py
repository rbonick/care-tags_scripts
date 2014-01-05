from bs4 import BeautifulSoup
from collections import defaultdict
import urllib
import urllib2
import cookielib
import re
import time

class RepReader:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Should be given the usernumber to retrieve
    # TODO: Support usernames
    # 
    # @Return: a list in the form [[username, posrep, negrep], ...]
    def parsehtml(self):
        
        # Make some soup
        soup = BeautifulSoup(self.__gethtml())
           
        # Find the reputation list section
        repsection = soup.find(id="post-reputation-list")
       
        repsection.contents = [a for a in repsection.contents if a != "\n"]
        
        repdict = defaultdict(list)

        for child in repsection.children:
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
        print(replist)
        return True

    def __gettotalrep(self, tag):
        print("called __gettotalrep")
        print(tag.prettify())
        print(str(tag.find("ul").find("li").text))
        return tag.find("ul").find("li").text

    # Gets the html for a page
    def __gethtml(self):
        
        ## Connect to phpbb and "login"
        username = self.username
        password = self.password
        print(username + " " + password)
        website = "http://www.care-tags.org/ucp.php?mode=login"
        loginmsg = "You have been successfully logged in." 
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        logindata = urllib.urlencode({"username": username,
                      "password":password, "autologin": "on", 
                      "login":"Login"})
                                    
        response = opener.open(website, logindata)
        bs = BeautifulSoup(response.read())
        print(bs.prettify())
        if loginmsg in response.read():
            print("Logged in " + username + " successfully!")
            print("Cookies are:")
            for cookie in cookies:
                print(cookie)
            
            testsite = "http://www.care-tags.org"
            logoutmsg = "Logout [ " + username + " ]"
            response = opener.open(testsite)
            if logoutmsg not in response.read():
                print("Lost the cookies!")
                print("Cookies are:")
                for cookie in cookies:
                    print(cookie)
        else:
            print("Did not get logged in")
         



        #Store each page in a list
        pages = []

        #Get access to user's rep page, and store it as Beautiful Soup  
        #TODO: Figure out how to be able to access the reputation page
        page = BeautifulSoup(urlopen("http://care-tags.org/reputation.php?&mode=details&u=" + str(self.usernumber)))
        
        #Find the overall number of reputation a user has
        totalrep=self.__gettotalrep(page.find(id="post-reputation-list"))
       
        #Iterate through all the pages
        repcount = 0 
        while repcount < totalrep:
            currentpage = BeautifulSoup(urlopen("http://care-tags.org/reputation.php?&mode=details&u=" + str(self.usernumber)+ "&start=" + repcount))
          
            #Parse each page
           
           
            repcount = repcount + 15
       

       ##OLD METHOD     
       #
       # # Open the file
       # return open("rep.html")

 
