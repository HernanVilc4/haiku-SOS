# Guía de Haiku en VirtualBox para Git Python y Java

## 1. Objetivo

Instalar Haiku R1/Beta 6 en una máquina virtual y dejar un entorno básico para practicar control de versiones con Git y programación con Python y Java. Esta guía no requiere capturas.

## 2. Material necesario

- Oracle VirtualBox 7.
- ISO de Haiku R1/Beta 6 de 64 bits (`haiku-r1beta6-x86_64-anyboot.iso`).
- Al menos 4 GB de RAM libre y 25 GB de espacio disponible.
- Conexión a Internet.

## 3. Crear la máquina virtual

1. Crear una VM llamada `Haiku-Desarrollo`.
2. Seleccionar tipo **Other/Unknown 64-bit**.
3. Asignar 4096 MB de RAM y 1 o 2 CPU.
4. Crear un disco VDI dinámico de 25 GB.
5. En Pantalla, usar **VMSVGA**, 64 MB de vídeo y desactivar aceleración 3D si aparecen fallos gráficos.
6. En Red, elegir **NAT** y adaptador **Intel PRO/1000 MT Desktop**.
7. Montar la ISO de Haiku en la unidad óptica e iniciar la VM.

Para consultar desde Windows un servidor web ejecutado en Haiku, crear esta regla de reenvío NAT:

| Nombre | Protocolo | IP anfitrión | Puerto anfitrión | IP invitado | Puerto invitado |
|---|---|---|---:|---|---:|
| DemoPython | TCP | 127.0.0.1 | 8080 | dejar vacío | 8000 |

## 4. Instalar Haiku

1. Elegir **Español** y distribución de teclado **Español**.
2. Pulsar **Instalar Haiku**.
3. Abrir **Configurar particiones**.
4. Inicializar el disco virtual con una tabla de particiones **Intel**.
5. Crear una partición que ocupe el disco, marcarla activa y asignar el tipo **Be File System**.
6. Formatearla como BFS. Si la interfaz no permite formatear, abrir Terminal y ejecutar, ajustando la ruta al disco mostrado por DriveSetup:

```sh
mkfs -t bfs /dev/disk/scsi/2/0/0/0 Haiku
```

7. Cerrar y volver a abrir el instalador si la partición no aparece.
8. Seleccionar como destino la partición de aproximadamente 25 GB y pulsar **Empezar**.
9. Cuando finalice, apagar la VM, retirar la ISO y arrancar desde el VDI.
10. En el primer inicio, elegir Español y **Probar Haiku** para entrar al escritorio instalado.

## 5. Verificar la red y las herramientas

Abrir **Deskbar > Applications > Terminal** y ejecutar:

```sh
ifconfig
pkgman list-repos
pkgman install git python3.14
git version
python3.14 --version
```

En la instalación comprobada el 19 de noviembre de 2026 se obtuvieron Git 2.54.0 y Python 3.14.7. Si otra versión aparece en el repositorio, usar esa versión y adaptar los comandos.

Instalar Java completo:

```sh
pkgman install openjdk17 openjdk17_default
java -version
javac -version
```

El entorno verificado instaló OpenJDK 17.0.14. Los dos comandos de versión deben responder; `javac` confirma que se instaló el JDK completo y no solo el entorno de ejecución.

Para instalar el editor/IDE Genio, intentar:

```sh
pkgman install genio
```

En la comprobación real, `pkgman search genio` no mostró resultados, pero `pkgman install genio` instaló Genio 6.0.2-3 y sus dependencias. La descarga se interrumpió una vez y se completó al repetir el mismo comando, reutilizando los paquetes ya descargados. Por eso, si un paquete no aparece en una búsqueda, probar igualmente la instalación directa y confirmar que los repositorios Haiku y HaikuPorts estén activos.

### Resultado verificado en la VM

| Componente | Resultado comprobado |
|---|---|
| Arranque | Haiku inicia desde el VDI de 25 GB sin la ISO |
| Red NAT | IP invitado 10.0.2.15 |
| Git | 2.54.0 |
| Python | 3.14.7 |
| Java y compilador | OpenJDK y javac 17.0.14 |
| Genio | 6.0.2-3 instalado; proyecto practica abierto en la rama master |
| Git funcional | Dos commits y árbol de trabajo limpio |
| Python | Salida S/ 15 y servidor HTTP accesible desde Windows |
| Java | Presupuesto.java compiló y mostró Total Java: S/ 20 |

