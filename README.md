# 🌍 Guardianes del Holoceno

Videojuego educativo sobre **límites planetarios**, construido con Flask.

> Evaluación Módulo 4 · Cátedra Ambiental · Universidad de Antioquia
> Estudiante: **Johan Granados Vega** (Programa de Estadística, FCEN)
> Profesora: **Cristina López-Gallego**

## ¿De qué trata?

Gobiernas el planeta entre 2025 y 2085. En cada turno tomas una decisión
(energía, agricultura, agua, plásticos, océanos, geoingeniería…) que afecta
los 9 límites planetarios definidos por Rockström et al. (2009). Una Tierra
animada gira en pantalla y **se degrada o sana visualmente** según tus
decisiones; un diagrama radial muestra el estado de cada límite. Entre
decisiones hay «pausas de saberes»: preguntas sobre la cartilla del módulo
que, si aciertas, alivian los límites más transgredidos.

## Ejecutar localmente

```bash
cd limites-planetarios
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# abre http://localhost:5000
```

## Desplegar en Railway

1. Sube esta carpeta a un repositorio de GitHub.
2. En [railway.app](https://railway.app): **New Project → Deploy from GitHub repo**.
3. Railway detecta Python con Nixpacks y usa el `Procfile` automáticamente.
4. En **Variables**, agrega `SECRET_KEY` con un valor aleatorio largo.
5. En **Settings → Networking**, genera el dominio público (`Generate Domain`).

## Estructura

```
app.py              # Rutas Flask y API del juego
game/motor.py       # Motor: estado, efectos, condiciones de fin
game/data/          # Límites, dilemas y quiz (contenido del módulo)
templates/          # Inicio, juego y créditos (Jinja2)
static/css|js|img   # Estilos, planeta animado, diagrama radial
```

## Referencias

Basado en la cartilla «Ciencia, conflictos y alternativas para el siglo XXI»
(Orozco-Echeverri, Mira Bohórquez, Muñoz Fonnegra — UdeA) y en Rockström et
al. (2009), Steffen et al. (2015), Persson et al. (2022) y Wang-Erlandsson
et al. (2022). Referencias completas en la página de créditos del juego.
