a = [ "Work", "it", "Work/A", "Work/B" ]

b = [ i for i in a if i[0:4] != "Work" ]

print(b)
