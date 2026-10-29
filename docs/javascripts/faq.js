/**
 * Filtres de la page « Questions fréquentes » (docs/faq/README.md).
 * Lit les blocs <details class="ifa-faq" data-profils="..."> et les titres H2
 * de section qui les précèdent. Filtres par profil, par thème et par mots ;
 * l'état se lit et s'écrit dans l'adresse (#profil=dirigeant&theme=creanciers).
 * Une ancre simple (#id-de-question) ouvre la question correspondante.
 * Sans JavaScript, toutes les questions restent affichées et dépliables.
 */
(function () {
  var PROFILS = {
    independant: "Indépendant",
    dirigeant: "Dirigeant de société",
    creancier: "Créancier",
    travailleur: "Travailleur"
  };

  function chip(label, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "ifa-tag";
    b.textContent = label;
    b.addEventListener("click", onClick);
    return b;
  }

  function normalize(text) {
    return (text || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }

  function readHash() {
    var out = {};
    var h = window.location.hash.replace(/^#/, "");
    if (h.indexOf("=") < 0) return out;
    h.split("&").forEach(function (part) {
      var kv = part.split("=");
      if (kv.length === 2) out[kv[0]] = decodeURIComponent(kv[1]);
    });
    return out;
  }

  function init() {
    var items = Array.prototype.slice.call(document.querySelectorAll("details.ifa-faq"));
    if (!items.length || document.querySelector(".ifa-filters")) return;

    // Section (H2) de chaque question
    var sections = [];
    items.forEach(function (d) {
      var el = d.previousElementSibling;
      while (el && el.tagName !== "H2") el = el.previousElementSibling;
      if (el && el.id) {
        d.dataset.theme = el.id;
        if (!sections.some(function (s) { return s[0] === el.id; })) {
          sections.push([el.id, el.childNodes[0].textContent.trim(), el]);
        }
      }
    });

    var fromHash = readHash();
    var state = {
      profil: PROFILS[fromHash.profil] ? fromHash.profil : null,
      theme: sections.some(function (s) { return s[0] === fromHash.theme; }) ? fromHash.theme : null,
      q: ""
    };

    var box = document.createElement("div");
    box.className = "ifa-filters ifa-faq-filters";
    box.setAttribute("role", "search");
    box.setAttribute("aria-label", "Filtrer les questions");

    function row(label, entries, key) {
      var r = document.createElement("div");
      r.className = "ifa-filters__row";
      r.dataset.key = key;
      var l = document.createElement("span");
      l.className = "ifa-filters__label";
      l.textContent = label;
      r.appendChild(l);
      r.appendChild(chip("Tous", function () { state[key] = null; apply(true); }));
      entries.forEach(function (e) {
        var c = chip(e[1], function () { state[key] = state[key] === e[0] ? null : e[0]; apply(true); });
        c.dataset.value = e[0];
        r.appendChild(c);
      });
      return r;
    }

    var search = document.createElement("input");
    search.type = "search";
    search.className = "ifa-faq-search";
    search.placeholder = "Rechercher dans les questions (ex. caution, délai, effacement)";
    search.setAttribute("aria-label", "Rechercher dans les questions");
    search.addEventListener("input", function () { state.q = normalize(search.value.trim()); apply(false); });

    box.appendChild(row("Je suis", Object.keys(PROFILS).map(function (p) { return [p, PROFILS[p]]; }), "profil"));
    box.appendChild(row("Thème", sections.map(function (s) { return [s[0], s[1]]; }), "theme"));
    box.appendChild(search);

    var count = document.createElement("p");
    count.className = "ifa-filters__empty ifa-faq-count";
    count.setAttribute("aria-live", "polite");

    function writeHash() {
      var parts = [];
      if (state.profil) parts.push("profil=" + state.profil);
      if (state.theme) parts.push("theme=" + state.theme);
      var url = window.location.pathname + window.location.search + (parts.length ? "#" + parts.join("&") : "");
      if (window.history && window.history.replaceState) window.history.replaceState(null, "", url);
    }

    function apply(updateHash) {
      var visible = 0;
      items.forEach(function (d) {
        var ok = (!state.profil || (" " + (d.dataset.profils || "") + " ").indexOf(" " + state.profil + " ") >= 0) &&
          (!state.theme || d.dataset.theme === state.theme) &&
          (!state.q || normalize(d.textContent).indexOf(state.q) >= 0);
        d.hidden = !ok;
        if (ok) visible++;
        // Une recherche par mots déplie les réponses pour montrer le contexte
        if (state.q) d.open = ok;
      });
      sections.forEach(function (s) {
        s[2].hidden = !items.some(function (d) { return d.dataset.theme === s[0] && !d.hidden; });
      });
      count.textContent = visible === items.length ? items.length + " questions" :
        (visible ? visible + " question" + (visible > 1 ? "s" : "") + " sur " + items.length : "Aucune question ne correspond à ces filtres.");
      box.querySelectorAll(".ifa-filters__row").forEach(function (r) {
        var current = state[r.dataset.key];
        r.querySelectorAll("button").forEach(function (b) {
          b.setAttribute("aria-pressed", String((b.dataset.value || null) === current));
        });
      });
      if (updateHash) writeHash();
    }

    var firstSection = sections.length ? sections[0][2] : items[0];
    firstSection.parentNode.insertBefore(box, firstSection);
    firstSection.parentNode.insertBefore(count, firstSection);
    apply(false);

    // Ancre vers une question : l'ouvrir et la rendre visible
    function openFromHash() {
      var id = window.location.hash.replace(/^#/, "");
      if (!id || id.indexOf("=") >= 0) return;
      var target = document.getElementById(id);
      if (target && target.tagName === "DETAILS") {
        target.hidden = false;
        target.open = true;
        target.scrollIntoView();
      }
    }
    openFromHash();
    window.addEventListener("hashchange", openFromHash);
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
