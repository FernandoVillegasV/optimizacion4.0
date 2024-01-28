<?php

include ("conexion.php");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$json = file_get_contents('php://input');
$data = json_decode($json);
$dato1 = $data->pin;
$dato2 = $data->token;
$dato3 = $data->fecha;

$consulta = $conexion -> prepare("SELECT correo FROM usuario WHERE pin = ?");
$consulta->bindparam(1, $dato1);
$consulta -> execute();
$respuesta = $consulta->fetchAll(PDO::FETCH_ASSOC);

if(empty($respuesta[0]["correo"])){
    echo json_encode("Tag no existe");
}
else{
    $insertar = $conexion -> prepare("INSERT INTO log (pin, token, generado) VALUES (?,?,?)");
    $insertar->bindparam(1, $dato1);
    $insertar->bindparam(2, $dato2);
    $insertar->bindparam(3, $dato3);
    $insertar -> execute();
    $correo = $respuesta[0]["correo"];
    echo json_encode($correo);
}

?>