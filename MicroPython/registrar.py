import enviar
import time
import random
import urequests
import datos_conexion
from machine import RTC, Pin

rojo = Pin(22, Pin.OUT)
verde = Pin(21, Pin.OUT)

#Funcion para insertar datos en la BD MySQL
def registrarDatos(identificador):
    
    #Generación del Token de posterior acceso
    aleatorio = random.randrange(10000, 99999)
                    
    #Permite definir la fecha y hora actual en formato definido
    (year, month, day, weekday, hour, minute, second, milisecond) = RTC().datetime()                
    RTC().init((year, month, day, weekday, hour, minute, second, milisecond))
    fecha = "{:02d}-{:02d}-{} {:02d}:{:02d}".format(RTC().datetime()[2], RTC().datetime()[1], RTC().datetime()[0], RTC().datetime()[4], RTC().datetime()[5])
        
    #Empleando una petición HTTP, se comunican los datos a la base de datos
    correcto = 0
    while correcto == 0:
        try:
            url = "https://unjealous-doorknob.000webhostapp.com/insertar_tras_consulta.php"
            data = {
                "pin": identificador,
                "token": aleatorio,
                "fecha": fecha
            }
            headers = {'Content-Type': 'application/json'}
            response = urequests.post(url, json=data, headers=headers)
            correo = str(response.content)
            correcto = 1
        except:
            print("Error de conexión a la BD, se vuelve a intentar")
            correcto = 0
    
    if "Tag no existe" not in correo:
        #Activa el led RGB color verde, usuario existe
        verde.value(1)
        rojo.value(0)    
        #Elimina caracteres adicionales a la cadena de correo electrónico para compartir el Token
        correo = list(str(response.content))
        del correo[-1]
        del correo[-1]
        del correo[0]
        del correo[0]
        del correo[0]
        cadenaCorreo = ''.join(correo)
        enviar.enviarCorreo(cadenaCorreo,aleatorio)
    else:
        print("Pin no se encuentra registrado, comuniquese con soporte técnico")
        #Activa el led RGB color rojo, usuario no existe
        verde.value(0)
        rojo.value(1) 
    
'''
#PARPADEO    
    tiempoLimite_02 = time.ticks_add(time.ticks_ms(), 100) # definimos la variable tiempoLimite_02 para el LED 02
                                                       # y establecemos su valor (tiempo actual+200 ms)
            while True:
                if time.ticks_diff(tiempoLimite_02, time.ticks_ms()) <= 0: #comprobamos si el tiempoLimite_02 se ha agotado
                    if rojo.value() == 1:        # si el tº se ha agotado y el LED 02 está encendido...                            
                        rojo.off()               # ... lo apagamos
                    else:                          # si el tº se ha agotado y el LED 02 no está encendido...
                        rojo.on()                # ...lo encendemos
                    tiempoLimite_02 = time.ticks_add(time.ticks_ms(), 100) #nuevo tiempoLimite_02 (tiempo actual+200 ms)
'''