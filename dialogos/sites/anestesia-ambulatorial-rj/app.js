const segmentos = [
  {
    nome: "Endoscopia diagnóstica e terapêutica",
    score: "A+",
    texto: "Alta compatibilidade com sedação ambulatorial, giro rápido e demanda recorrente."
  },
  {
    nome: "Medicina estética e dermatologia cirúrgica",
    score: "A",
    texto: "Mercado premium, sensível à experiência, conforto e recuperação rápida."
  },
  {
    nome: "Odontologia cirúrgica e implantodontia",
    score: "A-",
    texto: "Demanda por sedação segura em pacientes ansiosos e procedimentos longos."
  },
  {
    nome: "Reprodução humana",
    score: "B+",
    texto: "Procedimentos curtos, agenda programada e necessidade de acolhimento altamente qualificado."
  },
  {
    nome: "Oftalmologia",
    score: "B+",
    texto: "Grande volume potencial, com necessidade de fluxo padronizado e seleção rigorosa."
  },
  {
    nome: "Procedimentos guiados por imagem",
    score: "B",
    texto: "Intervenções percutâneas e diagnósticas podem se beneficiar de sedação estruturada."
  },
  {
    nome: "Pequenas cirurgias plásticas",
    score: "B",
    texto: "Potencial relevante, mas exige disciplina em seleção de risco e retaguarda."
  },
  {
    nome: "Dor intervencionista",
    score: "B",
    texto: "Demanda crescente em clínicas especializadas, com necessidade de protocolos por complexidade."
  }
];

const container = document.getElementById("segmentCards");

segmentos.forEach((segmento) => {
  const card = document.createElement("article");
  card.className = "segment-card";
  card.innerHTML = `
    <div class="score">${segmento.score}</div>
    <div>
      <h3>${segmento.nome}</h3>
      <p>${segmento.texto}</p>
    </div>
  `;
  container.appendChild(card);
});

const revealElements = document.querySelectorAll(".section, .hero-card, .segment-card, .driver-grid article, .step, .opportunity");

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealElements.forEach((element) => {
  element.classList.add("reveal");
  observer.observe(element);
});
