(() => {
  const key = "vis-guardian-ui";
  const languages = ["en", "fr", "es"];
  const copy = {
    fr: {
      skip:"Aller au contenu",education:"Education",evidence:"Preuves",primitives:"Primitives",boundaries:"Limites",source:"Source",
      eyebrow:"NIVEAU 4 / INTEGRITE VISUELLE / PRE-ALPHA PUBLIQUE",subtitle:"Des preuves visuelles sans accusation automatique.",
      intro:"V.I.S Guardian transforme contour, mouvement, saillance, occlusion, continuite et contradiction de scene en primitives de metadonnees. Neutro mesure l incertitude; un humain revise chaque cas non resolu.",
      inspect:"Inspecter le parcours de preuve",exploreSource:"Explorer le code source",local:"Local-first",metadata:"Metadonnees seulement par defaut",noFace:"Aucune reconnaissance faciale",human:"Revision humaine requise",
      observed:"Observe",inferred:"Infere",unknown:"Inconnu",consoleKicker:"REJEU SYNTHETIQUE / SURFACE DE REVISION",consoleTitle:"Une contradiction devient un dossier de revision, jamais un verdict.",synthetic:"Donnees synthetiques",
      ledgerTitle:"Registre de preuves",contour:"Contour",motion:"Mouvement",occlusion:"Occlusion",continuity:"Continuite de piste",contradiction:"Contradiction de scene",review:"Revision",reviewRequired:"REVISION REQUISE",unresolved:"Divergence panier / POS non resolue",
      reviewBody:"Les preuves ne concordent pas. Le systeme preserve les references et demande une revision humaine; il n identifie personne et ne pretend pas qu un acte fautif a eu lieu.",decision:"Decision",humanPending:"Revision humaine en attente",
      workflowKicker:"DU SIGNAL A LA REVISION",workflowTitle:"Quatre etapes bornees",stage1:"Creer une piste anonyme",stage1Body:"Un track_id temporaire limite un rejeu synthetique sans lier une identite reelle.",
      stage2:"Extraire de petites primitives",stage2Body:"Contour, mouvement, saillance, occlusion et continuite restent des metadonnees inspectables.",stage3:"Reconcilier les canaux",stage3Body:"Les preuves visuelles sont comparees au panier, au POS, a l inventaire et a la fermeture de caisse.",
      stage4:"Escalader l ambiguite",stage4Body:"Une contradiction produit un dossier a reviser par un operateur humain.",primitiveKicker:"SURFACE REELLE DU CODE",primitiveTitle:"Primitives d integrite visuelle",
      contourBody:"Enregistre une limite d objet sans attribuer identite ou intention.",motionBody:"Capture le changement visuel dans les mouvements de tablette, panier et caisse.",saliency:"Saillance",saliencyBody:"Indique une pression d attention. C est un signal a inspecter, jamais une preuve.",
      occlusionBody:"Enregistre une visibilite bloquee et augmente l incertitude plutot que de deviner.",continuityBody:"Mesure si des observations appartiennent a une meme piste temporaire anonyme.",contradictionBody:"Capture les conflits entre preuves visuelles, POS, inventaire, panier ou caisse.",
      boundaryKicker:"CONFIDENTIALITE / SECURITE / AUTORITE HUMAINE",boundaryTitle:"Le systeme peut demander une revision. Il ne peut pas accuser.",boundaryBody:"V.I.S Guardian est une pre-alpha educative instable. Elle utilise le rejeu synthetique et des metadonnees par defaut pour enseigner la reconciliation des preuves tout en preservant la responsabilite humaine.",
      noFaceTitle:"Aucune reconnaissance faciale",noFaceBody:"Aucune identification biometrique ni correspondance d identite.",noFramesTitle:"Aucune conservation d images brutes",noFramesBody:"Le contrat actuel des primitives rejette les references aux medias bruts.",
      noAuthorityTitle:"Aucune autorite autonome",noAuthorityBody:"La sortie machine reste observee, inferee ou inconnue.",lawTitle:"Posture Loi 25",lawBody:"Une evaluation d impact est requise avant tout usage en production.",
      parent:"MARKET GUARDIAN / RETAILGUARD",finalTitle:"Preserver l incertitude. Reviser les preuves.",viewRepo:"Voir le depot",footerStatus:"Pre-alpha publique / education supervisee",
      localOnly:"PREFERENCES LOCALES",accessTitle:"Reglages d acces",accessBody:"Choisissez un profil de lecture pour ce navigateur. Aucun compte ni suivi.",base:"Base",calm:"Autisme calme",sprint:"Sprint TDAH",deep:"Travail profond",
      supportTitle:"Soutenir le developpement",supportBody:"Le soutien volontaire finance l ecosysteme de recherche SecuredMe Education. Il ne modifie ni les preuves, ni les resultats de revision, ni l acces, ni le statut du produit.",supportAction:"Ouvrir le soutien PayPal securise",supportNote:"Ce soutien n est pas un don de bienfaisance et ne produit aucun recu fiscal."
    },
    es: {
      skip:"Ir al contenido",education:"Educacion",evidence:"Evidencia",primitives:"Primitivas",boundaries:"Limites",source:"Fuente",
      eyebrow:"NIVEL 4 / INTEGRIDAD VISUAL / PRE-ALFA PUBLICA",subtitle:"Evidencia visual sin acusacion automatica.",
      intro:"V.I.S Guardian convierte contorno, movimiento, saliencia, oclusion, continuidad y contradiccion de escena en primitivas de metadatos. Neutro mide la incertidumbre; una persona revisa cada caso no resuelto.",
      inspect:"Inspeccionar el flujo de evidencia",exploreSource:"Explorar el codigo",local:"Local-first",metadata:"Solo metadatos por defecto",noFace:"Sin reconocimiento facial",human:"Revision humana requerida",
      observed:"Observado",inferred:"Inferido",unknown:"Desconocido",consoleKicker:"REPETICION SINTETICA / SUPERFICIE DE REVISION",consoleTitle:"Una contradiccion se convierte en un paquete de revision, no en un veredicto.",synthetic:"Datos sinteticos",
      ledgerTitle:"Registro de evidencia",contour:"Contorno",motion:"Movimiento",occlusion:"Oclusion",continuity:"Continuidad de pista",contradiction:"Contradiccion de escena",review:"Revision",reviewRequired:"REVISION REQUERIDA",unresolved:"Divergencia cesta / POS no resuelta",
      reviewBody:"La evidencia no concuerda. El sistema conserva referencias y solicita revision; no identifica a una persona ni afirma una infraccion.",decision:"Decision",humanPending:"Revision humana pendiente",
      workflowKicker:"DE LA SENAL A LA REVISION",workflowTitle:"Cuatro etapas acotadas",stage1:"Crear una pista anonima",stage1Body:"Un track_id temporal limita una repeticion sintetica sin vincular identidad real.",
      stage2:"Extraer primitivas pequenas",stage2Body:"Contorno, movimiento, saliencia, oclusion y continuidad siguen siendo metadatos inspeccionables.",stage3:"Reconciliar canales",stage3Body:"La evidencia visual se compara con cesta, POS, inventario y cierre de caja.",
      stage4:"Escalar la ambiguedad",stage4Body:"La contradiccion genera un paquete para revision humana.",primitiveKicker:"SUPERFICIE REAL DEL CODIGO",primitiveTitle:"Primitivas de integridad visual",
      contourBody:"Registra el limite de un objeto sin asignar identidad ni intencion.",motionBody:"Captura cambios visuales en movimientos de estante, cesta y caja.",saliency:"Saliencia",saliencyBody:"Marca presion de atencion. Es una pista para inspeccionar, nunca una prueba.",
      occlusionBody:"Registra visibilidad bloqueada y aumenta incertidumbre en vez de adivinar.",continuityBody:"Mide si las observaciones pertenecen a una pista temporal anonima.",contradictionBody:"Captura conflictos entre evidencia visual, POS, inventario, cesta o caja.",
      boundaryKicker:"PRIVACIDAD / SEGURIDAD / AUTORIDAD HUMANA",boundaryTitle:"El sistema puede pedir revision. No puede acusar.",boundaryBody:"V.I.S Guardian es una pre-alfa educativa inestable. Usa repeticion sintetica y metadatos por defecto para ensenar reconciliacion de evidencia preservando responsabilidad humana.",
      noFaceTitle:"Sin reconocimiento facial",noFaceBody:"Sin identificacion biometrica ni coincidencia de identidad.",noFramesTitle:"Sin persistencia de cuadros brutos",noFramesBody:"El contrato actual rechaza referencias a medios brutos.",
      noAuthorityTitle:"Sin autoridad autonoma",noAuthorityBody:"La salida permanece observada, inferida o desconocida.",lawTitle:"Postura Ley 25",lawBody:"Se requiere evaluacion de impacto antes de cualquier uso en produccion.",
      parent:"MARKET GUARDIAN / RETAILGUARD",finalTitle:"Preserva la incertidumbre. Revisa la evidencia.",viewRepo:"Ver repositorio",footerStatus:"Pre-alfa publica / educacion supervisada",
      localOnly:"PREFERENCIAS LOCALES",accessTitle:"Ajustes de acceso",accessBody:"Elige un perfil de lectura para este navegador. Sin cuenta ni seguimiento.",base:"Base",calm:"Autismo calma",sprint:"Sprint TDAH",deep:"Trabajo profundo",
      supportTitle:"Apoyar el desarrollo",supportBody:"El apoyo voluntario financia el ecosistema de investigacion de SecuredMe Education. No cambia evidencia, resultados, acceso ni estado del producto.",supportAction:"Abrir apoyo seguro de PayPal",supportNote:"Este apoyo no es una donacion caritativa y no produce recibo fiscal."
    }
  };
  const english = {};
  document.querySelectorAll("[data-copy]").forEach((el) => { english[el.dataset.copy] ??= el.textContent; });
  let state = { language:"en", theme:"dark", access:"base" };
  try { state = { ...state, ...JSON.parse(localStorage.getItem(key) || "{}") }; } catch {}
  const languageButton = document.getElementById("language-button");
  const themeButton = document.getElementById("theme-button");
  const accessButton = document.getElementById("access-button");
  const supportButton = document.getElementById("support-button");
  const accessModal = document.getElementById("access-modal");
  const supportModal = document.getElementById("support-modal");
  const label = {
    en:{language:"Language",theme:"Theme",night:"Night",day:"Day",access:"Access",support:"Support SecuredMe"},
    fr:{language:"Langue",theme:"Theme",night:"Nuit",day:"Jour",access:"Accessibilite",support:"Soutenir SecuredMe"},
    es:{language:"Idioma",theme:"Tema",night:"Noche",day:"Dia",access:"Acceso",support:"Apoyar SecuredMe"}
  };
  function render() {
    document.documentElement.lang = state.language;
    document.documentElement.dataset.theme = state.theme;
    document.documentElement.dataset.access = state.access;
    document.querySelectorAll("[data-copy]").forEach((el) => {
      const translated = state.language === "en" ? english[el.dataset.copy] : copy[state.language]?.[el.dataset.copy];
      if (translated) el.textContent = translated;
    });
    const l = label[state.language];
    languageButton.textContent = `${l.language}: ${state.language.toUpperCase()}`;
    themeButton.textContent = `${l.theme}: ${state.theme === "dark" ? l.night : l.day}`;
    accessButton.textContent = l.access;
    supportButton.textContent = l.support;
    document.querySelectorAll("[data-profile]").forEach((button) => button.classList.toggle("active", button.dataset.profile === state.access));
    localStorage.setItem(key, JSON.stringify(state));
  }
  languageButton.addEventListener("click", () => { state.language = languages[(languages.indexOf(state.language) + 1) % languages.length]; render(); });
  themeButton.addEventListener("click", () => { state.theme = state.theme === "dark" ? "light" : "dark"; render(); });
  accessButton.addEventListener("click", () => { accessModal.hidden = false; accessModal.querySelector("[data-close]").focus(); });
  supportButton.addEventListener("click", () => { supportModal.hidden = false; supportModal.querySelector("[data-close]").focus(); });
  document.querySelectorAll("[data-profile]").forEach((button) => button.addEventListener("click", () => { state.access = button.dataset.profile; render(); }));
  document.querySelectorAll(".modal-backdrop").forEach((modal) => {
    modal.querySelector("[data-close]").addEventListener("click", () => { modal.hidden = true; });
    modal.addEventListener("click", (event) => { if (event.target === modal) modal.hidden = true; });
  });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") document.querySelectorAll(".modal-backdrop").forEach((modal) => { modal.hidden = true; }); });
  render();
})();
