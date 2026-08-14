(() => {
  "use strict";

  if (document.documentElement.hasAttribute("data-mind-map-script-initialised")) return;
  document.documentElement.setAttribute("data-mind-map-script-initialised", "");

  const interactiveSelector = [
    "a", "button", "input", "select", "textarea", "summary", "label",
    "[contenteditable]", "[data-mind-map-interactive]", "[data-presentation-toolbar]",
    "[role='button']", "[role='link']", "[role='checkbox']", "[role='radio']",
    "[role='switch']", "[role='textbox']", "[role='searchbox']", "[role='combobox']",
    "[role='listbox']", "[role='option']", "[role='menuitem']", "[role='tab']",
    "[role='slider']", "[role='spinbutton']"
  ].join(",");
  const arrowKeyControlSelector = [
    "input", "select", "textarea", "[contenteditable]:not([contenteditable='false'])",
    "[role='checkbox']", "[role='radio']", "[role='switch']", "[role='textbox']",
    "[role='searchbox']", "[role='combobox']", "[role='listbox']", "[role='option']",
    "[role='menu']", "[role='menuitem']", "[role='tablist']", "[role='tab']",
    "[role='slider']", "[role='spinbutton']", "[role='tree']", "[role='grid']",
    "[aria-haspopup]"
  ].join(",");
  const instances = new WeakMap();

  const isEditable = (element) => Boolean(element?.closest(
    "input, select, textarea, [contenteditable]:not([contenteditable='false']), [role='textbox'], [role='searchbox'], [role='combobox']"
  ));

  const presentationForFullscreenElement = () => {
    const fullscreenElement = document.fullscreenElement;
    if (!(fullscreenElement instanceof Element)) return null;
    if (fullscreenElement.matches("[data-mind-map-presentation]")) return fullscreenElement;
    return null;
  };

  const scrollContainerForSlide = (slide) => {
    if (!slide) return null;
    return slide.matches("[data-mind-map-slide-scroll]")
      ? slide
      : slide.querySelector("[data-mind-map-slide-scroll]") || slide;
  };

  function initialise(root) {
    if (instances.has(root) || root.hasAttribute("data-mind-map-initialised")) return instances.get(root) || null;

    const map = root.querySelector("[data-mind-map]");
    const slides = map ? Array.from(map.querySelectorAll(":scope > [data-mind-map-slide]")) : [];
    if (!map || !slides.length) return null;

    const controls = {
      start: root.querySelector("[data-presentation-start]"),
      toolbar: root.querySelector("[data-presentation-toolbar]"),
      previous: root.querySelector("[data-presentation-previous]"),
      next: root.querySelector("[data-presentation-next]"),
      fullscreen: root.querySelector("[data-presentation-fullscreen]"),
      exit: root.querySelector("[data-presentation-exit]"),
      progress: Array.from(root.querySelectorAll("[data-presentation-progress]")),
      status: root.querySelector("[data-presentation-status]")
    };
    const state = { active: false, index: 0, effectGroup: 0, effectController: null, lastNavigation: 0, openTrigger: null, pointerGesture: null, transitioning: false };
    root.setAttribute("data-mind-map-initialised", "");
    root.classList.add("mind-map-presentation--enhanced");
    map.classList.add("mind-map--enhanced");
    root.querySelectorAll("[data-criterion-tooltip]").forEach((tip) => { tip.hidden = true; });


    const criterionDetailsForTrigger = (trigger) => {
      const id = trigger.dataset.criterionId?.trim() || trigger.textContent.trim();
      const description = trigger.dataset.criterionText?.trim();
      if (id && description) return { id, description };
      const controls = trigger.getAttribute("aria-controls");
      const tip = controls ? root.querySelector(`#${CSS.escape(controls)}`) : null;
      const fallback = tip?.querySelector("[data-criterion-description], .criterion-dialog-text")?.textContent.trim();
      return id && fallback ? { id, description: fallback } : null;
    };

    const criteriaForSlide = (slide) => {
      const seen = new Set();
      return Array.from(slide.querySelectorAll("[data-criterion-trigger]")).reduce((criteria, trigger) => {
        const details = criterionDetailsForTrigger(trigger);
        if (!details || !details.id || !details.description || seen.has(details.id)) return criteria;
        seen.add(details.id);
        criteria.push(details);
        return criteria;
      }, []);
    };

    const renderCriterionList = (tip, criteria) => {
      const container = tip.querySelector("[data-criterion-list]") || tip.querySelector(".criterion-dialog-text");
      if (!container || !criteria.length) return;
      container.replaceChildren();
      const list = document.createElement("ul");
      list.className = "criterion-list";
      list.setAttribute("data-criterion-list-items", "");
      criteria.forEach(({ id, description }) => {
        const item = document.createElement("li");
        const label = document.createElement("strong");
        label.className = "criterion-list-id";
        label.textContent = id;
        item.append(label, document.createTextNode(` ${description}`));
        list.append(item);
      });
      container.append(list);
    };

    const updateScrollLock = () => {
      document.documentElement.classList.toggle("criterion-overlay-open", Boolean(document.querySelector("[data-criterion-tooltip]:not([hidden])")));
    };

    const closeTooltips = (except = null, restoreFocus = false) => {
      root.querySelectorAll("[data-criterion-trigger][aria-expanded='true']").forEach((trigger) => {
        if (trigger === except) return;
        trigger.setAttribute("aria-expanded", "false");
        const tip = root.querySelector(`#${CSS.escape(trigger.getAttribute("aria-controls"))}`);
        if (tip) tip.hidden = true;
        if (restoreFocus && trigger === state.openTrigger && trigger.isConnected) trigger.focus({ preventScroll: true });
      });
      if (!except) state.openTrigger = null;
      updateScrollLock();
    };

    const openTooltip = (trigger) => {
      const slide = trigger.closest("[data-mind-map-slide]");
      const criteria = slide ? criteriaForSlide(slide) : [];
      const opening = trigger.getAttribute("aria-expanded") !== "true";
      closeTooltips(trigger);
      const controls = trigger.getAttribute("aria-controls");
      const tip = controls ? root.querySelector(`#${CSS.escape(controls)}`) : null;
      if (!tip || !criteria.length) return;
      renderCriterionList(tip, criteria);
      trigger.setAttribute("aria-expanded", String(opening));
      tip.hidden = !opening;
      state.openTrigger = opening ? trigger : null;
      updateScrollLock();
      if (opening) tip.querySelector("[data-criterion-close]")?.focus({ preventScroll: true });
      else trigger.focus({ preventScroll: true });
    };

    const render = ({ announce = false } = {}) => {
      root.classList.toggle("is-presenting", state.active);
      root.toggleAttribute("data-presentation-fullscreen-active", document.fullscreenElement === root);
      controls.start?.setAttribute("aria-expanded", String(state.active));
      if (controls.toolbar) controls.toolbar.hidden = !state.active;
      slides.forEach((slide, index) => {
        const current = state.active && index === state.index;
        slide.hidden = state.active && !current;
        slide.toggleAttribute("inert", state.active && !current);
        if (current) {
          slide.setAttribute("aria-current", "step");
          slide.setAttribute("aria-label", `Slide ${index + 1} of ${slides.length}`);
        } else {
          slide.removeAttribute("aria-current");
          slide.removeAttribute("aria-label");
        }
        if (!state.active) slide.tabIndex = 0;
        else slide.removeAttribute("tabindex");
      });
      const final = state.index === slides.length - 1;
      const pendingEffects = state.effectGroup < (window.MindMapEffects?.getGroupCount(slides[state.index]) || 0);
      const progressText = `${state.index + 1} / ${slides.length}`;
      controls.progress.forEach((progress) => {
        if (!progress.querySelector("[data-presentation-progress-input]")) progress.textContent = progressText;
      });
      if (controls.previous) controls.previous.disabled = state.index === 0;
      if (controls.next) {
        controls.next.disabled = (final && !pendingEffects) || state.transitioning;
        controls.next.setAttribute("aria-label", pendingEffects ? "Run next effect group" : final ? "Final slide reached" : "Next slide");
      }
      if (controls.fullscreen) {
        const supported = Boolean(root.requestFullscreen && document.fullscreenEnabled);
        controls.fullscreen.hidden = !supported;
        const fullscreen = document.fullscreenElement === root;
        controls.fullscreen.textContent = fullscreen ? "Exit fullscreen" : "Enter fullscreen";
        controls.fullscreen.setAttribute("aria-pressed", String(fullscreen));
      }
      if (announce && controls.status) controls.status.textContent = `Slide ${state.index + 1} of ${slides.length}${final ? ", final slide" : ""}.`;
    };

    const go = async (index, { transition = true, throttle = true } = {}) => {
      const now = Date.now();
      if (!state.active || state.transitioning || index < 0 || index >= slides.length || index === state.index || (throttle && now - state.lastNavigation < 180)) return;
      state.lastNavigation = now;
      const startingIndex = state.index;
      const direction = index > startingIndex ? "forward" : "backward";
      if (transition) {
        state.transitioning = true;
        state.effectController = new AbortController();
        const controller = state.effectController;
        render();
        try {
          await window.MindMapEffects?.runTransition({
            root,
            slide: slides[startingIndex],
            fromIndex: startingIndex,
            toIndex: index,
            direction,
            signal: controller.signal
          });
        } finally {
          if (state.effectController === controller) state.effectController = null;
          state.transitioning = false;
        }
      }
      if (!state.active || state.index !== startingIndex) {
        render();
        return;
      }
      closeTooltips();
      window.MindMapEffects?.resetSlide(slides[startingIndex]);
      state.index = index;
      state.effectGroup = 0;
      window.MindMapEffects?.resetSlide(slides[index]);
      scrollContainerForSlide(slides[index]).scrollTop = 0;
      render({ announce: true });
    };

    const forward = async () => {
      if (!state.active || state.transitioning) return;
      const groupCount = window.MindMapEffects?.getGroupCount(slides[state.index]) || 0;
      if (state.effectGroup >= groupCount) {
        go(state.index + 1);
        return;
      }
      state.transitioning = true;
      state.effectController = new AbortController();
      const controller = state.effectController;
      render();
      const startingIndex = state.index;
      try {
        const ran = await window.MindMapEffects.runEffectGroup({ slide: slides[startingIndex], groupIndex: state.effectGroup, signal: controller.signal });
        if (ran && state.active && state.index === startingIndex) state.effectGroup += 1;
      } finally {
        if (state.effectController === controller) {
          state.effectController = null;
          state.transitioning = false;
        }
        render();
      }
    };

    instances.set(root, { state, render, go, forward });

    const restoreProgress = (progress) => {
      if (!progress.querySelector("[data-presentation-progress-input]")) return;
      progress.textContent = `${state.index + 1} / ${slides.length}`;
    };

    const editProgress = (progress) => {
      if (!state.active || progress.querySelector("[data-presentation-progress-input]")) return;
      const input = document.createElement("input");
      input.type = "number";
      input.className = "presentation-progress-input";
      input.setAttribute("data-presentation-progress-input", "");
      input.setAttribute("aria-label", `Go to slide (1 to ${slides.length})`);
      input.inputMode = "numeric";
      input.min = "1";
      input.max = String(slides.length);
      input.step = "1";
      input.value = String(state.index + 1);
      progress.replaceChildren(input);
      input.focus({ preventScroll: true });
      input.select();

      input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          restoreProgress(progress);
          progress.focus({ preventScroll: true });
          return;
        }
        if (event.key !== "Enter") return;
        event.preventDefault();
        event.stopPropagation();
        const value = input.value.trim();
        const slideNumber = Number(value);
        if (!/^\d+$/.test(value) || !Number.isSafeInteger(slideNumber) || slideNumber < 1 || slideNumber > slides.length) {
          input.setAttribute("aria-invalid", "true");
          return;
        }
        restoreProgress(progress);
        go(slideNumber - 1, { transition: false, throttle: false });
      });
      input.addEventListener("input", () => input.removeAttribute("aria-invalid"));
      input.addEventListener("blur", () => restoreProgress(progress));
    };

    controls.progress.forEach((progress) => {
      progress.tabIndex = 0;
      progress.setAttribute("role", "button");
      progress.setAttribute("aria-label", "Slide progress; activate to go to a slide");
      progress.addEventListener("click", () => editProgress(progress));
      progress.addEventListener("keydown", (event) => {
        if (event.target !== progress || !["Enter", " "].includes(event.key)) return;
        event.preventDefault();
        editProgress(progress);
      });
    });

    const exit = async () => {
      if (!state.active) return;
      state.effectController?.abort();
      state.effectController = null;
      if (document.fullscreenElement === root) {
        try { await document.exitFullscreen(); } catch (_) { /* Presentation can still exit. */ }
      }
      state.active = false;
      state.transitioning = false;
      state.effectGroup = 0;
      slides.forEach((slide) => window.MindMapEffects?.resetSlide(slide));
      controls.progress.forEach(restoreProgress);
      closeTooltips();
      render();
      controls.start?.focus({ preventScroll: true });
    };

    controls.start?.addEventListener("click", () => {
      state.active = true;
      state.effectController?.abort();
      state.effectController = null;
      state.index = 0;
      state.effectGroup = 0;
      state.transitioning = false;
      slides.forEach((slide) => window.MindMapEffects?.resetSlide(slide));
      scrollContainerForSlide(slides[0]).scrollTop = 0;
      render({ announce: true });
      if (root.requestFullscreen && document.fullscreenEnabled && !document.fullscreenElement) {
        const request = root.requestFullscreen();
        if (request?.catch) request.catch(() => {
          if (controls.status) controls.status.textContent = "Fullscreen was unavailable; presentation mode remains active.";
          render();
        });
      }
    });
    controls.previous?.addEventListener("click", () => go(state.index - 1));
    controls.next?.addEventListener("click", forward);
    controls.exit?.addEventListener("click", exit);
    controls.fullscreen?.addEventListener("click", async () => {
      try {
        if (document.fullscreenElement === root) await document.exitFullscreen();
        else await root.requestFullscreen();
      } catch (_) {
        if (controls.status) controls.status.textContent = "Fullscreen was unavailable; presentation mode remains active.";
      }
    });

    const isScrollbarGesture = (event) => {
      const target = event.target;
      if (!(target instanceof Element)) return false;
      const rect = target.getBoundingClientRect();
      return event.clientX >= rect.left + target.clientWidth || event.clientY >= rect.top + target.clientHeight;
    };

    root.addEventListener("pointerdown", (event) => {
      state.pointerGesture = {
        id: event.pointerId,
        x: event.clientX,
        y: event.clientY,
        target: event.target,
        scrollbar: isScrollbarGesture(event)
      };
    }, true);

    root.addEventListener("pointermove", (event) => {
      const gesture = state.pointerGesture;
      if (!gesture || gesture.id !== event.pointerId) return;
      if (Math.hypot(event.clientX - gesture.x, event.clientY - gesture.y) > 8) gesture.moved = true;
    }, true);

    root.addEventListener("pointercancel", () => { state.pointerGesture = null; }, true);

    root.addEventListener("click", (event) => {
      const gesture = state.pointerGesture;
      state.pointerGesture = null;
      const trigger = event.target.closest("[data-criterion-trigger]");
      if (trigger && root.contains(trigger)) {
        event.stopPropagation();
        openTooltip(trigger);
        return;
      }
      const tooltip = event.target.closest("[data-criterion-tooltip]");
      if (tooltip) {
        event.stopPropagation();
        if (event.target.closest("[data-criterion-close], [data-criterion-backdrop]")) closeTooltips(null, true);
        return;
      }
      closeTooltips();
      if (!state.active) {
        const selected = event.target.closest("[data-mind-map-slide]");
        if (selected && !event.target.closest(interactiveSelector)) {
          slides.forEach((slide) => slide === selected ? slide.setAttribute("aria-current", "step") : slide.removeAttribute("aria-current"));
        }
        return;
      }
      const actualFullscreen = document.fullscreenElement === root;
      if (!actualFullscreen && !slides[state.index].contains(event.target)) return;
      if (event.target.closest(interactiveSelector) || !window.getSelection()?.isCollapsed) return;
      if (gesture?.moved || gesture?.scrollbar || (gesture && gesture.target !== event.target)) return;
      forward();
    });

    root.addEventListener("keydown", (event) => {
      const openTooltipElement = root.querySelector("[data-criterion-tooltip]:not([hidden])");
      if (openTooltipElement && event.key.toLowerCase() === "q" && !isEditable(event.target)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        closeTooltips(null, true);
        return;
      }
      if (openTooltipElement && event.key === "Tab") {
        const focusable = Array.from(openTooltipElement.querySelectorAll("button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])")).filter((element) => !element.disabled);
        if (focusable.length) {
          const first = focusable[0];
          const last = focusable[focusable.length - 1];
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
          else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
        }
        return;
      }
      if (openTooltipElement) return;
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || isEditable(event.target)) return;
      if (!state.active) {
        const index = slides.indexOf(event.target);
        if (index < 0 || !["ArrowRight", "ArrowLeft", "ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) return;
        event.preventDefault();
        let next = event.key === "Home" ? 0 : event.key === "End" ? slides.length - 1 : index + (["ArrowRight", "ArrowDown"].includes(event.key) ? 1 : -1);
        next = (next + slides.length) % slides.length;
        slides.forEach((slide) => slide === slides[next] ? slide.setAttribute("aria-current", "step") : slide.removeAttribute("aria-current"));
        slides[next].focus();
        return;
      }
      if (event.defaultPrevented || !["ArrowRight", "ArrowLeft"].includes(event.key)) return;
      if (event.target.closest(arrowKeyControlSelector)) return;
      event.preventDefault();
      event.stopImmediatePropagation();
      if (event.key === "ArrowRight") forward();
      else go(state.index - 1);
    });
    render();
    return instances.get(root);
  }

  document.querySelectorAll("[data-mind-map-presentation]").forEach(initialise);

  document.addEventListener("keydown", (event) => {
    const arrowKeys = ["ArrowRight", "ArrowLeft", "ArrowDown", "ArrowUp"];
    if (event.defaultPrevented || !arrowKeys.includes(event.key)) return;
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;

    const root = presentationForFullscreenElement();
    const instance = root && instances.get(root);
    if (!instance?.state.active) return;

    const target = event.target instanceof Element ? event.target : null;
    const openTooltip = root.querySelector("[data-criterion-tooltip]:not([hidden])");
    if (openTooltip || target?.closest("[role='dialog'], [aria-modal='true'], [data-criterion-tooltip]")) return;
    if (target?.closest(arrowKeyControlSelector) || isEditable(target)) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
      if (event.key === "ArrowRight") instance.forward();
      else instance.go(instance.state.index - 1);
      return;
    }

    const activeSlide = root.querySelector("[data-mind-map-slide][aria-current='step']");
    if (!activeSlide) return;
    const scrollContainer = scrollContainerForSlide(activeSlide);
    const increment = Math.min(96, Math.max(40, scrollContainer.clientHeight * 0.1));
    scrollContainer.scrollBy({
      top: event.key === "ArrowDown" ? increment : -increment,
      behavior: "auto"
    });
  }, true);

  document.addEventListener("fullscreenchange", () => {
    document.querySelectorAll("[data-mind-map-presentation]").forEach((root) => {
      const instance = instances.get(root);
      if (instance?.state.active) instance.render();
    });
  });
})();
