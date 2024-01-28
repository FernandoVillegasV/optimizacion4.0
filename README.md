# optimizacion4.0
OPTIMIZACIÓN 4.0: Sistematización de formatos para agilizar la gestión documental a cargo de instructores - Sistema que permite integrar un módulo RFID de acceso e identificación de usuarios, bajo programación Python con comunicación a una base de datos MySQL gratuita empleando peticiones HTTP POST por medio de PHP - Servicio de Hosting 000webhost.

FUNCIONALIDAD: Optimización 4.0 es la primera versión de un sistema que permite la autenticación e identificación de usuarios por medio de un lector RFID, tras el acceso satisfactorio, el usuario podrá ágilmente diligenciar formatos de forma individual o masiva, se debe contar con un formato origen con extensión .xlsx, empleando este archivo origen, se asignan los datos de entrada a un archivo .xlsx de salida, este se exporta a formato .pdf y es enviado de forma desatendida al correo electrónico establecido, al usuario le es enviado un correo electrónico con los archivos generados en formato .zip.

1.	El mecanismo de autenticación e identificación de usuarios se realizará por medio de un módulo lector RFID – RC522 y el procesamiento de datos por medio de un chip ESP32.

2.	Adquisición de un servicio de Hosting – Hostinger: https://co.000webhost.com/

3.	Diseño de una base de datos empleando el SGBD MySQL.

4.	Base de datos: Carga de perfiles, datos por usuario y seguimiento de formatos generados.

5.	Generación de Token por usuario y acceso, comunicación del mismo al usuario vía correo electrónico.

6.	Validación de Token y acceso al sistema.

7.	Selección del formato a generar y lectura de los datos de entrada necesarios; individuales ingresados por el instructor, o masivos importados desde un archivo Excel.

8.	Carga de datos de entrada a archivo genérico en formato Excel. 

9.	Generación del documento diligenciado en formato .pdf.

10.	Envío empleando correo electrónico de los documentos generados, formato individual a cada aprendiz y un archivo comprimido al instructor encargado.

OBJETIVO: Sistematizar el conjunto de formatos para el seguimiento de los debidos procesos de aprendices que facilite la gestión documental de los instructores del Servicio Nacional de Aprendizaje empleando el lenguaje de programación Python. 

RECURSOS DEL REPOSITORIO:

FOLDER BASE DE DATOS: Dispone de un archivo en formato pdf, describe las tres tablas propuestas para la ejecución del sistema, descripción por tabla:

Tabla Frecuencia: Registra el número de formatos generados por usuario.

Tabla Log: Registra los datos de cada Token generado conjuntamente con las fechas de seguimiento.

Tabla Usuario: Registra los datos del usuario con acceso autorizado. 

El diccionario de datos define los datos y tipos de dato por tabla.

FOLDER FORMATOS: Dispone del conjunto de formatos con extensión .xlsx - Excel, a partir de estos se generan los documentos diligenciados a ser enviados a cada correo electrónico proporcionado. Es el usuario el que decide qué tipo de formato diligenciar, tenga en cuenta, cualquier formato puede ser automatizado si modifica la fuente de entrada de datos. Los formatos propuestos son:

1_formato_llamado_atencion.xlsx

2_formato_plan_mejoramiento.xlsx

3_formato_plan_trabajo_concertado.xlsx

4_base_de_datos-xlsx

instructor.png

logo.png

representante.png

Las imágenes en formato png se adicionan al archivo Excel antes de exportarlo a pdf.

FOLDER MICROPYTHON: Dispone de todos los módulos y componentes que permiten la comunicación entre el chip RFID-RC522, el microcontrolador ESP-32 de 30 pines y la implementación MicroPython, permite la conexión a una red Wi-Fi, lectura de Tag de radio frecuencia de 13.54 MHz, generar y registrar un Token en una base de datos MySQL proporcionada por el servicio de Hosting 000webhost, enviar un correo electrónico de notificación empleando SMTP. Archivos: 

lib/umail.py		

datos_conexion.py

enviar.py

leer_tag.py

mfrc522.py

registrar.py 

Archivo principal de ejecución: leer_tag.py puede posteriormente modificar su nombre por main.py para la ejecución de la aplicación sin necesidad de la máquina y del uso del IDE Thonny.

FOLDER PHP: Dispone de los archivos que permiten la interacción con la base de datos, al emplear un servicio de Hosting gratuito, no permite la conexión remota, por lo anterior, se definen archivos PHP que a partir de datos de entrada en formato JSON, ejecutan peticiones HTTP POST en una base de datos relacional MySQL. Archivos:

actualizar.php

conexion.php

insertar_tras_consulta.php

login.php

Estos deben ser alojados en el administrador de archivos del servicio de Hosting.

FOLDER PYTHON: Dispone de los archivos que representan la lógica del sistema, permite la comunicación de datos a los archivos .php, carga los datos de entrada para generar el documento de salida de un archivo Excel, genera un archivo de salida en formato Excel con los datos de entrada, finalmente, convierte el archivo de salida a formato pdf y envía el mismo vía correo electrónico, al usuario le envía un correo electrónico con los formatos generados en archivo comprimido .zip. Archivos:

datos_conexion.py

individual.py

masivo.py

pdf.py

principal.py

Archivo principal de ejecución: principal.py se comporta como el archivo Login o Index del sistema.
