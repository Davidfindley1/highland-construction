(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function setOpen(open) {
    if (!header || !toggle) return;
    header.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setOpen(!header.classList.contains("open"));
    });
  }

  if (nav) {
    nav.addEventListener("click", function (event) {
      if (event.target.tagName === "A") setOpen(false);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });

  var form = document.getElementById("quote-form");
  var thanks = document.getElementById("quote-thanks");

  if (form && thanks) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      form.hidden = true;
      thanks.hidden = false;
      thanks.setAttribute("tabindex", "-1");
      thanks.focus();
    });
  }
})();
