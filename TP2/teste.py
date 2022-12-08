import re
import time
from time import sleep

message = f'servername:10.0.20.2 time:1670463174.3541117 jumps:0 visited:'

splitted = re.split(' ',message)


for string in splitted:
    s = re.split(r':',string)
    if s[0] == 'servername':
        print('servername',s[1])
    if s[0] == 'time':


        x = time.time()

        print(x - float(s[1]))
    if s[0] == 'jumps':
        print(s[1])
    if s[0] == 'visited':
        a = re.split(',',s[1])
        
        print(a)

       
