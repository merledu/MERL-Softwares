
import os
import re

user=str(os.getlogin())

f1=open('main.desktop','rt')
r1=f1.read()
x= re.search('[/]home[/][A-Z|a-z].*[/]',r1)
if x:
    y=x[0].split('/')
    r1=r1.replace(f'/home/{y[2]}',f'/home/{user}')
    f1.close()
    f1=open('main.desktop','wt')

    f1.write(r1)
    f1.close()
print('DONE')

