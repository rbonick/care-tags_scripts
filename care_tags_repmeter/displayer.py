from math import ceil

class Displayer:

    def __init__(self):
        self.name = "hi"

    # Displays reputation created by RepReader receivedrep()
    #
    # Prints in a graph
    # @Return: nothing
    def displayAllRep(self, replist):
        
        maxrep = int(replist[0][1]) - int(replist[0][2])
        scalefactor = float(float(maxrep)/30)
        print("Username:".rjust(22) + " Reputation:")
        print("  ==============================" + 
            "==============================")
        
        for item in replist:
            
            scaledposrep = int(ceil(item[1]/scalefactor))
            plus = "".join("+" for i in range(scaledposrep))
            scalednegrep = int(ceil(item[2]/scalefactor)*-1)
            minus = "".join("-" for i in range(scalednegrep))
            
            print(str(item[0]).rjust(22) + " " + 
                (plus + minus).ljust(32) + 
                str(item[1])+"/" + str(item[2]))

    
    def displayMostRepped(self, mostrepped):
        print("Most repped post:")
        print("=================")
        print("Text:\n" + str(mostrepped["posttext"]) + "\n")
        print("Net reputation: " + str(mostrepped["netrep"]) + "\n")
        print("Direct link: " + str(mostrepped["url"]))
