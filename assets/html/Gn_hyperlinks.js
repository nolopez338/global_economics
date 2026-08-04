// Replace GN_TM and these placeholder URLs when adapting the template.
const GN_HYPERLINKS = {
  GN_TM: {
    learningEvidenceDocumentOne: "https://example.com/replace-with-learning-evidence-document-one",
    learningEvidenceDocumentTwo: "https://example.com/replace-with-learning-evidence-document-two"
  }
};

// Resolve declarative dot-separated keys without exposing URL values in diagnostics.
document.querySelectorAll("[data-gn-link]").forEach((element) => {
  const key = element.dataset.gnLink;
  const segments = key ? key.split(".") : [];
  let resolved = GN_HYPERLINKS;

  for (const segment of segments) {
    if (!segment || typeof resolved !== "object" || resolved === null ||
        !Object.prototype.hasOwnProperty.call(resolved, segment)) {
      resolved = undefined;
      break;
    }
    resolved = resolved[segment];
  }

  if (segments.length < 2 || typeof resolved !== "string" || !resolved) {
    console.warn(`[GN hyperlinks] Missing or invalid link key: ${key || "(empty)"}`);
    return;
  }

  element.href = resolved;
});
