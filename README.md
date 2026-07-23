# 🌍 Guardianes del Holoceno

*Un videojuego sobre los nueve límites planetarios*

> Videojuego educativo interactivo · Evaluación Módulo 4 · Límites planetarios
> **Cátedra Ambiental** · Universidad de Antioquia
>
> Estudiante: **Johan Granados Vega** — Programa de Estadística, Facultad de Ciencias Exactas y Naturales
> Trabajo presentado a: **Profesora Cristina López-Gallego**
> Medellín, 2026

## Enlaces de acceso

| | |
|---|---|
| 🎮 **Juega en línea** (aplicación desplegada) | <https://granados.up.railway.app/> |
| 💻 **Código fuente** (repositorio en GitHub) | <https://github.com/NahojG/limites-planetarios> |

El videojuego puede jugarse directamente desde cualquier navegador moderno, sin necesidad de instalación, a través del primer enlace. El segundo enlace da acceso al código fuente completo, las instrucciones para ejecutarlo localmente y la documentación del proyecto.

## Introducción

Durante aproximadamente 11.700 años, el Holoceno le ofreció a la humanidad un planeta excepcionalmente estable: un clima predecible, ecosistemas resilientes y ciclos biogeoquímicos en equilibrio que hicieron posible la agricultura, las ciudades y la civilización tal como la conocemos. En 2009, Johan Rockström y los científicos del Centro de Resiliencia de Estocolmo propusieron el marco de los nueve límites planetarios: los umbrales dentro de los cuales la humanidad puede operar con seguridad y más allá de los cuales el sistema terrestre corre el riesgo de cambios abruptos e irreversibles. Hoy, seis de esos nueve límites ya han sido transgredidos.

Comprender este marco constituye uno de los objetivos centrales del Módulo 4 de la Cátedra Ambiental. En esa dirección, este trabajo propone el desarrollo de un recurso pedagógico interactivo: el videojuego educativo *Guardianes del Holoceno*. En él, la persona que juega asume la responsabilidad de gobernar el planeta y experimenta, de manera vivencial, cómo las decisiones colectivas pueden degradar o restaurar las condiciones que sostienen la vida en la Tierra. Así, el juego convierte los conceptos abordados en la cartilla del módulo los límites planetarios, el Antropoceno y el Capitaloceno, la cultura de los límites y la justicia socioambiental en mecánicas concretas, dilemas con consecuencias y una representación visual del estado del sistema terrestre.

Este documento presenta el proyecto: sus objetivos, la descripción detallada del interactivo y los enlaces de acceso a la versión desplegada en la web y al código fuente abierto.

## Objetivos

### Objetivo general

Diseñar y desarrollar un videojuego educativo interactivo, accesible desde la web, que comunique de forma vivencial el concepto de los nueve límites planetarios y los contenidos del Módulo 4 de la Cátedra Ambiental, de modo que quien juega comprenda la interdependencia entre las decisiones humanas y la estabilidad del sistema terrestre.

### Objetivos específicos

- Traducir los nueve límites planetarios definidos por Rockström *et al.* (2009) y actualizados por Steffen *et al.* (2015), Persson *et al.* (2022) y Wang-Erlandsson *et al.* (2022) en variables medibles dentro de una mecánica de juego por turnos.
- Representar visualmente la degradación y la recuperación del planeta mediante una Tierra animada y un diagrama radial que reflejan, en tiempo real, las consecuencias de cada decisión.
- Integrar *pausas de saberes* (preguntas tipo quiz) que refuercen los conceptos clave de la cartilla y recompensen el aprendizaje aliviando los límites más transgredidos.
- Evidenciar las dimensiones de justicia socioambiental la responsabilidad diferenciada entre el Norte y el Sur global y la noción de Capitaloceno como parte ineludible de la crisis planetaria.
- Desplegar la aplicación en un servidor público y liberar el código fuente para garantizar el acceso abierto, la reproducibilidad y el uso pedagógico del recurso.

## ¿De qué trata? El interactivo

*Guardianes del Holoceno* es un juego de estrategia y decisión por turnos en el que asumes el gobierno del mundo entre los años 2025 y 2090. Cada turno representa un lapso de cinco años y plantea una decisión o una pregunta. La premisa es directa: el Holoceno nos regaló un planeta estable, pero seis de los nueve límites ya fueron transgredidos, y de tus decisiones depende devolver a la humanidad a un espacio operativo seguro o precipitar el colapso.

