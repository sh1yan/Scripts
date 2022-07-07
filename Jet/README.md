Estos scripts automatizan la explotación de el fortress Jet

· Para usar estos scripts necesitas tener instalada la libreria pwntools

    pip install pwntools

· Para el primero solo tenemos que ejecutar el script con python3 con tu ip (tun0) al final y obtenemos una shell como www-data

<img src="https://raw.githubusercontent.com/GatoGamer1155/Imagenes-Repositorios/main/wwwj.png">

· Para el segundo tenemos que exponer el servicio con socat desde www-data antes de ejecutar

    socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/home/leak

· Después solo queda ejecutar y obtener la shell como alex

<img src="https://raw.githubusercontent.com/GatoGamer1155/Imagenes-Repositorios/main/alexj.png">

