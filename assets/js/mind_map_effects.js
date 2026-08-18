(() => {
  "use strict";

  const effectTypes = new Map();
  const temporaryAnimations = new Set();
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

  const resetElementHighlights = (slide) => {
    slide.querySelectorAll("[data-mind-map-effect-element]").forEach((element) => {
      element.classList.remove("mind-map-effect-element", "is-highlighted");
      element.removeAttribute("data-mind-map-effect-element");
      element.removeAttribute("data-highlight-color");
    });
  };

  const removeTemporaryAnimations = () => {
    temporaryAnimations.forEach((element) => element.remove());
    temporaryAnimations.clear();
    document.querySelectorAll("[data-mind-map-transition-target]").forEach((slide) => {
      slide.removeAttribute("data-mind-map-transition-target");
      slide.hidden = true;
    });
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

  effectTypes.set("element-highlight", {
    run: async ({ slide, effect, signal }) => {
      if (signal?.aborted || typeof effect.selector !== "string") return;
      let elements;
      try { elements = slide.querySelectorAll(effect.selector); }
      catch (_) { console.warn("Ignoring invalid element-highlight selector."); return; }
      elements.forEach((element) => {
        element.classList.add("mind-map-effect-element");
        element.dataset.mindMapEffectElement = "";
        element.dataset.highlightColor = effect.color || "green";
        void element.offsetWidth;
        element.classList.add("is-highlighted");
      });
      await sleep(Math.max(0, Number(effect.duration) || 0), signal);
    },
    reset: ({ slide }) => resetElementHighlights(slide)
  });

  effectTypes.set("clear-highlights", {
    run: async ({ slide }) => {
      resetWordHighlights(slide);
      resetElementHighlights(slide);
    },
    reset: ({ slide }) => resetElementHighlights(slide)
  });

  effectTypes.set("move-matching-concepts", {
    run: async ({ root, slide, effect, toIndex, signal }) => {
      const slides = Array.from(root?.querySelectorAll("[data-mind-map] > [data-mind-map-slide]") || []);
      const sourceSlide = slide;
      const destinationSlide = slides[Number(toIndex)];
      if (!sourceSlide || !destinationSlide || signal?.aborted) return;

      removeTemporaryAnimations();
      destinationSlide.hidden = false;
      destinationSlide.setAttribute("data-mind-map-transition-target", "");

      const pairs = Array.from(sourceSlide.querySelectorAll("[data-mind-map-move-source]")).flatMap((source) => {
        const key = source.dataset.mindMapMoveSource;
        return Array.from(destinationSlide.querySelectorAll(`[data-mind-map-move-destination="${CSS.escape(key)}"]`))
          .map((destination) => ({ source, destination }));
      });
      const duration = Math.max(0, Number(effect.duration) || 700);

      pairs.forEach(({ source, destination }) => {
        const start = source.getBoundingClientRect();
        const finish = destination.getBoundingClientRect();
        if (!start.width || !start.height || !finish.width || !finish.height) return;
        const mover = document.createElement("span");
        mover.className = `mind-map-concept-mover mind-map-concept-mover--${source.dataset.mindMapConcept || "green"}`;
        mover.textContent = destination.textContent;
        mover.setAttribute("aria-hidden", "true");
        Object.assign(mover.style, {
          left: `${start.left}px`, top: `${start.top}px`, width: `${start.width}px`, height: `${start.height}px`,
          "--mind-map-move-x": `${finish.left - start.left}px`,
          "--mind-map-move-y": `${finish.top - start.top}px`,
          "--mind-map-move-scale-x": String(finish.width / start.width),
          "--mind-map-move-scale-y": String(finish.height / start.height),
          "--mind-map-move-duration": `${duration}ms`
        });
        document.body.append(mover);
        temporaryAnimations.add(mover);
        void mover.offsetWidth;
        mover.classList.add("is-moving");
      });

      await sleep(duration, signal);
      removeTemporaryAnimations();
    },
    reset: removeTemporaryAnimations
  });

  const runEffect = async ({ slide, effect, direction, signal, ...context }) => {
    if (!await sleep(Math.max(0, Number(effect.delay) || 0), signal)) return;
    const handler = effectTypes.get(effect.type);
    const run = typeof handler === "function" ? handler : handler?.run;
    if (run && !signal?.aborted) await run({ slide, effect, direction, signal, ...context });
  };

  const runEffectGroup = async ({ slide, groupIndex, signal }) => {
    const group = parseEffectGroups(slide)[groupIndex];
    if (!group) return false;
    await Promise.all(group.map((effect) => runEffect({ slide, effect, direction: "forward", signal })));
    return !signal?.aborted;
  };

  const resetSlide = (slide) => {
    removeTemporaryAnimations();
    const resetters = new Set();
    [...parseEffectGroups(slide).flat(), ...parseEffects(slide, "forward"), ...parseEffects(slide, "backward")]
      .forEach((effect) => {
        const handler = effectTypes.get(effect?.type);
        if (handler?.reset) resetters.add(handler.reset);
      });
    resetters.forEach((reset) => reset({ slide }));
    // Also clean up highlights created by older/changed configuration.
    resetWordHighlights(slide);
    resetElementHighlights(slide);
  };

  const runTransition = async ({ slide, direction = "forward", ...context }) => {
    const effects = parseEffects(slide, direction)
      .map((effect, index) => ({ ...effect, _sourceOrder: index }))
      .sort((left, right) => (Number(left.order) || 0) - (Number(right.order) || 0) || left._sourceOrder - right._sourceOrder);

    for (const effect of effects) {
      await runEffect({ slide, effect, direction, ...context });
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
