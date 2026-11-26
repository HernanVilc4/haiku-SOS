# Guion de exposición (≈10 min) — Haiku R1 Beta 6 en VirtualBox

Sin diapositivas: se comparte pantalla (VirtualBox con Haiku a pantalla grande). Dos expositores: **A** (tú) y **B** (compañero). Cada uno con su propia VM importada del mismo OVA.

## Frase de propósito (criterio 1 — dila al inicio y ponla en el Resumen del informe)

> "Haiku es un sistema operativo ligero, independiente (no es Linux), pensado para uso personal de escritorio; lo usamos como **entorno de desarrollo para estudiantes** que necesitan practicar **Git, Python y Java** en una máquina virtual pequeña que se importa en minutos, y probamos que **dos personas pueden colaborar** subiendo commits a un repositorio remoto."

- **Usuarios:** estudiantes y desarrolladores aficionados que quieren un SO ligero, rápido y con herramientas POSIX.
- **Caso concreto:** dos compañeros trabajan el mismo proyecto, cada uno en su VM Haiku, y sincronizan con Git remoto.

**Dónde ponerla en el informe (`Informe_Haiku_VirtualBox.docx`):** al final del párrafo de la sección **1 Resumen** y como primera línea de **2.1 Objetivo general**. En `LEEME_IMPORTAR_HAIKU.md`, justo bajo el título.

## Cronograma

| Min | Quién | Contenido |
|---|---|---|
| 0:00–1:30 | A | Propósito, usuarios, caso de uso (frase de arriba). Qué es Haiku: núcleo propio, BFS, paquetes HPKG, POSIX. |
| 1:30–4:00 | A | Instalación y configuración: mostrar **Configuración de la VM** en VirtualBox. Explicar cada decisión (ver abajo). Mencionar que se instaló desde ISO, DriveSetup, BFS, y que se exportó un OVA para repetirlo. |
| 4:00–5:30 | A | Herramientas con `pkgman`: mostrar `git version`, `python3.14 --version`, `javac -version`; abrir Genio. |
| 5:30–7:00 | A | Demo Python y Java (resultados esperados 15 y 20). Servidor HTTP y abrir `http://127.0.0.1:8080/resultado.html` en Windows (perspectiva del cliente). |
| 7:00–9:00 | A + B | Demo Git remoto entre las dos VMs (ver sección siguiente). |
| 9:00–10:00 | B | Limitaciones y conclusión. Abrir preguntas. |

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

## Git remoto con dos VMs (a probar ANTES de exponer)

Las dos VMs están en NAT en equipos distintos, así que **no se ven entre sí**. La opción más simple y robusta es un remoto en Internet (GitHub o Codeberg) que ambos usan:

**Preparación (en Windows, una sola vez):**
1. Crear un repositorio vacío `practica-haiku` en GitHub/Codeberg y dar acceso de escritura al compañero.
2. Cada uno crea un *token de acceso personal* con permiso de escritura en repos (se usa como contraseña por HTTPS). No lo pongas en pantalla durante la exposición.

**Persona A (en Haiku):**
```sh
cd /boot/home/Desarrollo/practica
git remote add origin https://github.com/USUARIO/practica-haiku.git
git push -u origin master        # usuario + token como contraseña
```

**Persona B (en su Haiku):**
```sh
cd /boot/home/Desarrollo
git clone https://github.com/USUARIO/practica-haiku.git
cd practica-haiku
git config user.name "Compañero"
git config user.email "companero@local"
echo "Cambio de B" >> README.md
git commit -am "Cambio desde la VM de B"
git push
```

**Persona A, para cerrar el ciclo:**
```sh
git pull
git log --oneline --graph
```
Se debe ver el commit de B en la VM de A. **Esa es la verificación**: un commit hecho en una VM aparece en la otra.

Extra si sobra tiempo (conflicto): ambos editan la misma línea de README, B hace push primero, A recibe el rechazo, hace `git pull`, resuelve y vuelve a hacer push. Muestra que entienden Git y no solo los comandos.

Notas:
- Revisar antes que `git push` por HTTPS funciona en Haiku (`pkgman list-repos` y red activa). Si falla la autenticación por HTTPS, probar con SSH (`ssh-keygen` y subir la clave pública a GitHub).
- Tener un plan B: si falla Internet durante la exposición, hacer el remoto con un repositorio *bare* local (`git init --bare /boot/home/remoto.git; git remote add local /boot/home/remoto.git`) y explicar que con dos máquinas se haría con SSH.

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
