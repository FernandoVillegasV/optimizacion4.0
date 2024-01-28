<?php
include ("conexion.php");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$json = file_get_contents('php://input');
$data = json_decode($json);
$dato1 = $data->token;
$dato2 = $data->fecha;

//Subconsulta, valida que el Token exista y su estado sea 1, además, que el número de formatos sea menor a 1000
$consulta = $conexion -> prepare("SELECT formatos,nombre,telefono,cedula,correo FROM usuario WHERE pin = (SELECT pin FROM log WHERE estado = 1 AND token = ?)");
$consulta -> bindparam(1, $dato1);
$consulta -> execute();
$respuesta = $consulta->fetchAll(PDO::FETCH_ASSOC);

if(empty($respuesta[0]["formatos"])){
    echo json_encode("A");
}
else if($respuesta[0]["formatos"]>1000){
    echo json_encode("B");
}
else{
    $actualizar = $conexion -> prepare("UPDATE log SET estado = 0, usado = ? WHERE token = ?");
    $actualizar -> bindParam(1, $dato2);
    $actualizar -> bindParam(2, $dato1);
    $actualizar -> execute();
    echo json_encode($respuesta);
}
?>