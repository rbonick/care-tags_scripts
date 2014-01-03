from bs4 import BeautifulSoup
from urllib import urlopen

class RepReader:

    def __init__(self):

    # Should be given the usernumber to retrieve
    # TODO: Support usernames
    # 
    # @Return: a list in the form [[username, posrep, negrep], ...]
    def parsehtml(self):
        
        # Make some soup
        soup = BeautifulSoup(self.__gethtml())
           
        # Find the reputation list section
        repsection = soup.find(id="post-reputation-list");

        return True

    def __gettotalrep(self, tag):
        print("called __gettotalrep")
        print(tag.prettify())
        print(str(tag.find("ul").find("li").text))
        return tag.find("ul").find("li").text

    # Gets the html for a page
    def __gethtml(self):
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
        return open("rep.html")

 
