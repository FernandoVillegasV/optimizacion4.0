import network
import urequests
import datos_conexion
from umail import SMTP
        
#Funcion para envío del correo electrónico
def enviarCorreo(correo, aleatorio):
    while True:
        try:
            mensaje = SMTP(host='smtp.gmail.com', port=465, ssl=True, username = datos_conexion.usuario_correo, password = datos_conexion.password_correo)
            mensaje.to(correo)
            asunto = "Envio de token de acceso - AGILIDAD REPETITIVA"
            mensaje.write("Subject:" + asunto + "\n")
            mensaje.write ("\n Gracias por utilizar nuestro servicio, su token de ingreso es:")
            mensaje.write ("\n TOKEN: ")
            mensaje.write (str(aleatorio))
            mensaje.write ("\n\n AGILIDAD REPETITIVA - Más que un documento")
            mensaje.send ()
            mensaje.quit()
            print("Mensaje enviado con éxito, Token",aleatorio, "al correo",correo)
            break
        except:
            print("Error en el envio del Token, se volverá a intentar")