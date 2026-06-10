/* Guardianes del Holoceno — lógica del cliente */

const $ = (id) => document.getElementById(id);

const FRASES_SALUD = {
  exuberante: "La Tierra florece: los ecosistemas se regeneran y el Holoceno respira.",
  estable: "El planeta se mantiene estable, pero varios límites siguen en zona de riesgo.",
  degradado: "La degradación es visible: smog, suelos secos y océanos opacos.",
  critico: "Estado crítico: el sistema terrestre se acerca a puntos de no retorno.",
  colapso: "El planeta agoniza. Los límites transgredidos detonan cambios en cascada.",
};

const RESULTADOS = {
  guardian: {
    titulo: "🌱 Guardiana/Guardián del Holoceno",
    texto: "Lograste devolver a la humanidad a un espacio operativo seguro sin sacrificar el bienestar: viviste con menos para vivir mejor. Como propone la cartilla, reconociste los límites no como escasez, sino como la condición para que la vida —humana y no humana— continúe.",
  },
  equilibrista: {
    titulo: "🌍 Equilibrista planetario",
    texto: "Mantuviste el sistema terrestre lejos del colapso, aunque varios límites siguen transgredidos. La cultura de los límites que propone Kallis exige más: la autolimitación es la condición para exigirle a la economía y a la política el respeto a los límites.",
  },
  al_borde: {
    titulo: "⚠️ Al borde del abismo",
    texto: "El planeta llega a 2090 herido: la mayoría de los límites están en zona de riesgo o transgredidos. Como advierte Clive Hamilton, incluso si detuviéramos todo hoy, podría tardar siglos volver a las maravillosas condiciones del Holoceno.",
  },
  herencia_rota: {
    titulo: "🔥 Una herencia rota",
    texto: "Las generaciones de 2090 heredan un planeta hostil. Vivimos los inverosímiles tiempos, dice Latour, en los que mientras se nos advierte del desastre, lo seguimos causando. El juego puede reiniciarse; el planeta real, no.",
  },
  colapso_planetario: {
    titulo: "💀 Colapso planetario",
    texto: "Demasiados límites cruzaron la zona de alto riesgo y el sistema terrestre cambió de estado. El modelo World3 lo predijo en 1972: con el business-as-usual, la crisis llegaría entre 2030 y 2040. No era una metáfora.",
  },
  colapso_social: {
    titulo: "🏚️ Colapso social",
    texto: "El bienestar social se desplomó y con él toda capacidad de acción colectiva. La sustentabilidad, recuerda la cartilla, también exige justicia entre seres humanos: sin acuerdos sobre la vida común no hay transición posible.",
  },
};

let bloqueado = false;

function claseSalud(salud) {
  if (salud >= 72) return "exuberante";
  if (salud >= 54) return "estable";
  if (salud >= 36) return "degradado";
  if (salud >= 18) return "critico";
  return "colapso";
}

function pintarPlaneta(salud) {
  const planeta = $("planeta");
  const estado = claseSalud(salud);
  planeta.className = "planeta salud-" + estado;
  $("estado-planeta").textContent = FRASES_SALUD[estado];
}

function pulsoPlaneta() {
  const planeta = $("planeta");
  planeta.classList.remove("pulso");
  void planeta.offsetWidth; // reinicia la animación
  planeta.classList.add("pulso");
}

function pintarMedidores(estado) {
  $("anio").textContent = estado.anio;
  const salud = $("medidor-salud");
  salud.style.width = estado.salud + "%";
  salud.style.backgroundColor =
    estado.salud >= 54 ? "#79b06a" : estado.salud >= 36 ? "#e9c46a" : "#e76f51";
  const bien = $("medidor-bienestar");
  bien.style.width = estado.bienestar + "%";
  bien.style.backgroundColor =
    estado.bienestar >= 50 ? "#e9c46a" : estado.bienestar >= 25 ? "#e76f51" : "#c1442e";
}

/* ---------- Diagrama radial de los 9 límites ---------- */
const COLORES_ZONA = { segura: "#79b06a", riesgo: "#e9c46a", alto: "#e76f51" };
const CENTRO = 160, R_BASE = 34, R_MAX = 140, R_LIMITE = R_BASE + (R_MAX - R_BASE) * 0.33;

