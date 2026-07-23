/* Guardianes del Holoceno — estadísticas de la profesora (Chart.js local).
   Los colores se leen de las variables CSS para respetar el tema claro/oscuro.
   Solo se grafican agregados; nunca datos individuales. */
(function () {
  const DATOS = JSON.parse(document.getElementById("datos-stats").textContent);

  function css(nombre) {
    return getComputedStyle(document.body).getPropertyValue(nombre).trim();
  }
  function colores() {
    return {
      ink: css("--texto"),
      muted: css("--texto-suave"),
      grid: css("--borde"),
      azul: css("--azul"),
      naranja: css("--naranja"),
      verde: css("--verde-vivo"),
      ocre: css("--ocre"),
      rojo: css("--rojo"),
    };
  }
  // Color de cada barra de límite según su zona (segura/riesgo/alto riesgo).
  function colorZona(v, c) {
    if (v < 33) return c.verde;
    if (v < 66) return c.ocre;
    return c.rojo;
  }

  const construido = {}; // tab -> [charts]
  let charts = [];

  function baseOpciones(c, { horizontal = false, leyenda = false, max = null } = {}) {
    const ejeValor = { grid: { color: c.grid }, ticks: { color: c.muted }, beginAtZero: true };
    if (max !== null) ejeValor.max = max;
    const ejeCat = { grid: { display: false }, ticks: { color: c.ink } };
    return {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: horizontal ? "y" : "x",
      scales: horizontal ? { x: ejeValor, y: ejeCat } : { x: ejeCat, y: ejeValor },
      plugins: {
        legend: leyenda
          ? { display: true, labels: { color: c.ink, boxWidth: 12, boxHeight: 12 } }
          : { display: false },
        tooltip: { enabled: true },
      },
    };
  }

  function barras(id, etiquetas, valores, color, opciones) {
    const canvas = document.getElementById(id);
    if (!canvas) return null;
    const colorArr = typeof color === "function" ? valores.map(color) : color;
    return new Chart(canvas, {
      type: "bar",
      data: {
        labels: etiquetas,
        datasets: [{ data: valores, backgroundColor: colorArr, borderRadius: 4, borderSkipped: false }],
      },
      options: opciones,
    });
  }

  function barrasDobles(id, etiquetas, s1, s2, c, opciones) {
    const canvas = document.getElementById(id);
    if (!canvas) return null;
    return new Chart(canvas, {
      type: "bar",
      data: {
        labels: etiquetas,
        datasets: [
          { label: "Inicio", data: s1, backgroundColor: c.azul, borderRadius: 4, borderSkipped: false },
          { label: "Fin", data: s2, backgroundColor: c.naranja, borderRadius: 4, borderSkipped: false },
        ],
      },
      options: opciones,
    });
  }

  function construirPrueba(prefijo, d, c) {
    const salida = [];
    salida.push(barras(prefijo + "-desenlaces", d.desenlaces.etiquetas, d.desenlaces.valores,
      c.azul, baseOpciones(c, { horizontal: true })));
    salida.push(barras(prefijo + "-limites", d.limites.etiquetas, d.limites.valores,
      (v) => colorZona(v, c), baseOpciones(c, { max: 100 })));
    salida.push(barras(prefijo + "-sexo", d.demografia.sexo.etiquetas, d.demografia.sexo.valores,
      c.azul, baseOpciones(c)));
    salida.push(barras(prefijo + "-edad", d.demografia.edad.etiquetas, d.demografia.edad.valores,
      c.azul, baseOpciones(c)));
    salida.push(barras(prefijo + "-programa", d.demografia.programa.etiquetas, d.demografia.programa.valores,
      c.azul, baseOpciones(c, { horizontal: true })));
    return salida.filter(Boolean);
  }

  function construirComparacion(d, c) {
    const salida = [];
    salida.push(barrasDobles("c-desenlaces", d.desenlaces.etiquetas, d.desenlaces.prueba1, d.desenlaces.prueba2,
      c, baseOpciones(c, { horizontal: true, leyenda: true })));
    salida.push(barrasDobles("c-limites", d.limites.etiquetas, d.limites.prueba1, d.limites.prueba2,
      c, baseOpciones(c, { leyenda: true, max: 100 })));
    salida.push(barras("c-decisiones", d.decisiones.etiquetas, d.decisiones.valores,
      c.azul, baseOpciones(c, { horizontal: true })));
    return salida.filter(Boolean);
  }

  function construir(tab) {
    if (construido[tab]) return;
    const c = colores();
    let hechos = [];
    if (tab === "p1") hechos = construirPrueba("p1", DATOS.prueba1, c);
    else if (tab === "p2") hechos = construirPrueba("p2", DATOS.prueba2, c);
    else if (tab === "comp") hechos = construirComparacion(DATOS.comparacion, c);
    construido[tab] = hechos;
    charts = charts.concat(hechos);
  }

  // --- Pestañas ---
  const tabs = document.querySelectorAll(".tab");
  const paneles = { p1: "tab-p1", p2: "tab-p2", comp: "tab-comp" };
  tabs.forEach((t) =>
    t.addEventListener("click", () => {
      const destino = t.dataset.tab;
      tabs.forEach((x) => x.classList.toggle("activo", x === t));
      Object.entries(paneles).forEach(([clave, id]) => {
        const panel = document.getElementById(id);
        const activo = clave === destino;
        panel.classList.toggle("activo", activo);
        panel.hidden = !activo;
      });
      construir(destino);
      // Chart.js necesita recalcular al hacerse visible el lienzo.
      (construido[destino] || []).forEach((ch) => ch.resize());
    })
  );

  // Re-render al cambiar el tema: se rehacen las gráficas con los colores nuevos.
  const botonTema = document.getElementById("boton-tema");
  if (botonTema) {
    botonTema.addEventListener("click", () => {
      setTimeout(() => {
        charts.forEach((ch) => ch.destroy());
        charts = [];
        const activos = Object.keys(construido);
        for (const k in construido) delete construido[k];
        activos.forEach(construir);
      }, 50);
    });
  }

  // Ajustes globales de tipografía.
  if (window.Chart) {
    Chart.defaults.font.family = "Karla, sans-serif";
    Chart.defaults.color = colores().ink;
  }
  construir("p1");
})();
