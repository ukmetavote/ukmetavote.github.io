# ukge2eu.py
#
#   based on http://www.dabeaz.com/coroutines/
# To run this, you will need a folder full of csv files 
from coroutines import *
import json
        

@coroutine
def getoeu():
    epcode2eu={}
    pcode2eu={}
    ptown2eu={}
    try:
        while True:
            line = (yield)
            postcode = line[1]
            if ' ' in postcode:
                prefix,suffix = postcode.split()
                eprefix = prefix+suffix[:1]
                ptown = postcode[0:2]
                ukge = line[18]
                ukeu = line[19]
                if prefix and ukeu:
                    lookup = pcode2eu.get(prefix,{})
                    lookup[ukeu] =  1+lookup.get(ukeu,0)
                    pcode2eu[prefix] = lookup
                
                    lookup = ptown2eu.get(ptown,{})
                    lookup[ukeu] =  1+lookup.get(ukeu,0)
                    ptown2eu[ptown] = lookup

                    lookup = epcode2eu.get(eprefix,{})
                    lookup[ukeu] =  1+lookup.get(ukeu,0)
                    epcode2eu[eprefix] = lookup
                
    except GeneratorExit:
        print json.dumps(ptown2eu, sort_keys=True,
                  indent=2, separators=(',', ':'))
        print json.dumps(pcode2eu, sort_keys=True,
                  indent=2, separators=(',', ':'))
        print json.dumps(epcode2eu, sort_keys=True,
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