function puntoPolar(angulo, radio) {
  const rad = ((angulo - 90) * Math.PI) / 180;
  return [CENTRO + radio * Math.cos(rad), CENTRO + radio * Math.sin(rad)];
}

function trazarCuna(a0, a1, r) {
  const [x0, y0] = puntoPolar(a0, R_BASE);
  const [x1, y1] = puntoPolar(a0, r);
  const [x2, y2] = puntoPolar(a1, r);
  const [x3, y3] = puntoPolar(a1, R_BASE);
  return `M ${x0} ${y0} L ${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2} L ${x3} ${y3} A ${R_BASE} ${R_BASE} 0 0 0 ${x0} ${y0} Z`;
}

function pintarDiagrama(limites) {
  const svg = $("diagrama");
  const ns = "http://www.w3.org/2000/svg";
  svg.innerHTML = "";

  const paso = 360 / limites.length;
  limites.forEach((limite, i) => {
    const a0 = i * paso + 2, a1 = (i + 1) * paso - 2;
    const radio = R_BASE + ((R_MAX - R_BASE) * limite.nivel) / 100;
    const cuna = document.createElementNS(ns, "path");
    cuna.setAttribute("d", trazarCuna(a0, a1, Math.max(radio, R_BASE + 4)));
    cuna.setAttribute("fill", COLORES_ZONA[limite.zona]);
    cuna.setAttribute("class", "cuna");
    cuna.addEventListener("click", () => mostrarInfo(limite));
    const titulo = document.createElementNS(ns, "title");
    titulo.textContent = `${limite.nombre}: nivel ${limite.nivel}/100`;
    cuna.appendChild(titulo);
    svg.appendChild(cuna);

    const [ex, ey] = puntoPolar((a0 + a1) / 2, R_MAX + 13);
    const texto = document.createElementNS(ns, "text");
    texto.setAttribute("x", ex);
    texto.setAttribute("y", ey);
    texto.setAttribute("text-anchor", "middle");
    texto.setAttribute("dominant-baseline", "middle");
    texto.setAttribute("font-size", "10.5");
    texto.setAttribute("font-weight", "700");
    texto.setAttribute("fill", "#56636e");
    texto.textContent = limite.corto;
    svg.appendChild(texto);
  });

  // círculo punteado: el límite (frontera de la zona segura)
  const frontera = document.createElementNS(ns, "circle");
  frontera.setAttribute("cx", CENTRO);
  frontera.setAttribute("cy", CENTRO);
  frontera.setAttribute("r", R_LIMITE);
  frontera.setAttribute("fill", "none");
  frontera.setAttribute("stroke", "#20303c");
  frontera.setAttribute("stroke-dasharray", "5 4");
  frontera.setAttribute("stroke-width", "1.6");
  frontera.setAttribute("opacity", "0.7");
  svg.appendChild(frontera);

  const nucleo = document.createElementNS(ns, "circle");
  nucleo.setAttribute("cx", CENTRO);
  nucleo.setAttribute("cy", CENTRO);
  nucleo.setAttribute("r", R_BASE - 6);
  nucleo.setAttribute("fill", "#1c5d99");
  svg.appendChild(nucleo);
}

function mostrarInfo(limite) {
  $("info-limite").classList.remove("oculto");
  $("info-nombre").textContent = `${limite.nombre} — nivel ${limite.nivel}/100 (zona ${
    limite.zona === "alto" ? "de alto riesgo" : limite.zona === "riesgo" ? "de riesgo" : "segura"
  })`;
  $("info-descripcion").textContent = limite.descripcion;
  $("info-referencia").textContent = limite.referencia;
}

