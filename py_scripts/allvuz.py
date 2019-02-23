import re

with open('txt_i_2016.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

res = re.findall(r'id=(.*?)\" target', data)

f = open("vuz_ids_2016.txt", "x")
f.write(str(res))
f.close()
print(len(res))

#with open("vuz_ids.txt", "r") as nf:
#    print(nf.read())
