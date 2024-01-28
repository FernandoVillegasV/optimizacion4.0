import registrar
import enviar
import network
import time
import datos_conexion
from mfrc522 import MFRC522
from machine import RTC

#Conexion a WiFi
print("Conectando", end="")
estado = network.WLAN(network.STA_IF)
estado.active(True)
estado.connect(datos_conexion.nombre_red, datos_conexion.password)
while not estado.isconnected():
  print(".", end="")
  time.sleep(0.5)
print(" Conexión disponible")

#Codigo del lector
lector = MFRC522(sck=18, miso=19, mosi=23, cs=5, rst=2)
print("Lector activo...\n")

while True:
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            print("Código del Tag: "+str(identificador))
            registrar.registrarDatos(identificador)
            time.sleep(2)