// Quote form: turns the form into a pre-filled WhatsApp message (no server needed).
(function () {
  var WA = "923152020525";
  var form = document.getElementById("quote-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = form.elements;
      var lines = [
        "Assalam o Alaikum, I want a quote.",
        "Name: " + f.name.value.trim(),
        "Area: " + f.area.value.trim(),
        "Interested in: " + f.need.value,
        f.bill.value ? "Monthly bill / units: " + f.bill.value.trim() : "",
        f.msg.value.trim() ? "Details: " + f.msg.value.trim() : ""
      ].filter(Boolean);
      window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
  }
  // Pre-select a package when arriving from a "Get price" link, e.g. contact.html?need=5kW
  var need = new URLSearchParams(location.search).get("need");
  var sel = document.getElementById("need");
  if (need && sel) {
    for (var i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value.indexOf(need) === 0) { sel.selectedIndex = i; break; }
    }
  }
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