### Los nueve límites en juego

El estado del planeta se mide a través de los nueve límites planetarios. Cada uno se cuantifica en una escala de transgresión de 0 a 100, dividida en tres zonas: **zona segura** (0–32), **zona de riesgo** (33–65) y **zona de alto riesgo** (66–100). La partida comienza con el planeta ya bajo presión:

| Límite planetario | Nivel inicial | Zona |
|---|:---:|:---:|
| Ciclos de nitrógeno y fósforo | 75 | 🔴 Alto riesgo |
| Integridad de la biósfera | 70 | 🔴 Alto riesgo |
| Nuevas entidades (plásticos) | 62 | 🟠 Riesgo |
| Cambio climático | 55 | 🟠 Riesgo |
| Cambios en los sistemas de suelo | 50 | 🟠 Riesgo |
| Agua verde | 48 | 🟠 Riesgo |
| Acidificación de los océanos | 32 | 🟢 Segura |
| Aerosoles atmosféricos | 28 | 🟢 Segura |
| Ozono estratosférico | 15 | 🟢 Segura |

### Cómo se juega

A lo largo de la partida tomas trece decisiones: diez *dilemas* de gobernanza intercalados con tres *pausas de saberes*. Cada dilema presenta una situación real la matriz energética, alimentar al mundo, el secamiento de la Amazonía, el planeta plástico, el ciclo del agua verde, las ciudades, la meta del crecimiento (PIB), la geoingeniería, la pesca de arrastre y la negociación Norte–Sur global con tres opciones de respuesta. Cada opción modifica los niveles de los límites y un indicador de bienestar social, y ofrece una retroalimentación que explica las consecuencias de la elección a la luz de la cartilla.

Las *pausas de saberes* son preguntas de opción múltiple sobre los contenidos del módulo (por ejemplo, cuántos límites planetarios existen, qué significa el «agua verde» o qué propone el concepto de *Capitaloceno*). Si aciertas, el conocimiento «sana»: se alivian automáticamente los dos límites más transgredidos. Así, el juego premia el aprendizaje como herramienta de transformación.

### La Tierra que reacciona

El corazón visual del juego es una **Tierra animada que gira en pantalla** y que **sana o se marchita** con cada decisión: los océanos, los continentes, las nubes y el esmog cambian según la salud planetaria. Un diagrama radial muestra simultáneamente el estado de los nueve límites, permitiendo ver de un vistazo cuáles están en zona segura, de riesgo o de alto riesgo. Esta retroalimentación inmediata convierte conceptos abstractos en una experiencia tangible.

### Finales posibles

El juego tiene seis desenlaces. Dos son *colapsos anticipados* que pueden interrumpir la partida en cualquier turno, y cuatro son *veredictos finales* que se otorgan al completar el recorrido hasta 2090. En todos los casos, lo que decide el final es el promedio de transgresión de los nueve límites y el nivel de bienestar social. Una regla atraviesa toda la partida y refuerza el mensaje del módulo: **no hay bienestar duradero fuera de la zona segura**. Cuando la degradación promedio es alta, el bienestar se erosiona turno a turno (sequías, desastres y desplazamientos) por más que la economía parezca prosperar.

#### Colapsos anticipados

Terminan la partida antes de 2090 si el planeta o la sociedad tocan fondo:

- **🏚️ Colapso social:** El bienestar social llega a cero. Sin capacidad de acción colectiva no hay transición posible. El final recuerda, con la cartilla, que la sustentabilidad también exige justicia entre seres humanos: sin acuerdos sobre la vida común, ninguna política ambiental se sostiene.
- **💀 Colapso planetario:** El sistema terrestre cambia de estado, ya sea porque la degradación promedio se vuelve extrema o porque varios límites se disparan al máximo simultáneamente. El final evoca el modelo *World3* de *Los límites del crecimiento* (1972), que anticipó una crisis del *business-as-usual* entre 2030 y 2040.

#### Veredictos al llegar a 2090

Si se completa el recorrido, el estado final del planeta determina cuál de estos cuatro finales se obtiene, ordenados del mejor al peor:

