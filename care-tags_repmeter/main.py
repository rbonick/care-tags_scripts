from repreader import RepReader
from operator import itemgetter

test = RepReader("PythonBot","autonomous")
print("Total reputation received:")
for item in sorted(test.receivedrep(59),key=itemgetter(1),reverse=True):
    print(item)
print("\nMost repped post:")
for item in test.mostrepped(59):
    print(item)
print("done")
