# Paquete Haiku Desarrollo

Este paquete contiene una máquina virtual Haiku R1 Beta 6 lista para utilizar con Git, Python, Java y Genio.

## Requisito

Instalar Oracle VirtualBox 7 o una versión compatible desde:

https://www.virtualbox.org/wiki/Downloads

## Importar y ejecutar

1. Descomprimir completamente este ZIP en una carpeta local.
2. Abrir Oracle VirtualBox.
3. Elegir **Archivo > Importar servicio virtualizado**.
4. Seleccionar `Haiku-Desarrollo-Listo.ova`.
5. Mantener 4096 MB de RAM, 1 CPU y red NAT; después pulsar **Importar**.
6. Iniciar la máquina virtual importada.

La máquina incluye:

- Haiku R1 Beta 6 instalado en un disco virtual de 25 GB.
- Git 2.54.0.
- Python 3.14.7.
- OpenJDK y javac 17.0.14.
- Genio 6.0.2-3.
- Proyecto `/boot/home/Desarrollo/practica` con ejercicios de Git, Python y Java.

## Prueba rápida

Abrir Terminal en Haiku y ejecutar:

```sh
cd /boot/home/Desarrollo/practica
git status
python3.14 presupuesto.py
javac Presupuesto.java
java Presupuesto
```

Resultados esperados:

- Git indica que el árbol de trabajo está limpio.
- Python muestra `Cuaderno: 3 x S/ 5 = S/ 15`.
- Java muestra `Total Java: S/ 20`.

## Servidor web

Ejecutar en la carpeta del proyecto:

```sh
python3.14 -m http.server 8000 --bind 0.0.0.0
```

En Windows abrir `http://127.0.0.1:8080/resultado.html`.

Si el puerto 8080 ya está ocupado, cambiar la regla de reenvío NAT en la configuración de red de la VM.

## Verificar la descarga

El archivo `SHA256SUMS.txt` contiene la huella SHA-256 del OVA. En PowerShell se puede comprobar con:

```powershell
Get-FileHash .\Haiku-Desarrollo-Listo.ova -Algorithm SHA256
```