- **🌱 Guardiana/Guardián del Holoceno:** El mejor desenlace. Devolviste a la humanidad a un espacio operativo seguro *sin sacrificar el bienestar*: viviste con menos para vivir mejor. Requiere una degradación promedio baja y, a la vez, un bienestar alto (las dos cosas al tiempo), encarnando la idea de que los límites no son escasez, sino la condición para que la vida continúe.
- **🌍 Equilibrista planetario:** Mantuviste el sistema lejos del colapso, aunque varios límites siguen transgredidos. La reflexión apela a la *cultura de los límites* de **Giorgos Kallis**: la autolimitación es la condición para exigirle a la economía y a la política el respeto a los límites.
- **⚠️ Al borde del abismo:** El planeta llega a 2090 herido, con la mayoría de los límites en zona de riesgo o transgredidos. Cita a **Clive Hamilton**: incluso si detuviéramos todo hoy, podría tardar siglos volver a las maravillosas condiciones del Holoceno.
- **🔥 Una herencia rota:** El peor desenlace de 2090: las generaciones futuras heredan un planeta hostil. Recoge la advertencia de **Bruno Latour** sobre los «inverosímiles tiempos» en los que, mientras se nos anuncia el desastre, lo seguimos causando. El juego puede reiniciarse; el planeta real, no.

#### Puntajes de cada desenlace

Los umbrales se evalúan sobre dos cifras: la **transgresión promedio** de los nueve límites (0 = intactos, 100 = todos al máximo) y el **bienestar social** (0–100). Como el juego muestra en pantalla la *salud planetaria* (`= 100 − transgresión promedio`), se incluye también su equivalente:

| Desenlace | ¿Cuándo? | Transgresión promedio | Salud planetaria | Bienestar |
|---|---|:---:|:---:|:---:|
| 💀 **Colapso planetario** | En cualquier turno | ≥ 70 · o bien 3+ límites en ≥ 90 | ≤ 30 | — |
| 🏚️ **Colapso social** | En cualquier turno | — | — | = 0 |
| 🌱 **Guardiana/Guardián del Holoceno** | Al llegar a 2090 | < 42 | > 58 | ≥ 50 |
| 🌍 **Equilibrista planetario** | Al llegar a 2090 | < 52 | > 48 | — |
| ⚠️ **Al borde del abismo** | Al llegar a 2090 | < 64 | > 36 | — |
| 🔥 **Una herencia rota** | Al llegar a 2090 | 64 – 69 | 31 – 36 | — |

Los cuatro veredictos de 2090 se comprueban en ese orden y son excluyentes: se otorga el primero que se cumpla (por eso *Equilibrista* exige transgresión < 52 **pero sin llegar** a la condición de *Guardián*, y así sucesivamente). El mejor final es el único que impone dos condiciones a la vez (planeta sano **y** bienestar alto), reflejando que un espacio seguro sin justicia social no basta. Además, una regla continua penaliza cada turno el bienestar cuando la transgresión promedio es ≥ 58, de modo que dejar que el planeta se degrade arrastra tarde o temprano al colapso social.

Cada final cierra, así, con una reflexión que conecta la experiencia de juego con el pensamiento ambiental del módulo.

### Actividad del curso: dos mediciones y estadísticas

Además del juego libre, la plataforma incluye un modo pensado para usarse dentro del curso. La profesora abre desde un panel privado la **Prueba 1** al inicio del semestre y la **Prueba 2** al final. Cuando una prueba está abierta, cada estudiante se registra (el correo es el único dato obligatorio; nombre, sexo, edad y programa son opcionales) y su partida queda asociada a él. Al completar la Prueba 2, el estudiante ve un **comparativo** de su propio recorrido: cómo dejó el planeta al inicio frente al final del curso, el cambio en cada uno de los nueve límites y las decisiones de gobernanza que modificó.

La profesora dispone de una **pestaña de estadísticas** protegida por contraseña que reúne tres momentos: los resultados agregados de la Prueba 1, los de la Prueba 2 y la comparación entre ambas (para quienes hicieron las dos). Se muestran la distribución de desenlaces, la salud y el bienestar promedio, la transgresión media de cada límite, la demografía del grupo y las tasas de participación. Toda la información es agregada, sin exponer datos individuales. Cada semestre puede reiniciarse: al abrir uno nuevo, el anterior se archiva y queda disponible para consulta.

### Cómo está construido

El juego es una aplicación web desarrollada en Python con el microframework Flask. El motor del juego gestiona el estado, los efectos de cada decisión y las condiciones de fin; el contenido (límites, dilemas y preguntas) se basa directamente en la cartilla «Ciencia, conflictos y alternativas para el siglo XXI» (Orozco-Echeverri, Mira Bohórquez y Muñoz Fonnegra, UdeA). La interfaz emplea HTML, CSS animado y gráficos SVG para el planeta y el diagrama radial, y la biblioteca Chart.js (servida localmente, sin CDN) para las estadísticas. El registro de estudiantes y los resultados de las pruebas se guardan en una base de datos PostgreSQL. La aplicación está desplegada en la plataforma Railway y su código es abierto.

