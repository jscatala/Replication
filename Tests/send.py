#!/usr/bin/env python

from socket import *
import sys
import string
from random import randint,choice
from time import sleep
import datetime as dt

def randvarchar(size=randint(5,15), chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for x in range(size))

s = socket(AF_INET,SOCK_DGRAM)
host =sys.argv[1]
port = 9999
addr = (host,port)

#Tiempo que queremos que corra
min=int(sys.argv[2])

#Tiempo de termino
end = dt.datetime.now() + dt.timedelta(minutes=min)

#Contador de paquetes
count=0

while ( end > dt.datetime.now() ):
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    sleep(randint(1,50)/100)
    movil = randint(1,15)
    vchar = randvarchar() 
    data  = "{0},{1},{2}".format(now,movil,vchar)
    #print data
    if(s.sendto(data,addr)):
        count+=1
        sys.stdout.write("Paquetes totales enviados: {0}\r".format(count))
	sys.stdout.flush()

s.close()
sys.stdout.write("\n")
