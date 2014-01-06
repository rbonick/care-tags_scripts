from repreader import RepReader

test = RepReader("PythonBot","autonomous")
print("Total reputation received:")
for item in test.receivedrep(249):
    print(item)
print("\nMost repped post:")
for item in test.mostrepped(249):
    print(item)
print("done")
