import pdf
import time
import requests   # Para realizar las peticiones HTTP - Post o Get
# Se debe instalar el servicio para formato de la hoja pip install openpyxl
import openpyxl   # Para poder leer y modificar el archivo Excel
import os
from openpyxl.drawing.image import Image  # Para insertar una imagen al archivo Excel
from datetime import datetime

def llamado_atencion(datos, fecha_frecuencia): 
    fecha = datetime.now()
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    month = months[fecha.month - 1]
    fecha_completa = "{} de {} de {}".format(fecha.day, month, fecha.year)
    
    #Se define una lista que almacenará todos los datos de entrada
    lis = []     
    #Entrada de datos
    programa = input("""Seleccione el nombre del PROGRAMA de formación:
                 1 - Técnico en programación de SOFTWARE
                 2 - Técnico en programación de aplicaciones y servicios para la NUBE
                 3 - Técnico en programación de aplicaciones para dispositivos MOVILES
                 """)
    if programa == "1":
      lis.append("Técnico en programación de Software")
    elif programa == "2":
      lis.append("Técnico en programación de aplicaciones y servicios para la nube")
    else:
      lis.append("Técnico en programación de aplicaciones para dispositivos móviles")

    # 1
    lis.append(input("Digite el número de la FICHA:"))  
    lis.append(input("Digite el NOMBRE del aprendiz:"))
    # 3
    lis.append(input("Digite los APELLIDOS del aprendiz:"))  
    lis.append(input("Digite el número de DOCUMENTO del aprendiz:"))
    # 5
    lis.append(input("Digite el CORREO electrónico del aprendiz:")) 
    lis.append(input("Digite el MOTIVO del llamado de atención:"))
    # 7
    lis.append(input("Digite a partir del REGLAMENTO del aprendiz, los artículos infringidos:"))
    lis.append(input("Digite la FASE del proyecto para el plan de mejoramiento:"))
    #9
    lis.append(input("Digite el nombre del PROYECTO formativo para el plan de mejoramiento:"))
    lis.append(input("Digite la ACTIVIDAD del proyecto para el plan de mejoramiento:"))
    #11
    lis.append(input("Digite el RESULTADO DE APRENDIZAJE para el plan de mejoramiento:"))
    lis.append(input("Digite la FECHA DE ENTREGA para el plan de mejoramiento:"))
    #13
    lis.append(input("Digite la HORA DE ENTREGA para el plan de mejoramiento:"))
    lis.append(input("Digite el LUGAR DE ENTREGA para el plan de mejoramiento:"))
    #15
    lis.append(input("Digite la primera ACTIVIDAD a entregar para el plan de mejoramiento:"))
    lis.append(input("Digite la segunda ACTIVIDAD a entregar para el plan de mejoramiento (Opcional):"))
    #17
    lis.append(input("Digite la tercera ACTIVIDAD a entregar para el plan de mejoramiento (Opcional):"))
    lis.append(input("Digite el nombre del INVITADO para adicionar al plan de mejoramiento (Opcional):"))
    #19
    lis.append(input("Digite el CARGO del invitado para adicionar al plan de mejoramiento (Opcional):"))
    lis.append(input("Digite la ENTIDAD que representa el invitado para adicionar al plan de mejoramiento (Opcional):"))
    #21
    lis.append(input("Digite el CORREO del invitado para adicionar al plan de mejoramiento (Opcional):"))
    lis.append(input("Digite el nombre del REPRESENTANTE de la ficha:"))
    lis.append(input("Digite el DOCUMENTO del representante de la ficha:"))
    
    # Flujo de archivos STREAM, modo lectura, escritura y actualización 
    archivo_excel = "downloads/formatos/1_formato_llamado_atencion.xlsx"
    workbook = openpyxl.load_workbook(archivo_excel)
    # Selecciona la hoja de trabajo
    hoja = workbook.active
    
    # Modifica las celdas según sea necesario para el LLAMADO DE ATENCIÓN
    hoja['C5'] = "Bogotá D.C., "+fecha_completa
    hoja['C6'] = lis[2]+" "+lis[3]
    hoja['C7'] = lis[0]
    hoja['C8'] = lis[1]
    hoja['C10'] = lis[6]
    hoja['C13'] = lis[7]
    hoja['B18'] = datos[0]['nombre']
    hoja['B19'] = "Documento: "+str(datos[0]['cedula'])
    hoja['D18'] = lis[2]+" "+lis[3]
    hoja['D19'] = "Documento: "+lis[4]    
    hoja['B22'] = lis[22]
    hoja['B23'] = "Documento: "+lis[23]
    hoja['C25'] = fecha_completa+" - "+lis[3]+" "+lis[2]

    # Logo de los formatos
    imagen1 = "downloads/formatos/logo.png"
    celda_destino = "B2"
    img1 = Image(imagen1)
    hoja.add_image(img1, celda_destino)
    
    # Firma del instructor
    imagen2 = "downloads/formatos/instructor.png"
    celda_destino = "B16"
    img2 = Image(imagen2)
    hoja.add_image(img2, celda_destino)
    
    # Firma del representante
    imagen3 = "downloads/formatos/representante.png"
    celda_destino = "B20"
    img3 = Image(imagen3)
    hoja.add_image(img3, celda_destino)
    
    # Crea la carpeta destino de los nuevos archivos
    try:
      carpeta = "downloads/Documentos_"+fecha_completa 
      os.mkdir(carpeta)
    except:
      print("Carpeta ya existe")
    
    res = input("¿Desea enviar vía correo electrónico el formato al APRENDIZ? Si / No")
    if res=="SI" or res=="Si" or res=="si" or res=="sI" or res=="s" or res=="S":
      res = "s" 
    
    while True:
      try:
        url = "https://unjealous-doorknob.000webhostapp.com/actualizar.php"
        data = {
          "usuario": datos[0]['cedula'],
          "generados": "2",
          "fecha": fecha_frecuencia
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, json=data, headers=headers)
        break
      except:
        print("Conectando con el servidor, un momento por favor...")
        time.sleep(3)
      
    # Guarda los cambios en el nuevo archivo, en la nueva carpeta
    nuevoarchivo = "downloads/Documentos_"+fecha_completa+"/"+lis[3]+" "+lis[2]+"_"+"llamado_atencion"+"_"+fecha_completa
    extension = ".xlsx"
    workbook.save(nuevoarchivo+extension)
    # Llama la función para convertir el llamado de atención a PDF
    pdf.convertirpdf(nuevoarchivo, res, lis[5])
     
    archivo_excel = "downloads/formatos/2_formato_plan_mejoramiento.xlsx"
    workbook = openpyxl.load_workbook(archivo_excel)
    # Selecciona la hoja de trabajo
    hoja = workbook.active
    
    # Modifica las celdas según sea necesario para el PLAN DE MEJORAMIENTO
    hoja['B5'] = "Bogotá D.C., "+fecha_completa
    hora_actual = int(datetime.now().hour)
    minutos_actuales = int(datetime.now().minute)
    hoja['D5'] = str(hora_actual)+":"+str(minutos_actuales)
    nueva_hora = hora_actual+1
    hoja['E5'] = str(nueva_hora)+":"+str(minutos_actuales)
    hoja['B7'] = lis[14]
    hoja['B9'] = "Documento: "+lis[4]+" - "+lis[2]+" "+lis[3]
    hoja['B13'] = lis[7]
    hoja['B15'] = lis[6]
    hoja['B16'] = "Junto con el (la) vocero y/o suplente de los aprendices como testigo, de la ficha de caracterización número "+lis[1]+" del programa de formación "+lis[0]+", asociada al proyecto formativo "+lis[9]+", que en este momento se encuentra en la fase de "+lis[8]+", en la actividad de proyecto "+lis[10]+", los conocimientos, habilidades y destrezas pertinentes a las competencias del programa de formación asumiendo estrategias y metodologías de autogestión, teniendo en cuenta las especificaciones funcionales del sistema y el resultado de aprendizaje "+lis[11]+" para la revisión de la propuesta de proyecto formativo."

    hoja['B39'] = lis[18]
    hoja['D39'] = lis[19]
    hoja['E39'] = lis[20]

    hoja['B20'] = datos[0]['nombre']
    hoja['D20'] = lis[12]+" "+lis[13]
    hoja['E20'] = lis[14]
    if lis[15]:
      hoja['B29'] = lis[15]
      hoja['D29'] = "Aprendiz"
      hoja['E29'] = lis[12]
    if lis[16]:
      hoja['B30'] = lis[16]
      hoja['D30'] = "Aprendiz"
      hoja['E30'] = lis[12]
    if lis[17]:
      hoja['B31'] = lis[17]
      hoja['D31'] = "Aprendiz"
      hoja['E31'] = lis[12]
    hoja['B34'] = lis[2]+" "+lis[3]
    hoja['B35'] = lis[22]
    hoja['B36'] = datos[0]['nombre']
     
    # Logo de los formatos
    imagen1 = "downloads/formatos/logo.png"
    celda_destino = "B2"
    img1 = Image(imagen1)
    hoja.add_image(img1, celda_destino)
    
    # Guarda los cambios en el nuevo archivo, en la nueva carpeta
    nuevoarchivo = "downloads/Documentos_"+fecha_completa+"/"+lis[3]+" "+lis[2]+"_"+"plan_mejoramiento"+"_"+fecha_completa
    extension = ".xlsx"
    workbook.save(nuevoarchivo+extension)
    # Llama la función para convertir el plan de majoramiento pdf 
            
    pdf.convertirpdf(nuevoarchivo, res, lis[5])
    valores = [str(datos[0]['telefono']), lis[5], nuevoarchivo, fecha_completa, "1"]
    return valores