/* ---------- Tarjetas y flujo de turnos ---------- */
function pintarTarjeta(estado) {
  const tarjeta = $("tarjeta");
  if (estado.terminado || !estado.tarjeta) {
    tarjeta.classList.add("oculto");
    return;
  }
  const t = estado.tarjeta;
  tarjeta.classList.remove("oculto");
  tarjeta.classList.toggle("es-quiz", t.tipo === "quiz");
  $("tarjeta-tipo").textContent =
    t.tipo === "quiz" ? "Pausa de saberes · responde bien y el planeta sana" : `Decisión ${estado.turno + 1} de ${estado.total_turnos}`;
  $("tarjeta-titulo").textContent = t.titulo;
  $("tarjeta-contexto").textContent = t.contexto;

  const caja = $("opciones");
  caja.innerHTML = "";
  t.opciones.forEach((texto, i) => {
    const boton = document.createElement("button");
    boton.className = "opcion";
    boton.textContent = texto;
    boton.addEventListener("click", () => decidir(i));
    caja.appendChild(boton);
  });
}

function pintarCambios(respuesta) {
  const caja = $("cambios");
  caja.innerHTML = "";
  const nombres = {
    clima: "Clima", biosfera: "Biósfera", biogeoquimicos: "N y P", suelo: "Suelos",
    entidades: "Plásticos", agua: "Agua", oceanos: "Océanos", ozono: "Ozono", aerosoles: "Aerosoles",
  };
  Object.entries(respuesta.efectos || {}).forEach(([clave, delta]) => {
    if (!delta) return;
    const ficha = document.createElement("span");
    ficha.className = "ficha " + (delta > 0 ? "sube" : "baja");
    ficha.textContent = `${nombres[clave]} ${delta > 0 ? "▲ se degrada" : "▼ sana"}`;
    caja.appendChild(ficha);
  });
  const bien = respuesta.bienestar || 0;
  if (bien) {
    const ficha = document.createElement("span");
    ficha.className = "ficha " + (bien > 0 ? "baja" : "sube");
    ficha.textContent = `Bienestar ${bien > 0 ? "▲" : "▼"}`;
    caja.appendChild(ficha);
  }
}

async function decidir(opcion) {
  if (bloqueado) return;
  bloqueado = true;
  document.querySelectorAll(".opcion").forEach((b) => (b.disabled = true));

  const res = await fetch("/api/decidir", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ opcion }),
  });
  const datos = await res.json();
  if (datos.error) { bloqueado = false; return; }

  const { respuesta, estado } = datos;
  ultimoEstado = estado;

  // Mostrar consecuencias
  $("tarjeta").classList.add("oculto");
  const feedback = $("feedback");
  feedback.classList.remove("oculto");
  $("feedback-tipo").textContent =
    respuesta.tipo === "quiz"
      ? respuesta.acierto ? "✓ ¡Correcto!" : `✗ La respuesta era: ${respuesta.correcta}`
      : "Consecuencias";
  $("feedback-texto").textContent = respuesta.feedback;
  pintarCambios(respuesta);

  // El planeta reacciona de inmediato
  pulsoPlaneta();
  pintarPlaneta(estado.salud);
  pintarMedidores(estado);
  pintarDiagrama(estado.limites);
  bloqueado = false;
}

function continuar() {
  $("feedback").classList.add("oculto");
  if (ultimoEstado.terminado) {
    const resultado = RESULTADOS[ultimoEstado.resultado] || RESULTADOS.equilibrista;
    $("final-titulo").textContent = resultado.titulo;
    $("final-texto").textContent = resultado.texto;
    $("final").classList.remove("oculto");
  } else {
    pintarTarjeta(ultimoEstado);
  }
}

let ultimoEstado = null;

async function iniciar() {
  const res = await fetch("/api/estado");
  ultimoEstado = await res.json();
  pintarPlaneta(ultimoEstado.salud);
  pintarMedidores(ultimoEstado);
  pintarDiagrama(ultimoEstado.limites);
  if (ultimoEstado.terminado) {
    const resultado = RESULTADOS[ultimoEstado.resultado] || RESULTADOS.equilibrista;
    $("final-titulo").textContent = resultado.titulo;
    $("final-texto").textContent = resultado.texto;
    $("final").classList.remove("oculto");
    $("tarjeta").classList.add("oculto");
  } else {
    pintarTarjeta(ultimoEstado);
  }
  $("continuar").addEventListener("click", continuar);
}

iniciar();
