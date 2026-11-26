# Haiku SOS — entorno de desarrollo en VirtualBox

Este repositorio reúne la máquina virtual compartible, el informe, la guía de instalación y práctica, el código de ejemplo y evidencias del trabajo realizado con Haiku R1 Beta 6.

## Inicio rápido

El archivo principal es `Paquete_Haiku_Desarrollo_Listo_20261122.zip`. Debido a su tamaño, se publica como archivo adjunto de la versión **Entrega Haiku v1.0.0** en la sección **Releases** de este repositorio.

Después, descomprimir el ZIP y seguir `documentacion/LEEME_IMPORTAR_HAIKU.md`. La OVA se importa desde **Archivo > Importar servicio virtualizado** en VirtualBox.

## Contenido

- `Releases > Entrega Haiku v1.0.0`: ZIP con la OVA lista para importar y los documentos de entrega.
- `documentacion/`: informe de 9 páginas sin capturas, guía del compañero, guía base, instrucciones, suma SHA-256 y relevo del estado actual.
- `codigo/`: ejemplos de Python y Java incluidos en el proyecto de Haiku.
- `evidencias/`: capturas técnicas separadas del informe.
- `scripts/`: generadores usados para producir el informe y la guía.

## Entorno preparado

- Haiku R1 Beta 6.
- Git 2.54.0.
- Python 3.14.7.
- OpenJDK y `javac` 17.0.14.
- Genio 6.0.2-3.
- Red NAT con reenvío `127.0.0.1:8080` hacia el puerto `8000` de Haiku.

## Estado frente a la rúbrica

La instalación, el entorno de desarrollo, la conectividad, el informe y el paquete compartible están terminados. El avance exacto de la rúbrica es aproximadamente **90 %**: quedan las pruebas específicas `35 → 40`, `index.html`, la ventana gráfica de Java, la comprobación tras reinicio y el apagado desde Deskbar. El detalle está en `documentacion/HANDOFF_ESTADO.md`.

## Integridad

- SHA-256 del OVA incluido en el ZIP: `D1E613D2E5C6E7A41EE4C67C55BE0EB32A0DA93FB0E330C79439AE6B8DB466B2`.
- SHA-256 del ZIP: `9C42678DEA1F0CDF0274DC8534164DF8710612D3C94022755169CA3CFF6C94FA`.

No se incluye la ISO original ni el VDI de trabajo porque el ZIP de la versión ya contiene la OVA necesaria para abrir el mismo entorno sin duplicar más de 2 GB de archivos.
