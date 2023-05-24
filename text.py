from math import ceil
def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

newidlist = []
newStr = ''

with open("/home/aymichael/studying/python_tst/oskelly/id.txt") as file:
        ids = file.read().split(', ')
        # print("Список айдишников получен", len(ids), ids[1:4])

print("Тип партинга - ",type(parting(ids, 8)))
i = 1
for part in parting(ids, 8)[::-1]:
      if i == 1 or i == 4: 
            newidlist.append(part)
    #   print(len(part))
      i+=1
      
newids = str(newidlist)


newids = newids.split(", ")
for elem in newids:
    elem = elem[1:-1]
    newStr+=elem + ', '
# print(newStr)

with open('/home/aymichael/studying/python_tst/oskelly/idNew.txt', 'w') as file:
    file.write(newStr)