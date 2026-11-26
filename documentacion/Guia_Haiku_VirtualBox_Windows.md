# Haiku en VirtualBox: instalación y entorno de desarrollo

## 1. Objetivo de la práctica

Preparar un escritorio Haiku para un estudiante que necesita editar código, ejecutar Python y Java, guardar resultados y consultarlos desde Windows. La demostración será una aplicación sencilla de presupuesto.

Haiku es un sistema independiente inspirado en BeOS, con núcleo derivado de NewOS y compatibilidad POSIX. No utiliza el núcleo Linux. Evitar afirmar que no tiene relación alguna con Unix: admite interfaces y herramientas POSIX.

## 2. Descargas y requisitos

- [Haiku: descarga oficial](https://www.haiku-os.org/get-haiku/). Elegir **R1/beta6, x86_64, Anyboot ISO**.
- [ISO de 64 bits: descarga directa](https://haiku.osuosl.org/r1beta6/haiku-r1beta6-x86_64-anyboot.iso).
- [VirtualBox para Windows](https://www.virtualbox.org/wiki/Downloads): elegir **Windows hosts**.
- PC Windows con procesador Intel/AMD de 64 bits, virtualización VT-x/AMD-V habilitada, 8 GB de RAM recomendados y 30 GB libres.

**Asignación para esta práctica:** 4 GB de RAM y disco de 25 GB. No utilizar 1 GB como configuración de desarrollo; el navegador y los compiladores necesitan margen.

## 3. Crear la máquina virtual

En VirtualBox → **Nueva**:

| Opción | Valor |
|---|---|
| Nombre | `Haiku-Desarrollo` |
| Imagen ISO | La ISO descargada |
| Instalación desatendida | Omitir/desactivar |
| Tipo y versión | Haiku de 64 bits si aparece; en caso contrario, Other → Other/Unknown (64-bit) |
| RAM | 4096 MB; 2048 MB si el equipo tiene pocos recursos |
| Procesadores | 1 para la instalación inicial |
| Disco | VDI, reservado dinámicamente, 25 GB |
| Firmware | BIOS; EFI desactivado |
| Pantalla | VMSVGA, 64 MB de vídeo, aceleración 3D desactivada |
| Red | Adaptador 1: NAT, cable conectado, Intel PRO/1000 MT Desktop |
| Arranque inicial | Óptico antes del disco duro |

Con la VM apagada, abrir **Configuración → Red → Adaptador 1 → Avanzadas → Reenvío de puertos** y añadir:

| Nombre | Protocolo | IP anfitrión | Puerto anfitrión | IP invitado | Puerto invitado |
|---|---|---|---|---|---|
| DemoPython | TCP | `127.0.0.1` | `8080` | Dejar vacío | `8000` |

## 4. Instalar en el disco virtual

1. Iniciar la VM. Elegir idioma español y distribución de teclado correspondiente.
2. Seleccionar **Install Haiku / Instalar Haiku**.
3. En Installer, abrir **Set up partitions… / Configurar particiones…**.
4. En DriveSetup, seleccionar el **disco virtual vacío de 25 GB**, identificándolo por su tamaño.
5. Elegir **Disk → Initialize → Intel Partition Map** y confirmar.
6. Seleccionar el espacio libre → **Partition → Create**. Utilizar el espacio disponible, tipo **Be File System** y marcar **Active partition**.
7. Seleccionar la partición creada → **Partition → Format → Be File System**. Poner nombre `Haiku` y confirmar.
8. Cerrar DriveSetup. En Installer, seleccionar el medio de instalación como origen y el volumen `Haiku` como destino.
9. Pulsar **Begin / Comenzar** y esperar a que termine.
10. Apagar la VM. En VirtualBox → **Almacenamiento**, retirar la ISO de la unidad óptica.
11. Iniciar de nuevo. Comprobar que arranca desde el disco virtual sin la ISO.

## 5. Configuración inicial

En el menú **Deskbar → Preferences / Preferencias**:

- **Locale:** español y teclado correcto.
- **Time:** fecha, hora y zona horaria de Lima.
- **Screen:** resolución de 1366 × 768 si está disponible.
- **Network:** conexión Ethernet con configuración automática DHCP.

Abrir **WebPositive** y cargar `https://www.haiku-os.org` para verificar Internet.

Abrir **SoftwareUpdater**, instalar las actualizaciones propuestas y reiniciar cuando lo solicite. Mantener los repositorios de la versión instalada.

Si faltan resoluciones, abrir **Terminal** e instalar:

```sh
pkgman install vmware_addons
```

Reiniciar y volver a Screen. El paquete incluye un controlador VMSVGA útil en VirtualBox; no garantiza todas las funciones de integración con Windows.

## 6. Instalar herramientas de desarrollo

Abrir **Deskbar → Applications → HaikuDepot**, seleccionar **All packages / Todos los paquetes** y buscar e instalar:

| Paquete | Uso |
|---|---|
| `genio` | IDE nativo con pestañas, resaltado y soporte LSP |
| `git` | Control de versiones |
| `python3.12` | Intérprete Python para la práctica |
| `openjdk17` | JDK para compilar y ejecutar Java; instalar el JDK completo |

Aceptar las dependencias. Si una versión no aparece, buscar `python` u `openjdk` e instalar una versión disponible del intérprete o JDK completo, ajustando los comandos siguientes.

Abrir una Terminal nueva y comprobar:

```sh
uname -a
python3.12 --version
java -version
javac -version
git --version
mkdir -p /boot/home/Desarrollo/presupuesto
cd /boot/home/Desarrollo/presupuesto
```

**No continuar con Java hasta que funcionen `java` y `javac`.** Si solo funciona `java`, revisar en HaikuDepot que esté instalado el JDK completo y no únicamente el JRE.

Abrir **Genio** desde Applications. Guardar los siguientes archivos dentro de `/boot/home/Desarrollo/presupuesto`. Ejecutar los comandos en Terminal; el soporte de autocompletado depende del servidor LSP configurado para cada lenguaje.

## 7. Prueba funcional en Python

En Genio, crear y guardar `presupuesto.py`:

```python
from pathlib import Path

productos = [("Cuaderno", 3, 5), ("Lapicero", 10, 2)]
total = sum(cantidad * precio for _, cantidad, precio in productos)
filas = "".join(
    f"<tr><td>{nombre}</td><td>{cantidad}</td><td>{precio}</td>"
    f"<td>{cantidad * precio}</td></tr>"
    for nombre, cantidad, precio in productos
)
html = f"""<!doctype html>
<html lang="es"><meta charset="utf-8"><title>Presupuesto Haiku</title>
<body><h1>Presupuesto generado en Haiku</h1>
<table border="1"><tr><th>Producto</th><th>Cantidad</th>
<th>Precio S/</th><th>Subtotal S/</th></tr>{filas}</table>
<h2>Total: S/ {total:.2f}</h2></body></html>"""
Path("index.html").write_text(html, encoding="utf-8")
print(f"Archivo generado. Total: S/ {total:.2f}")
```

En Terminal:

```sh
cd /boot/home/Desarrollo/presupuesto
python3.12 presupuesto.py
python3.12 -m http.server 8000 --bind 0.0.0.0
```

Dejar esa Terminal abierta mientras se realiza la prueba.

1. En WebPositive de Haiku, abrir `http://127.0.0.1:8000`.
2. En Chrome o Edge de **Windows**, abrir `http://127.0.0.1:8080`.
3. Ambos deben mostrar la tabla y **Total: S/ 35.00**. Verificar: `3 × 5 + 10 × 2 = 35`.
4. Cambiar en Genio la cantidad de cuadernos de `3` a `4`, guardar y volver a ejecutar `python3.12 presupuesto.py` en otra Terminal, desde la misma carpeta.
5. Actualizar el navegador de Windows: debe aparecer **Total: S/ 40.00**. La Terminal del servidor debe registrar la petición HTTP.

Para detener el servidor, presionar `Ctrl+C` en su Terminal. Se inicia manualmente después de cada reinicio.

## 8. Prueba funcional en Java

Crear en Genio `Presupuesto.java`:

```java
import javax.swing.JOptionPane;

public class Presupuesto {
    public static void main(String[] args) {
        String entrada = JOptionPane.showInputDialog(
            null, "Cantidad de cuadernos:", "3");
        if (entrada == null) return;
        try {
            int cantidad = Integer.parseInt(entrada);
            if (cantidad < 0) throw new NumberFormatException();
            int total = cantidad * 5 + 10 * 2;
            JOptionPane.showMessageDialog(null, "Total: S/ " + total);
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(null, "Ingrese un entero no negativo.");
        }
    }
}
```

En otra Terminal:

```sh
cd /boot/home/Desarrollo/presupuesto
javac Presupuesto.java
java Presupuesto
```

Ingresar `3`: debe mostrar **S/ 35**. Repetir con `4`: **S/ 40**. Ingresar letras: debe mostrar el mensaje de validación. Esto comprueba compilación, ejecución e interfaz gráfica dentro de Haiku.

## 9. C#, VS Code, IntelliJ y agentes

| Herramienta | Decisión para esta práctica |
|---|---|
| C# / .NET | Haiku no figura entre las plataformas oficiales de .NET. Utilizar Windows si se necesita C#; no presentarlo como instalado en Haiku. |
| VS Code e IntelliJ | Sus distribuciones oficiales no incluyen Haiku. Utilizar Genio dentro de la VM. |
| Claude Code y Codex | No basar la práctica en una instalación nativa sin soporte confirmado para Haiku. Si se usan en Windows para ayudar a escribir código, ejecutar y comprobar el resultado dentro de Haiku. |

## 10. Dejar la VM lista

1. Guardar los fuentes y `index.html` en la carpeta del proyecto.
2. Reiniciar Haiku y comprobar que los archivos permanecen y Java/Python siguen funcionando.
3. Volver a iniciar el servidor Python y comprobar el acceso desde Windows.
4. Apagar Haiku correctamente desde Deskbar.
5. Crear una instantánea en VirtualBox llamada **Haiku listo para desarrollo**.

## 11. Evidencias y exposición según la rúbrica

| Criterio | Evidencia que se debe mostrar |
|---|---|
| Propósito y contexto — 3 puntos | Estudiante que desarrolla una aplicación de presupuesto en un escritorio alternativo. |
| Instalación y configuración — 4 puntos | Configuración de VM, partición BFS, arranque sin ISO, red y versiones de las herramientas. Explicar RAM, BIOS y NAT. |
| Demostración — 7 puntos | Editar y ejecutar Python; consultar desde Windows; cambiar la entrada y verificar 35 → 40; compilar Java y probar su ventana. |
| Dominio técnico — 4 puntos | Explicar núcleo independiente, compatibilidad POSIX, BFS, paquetes HPKG, compilación frente a interpretación y limitaciones del software. |
| Claridad — 2 puntos | Orden: necesidad → configuración → prueba → resultados → limitaciones. Ajustar la duración al tiempo del docente. |

Guardar capturas de la configuración, particionado, arranque instalado, versiones, código en Genio, resultados en Windows y ventana Java. Ensayar sin depender de nuevas descargas. Mostrar solo el escritorio no cumple la demostración funcional.

## 12. Fallos frecuentes

| Problema | Acción |
|---|---|
| Regresa al instalador | Retirar la ISO y poner el disco duro primero en el arranque. |
| No arranca desde el disco | Comprobar partición activa. Arrancar con la ISO y usar Installer → Tools → Write boot sector sobre el volumen instalado. |
| No hay Internet | Revisar NAT, cable conectado y DHCP; comprobar fecha y hora si falla HTTPS. |
| Windows no abre el presupuesto | Mantener el servidor activo, revisar reenvío TCP 8080 → 8000 y probar primero el acceso local en Haiku. |
| Puerto 8080 ocupado | Cambiar solo el puerto anfitrión a 8081 y abrir `http://127.0.0.1:8081`. |
| Un paquete no aparece | Actualizar la lista de HaikuDepot, revisar Todos los paquetes y buscar el nombre base. |
| Cursor atrapado | Presionar Ctrl derecho para devolver el control a Windows. |

## Fuentes de consulta

- [Descargas y arquitecturas de Haiku](https://download.haiku-os.org/).
- [Notas de Haiku R1/beta6 y requisitos](https://github.com/haiku/website/blob/master/content/get-haiku/r1beta6/release-notes.md).
- [DriveSetup: particiones y BFS](https://i18n.haiku-os.org/userguide/data/export/docs/userguide/en/applications/drivesetup.html).
- [Instalación de aplicaciones y paquetes](https://i18n.haiku-os.org/userguide/data/export/docs/userguide/en/applications.html).
- [Genio: proyecto oficial](https://codeberg.org/Genio/Genio).
- [Controlador VMSVGA para Haiku](https://github.com/HaikuArchives/VMwareAddons).
- [Requisitos de VS Code](https://code.visualstudio.com/docs/supporting/requirements), [IntelliJ](https://www.jetbrains.com/help/idea/installation-guide.html), [.NET](https://github.com/dotnet/core/blob/main/release-notes/10.0/supported-os.md) y [Claude Code](https://code.claude.com/docs/en/setup).

**Validación pendiente en el equipo del compañero:** completar las pruebas de las secciones 7, 8 y 10 antes de exponer.