### Continuar desde la copia compartible

Se generó `Haiku-Desarrollo-Listo.ova` con el estado funcional final y se validó con la importación en seco de VirtualBox. Para usarlo en otro equipo:

1. Abrir VirtualBox y elegir **Archivo > Importar servicio virtualizado**.
2. Seleccionar `Haiku-Desarrollo-Listo.ova`.
3. Revisar 4096 MB de RAM, 1 CPU y red NAT; luego importar.
4. Iniciar la VM. Genio, Git, Python, Java y el proyecto `/boot/home/Desarrollo/practica` ya están incluidos.
5. Si el puerto 8080 está ocupado en Windows, cambiar la regla NAT del anfitrión a otro puerto libre.

## 6. Práctica básica con Git

Crear un repositorio local:

```sh
mkdir -p /boot/home/Desarrollo/practica
cd /boot/home/Desarrollo/practica
git init
git config user.name "Estudiante Haiku"
git config user.email "estudiante@local"
```

Crear `README.md` con un editor y guardar este texto:

```text
# Práctica en Haiku
Repositorio para ejercicios de Git, Python y Java.
```

Registrar el primer cambio:

```sh
git add README.md
git commit -m "Primer commit"
git status
git log --oneline
```

Ejercicio sugerido: editar el README, revisar `git diff`, crear una rama con `git switch -c mejora-readme`, hacer otro commit y volver con `git switch master`.

## 7. Práctica de Python

Crear `presupuesto.py`:

```python
articulo = "Cuaderno"
cantidad = 3
precio = 5
total = cantidad * precio
print(f"{articulo}: {cantidad} x S/ {precio} = S/ {total}")
```

Ejecutar:

```sh
python3.14 presupuesto.py
```

El resultado esperado es `Cuaderno: 3 x S/ 5 = S/ 15`.

Para probar la comunicación con Windows, iniciar en la carpeta del proyecto:

```sh
python3.14 -m http.server 8000 --bind 0.0.0.0
```

En Windows abrir `http://127.0.0.1:8080`. Debe mostrarse el contenido de la carpeta servida por Haiku. Detener el servidor con `Ctrl+C`.

## 8. Práctica de Java

Crear `Presupuesto.java`:

```java
public class Presupuesto {
    public static void main(String[] args) {
        int cantidad = 4;
        int precio = 5;
        System.out.println("Total: S/ " + (cantidad * precio));
    }
}
```

Compilar y ejecutar:

```sh
javac Presupuesto.java
java Presupuesto
```

El resultado esperado es `Total: S/ 20`.

## 9. Guardar el trabajo con Git

```sh
git add README.md presupuesto.py Presupuesto.java
git commit -m "Agregar prácticas de Python y Java"
git status
git log --oneline
```

`git status` debe indicar que no hay cambios pendientes.

## 10. Problemas frecuentes

- **No aparece el disco destino:** comprobar que la partición sea tipo Be File System, esté formateada en BFS y tenga un nombre distinto del volumen de arranque; cerrar y reabrir el instalador.
- **No hay red:** usar NAT e Intel PRO/1000 MT Desktop; comprobar que `ifconfig` muestre una IP parecida a `10.0.2.15`.
- **No aparece un paquete en `pkgman search`:** intentar `pkgman install nombre_paquete`; verificar `pkgman list-repos`.
- **`java` funciona pero `javac` no:** instalar también `openjdk17_default` y confirmar que se instaló el JDK completo.
- **Windows no abre el servidor:** revisar la regla NAT 8080→8000 y que Python esté escuchando en `0.0.0.0`, no solo en `127.0.0.1` dentro de Haiku.
- **Antes de experimentar:** crear una instantánea de VirtualBox con la VM apagada o estable.

## 11. Lista de comprobación

- [ ] Haiku arranca sin la ISO.
- [ ] La red obtiene una dirección IP.
- [ ] `git version` responde.
- [ ] `python3.14 --version` responde.
- [ ] `java -version` y `javac -version` responden.
- [ ] Se crea al menos un commit local.
- [ ] Python ejecuta el ejercicio y el servidor es accesible desde Windows.
- [ ] Java compila y ejecuta el ejercicio.
- [ ] Se crea una instantánea final de la VM.

En la VM preparada todos los puntos anteriores quedaron comprobados. La instantánea final se llama `Haiku listo para desarrollo`.
