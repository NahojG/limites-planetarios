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

Comprender este marco constituye uno de los objetivos centrales del Módulo 4 de la Cátedra Ambiental. En esa dirección, este trabajo propone el desarrollo de un recurso pedagógico interactivo: el videojuego educativo *Guardianes del Holoceno*. En él, la persona que juega asume la responsabilidad de gobernar el planeta y experimenta, de manera vivencial, cómo las decisiones colectivas pueden degradar o restaurar las condiciones que sostienen la vida en la Tierra. Así, el juego convierte los conceptos abordados en la cartilla del módulo —los límites planetarios, el Antropoceno y el Capitaloceno, la cultura de los límites y la justicia socioambiental— en mecánicas concretas, dilemas con consecuencias y una representación visual del estado del sistema terrestre.

Este documento presenta el proyecto: sus objetivos, la descripción detallada del interactivo y los enlaces de acceso a la versión desplegada en la web y al código fuente abierto.

## Objetivos

### Objetivo general

Diseñar y desarrollar un videojuego educativo interactivo, accesible desde la web, que comunique de forma vivencial el concepto de los nueve límites planetarios y los contenidos del Módulo 4 de la Cátedra Ambiental, de modo que quien juega comprenda la interdependencia entre las decisiones humanas y la estabilidad del sistema terrestre.

### Objetivos específicos

- Traducir los nueve límites planetarios definidos por Rockström *et al.* (2009) y actualizados por Steffen *et al.* (2015), Persson *et al.* (2022) y Wang-Erlandsson *et al.* (2022) en variables medibles dentro de una mecánica de juego por turnos.
- Representar visualmente la degradación y la recuperación del planeta mediante una Tierra animada y un diagrama radial que reflejan, en tiempo real, las consecuencias de cada decisión.
- Integrar *pausas de saberes* (preguntas tipo quiz) que refuercen los conceptos clave de la cartilla y recompensen el aprendizaje aliviando los límites más transgredidos.
- Evidenciar las dimensiones de justicia socioambiental —la responsabilidad diferenciada entre el Norte y el Sur global— y la noción de Capitaloceno como parte ineludible de la crisis planetaria.
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

A lo largo de la partida tomas trece decisiones: diez *dilemas* de gobernanza intercalados con tres *pausas de saberes*. Cada dilema presenta una situación real —la matriz energética, alimentar al mundo, el secamiento de la Amazonía, el planeta plástico, el ciclo del agua verde, las ciudades, la meta del crecimiento (PIB), la geoingeniería, la pesca de arrastre y la negociación Norte–Sur global— con tres opciones de respuesta. Cada opción modifica los niveles de los límites y un indicador de bienestar social, y ofrece una retroalimentación que explica las consecuencias de la elección a la luz de la cartilla.

Las *pausas de saberes* son preguntas de opción múltiple sobre los contenidos del módulo (por ejemplo, cuántos límites planetarios existen, qué significa el «agua verde» o qué propone el concepto de *Capitaloceno*). Si aciertas, el conocimiento «sana»: se alivian automáticamente los dos límites más transgredidos. Así, el juego premia el aprendizaje como herramienta de transformación.

### La Tierra que reacciona

El corazón visual del juego es una **Tierra animada que gira en pantalla** y que **sana o se marchita** con cada decisión: los océanos, los continentes, las nubes y el esmog cambian según la salud planetaria. Un diagrama radial muestra simultáneamente el estado de los nueve límites, permitiendo ver de un vistazo cuáles están en zona segura, de riesgo o de alto riesgo. Esta retroalimentación inmediata convierte conceptos abstractos en una experiencia tangible.

### Finales posibles

La partida puede terminar de forma anticipada por un colapso social (si el bienestar se desploma) o un colapso planetario (si demasiados límites cruzan la zona de alto riesgo). Si se completa el recorrido hasta 2090, el resultado depende del estado final del planeta: 🟢 **Guardiana/Guardián del Holoceno** (espacio seguro recuperado sin sacrificar el bienestar), *Equilibrista planetario*, *Al borde del abismo* o 🔴 **Una herencia rota**. Cada final cierra con una reflexión de autores como Kallis, Hamilton o Latour, conectando la experiencia de juego con el pensamiento ambiental del módulo.

### Cómo está construido

El juego es una aplicación web desarrollada en Python con el microframework Flask. El motor del juego gestiona el estado, los efectos de cada decisión y las condiciones de fin; el contenido (límites, dilemas y preguntas) se basa directamente en la cartilla «Ciencia, conflictos y alternativas para el siglo XXI» (Orozco-Echeverri, Mira Bohórquez y Muñoz Fonnegra, UdeA). La interfaz emplea HTML, CSS animado y gráficos SVG para el planeta y el diagrama radial. La aplicación está desplegada en la plataforma Railway y su código es abierto.

## Documentación técnica

### Ejecutar localmente

```bash
cd limites-planetarios
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# abre http://localhost:5000
```

### Desplegar en Railway

1. Sube esta carpeta a un repositorio de GitHub.
2. En [railway.app](https://railway.app): **New Project → Deploy from GitHub repo**.
3. Railway detecta Python con Nixpacks y usa el `Procfile` automáticamente.
4. En **Variables**, agrega `SECRET_KEY` con un valor aleatorio largo.
5. En **Settings → Networking**, genera el dominio público (`Generate Domain`).

### Estructura

```
app.py              # Rutas Flask y API del juego
game/motor.py       # Motor: estado, efectos, condiciones de fin
game/data/          # Límites, dilemas y quiz (contenido del módulo)
templates/          # Inicio, juego y créditos (Jinja2)
static/css|js|img   # Estilos, planeta animado, diagrama radial
```

## Referencias

Basado en la cartilla «Ciencia, conflictos y alternativas para el siglo XXI» (Orozco-Echeverri, Mira Bohórquez, Muñoz Fonnegra — UdeA) y en Rockström et al. (2009), Steffen et al. (2015), Persson et al. (2022) y Wang-Erlandsson et al. (2022). Referencias completas en la página de créditos del juego.
