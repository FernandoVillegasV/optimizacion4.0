<?php
include ("conexion.php");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$json = file_get_contents('php://input');
$data = json_decode($json);
$dato1 = $data->usuario;
$dato2 = $data->generados;
$dato3 = $data->fecha;

$insertar = $conexion -> prepare("INSERT INTO frecuencia (cedula, formatos_generados, fecha) VALUES (?,?,?)");
$insertar -> bindParam(1, $dato1);
$insertar -> bindParam(2, $dato2);
$insertar -> bindParam(3, $dato3);
$insertar -> execute();

$actualizar = $conexion -> prepare("UPDATE usuario SET formatos = formatos + ? WHERE cedula = ?");
$actualizar -> bindParam(1, $dato2);
$actualizar -> bindParam(2, $dato1);
$actualizar -> execute();

?>