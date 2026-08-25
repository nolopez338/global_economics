(() => {
  "use strict";
  const api = window.MindMap = window.MindMap || {};
  if (api.initialised) return;
  api.initialised = true;
  api.roots = () => Array.from(document.querySelectorAll("[data-mind-map-presentation]"));
  api.features = api.features || new Map();
  api.register = (name, initialise) => {
    if (!name || typeof initialise !== "function" || api.features.has(name)) return;
    api.features.set(name, initialise);
    api.roots().forEach((root) => initialise(root));
  };
})();
