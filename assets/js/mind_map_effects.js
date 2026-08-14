(() => {
  "use strict";

  const effectTypes = new Map();
  const sleep = (milliseconds, signal) => new Promise((resolve) => {
    if (signal?.aborted) { resolve(false); return; }
    const timeout = window.setTimeout(() => { cleanup(); resolve(true); }, milliseconds);
    const abort = () => { window.clearTimeout(timeout); cleanup(); resolve(false); };
    const cleanup = () => signal?.removeEventListener("abort", abort);
    signal?.addEventListener("abort", abort, { once: true });
  });

  const parseEffects = (slide, direction) => {
    const attribute = direction === "backward"
      ? "data-mind-map-transition-backward"
      : "data-mind-map-transition-forward";
    const configuration = slide.getAttribute(attribute);
    if (!configuration) return [];

    try {
      const effects = JSON.parse(configuration);
      return Array.isArray(effects) ? effects : [];
    } catch (_) {
      console.warn(`Ignoring invalid mind-map transition configuration in ${attribute}.`);
      return [];
    }
  };

  const parseEffectGroups = (slide) => {
    const attribute = "data-mind-map-effect-groups";
    const configuration = slide.getAttribute(attribute);
    if (!configuration) return [];

    try {
      const groups = JSON.parse(configuration);
      if (!Array.isArray(groups)) return [];
      return groups
        .map((group) => Array.isArray(group) ? group : group?.effects)
        .filter(Array.isArray);
    } catch (_) {
      console.warn(`Ignoring invalid mind-map effect configuration in ${attribute}.`);
      return [];
    }
  };

  const findWord = (slide, target, occurrence = 1) => {
    if (!target) return null;
    const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) => node.parentElement?.closest("script, style, [data-mind-map-effect-word]")
        ? NodeFilter.FILTER_REJECT
        : NodeFilter.FILTER_ACCEPT
    });
    const escapedTarget = target.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const expression = new RegExp(`\\b${escapedTarget}\\b`, "gi");
    let matchCount = 0;
    let node;

    while ((node = walker.nextNode())) {
      let match;
      while ((match = expression.exec(node.nodeValue))) {
        matchCount += 1;
        if (matchCount !== occurrence) continue;
        const word = document.createElement("span");
        word.className = "mind-map-effect-word";
        word.dataset.mindMapEffectWord = target.toLowerCase();
        word.textContent = match[0];
        const remainder = node.splitText(match.index);
        remainder.splitText(match[0].length);
        remainder.replaceWith(word);
        return word;
      }
    }
    return null;
  };

  const resetWordHighlights = (slide) => {
    slide.querySelectorAll("[data-mind-map-effect-word]").forEach((word) => {
      word.replaceWith(document.createTextNode(word.textContent));
    });
    slide.normalize();
  };

  effectTypes.set("word-highlight", {
    run: async ({ slide, effect, signal }) => {
      if (signal?.aborted) return;
      const word = slide.querySelector(`[data-mind-map-effect-word="${CSS.escape(String(effect.target).toLowerCase())}"]`)
        || findWord(slide, String(effect.target || ""), Number(effect.occurrence) || 1);
      if (!word || signal?.aborted) return;
      word.classList.remove("is-highlighted");
      word.dataset.highlightColor = effect.color || "green";
      // Force a style flush so a repeated transition can replay the animation.
      void word.offsetWidth;
      word.classList.add("is-highlighted");
      await sleep(Math.max(0, Number(effect.duration) || 0), signal);
    },
    reset: ({ slide }) => resetWordHighlights(slide)
  });

  const runEffect = async ({ slide, effect, direction, signal }) => {
    if (!await sleep(Math.max(0, Number(effect.delay) || 0), signal)) return;
    const handler = effectTypes.get(effect.type);
    const run = typeof handler === "function" ? handler : handler?.run;
    if (run && !signal?.aborted) await run({ slide, effect, direction, signal });
  };

  const runEffectGroup = async ({ slide, groupIndex, signal }) => {
    const group = parseEffectGroups(slide)[groupIndex];
    if (!group) return false;
    await Promise.all(group.map((effect) => runEffect({ slide, effect, direction: "forward", signal })));
    return !signal?.aborted;
  };

  const resetSlide = (slide) => {
    const resetters = new Set();
    [...parseEffectGroups(slide).flat(), ...parseEffects(slide, "forward"), ...parseEffects(slide, "backward")]
      .forEach((effect) => {
        const handler = effectTypes.get(effect?.type);
        if (handler?.reset) resetters.add(handler.reset);
      });
    resetters.forEach((reset) => reset({ slide }));
    // Also clean up highlights created by older/changed configuration.
    resetWordHighlights(slide);
  };

  const runTransition = async ({ slide, direction = "forward" }) => {
    const effects = parseEffects(slide, direction)
      .map((effect, index) => ({ ...effect, _sourceOrder: index }))
      .sort((left, right) => (Number(left.order) || 0) - (Number(right.order) || 0) || left._sourceOrder - right._sourceOrder);

    for (const effect of effects) {
      await runEffect({ slide, effect, direction });
    }
  };

  window.MindMapEffects = Object.freeze({
    register(type, run, reset) {
      if (typeof type !== "string") return;
      if (typeof run === "function") effectTypes.set(type, { run, reset });
      else if (run && typeof run.run === "function") effectTypes.set(type, run);
    },
    getGroupCount: (slide) => parseEffectGroups(slide).length,
    resetSlide,
    runEffectGroup,
    runTransition
  });
})();
