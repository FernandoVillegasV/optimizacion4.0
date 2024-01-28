# Se requiere instalar el módulo pip install pywin32
from win32com.client import Dispatch  # Para generar el archivo PDF
import os
import time
# Modulos empleados para envio del correo electrónico
import smtplib, ssl
import datos_conexion
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def convertirpdf(archivo, res, correo_Aprendiz = "1"):
    in_file = os.path.abspath(archivo+'.xlsx')
    out_file = os.path.abspath(archivo+'.pdf')
    excel = Dispatch("Excel.Application")
    excel.Visible = False  # Puede establecer esto en True para ver la aplicación Excel durante la conversión
    workbook = excel.Workbooks.Open(in_file)
    workbook.ExportAsFixedFormat(0, out_file, 1, 0)
    workbook.Close()
    excel.Quit()
    
    # Envio del formato diligenciado PDF al aprendiz
    if res=="s":
        while True:
            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = "DEBIDO PROCESO SENA - DOCUMENTACIÓN"
                message["From"] = datos_conexion.email_address
                message["To"] = correo_Aprendiz
                text = '''
                Adjunto los formatos generados para su conocimiento y cumplimiento
                '''
                html = '''
                <html>
                <body>
                <h1>DEBIDO PROCESO SENA - DOCUMENTACIÓN IMPORTANTE</h1>
                <p>Aprendiz, cordial saludo, ante el incumplimiento registrado, adjunto encontrará el llamado de atención y plan de mejoramiento a cumplir para evitar dar continuidad al debido proceso.</p>
                <p>No siendo más el motivo y esperando cumplimiento a la actividad asignada,</p>
                <p>Atentamente:<br>
                Instructor asignado
                </p>
                </body>
                </html>
                '''
                text_mime = MIMEText(text, 'plain')
                html_mime = MIMEText(html, 'html')
                
                # Adjuntar archivo al mensaje
                archivo_adjunto = archivo+'.pdf'
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
                print("No fue enviado el formato, espere un momento, intentando de nuevo...") 
                time.sleep(3)                   
