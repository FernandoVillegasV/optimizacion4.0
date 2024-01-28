import os
import json
import individual
import masivo
import datos_conexion
import time
import requests   # Para realizar las peticiones HTTP - Post o Get
from datetime import datetime
#Se debe instalar el servicio pip install pywhatkit para enviar mensajes vía WhatsApp
import shutil   # Modulo empleado para comprimir un archivo o carpeta
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

while True:
  #Login funcional ----------------------------------------------------------------------
  ahora = datetime.now()
  fecha = ahora.strftime('%Y-%m-%d %H:%M')
  token = input("Digite su TOKEN de acceso:")

  while True:
    try:
      url = "https://unjealous-doorknob.000webhostapp.com/login.php"
      data = {
        "token": token,
        "fecha": fecha
      }
      headers = {'Content-Type': 'application/json'}
      respuesta = requests.post(url, json=data, headers=headers)
      respuesta = respuesta.content
      if len(respuesta) > 3:
        # Los datos devueltos son inaccesibles, se convierten de ASCII a formato legible
        datos_lista_json = respuesta.decode('utf-8')
        # Se carga el JSON como un diccionario de Python
        diccionario = json.loads(datos_lista_json)
      else:
        respuesta = str(respuesta)
      break
    except:
      print("Se esta intentando conectar con el servidor, espere por favor...")
      time.sleep(4)

  try:
    if "A" in respuesta:
      print("El token no existe, verifique su correo electrónico registrado o solicite uno de nuevo")
    elif "B" in respuesta:
      print("El número de formatos generados excede la licencia, comuniquese con el Administrador")
  except:
    while True:
      opcion = input("""Seleccione la labor a realizar:
          1 - Generación de formato INDIVIDUAL - Llamado de atención y plan de mejoramiento
          2 - Generación de formatos MASIVOS
          """)
      if opcion == "1":
        retorno = individual.llamado_atencion(diccionario, fecha)
        break
      elif opcion == "2":
        formato = input("""Seleccione el tipo de formato a generar:
            1 - Trabajo concertado
            2 - Llamado de atención y plan de mejoramiento
            """)
        if formato == "1":
          retorno = masivo.plan_trabajo(diccionario, fecha)
          break
        elif formato == "2":
          masivo.llamado_atencion()
          break
      else:
        print("Opción no existe, verifique sus datos")
        
    # Comprime la carpeta de todos los archivos para enviar al instructor
    ruta_carpeta = 'downloads'  
    ruta_destino_comprimido = ruta_carpeta
    # Se genera el nuevo archivo comprimido
    if retorno[4]=="1":
      shutil.make_archive(os.path.join(ruta_destino_comprimido, 'Documentos_'+retorno[3]), 'zip', ruta_carpeta, 'Documentos_'+retorno[3])
    else:
      shutil.make_archive(os.path.join(ruta_destino_comprimido, 'Plan_Trabajo_'+retorno[3]), 'zip', ruta_carpeta, 'Plan_Trabajo_'+retorno[3])

    # Envío del archivo comprimido al instructor      
    while True:
      try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Formatos generados - Debido proceso"
        message["From"] = datos_conexion.email_address
        message["To"] = diccionario[0]["correo"] 
        text = '''
               Adjunto los formatos generados para su conocimiento y cumplimiento
               '''
        html = '''
               <html>
               <body>
               <h1>FORMATOS GENERADOS - DEBIDO PROCESO</h1>
               <p>Instructor, cordial saludo, se adjunta el archivo comprimido con los documentos generados.</p>
               <p>No siendo más el motivo,</p>
               <p>Atentamente:<br>
               <strong>A</strong>GILIDAD <strong>R</strong>EPETITIVA
               </p>
               </body>
               </html>
               '''
        text_mime = MIMEText(text, 'plain')
        html_mime = MIMEText(html, 'html')
        
        # Adjuntar archivo al mensaje
        if retorno[4]=="1":
          archivo_adjunto = 'downloads/Documentos_'+retorno[3]+'.zip'
        else:
          archivo_adjunto = 'downloads/Plan_Trabajo_'+retorno[3]+'.zip'

        with open(archivo_adjunto, 'rb') as archivo:
          archivo_mime = MIMEBase('application', 'octet-stream')
          archivo_mime.set_payload(archivo.read())
        encoders.encode_base64(archivo_mime)
        archivo_mime.add_header('Content-Disposition', f'attachment; filename= {archivo_adjunto}')

        message.attach(archivo_mime)
        message.attach(text_mime)
        message.attach(html_mime)
               
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(datos_conexion.smtp_address, datos_conexion.smtp_port, context=context) as server:
          server.login(datos_conexion.email_address, datos_conexion.email_password)
          server.sendmail(datos_conexion.email_address, message["To"], message.as_string())
        break
      except:
        print("No fue enviado el archivo al instructor, espere un momento, intentando de nuevo...") 
        time.sleep(3)                   

'''
    # ENVIO DE MENSAJES Y ARCHIVOS VÍA WHATSAPP - FUNCIONAL -----------------------------------------------
    # Obtener la hora y minutos actuales
    hora_actual = int(datetime.now().hour)
    minutos_actuales = int(datetime.now().minute)+1
    # Ruta de la carpeta comprimida
    ruta = 'FormatosGenerados_'+retorno[3]+'.zip'
    # Envío WhatsApp - Exige 4 parámetros, teléfono, contenido, hora y minuto de envío
    pywhatkit.sendwhatmsg("+57"+retorno[0], "Agilidad Repetitiva - Formatos generados", hora_actual, minutos_actuales)   
    # Esperar unos segundos para que WhatsApp Web se cargue completamente
    time.sleep(2)
    # Hacer clic en el icono de adjuntar archivo
    pyautogui.click(x=448, y=694)  # (Coordenadas x, y del icono en tu pantalla)
    time.sleep(1)
    pyautogui.click(x=516, y=433)  # (Coordenadas x, y del icono en tu pantalla)
    time.sleep(1)
    pyautogui.write(ruta)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.click(x=1326, y=692)  # (Coordenadas x, y del botón de enviar)    
    print("Proceso finalizado")
'''
