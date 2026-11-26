# Relevo de trabajo — Haiku en VirtualBox

Última actualización: 2026-11-25 (America/Lima)

## Objetivo

Completar en VirtualBox la instalación y preparación de Haiku para desarrollo, ejecutar las pruebas solicitadas y entregar un informe de máximo 10 páginas sin capturas.

## Avance real frente a la rúbrica

**Aproximadamente 90 %.** La instalación, el entorno, la red, Git, Python, Java, Genio, el informe y la máquina compartible están terminados. Para afirmar 100 % de la rúbrica todavía deben realizarse y documentarse las pruebas exactas indicadas al final de este archivo.

## Trabajo completado

- VM `Haiku-Desarrollo-Listo` con Haiku R1 Beta 6 instalado.
- Configuración: 4096 MB RAM, 1 CPU, VMSVGA 64 MB, NAT y disco virtual de 25 GB.
- Reenvío NAT: `127.0.0.1:8080` en Windows hacia el puerto `8000` de Haiku.
- Git 2.54.0, Python 3.14.7, OpenJDK/javac 17.0.14 y Genio 6.0.2-3 instalados.
- Proyecto `/boot/home/Desarrollo/practica` abierto en Genio y versionado con Git.
- Pruebas funcionales actuales: Python muestra `Cuaderno: 3 x S/ 5 = S/ 15`; Java muestra `Total Java: S/ 20`; Git tiene dos commits y árbol limpio.
- Servidor HTTP probado desde Windows con respuesta 200 en `http://127.0.0.1:8080/resultado.html`.
- Instantánea `Haiku listo para desarrollo` creada.
- OVA exportado y validado: `Haiku-Desarrollo-Listo.ova`.
- SHA-256 del OVA: `D1E613D2E5C6E7A41EE4C67C55BE0EB32A0DA93FB0E330C79439AE6B8DB466B2`.
- Informe final de 9 páginas, sin capturas ni imágenes.
- Guía para el compañero en Markdown y DOCX.
- ZIP compartible con la OVA, documentos e instrucciones de importación.

## Pendiente para cerrar el 100 % exacto de la rúbrica

1. Adaptar y demostrar la prueba de Python con el cambio de entrada que produzca `35` y luego `40`.
2. Crear o usar `index.html` según la guía y comprobarlo desde Windows.
3. Ejecutar la versión Java con ventana gráfica y conservar evidencia de esa ventana.
4. Reiniciar Haiku y volver a comprobar persistencia de archivos y funcionamiento de Python y Java.
5. Apagar Haiku correctamente desde Deskbar y registrar la evidencia correspondiente.
6. Después de esas pruebas, actualizar informe, OVA, suma SHA-256 y ZIP final.

## Archivos principales

- `Informe_Haiku_VirtualBox.docx`: informe de 9 páginas sin capturas.
- `Guia_Companero_Haiku_Git_Programacion.md` y `.docx`: guía reproducible.
- `Paquete_Haiku_Desarrollo_Listo_20261122.zip`: paquete importable actual.
- `LEEME_IMPORTAR_HAIKU.md`: instrucciones de importación.
- `SHA256SUMS.txt`: huella del OVA incluido en el paquete.

## Nota para continuar

La VM lista se llama `Haiku-Desarrollo-Listo`. La ventana de VirtualBox puede ejecutarse elevada; las verificaciones también se pueden realizar con `VBoxManage`.

## Actualización 2026-11-25 (noche, hora de Lima)

### Equipo y repos
- Estudiantes: Gianluck Yhudá Pastor Lovón (`Gian999`) y Jorge Hernan Vilca Apaza (`HernanVilc4`). Curso: Sistemas Operativos. Docente: Fredy Abel Huanca Torres. Institución: UPEU.
- Repo de la entrega: `HernanVilc4/haiku-SOS` (este). Repo de ensayo de Git remoto: `Gian999/haiku-pruebas`, con Hernán como colaborador.
- Plan de trabajo y guía de exposición (artifact): https://claude.ai/artifact/9JQckytL6r9YGpdsQV2GEj

### Hecho en esta sesión
- Informe `Informe_Haiku_VirtualBox.docx` actualizado: nombres, curso, docente, institución y un párrafo de "Propósito y caso de uso" en el Resumen. No se revisó el formato abierto en Word.
- Guion de 10 minutos con reparto entre Gianluck y Hernán: `documentacion/Guion_Exposicion_10min.md`.
- Git remoto probado a medias en `Gian999/haiku-pruebas`: llegó a GitHub el commit de Gianluck (22:10) y el de Hernán (22:37). Falta el `git pull` de cada uno para ver el commit del otro.
- Token guardado en la VM de Gianluck con `credential.helper store` (comprobado: archivo `.git-credentials` de 68 bytes).
- La hora de la PC estaba 5 horas adelantada respecto a Lima y se corrigió.

### Problema conocido: no instalar Guest Additions
- `pkgman install virtualbox_guest_additions` deja a Haiku congelado en la pantalla del logo (paquete 6.1.26 frente a VirtualBox 7.2). No hay copiar y pegar entre Windows y la VM; el token se escribe a mano.
- Recuperación: al arrancar, pulsar Espacio varias veces hasta ver "Haiku Boot Loader", elegir "Select boot volume/state", Enter, Enter, el estado con fecha anterior al "Latest state", luego "Return to main menu" y "Continue booting".
- Esto hay que repetirlo en cada arranque hasta crear un estado nuevo de paquetes. Se intentó con `nano` (ya instalado) y `htop` (no existe en los repos). Pendiente: instalar un paquete pequeño que no esté instalado, por ejemplo `tree`.

### Pendiente
1. Fijar el estado de arranque bueno de la VM (o practicar el menú con Espacio).
2. `git pull` en las dos VMs y ver los dos commits con `git log`; ensayar un conflicto.
3. Ensayo cronometrado de 10 minutos, meta 9:30.
4. Revisar con Hernán las pruebas pendientes de la sección anterior (Python con 35 y 40, `index.html`, Java con ventana, reinicio y apagado) y confirmar con el docente si las pidió.
5. Abrir el informe en Word y revisar el formato.

### Avance frente a la rúbrica (estimación, no nota)
Aproximadamente 16,75 de 20 (cerca del 84 %): propósito 3/3, instalación 4/4, demostración 5,5/7, dominio 3/4, claridad 1,25/2. Lo más grande que falta es completar y ensayar la demostración de Git remoto.
