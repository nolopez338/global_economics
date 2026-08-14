(() => {
  "use strict";

  const effectTypes = new Map();
  const sleep = (milliseconds) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));

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

  effectTypes.set("word-highlight", async ({ slide, effect }) => {
    const word = slide.querySelector(`[data-mind-map-effect-word="${CSS.escape(String(effect.target).toLowerCase())}"]`)
      || findWord(slide, String(effect.target || ""), Number(effect.occurrence) || 1);
    if (!word) return;
    word.classList.remove("is-highlighted");
    word.dataset.highlightColor = effect.color || "green";
    // Force a style flush so a repeated transition can replay the animation.
    void word.offsetWidth;
    word.classList.add("is-highlighted");
    await sleep(Math.max(0, Number(effect.duration) || 0));
  });

  const runTransition = async ({ slide, direction = "forward" }) => {
    const effects = parseEffects(slide, direction)
      .map((effect, index) => ({ ...effect, _sourceOrder: index }))
      .sort((left, right) => (Number(left.order) || 0) - (Number(right.order) || 0) || left._sourceOrder - right._sourceOrder);

    for (const effect of effects) {
      await sleep(Math.max(0, Number(effect.delay) || 0));
      const run = effectTypes.get(effect.type);
      if (run) await run({ slide, effect, direction });
    }
  };

  window.MindMapEffects = Object.freeze({
    register(type, run) {
      if (typeof type === "string" && typeof run === "function") effectTypes.set(type, run);
    },
    runTransition
  });
})();
