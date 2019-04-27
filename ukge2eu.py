# ukge2eu.py
#
#   based on http://www.dabeaz.com/coroutines/
# To run this, you will need a folder full of csv files 
from coroutines import *
import json
        

@coroutine
def getoeu():
    constituencies={}
    try:
        while True:
            line = (yield)
            ukge = line[18]
            ukeu = line[19]
            if ukge and ukeu:
                constituencies[ukge] = ukeu
    except GeneratorExit:
        print json.dumps(constituencies, sort_keys=True,
                  indent=2, separators=(',', ':'))

@coroutine
def printer():
    while True:
         line = (yield)
         print line,

if __name__ == '__main__':
    readallcsvfiles('NSPL_AUG_2018_UK/Data/multi_csv/*.csv',
            getoeu() #output
        )
