import os

f = open("out.txt").read()
o = open("done.txt", 'wa')
lines = f.split("\n")

for line in lines[1::3]:
    r = os.system("wget -c "+line)
    o.write(line)
