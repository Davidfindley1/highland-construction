(function () {

  // FINANCING LINK (swap this one constant after Highland signs up with Acorn)
  // Until then, this is Acorn Finance's public homeowner apply page.
  // After signup, log in at https://my.acornfinance.com/ and replace the value
  // below with Highland's personalized partner / financing-page link.
  var ACORN_FINANCING_URL = "https://your.acornfinance.com/apply/";

  document.querySelectorAll("a.js-acorn-link").forEach(function (anchor) {
    anchor.href = ACORN_FINANCING_URL;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
  });

  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  var TOPIC = "highland-leads-30cqw0l9jkqz34xlx6yi";

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
  var errorBox = document.getElementById("quote-error");
  var submitBtn = document.getElementById("quote-submit");
  var retryBtn = document.getElementById("quote-retry");

  function field(name) {
    var el = form.elements[name];
    return el ? String(el.value).trim() : "";
  }

  function telLink(raw) {
    var digits = String(raw).replace(/\D/g, "");
    if (digits.length === 10) return "tel:+1" + digits;
    if (digits.length === 11 && digits.charAt(0) === "1") return "tel:+" + digits;
    if (digits) return "tel:+" + digits;
    return "";
  }

  function show(el) {
    if (form) form.hidden = true;
    if (thanks) thanks.hidden = true;
    if (errorBox) errorBox.hidden = true;
    if (el) {
      el.hidden = false;
      el.setAttribute("tabindex", "-1");
      el.focus();
    }
  }

  function showForm() {
    if (thanks) thanks.hidden = true;
    if (errorBox) errorBox.hidden = true;
    if (form) {
      form.hidden = false;
      var name = form.elements.name;
      if (name) name.focus();
    }
  }

  function setSending(on) {
    if (!form || !submitBtn) return;
    form.classList.toggle("is-sending", on);
    submitBtn.disabled = !!on;
    submitBtn.textContent = on ? "Sending…" : "Request a Quote";
  }

  function sendLead() {
    var name = field("name");
    var phone = field("phone");
    var click = telLink(phone);
    var lines = [
      "New quote request from the Highland Construction website.",
      "",
      "Name: " + (name || "—"),
      "Phone: " + (phone || "—"),
      "Email: " + (field("email") || "—"),
      "City/town: " + (field("city") || "—"),
      "Service: " + (field("project") || "—"),
      "Preferred contact time: " + (field("when") || "—"),
      "",
      "Project details:",
      field("message") || "—"
    ];
    var headers = {
      Title: "New Highland lead: " + (name || "Unknown"),
      Priority: "high",
      Tags: "house,telephone,construction"
    };
    if (click) {
      headers.Click = click;
      headers.Actions = "view, Call customer, " + click + ", clear=true";
    }
    return fetch("https://ntfy.sh/" + TOPIC, {
      method: "POST",
      body: lines.join("\n"),
      headers: headers
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
    });
  }

  if (form && thanks) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      // Honeypot: pretend to succeed, do not notify.
      if (field("website")) {
        show(thanks);
        return;
      }
      if (!form.reportValidity()) return;
      setSending(true);
      sendLead()
        .then(function () { show(thanks); })
        .catch(function () { show(errorBox); })
        .then(function () { setSending(false); });
    });
  }

  if (retryBtn) {
    retryBtn.addEventListener("click", showForm);
  }
})();
