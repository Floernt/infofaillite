/**
 * Filtres de la page « Questions fréquentes » (docs/faq/README.md).
 * Lit les blocs <details class="ifa-faq" data-profils="..."> et les titres H2
 * de section qui les précèdent. Filtres par profil, par thème et par mots ;
 * l'état se lit et s'écrit dans l'adresse (#profil=dirigeant&theme=creanciers&q=caution).
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

  // --- Recherche par mots ---------------------------------------------------
  // Chaque mot de la requête est cherché séparément (ordre indifférent), sans
  // accents ni mots vides, au singulier comme au pluriel et dans sa famille
  // (« déclarer » trouve « déclaration »).

  var STOP = ("a au aux avec ce ces cet cette d de des du elle en est et il ils je j l la le les " +
    "leur leurs ma mes mon ne ni nos notre nous on ou par pas pour qu que quel quelle quels quelles " +
    "qui sa se ses si son sont sur ta tes ton tu un une vos votre vous y suis puis peut dois doit " +
    "faut comment quoi quand").split(" ");

  function normalize(text) {
    return (text || "").toLowerCase()
      .replace(/œ/g, "oe").replace(/æ/g, "ae")
      .normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9]+/g, " ").trim();
  }

  // Racine grossière : retire les terminaisons courantes du français.
  function stem(word) {
    var m = word.match(/^(.{4,}?)(issements|issement|ations|ation|ements|ement|ments|ment|ions|ion|euses|euse|eurs|eur|ives|ive|ifs|if|ees|ee|es|er|ez|e|s|x)$/);
    return m ? m[1] : word;
  }

  function terms(query) {
    var seen = {};
    return normalize(query).split(" ").filter(function (w) {
      if (w.length < 2 || STOP.indexOf(w) >= 0 || seen[w]) return false;
      seen[w] = true;
      return true;
    }).map(function (w) {
      var root = stem(w);
      // Mots longs : tolère deux lettres d'écart (« responsable » / « responsabilité »)
      return { word: w, root: root.length >= 7 ? root.slice(0, root.length - 2) : root };
    });
  }

  function wordRoots(text) {
    return normalize(text).split(" ").map(stem);
  }

  // Un terme est trouvé si une racine du texte commence par la sienne.
  function hasTerm(roots, t) {
    for (var i = 0; i < roots.length; i++) {
      if (roots[i].lastIndexOf(t.root, 0) === 0) return true;
    }
    return false;
  }

  // Surlignage : enveloppe dans <mark> les mots dont la racine correspond.
  function unmark(el) {
    el.querySelectorAll("mark.ifa-hit").forEach(function (m) {
      m.replaceWith(document.createTextNode(m.textContent));
    });
    el.normalize();
  }

  function mark(el, ts) {
    if (!ts.length) return;
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var parts = node.nodeValue.split(/([A-Za-zÀ-ÖØ-öø-ÿœŒæÆ0-9]+)/);
      if (parts.length < 2) return;
      var hit = false;
      var frag = document.createDocumentFragment();
      parts.forEach(function (p, i) {
        var r = i % 2 ? stem(normalize(p)) : "";
        if (r && ts.some(function (t) { return r.lastIndexOf(t.root, 0) === 0; })) {
          var m = document.createElement("mark");
          m.className = "ifa-hit";
          m.textContent = p;
          frag.appendChild(m);
          hit = true;
        } else if (p) {
          frag.appendChild(document.createTextNode(p));
        }
      });
      if (hit) node.parentNode.replaceChild(frag, node);
    });
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
      q: fromHash.q || ""
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

    // Texte indexé une fois pour toutes : question (summary + identifiant) et réponse.
    // Un repère invisible marque la place d'origine de chaque question, pour la
    // remettre dans sa section après une recherche.
    items.forEach(function (d, i) {
      var s = d.querySelector("summary");
      d._qRoots = wordRoots((s ? s.textContent : "") + " " + d.id.replace(/-/g, " "));
      d._roots = wordRoots(d.textContent + " " + d.id.replace(/-/g, " "));
      d._index = i;
      d._home = document.createComment("");
      d.parentNode.insertBefore(d._home, d);
    });

    var search = document.createElement("input");
    search.type = "search";
    search.className = "ifa-faq-search";
    search.placeholder = "Rechercher : caution, délai de déclaration, salaire impayé…";
    search.setAttribute("aria-label", "Rechercher dans les questions");
    search.setAttribute("autocomplete", "off");
    search.setAttribute("enterkeyhint", "search");
    search.value = state.q;
    var timer = null;
    search.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { state.q = search.value; apply(true); }, 150);
    });
    search.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && search.value) {
        e.preventDefault();
        e.stopPropagation();
        search.value = "";
        state.q = "";
        apply(true);
      }
    });

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
      if (state.q.trim()) parts.push("q=" + encodeURIComponent(state.q.trim()));
      var url = window.location.pathname + window.location.search + (parts.length ? "#" + parts.join("&") : "");
      if (window.history && window.history.replaceState) window.history.replaceState(null, "", url);
    }

    function inFilters(d) {
      return (!state.profil || (" " + (d.dataset.profils || "") + " ").indexOf(" " + state.profil + " ") >= 0) &&
        (!state.theme || d.dataset.theme === state.theme);
    }

    function plural(n, word) { return n + " " + word + (n > 1 ? "s" : ""); }

    function resetFilters() {
      state.profil = null;
      state.theme = null;
      apply(true);
    }

    function setCount(text, linkLabel) {
      count.textContent = text;
      if (linkLabel) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "ifa-faq-reset";
        b.textContent = linkLabel;
        b.addEventListener("click", resetFilters);
        count.appendChild(document.createTextNode(" "));
        count.appendChild(b);
      }
    }

    function apply(updateHash) {
      var ts = terms(state.q);
      var filtered = !!(state.profil || state.theme);
      var shown = [];
      var full = 0;
      var outside = 0;

      if (!ts.length) {
        shown = items.filter(inFilters);
      } else {
        // Une question est retenue dès qu'elle contient l'un des mots.
        // Classement : d'abord le nombre de mots trouvés, puis le poids
        // (un mot présent dans l'intitulé de la question compte double).
        items.forEach(function (d) {
          d._hits = 0;
          d._score = 0;
          ts.forEach(function (t) {
            if (hasTerm(d._qRoots, t)) { d._hits++; d._score += 2; }
            else if (hasTerm(d._roots, t)) { d._hits++; d._score += 1; }
          });
        });
        shown = items.filter(function (d) { return d._hits && inFilters(d); });
        full = shown.filter(function (d) { return d._hits === ts.length; }).length;
        if (filtered) outside = items.filter(function (d) { return d._hits && !inFilters(d); }).length;
      }

      // Recherche : résultats classés par pertinence dans une liste unique ;
      // sans recherche, chaque question regagne sa section.
      if (ts.length) {
        shown.sort(function (a, b) {
          return (b._hits - a._hits) || (b._score - a._score) || (a._index - b._index);
        });
        shown.forEach(function (d) { results.appendChild(d); });
      } else {
        items.forEach(function (d) {
          if (d.parentNode === results) d._home.parentNode.insertBefore(d, d._home.nextSibling);
        });
      }

      // Peu de résultats : réponses dépliées ; sinon, questions seules
      var openAll = ts.length && shown.length <= 3;
      items.forEach(function (d) {
        var ok = shown.indexOf(d) >= 0;
        d.hidden = !ok;
        unmark(d);
        if (ts.length) {
          if (ok) mark(d, ts);
          d.open = ok && openAll;
          d._openedBySearch = d.open;
        } else if (d._openedBySearch) {
          d.open = false;
          d._openedBySearch = false;
        }
      });
      sections.forEach(function (s) {
        s[2].hidden = ts.length > 0 ||
          !items.some(function (d) { return d.dataset.theme === s[0] && !d.hidden; });
      });

      var n = shown.length;
      if (!ts.length) {
        setCount(n === items.length ? items.length + " questions" :
          (n ? plural(n, "question") + " sur " + items.length : "Aucune question ne correspond à ces filtres."),
          null);
      } else if (n) {
        var detail = "";
        if (ts.length > 1) {
          detail = full === n ? ", toutes avec l'ensemble des mots" :
            full ? " ; " + (full > 1 ? "les " + full + " premières contiennent" : "la première contient") + " tous les mots" :
            " ; aucune ne contient tous les mots";
        }
        setCount(plural(n, "question") + " pour « " + state.q.trim() + " »" + detail +
          (outside ? ", et " + outside + " hors des filtres sélectionnés." : "."),
          outside ? "Chercher dans toutes les questions" : null);
      } else if (outside) {
        setCount("Aucune question dans les filtres sélectionnés, mais " + plural(outside, "réponse") +
          " ailleurs dans la FAQ.", "Chercher dans toutes les questions");
      } else {
        setCount("Aucune question ne correspond à « " + state.q.trim() + " ». Essayez un autre mot (caution, délai, salaire…).",
          filtered ? "Retirer les filtres" : null);
      }
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
    var results = document.createElement("div");
    results.className = "ifa-faq-results";
    firstSection.parentNode.insertBefore(results, firstSection);
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
