from bs4 import BeautifulSoup
from urllib import urlopen

class RepReader:

    #Should be given a usernumber to retrieve rep on
    #TODO: Support usernames
    def __init__(self, usernumber=2):
        self.usernumber = usernumber

    def parsehtml(self):
       # #Get access to user's rep page, and store it as Beautiful Soup  
       # #TODO: Figure out how to be able to access the reputation page
       # page = BeautifulSoup(urlopen("http://care-tags.org/reputation.php?&mode=details&u=" + str(self.usernumber)))
       #  
       # #Find the overall number of reputation a user has
       # totalrep=self.__gettotalrep(page.find(id="post-reputation-list"))
       # 
       # #Iterate through all the pages
       # repcount = 0 
       # while repcount < totalrep:
       #     currentpage = BeautifulSoup(urlopen("http://care-tags.org/reputation.php?&mode=details&u=" + str(self.usernumber)+ "&start=" + repcount))
       #    
       #     #Parse each page
       #     
       #     
       #     repcount = repcount + 15
       #

        # Open the file
        soup = BeautifulSoup(open("rep.html"))

        # Find the reputation list section
        repsection = soup.find(id="post-reputation-list");

        return True

    def __gettotalrep(self, tag):
        print("called __gettotalrep")
        print(tag.prettify())
        print(str(tag.find("ul").find("li").text))
        return tag.find("ul").find("li").text
        
