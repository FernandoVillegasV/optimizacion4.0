<?php

$GLOBALS["conexion"] = new PDO('mysql:host=localhost; dbname=Nombre_De_Su_Base_De_Datos', 'Usuario_De_Su_Base_De_Datos', 'Password_De_Su_Base_De_Datos');
$GLOBALS["conexion"] -> exec("set names utf8");

?>
