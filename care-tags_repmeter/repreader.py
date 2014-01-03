from bs4 import BeautifulSoup
from urllib import urlopen
from collections import defaultdict

class RepReader:

    def __init__(self):
        self.message = "hi"

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

 
