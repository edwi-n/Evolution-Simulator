test = (10, 2)
values = {test: True}
previous = (test[0], test[1])
values.pop(previous)
previous = (previous[0]+1, previous[1]-1)
values[previous] = True
print(values)
