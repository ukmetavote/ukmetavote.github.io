
# coroutines.py
#
# processing pipelines with coroutines.  based on http://www.dabeaz.com/coroutines/
# To run this, you will need a folder full of csv files 

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

# A data source.  This is not a coroutine, but it sends
# data into one (target)

import time
def follow(thefile, target):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         target.send(line)

# a data source.  This reads all files in a dir
# data into a coroutine (target)

import os.path
import glob
def readallfiles(dir, target):
    abspath= os.path.abspath(dir)
    print abspath
    allfiles = glob.glob(abspath)
    for fname in allfiles:
        with open(fname) as f:
            readfile(f,target)
# a data source.  This reads all files in a dir
# data into a coroutine (target)

import os.path
import glob
def readallcsvfiles(dir, target):
    abspath= os.path.abspath(dir)
    allfiles = glob.glob(abspath)
    for fname in allfiles:
        with open(fname) as f:
            readcsvfile(f,target)

# Another data source.  This is not a coroutine, but it sends
# data into one (target)
         
def readfile(thefile, target):
    while True:
         line = thefile.readline()
         if not line:
             break
         target.send(line)

# A CSV data source.  This is not a coroutine, but it sends
# data into one (target)
         
import pymysql.cursors

def readSQLquery(query, target):
    arraysize=1000
    # Connect to the database - edit for your config
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='root',
                                 db='default',
                                 port = 3306,
                                 charset='latin1',
                                 cursorclass=pymysql.cursors.SSDictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(query)
            results = ['dummy']
            while results:
                results = cursor.fetchmany(arraysize)
                for result in results:
                    target.send(result)
    finally:
        connection.close()

# A MySQL data source.  This is not a coroutine, but it sends
# data into one (target)
         
import csv
def readcsvfile(thefile, target):
    reader = csv.reader(thefile)
    for row in reader:
        target.send(row)


# A filter that matches text

@coroutine
def match(pattern,target):
    while True:
        line = (yield)           # Receive a line
        if pattern in line:
            target.send(line)    # Send to next stage

# A filter that outputs when text doesn't match

@coroutine
def nomatch(pattern,target):
    while True:
        line = (yield)           # Receive a line
        if pattern not in line:
            target.send(line)    # Send to next stage
            
# A filter that turns apache log lines into tab separated ones
import re
from dateutil.parser import parse
logpattern = re.compile(r'^([0-9.]+)[^\[]*\[([^\]]*)\]\s"([^"]*)"\s([0-9]+)\s([0-9]+)\s"([^"]*)"\s"([^"]*)"')
        
@coroutine
def logtotsv(target):
    while True:
        line = (yield)           # Receive a line
        result = logpattern.match(line)
        fields = list(result.groups())
        #turn apache's godawful date format into ISO, then mung that into spreadsheet compatible datetime by removing TZ
        datefield = fields[1]
        isodate = str(parse(datefield[:11]+" "+datefield[12:]))
        fields[1] = isodate.split('+')[0]
        if result:
            target.send("\t".join(fields)+'\n')    # Send to next stage

#count lines  
@coroutine
def count():
    count=0
    try:
        while True:
            line = (yield)
            count +=1
    except GeneratorExit:
        print "got " +str(count)+" lines"
        
# A sink.  A coroutine that receives data

@coroutine
def printer():
    while True:
         line = (yield)
         print line,

def quantize(x,n=50):
    return int(x+n/2-(x%n))

# Example use
if __name__ == '__main__':
    readSQLquery('select * from versions',
        printer() #output
        )
