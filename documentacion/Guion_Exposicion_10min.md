# Guion de exposición (≈10 min) — Haiku R1 Beta 6 en VirtualBox

Sin diapositivas: se comparte pantalla (VirtualBox con Haiku a pantalla grande). Dos expositores: **Gianluck** y **Hernán**. Cada uno con su propia VM importada del mismo OVA. Cada uno comparte la pantalla de su PC cuando le toca.

## Frase de propósito (criterio 1 — dila al inicio y ponla en el Resumen del informe)

> "Haiku es un sistema operativo ligero, independiente (no es Linux), pensado para uso personal de escritorio; lo usamos como **entorno de desarrollo para estudiantes** que necesitan practicar **Git, Python y Java** en una máquina virtual pequeña que se importa en minutos, y probamos que **dos personas pueden colaborar** subiendo commits a un repositorio remoto."

- **Usuarios:** estudiantes y desarrolladores aficionados que quieren un SO ligero, rápido y con herramientas POSIX.
- **Caso concreto:** dos compañeros trabajan el mismo proyecto, cada uno en su VM Haiku, y sincronizan con Git remoto.

**Dónde ponerla en el informe (`Informe_Haiku_VirtualBox.docx`):** al final del párrafo de la sección **1 Resumen** y como primera línea de **2.1 Objetivo general**. En `LEEME_IMPORTAR_HAIKU.md`, justo bajo el título.

## Cronograma

| Min | Quién | Contenido |
|---|---|---|
| 0:00–1:30 | Gianluck | Propósito, usuarios y caso de uso (frase de arriba). Qué es Haiku. |
| 1:30–3:30 | Gianluck | Configuración de la VM: Configuración, Sistema, Pantalla, Almacenamiento y Red con el reenvío de puertos. |
| 3:30–5:30 | Gianluck | Herramientas con `pkgman`: versiones de Git, Python y Java; abrir Genio. |
| 5:30–7:00 | Hernán | Demo Python y Java en vivo. Servidor HTTP y abrir `http://127.0.0.1:8080/resultado.html` en Windows. |
| 7:00–9:00 | Los dos | Git remoto entre las dos VMs (ver sección siguiente). |
| 9:00–10:00 | Hernán | Limitaciones, conclusión y preguntas. Responde primero quien menos habló. |

### Decisiones a explicar en 1:30–4:00
- **4096 MB RAM:** el IDE y el compilador Java necesitan memoria; con menos se vuelve lento.
- **1 CPU:** evita problemas de arranque durante la instalación; se puede subir después.
- **Disco VDI dinámico 25 GB:** no ocupa los 25 GB desde el inicio.
- **BIOS (no EFI):** es la opción con la que se verificó la instalación.
- **VMSVGA, 64 MB, sin 3D:** salida compatible, evita fallos gráficos.
- **NAT + Intel PRO/1000:** da Internet sin exponer la VM; Haiku lo reconoce (IP 10.0.2.15). El reenvío 8080→8000 permite que Windows consulte el servidor de Haiku.
- **BFS:** sistema de archivos nativo de Haiku; el instalador solo acepta destinos BFS.

### Demo local (comandos)
```sh
cd /boot/home/Desarrollo/practica
git status
python3.14 presupuesto.py        # Cuaderno: 3 x S/ 5 = S/ 15
javac Presupuesto.java
java Presupuesto                 # Total Java: S/ 20
python3.14 -m http.server 8000 --bind 0.0.0.0
```
En Windows: `http://127.0.0.1:8080/resultado.html` → HTTP 200.
**Cómo verificas:** resultado esperado = 3×5 = 15 y 4×5 = 20 calculados a mano; HTTP 200 y la línea de registro en la Terminal de Haiku; `git status` limpio.

## Git remoto con dos VMs (repo de ensayo: Gian999/haiku-pruebas)

Las VMs están en NAT en equipos distintos y no se ven entre sí. Usan un repositorio en Internet. El repo de la entrega (`HernanVilc4/haiku-SOS`) no se toca en los ensayos.

Cada uno, una vez, en su Haiku: nombre y correo con `git config --global`, `git config --global credential.helper store`, token clásico con permiso `repo` (se escribe a mano la primera vez) y clonar:
```sh
git clone https://github.com/Gian999/haiku-pruebas.git
cd haiku-pruebas
```

**En la exposición (7:00 a 9:00):**
1. **Gianluck:** `echo "Ensayo" >> ensayo.txt`, `git add ensayo.txt`, `git commit -m "..."`, `git push`.
2. **Hernán:** `git pull` y `git log`. Dice en voz alta que ve el commit de Gianluck.
3. **Hernán:** hace su cambio y `git push`.
4. **Gianluck:** `git pull` y `git log`.
5. **Gianluck:** abre en el navegador la página de commits de `github.com/Gian999/haiku-pruebas` y señala los dos nombres. **Esa es la verificación.**

Extra si sobra tiempo: conflicto a propósito. Los dos reemplazan el contenido de `ensayo.txt`, Hernán sube primero, Gianluck recibe el rechazo, hace `git pull`, resuelve las marcas y vuelve a hacer `git push`.

Plan B si falla Internet: repo local `git init --bare /boot/home/remoto.git`, `git remote add local /boot/home/remoto.git`, `git push local main`.

El detalle paso a paso con clics está en el artifact: https://claude.ai/artifact/9JQckytL6r9YGpdsQV2GEj

## Preguntas probables y respuestas cortas
- **¿Haiku es Linux?** No. Núcleo propio (derivado de NewOS), compatible con POSIX, por eso Git y Python funcionan igual.
- **¿Por qué NAT y no puente?** NAT es más seguro y simple; el reenvío de puertos basta para la demo. Con puente la VM tendría IP en la red física.
- **¿Qué es `0.0.0.0` en el servidor?** Escuchar en todas las interfaces; si fuera `127.0.0.1` Windows no podría entrar por el reenvío.
- **¿Por qué `javac` y `java`?** `javac` compila a bytecode, `java` lo ejecuta en la JVM; Python interpreta directamente.
- **¿Limitaciones?** No hay .NET, VS Code ni IntelliJ oficiales; pocos paquetes frente a Linux; rendimiento gráfico limitado en VM.
- **¿Qué es un paquete HPKG?** Formato de paquete de Haiku, gestionado con `pkgman` o HaikuDepot.
- **¿Qué pasa si falla la demo?** Mostrar el informe con las evidencias y el OVA como respaldo.

## Lista previa a exponer
- [ ] Informe con nombres, curso y docente completados.
- [ ] Ambas VMs arrancan y tienen Internet (`ping` o `pkgman list-repos`).
- [ ] Repositorio remoto creado, tokens guardados fuera de pantalla.
- [ ] Ensayo completo con cronómetro (objetivo 9:30).
- [ ] Instantánea de la VM tomada antes de la exposición.
- [ ] Puerto 8080 libre en Windows.
