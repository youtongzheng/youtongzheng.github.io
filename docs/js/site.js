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