## Documentación técnica

### Ejecutar localmente

```bash
cd limites-planetarios
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# abre http://localhost:5000
```

El juego libre funciona sin más configuración. Para probar el modo del curso (registro, pruebas y estadísticas) hace falta una base PostgreSQL y dos variables de entorno:

```bash
export DATABASE_URL="postgresql://usuario:clave@localhost:5432/holoceno"
export PROFESOR_PASSWORD="una-clave-para-el-panel"
python app.py
```

Sin `DATABASE_URL`, la aplicación arranca igual pero en modo de juego libre y anónimo (no se registra ni se guarda nada). Un PostgreSQL local rápido para desarrollo:

```bash
docker run -d --name holoceno-pg -e POSTGRES_PASSWORD=clave \
  -e POSTGRES_DB=holoceno -p 5432:5432 postgres:16-alpine
```

### Variables de entorno

| Variable | Para qué |
|---|---|
| `SECRET_KEY` | Firma las sesiones de Flask. Usa un valor aleatorio largo. |
| `DATABASE_URL` | Cadena de conexión a PostgreSQL. Si falta, se desactiva el modo del curso. |
| `PROFESOR_PASSWORD` | Contraseña del panel docente (`/panel`) y de las estadísticas. |

### Desplegar en Railway

1. Sube esta carpeta a un repositorio de GitHub.
2. En [railway.app](https://railway.app): **New Project → Deploy from GitHub repo**.
3. Railway detecta Python con Nixpacks y usa el `Procfile` automáticamente.
4. Añade una base de datos: **New → Database → Add PostgreSQL**. Railway inyecta `DATABASE_URL` automáticamente en el servicio de la app.
5. En **Variables**, agrega `SECRET_KEY` (valor aleatorio largo) y `PROFESOR_PASSWORD` (la clave del panel).
6. En **Settings → Networking**, genera el dominio público (`Generate Domain`).
7. La profesora entra al panel en `TU-DOMINIO/panel`.

### Datos de demostración

La forma más fácil de previsualizar las estadísticas es desde el propio panel docente: en **`/panel`** hay una sección «Herramientas de demostración» con botones para **cargar** datos ficticios y **borrar** todo. Corre dentro de la app desplegada, así que no hay que instalar nada ni configurar la URL.

También hay dos scripts por línea de comandos que operan sobre la base indicada en `DATABASE_URL`:

```bash
python poblar_demo.py          # crea un semestre "DEMO" con estudiantes ficticios
python poblar_demo.py -n 80    # con 80 estudiantes
python borrar_datos.py         # borra TODOS los datos (pide confirmación)
```

En Railway se ejecutan con `railway run python poblar_demo.py`. Si el shell no recibe `DATABASE_URL`, pásala con `--url`:

```bash
python poblar_demo.py --url "$DATABASE_URL"
python poblar_demo.py --url "postgresql://usuario:clave@host:puerto/base"
```

Los datos son inventados y sirven solo para ver la interfaz.

### Estructura

```
app.py              # Rutas Flask, API del juego, registro, panel y estadísticas
game/motor.py       # Motor: estado, efectos, condiciones de fin, historial de decisiones
game/db.py          # Capa PostgreSQL: semestres, estudiantes y resultados
game/stats.py       # Agregaciones para la pestaña de estadísticas
game/data/          # Límites, dilemas y quiz (contenido del módulo)
templates/          # Inicio, juego, registro, comparativo, panel, estadísticas (Jinja2)
static/css|js|img   # Estilos, planeta animado, diagrama radial, Chart.js local
poblar_demo.py      # Puebla la base con datos ficticios (para ver las estadísticas)
borrar_datos.py     # Borra todos los datos de la base
```

## Referencias

Basado en la cartilla «Ciencia, conflictos y alternativas para el siglo XXI» (Orozco-Echeverri, Mira Bohórquez, Muñoz Fonnegra — UdeA) y en Rockström et al. (2009), Steffen et al. (2015), Persson et al. (2022) y Wang-Erlandsson et al. (2022). Referencias completas en la página de créditos del juego.
