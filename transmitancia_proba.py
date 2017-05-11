#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 14:20:40 2017

@author: Víctor
"""




import onewirerpi as ow
import httplib, urllib, os, glob, time

bus = ow.DS18b20()
# Indentificadores de sensor
sensores = bus.ids()
si, se, ssi, sse = sensores
hci = 7.69
while True:
    leitura = bus.read()
    if leitura is None:
        continue
    temperaturas = [leitura[s] for s in sensores]
    ti, te, tsi, tse = temperaturas
    
#    ti, te, tsi, tse = 21.2, 22.4, 25.1, 20.3
    
    transmitancia = hci*(ti-tsi) / (ti-te)
    
    params = urllib.urlencode({'field1': ti, 'field2': te, 'field3': tsi, \
                               'field4': tse, 'field5': transmitancia, \
                               'key': '6NZS0EBQ7X3MZX6L'})
#    params = urllib.urlencode({'field5': transmitancia, \
#                               'key': '6NZS0EBQ7X3MZX6L'})
                              
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    conn = httplib.HTTPConnection('api.thingspeak.com:80')
    conn.request('POST', '/update', params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    time.sleep(1)
    










#temperatura = read_temp()
#params = urllib.urlencode({'field1': temperatura, 'key':'Pon_aquí_tu_key'})
#headers = {"Content-type": "application/x-www-form-urlencoded","Accept":
#        "text/plain"}
#conn = httplib.HTTPConnection("api.thingspeak.com:80")
#conn.request("POST", "/update", params, headers)
#response = conn.getresponse()
#print response.status, response.reason
#data = response.read()
#conn.close()


