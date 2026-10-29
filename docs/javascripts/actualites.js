/**
 * Filtres par type et par thème sur la liste des actualités.
 * Lit les attributs data-type / data-themes des blocs .ifa-note générés par
 * scripts/build_actualites.py. Sans JavaScript, la liste reste complète.
 */
(function () {
  var TYPES = { jurisprudence: "Jurisprudence", doctrine: "Doctrine", legislation: "Législation", pratique: "Pratique" };

  function chip(label, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "ifa-tag";
    b.textContent = label;
    b.addEventListener("click", onClick);
    return b;
  }

  function init() {
    var notes = Array.prototype.slice.call(document.querySelectorAll(".ifa-note"));
    if (!notes.length || document.querySelector(".ifa-filters")) return;

    // Libellés des thèmes repris des étiquettes déjà rendues dans la liste
    var themeLabels = {};
    notes.forEach(function (n) {
      n.querySelectorAll("a.ifa-tag").forEach(function (a) {
        var slug = (a.getAttribute("href") || "").split("#")[1];
        if (slug) themeLabels[slug] = a.textContent.trim();
      });
    });

    var state = { type: null, theme: null };
    var box = document.createElement("div");
    box.className = "ifa-filters";
    box.setAttribute("role", "group");
    box.setAttribute("aria-label", "Filtrer les notes");
    var empty = document.createElement("p");
    empty.className = "ifa-filters__empty";
    empty.textContent = "Aucune note ne correspond à ces filtres.";
    empty.hidden = true;

    function row(label, entries, key) {
      var r = document.createElement("div");
      r.className = "ifa-filters__row";
      var l = document.createElement("span");
      l.className = "ifa-filters__label";
      l.textContent = label;
      r.appendChild(l);
      r.appendChild(chip("Tous", function () { state[key] = null; apply(); }));
      entries.forEach(function (e) {
        var c = chip(e[1], function () { state[key] = state[key] === e[0] ? null : e[0]; apply(); });
        c.dataset.value = e[0];
        r.appendChild(c);
      });
      r.dataset.key = key;
      return r;
    }

    var usedTypes = Object.keys(TYPES).filter(function (t) {
      return notes.some(function (n) { return n.dataset.type === t; });
    });
    var usedThemes = Object.keys(themeLabels).sort(function (a, b) {
      return themeLabels[a].localeCompare(themeLabels[b], "fr");
    });
    box.appendChild(row("Type", usedTypes.map(function (t) { return [t, TYPES[t]]; }), "type"));
    box.appendChild(row("Thème", usedThemes.map(function (t) { return [t, themeLabels[t]]; }), "theme"));

    function apply() {
      var visible = 0;
      notes.forEach(function (n) {
        var ok = (!state.type || n.dataset.type === state.type) &&
          (!state.theme || (" " + n.dataset.themes + " ").indexOf(" " + state.theme + " ") >= 0);
        n.hidden = !ok;
        if (ok) visible++;
      });
      // Masque les titres d'année sans note visible
      document.querySelectorAll(".md-content h2").forEach(function (h) {
        var el = h.nextElementSibling, any = false;
        while (el && el.tagName !== "H2") {
          if (el.classList.contains("ifa-note") && !el.hidden) any = true;
          el = el.nextElementSibling;
        }
        if (/^\d{4}$/.test(h.textContent.replace(/\W/g, ""))) h.hidden = !any;
      });
      empty.hidden = visible > 0;
      box.querySelectorAll(".ifa-filters__row").forEach(function (r) {
        var current = state[r.dataset.key];
        r.querySelectorAll("button").forEach(function (b) {
          b.setAttribute("aria-pressed", String((b.dataset.value || null) === current));
        });
      });
    }

    var first = notes[0].previousElementSibling && notes[0].previousElementSibling.tagName === "H2"
      ? notes[0].previousElementSibling : notes[0];
    first.parentNode.insertBefore(box, first);
    first.parentNode.insertBefore(empty, first);
    apply();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
