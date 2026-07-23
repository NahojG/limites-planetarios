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
  const fabricas = {};   // id de lienzo -> función(canvas) que crea la gráfica
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

  function crearBarras(canvas, etiquetas, valores, color, opciones) {
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

  function crearBarrasDobles(canvas, etiquetas, s1, s2, c, opciones) {
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

  function crearLineas(canvas, etiquetas, series, opciones) {
    return new Chart(canvas, {
      type: "line",
      data: {
        labels: etiquetas,
        datasets: series.map((s) => ({
          label: s.label,
          data: s.data,
          borderColor: s.color,
          backgroundColor: s.color,
          tension: 0.3,
          spanGaps: true,
          borderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        })),
      },
      options: opciones,
    });
  }

  // Registra la fábrica de una gráfica y la construye en su lienzo de la página.
  function registrar(id, fabrica) {
    const canvas = document.getElementById(id);
    if (!canvas) return null;
    fabricas[id] = fabrica;
    return fabrica(canvas);
  }

  function especificacionesPrueba(prefijo, d, c) {
    return [
      [prefijo + "-desenlaces", (cv) => crearBarras(cv, d.desenlaces.etiquetas, d.desenlaces.valores, c.azul, baseOpciones(c, { horizontal: true }))],
      [prefijo + "-limites", (cv) => crearBarras(cv, d.limites.etiquetas, d.limites.valores, (v) => colorZona(v, c), baseOpciones(c, { max: 100 }))],
      [prefijo + "-sexo", (cv) => crearBarras(cv, d.demografia.sexo.etiquetas, d.demografia.sexo.valores, c.azul, baseOpciones(c))],
      [prefijo + "-edad", (cv) => crearBarras(cv, d.demografia.edad.etiquetas, d.demografia.edad.valores, c.azul, baseOpciones(c))],
      [prefijo + "-programa", (cv) => crearBarras(cv, d.demografia.programa.etiquetas, d.demografia.programa.valores, c.azul, baseOpciones(c, { horizontal: true }))],
    ];
  }

  function especificacionesComparacion(d, c) {
    return [
      ["c-desenlaces", (cv) => crearBarrasDobles(cv, d.desenlaces.etiquetas, d.desenlaces.prueba1, d.desenlaces.prueba2, c, baseOpciones(c, { horizontal: true, leyenda: true }))],
      ["c-limites", (cv) => crearBarrasDobles(cv, d.limites.etiquetas, d.limites.prueba1, d.limites.prueba2, c, baseOpciones(c, { leyenda: true, max: 100 }))],
      ["c-decisiones", (cv) => crearBarras(cv, d.decisiones.etiquetas, d.decisiones.valores, c.azul, baseOpciones(c, { horizontal: true }))],
    ];
  }

  function especificacionesSemestres(d, c) {
    return [
      ["sem-salud", (cv) => crearLineas(cv, d.etiquetas, [
        { label: "Inicio", data: d.salud1, color: c.azul },
        { label: "Fin", data: d.salud2, color: c.naranja },
      ], baseOpciones(c, { leyenda: true, max: 100 }))],
      ["sem-mejora", (cv) => crearBarras(cv, d.etiquetas, d.mejora, c.verde, baseOpciones(c))],
      ["sem-participacion", (cv) => crearBarrasDobles(cv, d.etiquetas, d.participacion1, d.participacion2, c, baseOpciones(c, { leyenda: true }))],
    ];
  }

  function construir(tab) {
    if (construido[tab]) return;
    const c = colores();
    let specs = [];
    if (tab === "p1") specs = especificacionesPrueba("p1", DATOS.prueba1, c);
    else if (tab === "p2") specs = especificacionesPrueba("p2", DATOS.prueba2, c);
    else if (tab === "comp") specs = especificacionesComparacion(DATOS.comparacion, c);
    else if (tab === "sem") specs = especificacionesSemestres(DATOS.semestres, c);
    const hechos = specs.map(([id, f]) => registrar(id, f)).filter(Boolean);
    construido[tab] = hechos;
    charts = charts.concat(hechos);
  }

  // --- Modal para ampliar una gráfica ---
  const modal = document.getElementById("modal-grafico");
  const modalCanvas = document.getElementById("modal-grafico-canvas");
  const modalTitulo = document.getElementById("modal-grafico-titulo");
  let modalChart = null;

  function abrirModal(id, titulo) {
    if (!fabricas[id]) return;
    if (modalChart) modalChart.destroy();
    modalTitulo.textContent = titulo;
    modal.showModal();
    // El lienzo debe estar visible para que Chart.js lo mida bien.
    // Tipografía más grande para que sea legible al proyectar en un auditorio.
    const fuentePrevia = Chart.defaults.font.size;
    Chart.defaults.font.size = 18;
    modalChart = fabricas[id](modalCanvas);
    Chart.defaults.font.size = fuentePrevia;
  }
  function cerrarModal() {
    if (modalChart) { modalChart.destroy(); modalChart = null; }
    modal.close();
  }
  document.getElementById("modal-grafico-cerrar").addEventListener("click", cerrarModal);
  modal.addEventListener("click", (e) => { if (e.target === modal) cerrarModal(); });
  modal.addEventListener("close", () => { if (modalChart) { modalChart.destroy(); modalChart = null; } });

  document.querySelectorAll(".grafico").forEach((fig) => {
    fig.addEventListener("click", () => {
      const canvas = fig.querySelector("canvas");
      const cap = fig.querySelector("figcaption");
      if (canvas) abrirModal(canvas.id, cap ? cap.textContent.replace("⤢", "").trim() : "");
    });
  });

  // --- Pestañas ---
  const tabs = document.querySelectorAll(".tab");
  const paneles = { p1: "tab-p1", p2: "tab-p2", comp: "tab-comp", sem: "tab-sem" };
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

  if (window.Chart) {
    Chart.defaults.font.family = "Karla, sans-serif";
    Chart.defaults.color = colores().ink;
  }
  construir("p1");
})();
