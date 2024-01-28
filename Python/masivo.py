import time
import openpyxl   # Para poder leer y modificar el archivo Excel
import pdf
import os
import requests   # Para realizar las peticiones HTTP - Post o Get
from datetime import datetime
from openpyxl.drawing.image import Image  # Para insertar una imagen al archivo Excel

def plan_trabajo(datos, fecha_frecuencia):
      # Fecha para nombrar carpetas y archivos generados
      fecha = datetime.now()
      months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
      month = months[fecha.month - 1]
      fecha_completa = "{} de {} de {}".format(fecha.day, month, fecha.year)
    
      try:
            carpeta = "downloads/Plan_Trabajo_"+fecha_completa 
            os.mkdir(carpeta)
      except:
            print("Carpeta ya existe")
      
      print("NO OLVIDE, los datos para generar el plan de trabajo concertado, provienen del archivo 4_base_de_datos, cargue los datos primero allí...")
      res = input("¿Desea enviar vía correo electrónico el formato al APRENDIZ? Si / No")
      if res=="SI" or res=="Si" or res=="si" or res=="sI" or res=="s" or res=="S":
            res = "s"            
      
      archivo_excel = "downloads/formatos/4_base_de_datos.xlsx"
      workbook = openpyxl.load_workbook(archivo_excel)
      # Selecciona la hoja de trabajo
      hoja = workbook.active
      
      # Toma los valores del archivo BD de Excel      
      programa = hoja["C3"].value
      ficha = hoja["C4"].value
      guia = hoja["C5"].value
      fecha = hoja["C6"].value
      actividades = []  # Lista que almacena las actividades señaladas
      actividades.append(hoja["C7"].value)
      if hoja["C8"].value:
            actividades.append(hoja['C8'].value)
      if hoja["C9"].value:
            actividades.append(hoja['C9'].value)
      if hoja["C10"].value:
            actividades.append(hoja['C10'].value)
      if hoja["C11"].value:
            actividades.append(hoja['C11'].value)
      if hoja["C12"].value:
            actividades.append(hoja['C12'].value)
      if hoja["C13"].value:
            actividades.append(hoja['C13'].value)

      # Lectura del archivo - Datos masivos por aprendiz
      matriz = []
      diccionario = {}
      cont = 16         # Fila de inicio en el archivo Excel
      while True:       
            if hoja['B'+str(cont)].value is not None:
                  diccionario = {"nombres":hoja['B'+str(cont)].value, "apellidos":hoja['C'+str(cont)].value, "correo":hoja['D'+str(cont)].value}
                  matriz.append(diccionario)      
                  cont+=1
            else:
                  break
      
      while True:
            try:
                  url = "https://unjealous-doorknob.000webhostapp.com/actualizar.php"
                  data = {
                        "usuario": datos[0]['cedula'],
                        "generados": str(len(matriz)),
                        "fecha": fecha_frecuencia
                  }
                  headers = {'Content-Type': 'application/json'}
                  requests.post(url, json=data, headers=headers)
                  break
            except:
                  print("Conectando con el servidor, un momento por favor...")
                  time.sleep(3)
    
      j = 0
      while j < len(matriz):
            # Modifica el Excel de salida
            archivo_excel = "downloads/formatos/3_formato_plan_trabajo_concertado.xlsx"
            workbook = openpyxl.load_workbook(archivo_excel)
            # Selecciona la hoja de trabajo
            hoja = workbook.active
            # Modifica las celdas según sea necesario para el PLAN DE MEJORAMIENTO
            hoja['C6'] = programa
            hoja['C8'] = ficha
            hoja['C10'] = datos[0]['nombre']
            hoja['C12'] = guia
            hoja['G12'] = fecha_completa
            fila = matriz[j]
            hoja['A17'] = fila["nombres"] +" "+ fila["apellidos"]
            # Adiciona las N actividades al formato
            i = 0
            while i < len(actividades):
                  hoja['C'+str(i+17)] = actividades[i]
                  hoja['F'+str(i+17)] = "X"
                  hoja['G'+str(i+17)] = fecha
                  i+=1
      
            # Logo de los formatos
            imagen1 = "downloads/formatos/logo.png"
            celda_destino = "A1"
            img1 = Image(imagen1)
            hoja.add_image(img1, celda_destino)

            # Guarda los cambios en el nuevo archivo, en la nueva carpeta
            nuevoarchivo = "downloads/Plan_Trabajo_"+fecha_completa+"/"+fila["apellidos"]+" "+fila["nombres"]+"_plan_trabajo_concertado"+"_"+guia
            extension = ".xlsx"
            workbook.save(nuevoarchivo+extension)
            correo_Aprendiz = fila["correo"]
            # Llama la función para convertir el llamado de atención a PDF
            
            pdf.convertirpdf(nuevoarchivo, res, correo_Aprendiz)
            j+=1
      valores = [str(datos[0]['telefono']), correo_Aprendiz, nuevoarchivo, fecha_completa, "2"]
      return valores