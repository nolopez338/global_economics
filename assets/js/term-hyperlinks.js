// Resolve reusable, declarative term-resource keys supplied by the page's map.
document.querySelectorAll("[data-gn-link]").forEach((element) => {
  const key = element.dataset.gnLink;
  const segments = key ? key.split(".") : [];
  let resolved = window.TERM_HYPERLINKS;

  for (const segment of segments) {
    if (!segment || typeof resolved !== "object" || resolved === null ||
        !Object.prototype.hasOwnProperty.call(resolved, segment)) {
      resolved = undefined;
      break;
    }
    resolved = resolved[segment];
  }

  if (segments.length < 2 || typeof resolved !== "string" || !resolved) {
    console.warn(`[Term hyperlinks] Missing or invalid link key: ${key || "(empty)"}`);
    element.removeAttribute("href");
    element.setAttribute("aria-disabled", "true");
    return;
  }

  element.href = resolved;
});
