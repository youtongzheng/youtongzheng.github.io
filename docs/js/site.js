// Publication search and filters (only runs on the Publications page).
(function () {
  var search = document.getElementById("pub-search");
  if (!search) return;
  var chips = document.querySelectorAll(".chip[data-filter]");
  var filter = "all";

  function apply() {
    var q = search.value.trim().toLowerCase();
    var shown = 0;
    document.querySelectorAll(".pub-year").forEach(function (sec) {
      var any = false;
      sec.querySelectorAll(".pub").forEach(function (li) {
        var ok = (filter === "all" || li.dataset[filter] === "1") &&
                 (!q || li.dataset.text.indexOf(q) !== -1);
        li.hidden = !ok;
        if (ok) { any = true; shown++; }
      });
      sec.hidden = !any;
    });
    document.getElementById("pub-empty").hidden = shown > 0;
  }

  search.addEventListener("input", apply);
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      chips.forEach(function (x) { x.classList.remove("active"); });
      c.classList.add("active");
      filter = c.dataset.filter;
      apply();
    });
  });
})();

// Live weather: reload each image on its own schedule with a cache-busting query.
(function () {
  var imgs = document.querySelectorAll("img.live");
  if (!imgs.length) return;
  function stamp(img) {
    var s = img.closest("figure").querySelector(".stamp");
    if (s) s.textContent = "loaded " + new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }
  imgs.forEach(function (img) {
    var base = img.dataset.src;
    var mins = parseFloat(img.dataset.refresh) || 5;
    function load() { img.src = base + (base.indexOf("?") < 0 ? "?" : "&") + "t=" + Date.now(); }
    img.addEventListener("load", function () { stamp(img); });
    load();
    setInterval(load, mins * 60 * 1000);
  });
  // Also refresh everything when the tab becomes visible again.
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") {
      imgs.forEach(function (img) { img.src = img.dataset.src + "?t=" + Date.now(); });
    }
  });
})();
