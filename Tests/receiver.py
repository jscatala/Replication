#!/usr/bin/env python

from socket import *
from random import randint,uniform
import datetime as dt
import sys
import select
import psycopg2

host = "0.0.0.0"
port = 9999
s    = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf  = 1024
con  = None

try:
    con = psycopg2.connect(database='inducom', user='postgres', password='psql_pass', host='localhost')
    cur = con.cursor()
    f   = open("/tmp/received.txt","w")
    n   = 0

    data,addr = s.recvfrom(buf)

    try:
        while(data):
            f.write(data+'\n')
            n+=1
            s.settimeout(4)
            data,addr = s.recvfrom(buf)
            ft_data = data.split(',')[0]
            movil   = data.split(',')[1]
            vchar   = data.split(',')[2]
            lat     = uniform(17.1,56.18)
            long    = uniform(70.1,73.1)
            speed   = randint(5,120)
            query   = "INSERT INTO datos values ('{0}','{1}',{2},'{3}',{4},{5},{6})".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),ft_data,movil,vchar,lat,long,speed)
            cur.execute(query)
            con.commit()

    except timeout:
        if con:
            con.close()
        s.close()
        f.close()
        print "Paquetes Totales recibidos {0}".format(n)

except psycopg2.DatabaseError, e :
    if con:
        con.rollback()
    
    print 'Error %s' % e
    sys.exit(1)

finally:

    if con:
        con.close()

