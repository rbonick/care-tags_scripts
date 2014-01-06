from repreader import RepReader
from operator import itemgetter
from displayer import Displayer

test = RepReader("PythonBot","autonomous")
display = Displayer()

allrep = sorted(test.receivedrep(2),key=itemgetter(1),reverse=True)
display.displayAllRep(allrep)

mostrep = test.mostrepped(2)

print("done")
