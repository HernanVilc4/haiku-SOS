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
