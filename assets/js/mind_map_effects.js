(() => {
  "use strict";
  if (window.MindMapEffects) return;
  const types = new Map();
  const sleep = (ms, signal) => new Promise((resolve) => {
    if (signal?.aborted) return resolve(false);
    const done = () => { signal?.removeEventListener("abort", abort); resolve(true); };
    const timer = setTimeout(done, Math.max(0, ms));
    const abort = () => { clearTimeout(timer); signal.removeEventListener("abort", abort); resolve(false); };
    signal?.addEventListener("abort", abort, { once: true });
  });
  const parse = (element, attribute) => {
    const value = element?.getAttribute(attribute);
    if (!value) return [];
    try { const result = JSON.parse(value); return Array.isArray(result) ? result : []; }
    catch (_) { console.warn(`Ignoring invalid mind-map configuration in ${attribute}.`); return []; }
  };
  const groups = (slide) => parse(slide, "data-mind-map-effect-groups")
    .map((group) => Array.isArray(group) ? group : group?.effects).filter(Array.isArray);
  const run = async ({ effect, signal, ...context }) => {
    if (!await sleep(Number(effect?.delay) || 0, signal)) return;
    const handler = types.get(effect?.type);
    if (handler && !signal?.aborted) await handler.run({ effect, signal, ...context });
  };
  const resetSlide = (slide) => {
    const configured = [...groups(slide).flat(), ...parse(slide, "data-mind-map-transition-forward"), ...parse(slide, "data-mind-map-transition-backward")];
    new Set(configured.map((effect) => types.get(effect?.type)?.reset).filter(Boolean)).forEach((reset) => reset({ slide }));
  };
  window.MindMapEffects = Object.freeze({
    register(type, runEffect, reset) {
      if (!type || types.has(type)) return;
      const handler = typeof runEffect === "function" ? { run: runEffect, reset } : runEffect;
      if (typeof handler?.run === "function") types.set(type, handler);
    },
    getGroupCount: (slide) => groups(slide).length,
    async runEffectGroup({ slide, groupIndex, signal }) {
      const group = groups(slide)[groupIndex];
      if (!group) return false;
      await Promise.all(group.map((effect) => run({ slide, effect, direction: "forward", signal })));
      return !signal?.aborted;
    },
    async runTransition({ slide, direction = "forward", ...context }) {
      const attribute = `data-mind-map-transition-${direction}`;
      const effects = parse(slide, attribute).map((effect, order) => ({ ...effect, _order: order }))
        .sort((a, b) => (Number(a.order) || 0) - (Number(b.order) || 0) || a._order - b._order);
      for (const effect of effects) await run({ slide, effect, direction, ...context });
    },
    resetSlide,
    cancel(slide) { resetSlide(slide); }
  });
})();
