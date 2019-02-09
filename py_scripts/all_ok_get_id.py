import re

with open('all_ok_ids_raw.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

res = re.findall(r'data-id=\"(.*?)\" data', data)

f = open("all_ok_ids.txt", "x")
f.write(str(res))
f.close()
print(len(res))
