#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

"""
A libreria RPi.GPIO non le o bus 1-wire ao que están conectadas as DS18b20,
polo que haberá que acceder directamente ao bus coas ferramentas do sistema.

Previo á utilización do bus 1-wire hai que activalo engadindo ao arquivo 
/boot/config.txt a liña: dtoverlay=w1-gpio

Aparecerá un directorio /sys/bus/w1 os dispositivos conectados ao bus están en
/sys/bus/w1/devices/xx-xxxxxxxxxxxx sendo x díxitos hexadecimais. No caso de
non haber dispositivos conectados aparecerán directorios temporais con nomes 
00-0x0000000000 que desaparecerán para daren paso a outros similares. Existe un
directorio adicional: /sys/bus/w1/devices/w1_bus_master1 onde está a información
relativa ao bus.

Para lermos a temperatura debemos consultar o arquivo w1_slave na ruta 
/sys/bus/w1/devices/xx-xxxxxxxxxxxx relativa a cada dispositivo. No arquivo
w1_slave aparecen dúas liñas que empezan con nove parellas de díxitos hexadecimais
e ao final de cada unha delas: (1) código crc e YES ou NO indicando recepción
correcta do dato, e (2) temperatura como valor enteiro en milésimas de ºC. 

No bus cada sensor queda identificado por un código hexadecimal. O problema que
atopo é que non é posible distinguir cal deles é un sensor determinado. Así
cando sexa de poñer os sensores externos (p.ex) non será fácil decidir cal é
o que mide temperatura ambiente e cales temperatura superficial.
"""

class DS18b20:
    """
    Encapsula o acceso ao bus 1-Wire e a lectura dos sensores de temperatura
    DS18b20 que estean conectados.
    
    A clase proporciona un diccionario coas temperaturas en ºC indexadas por 
    identificador de sensor no bus. Pódense obter os identificadores e as 
    temperaturas por separado (non necesariamente na mesma orde). A clase fai
    unha consulta á última temperatura dispoñible no bus cada vez que se 
    chama a read() ou a temperatures().
    
    Se o crc dalgún dos sensores non fora correcto a clase desbota a leitura
    dos outros sensores e devolve None.
    
    Lánzase unha excepción UserWarning() no caso de non haber sensores conectados
    ao bus ou fallar a leitura do sensor (non se lanza cando o crc é incorrecto).
    """
    
    def __init__(self):
        self.sensors = self.__sensors__()
            
    def __sensors__(self):
        base_dir = '/sys/bus/w1/devices/'
        directorios = os.listdir(base_dir)
        if len(directorios) == 1 and directorios[0] == 'w1_bus_master1':
            raise UserWarning('Non hai sensores conectados')
        sensores = {}
        for d in directorios:
            if re.match('[0-9A-Fa-f]{2}-[0-9A-Fa-f]+', d): # Entradas xx-xxxxx con x Hex
                if re.match('00-[0-9A-Fa-f]+', d):
                    raise UserWarning('Non hai sensores conectados')
                ruta = base_dir + d + '/w1_slave'
                sensores[d] = ruta
        return sensores
        
    def read(self):
        temperaturas = {}
        for sensor in self.sensors:
            ruta = self.sensors[sensor]
            f = open(ruta, 'r')
            texto = f.read()
            f.close()
            if not 'YES' in texto:
                return None
            m = re.match('.*\n.*t=(?P<temp>[0-9]{5}).*', texto)
            if not m:
                raise UserWarning('Non se atopa a temperatura do sensor ' + sensor)
            temperaturas[sensor] = float(m.group('temp'))/1000      # Temperatura en ºC
        return temperaturas
        
    def ids(self):
        return list(self.sensors.keys())
        
    def temperatures(self):
        return list(self.read().values())
            
            


       