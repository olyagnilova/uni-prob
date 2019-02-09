import re

with open('txt_i.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

res = re.findall(r'id=(.*?)\' target', data)

f = open("vuz_ids_2a.txt", "x")
f.write(str(res))
f.close()
print(len(res))

#with open("vuz_ids.txt", "r") as nf:
#    print(nf.read())
