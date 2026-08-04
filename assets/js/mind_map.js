(() => {
  "use strict";

  const interactiveSelector = [
    "a", "button", "input", "select", "textarea", "summary", "label",
    "[contenteditable]", "[data-mind-map-interactive]"
  ].join(",");
  const instances = new WeakMap();

  const isEditable = (element) => Boolean(element?.closest(
    "input, select, textarea, [contenteditable], [role='textbox'], [role='slider']"
  ));

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
    const state = { active: false, index: 0, lastNavigation: 0, openTrigger: null };
    instances.set(root, state);
    root.setAttribute("data-mind-map-initialised", "");
    root.classList.add("mind-map-presentation--enhanced");
    map.classList.add("mind-map--enhanced");
    root.querySelectorAll("[data-criterion-tooltip]").forEach((tip) => { tip.hidden = true; });

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
      const opening = trigger.getAttribute("aria-expanded") !== "true";
      closeTooltips(trigger);
      const tip = root.querySelector(`#${CSS.escape(trigger.getAttribute("aria-controls"))}`);
      if (!tip) return;
      trigger.setAttribute("aria-expanded", String(opening));
      tip.hidden = !opening;
      state.openTrigger = opening ? trigger : null;
      updateScrollLock();
      if (opening) tip.querySelector("[data-criterion-close]")?.focus({ preventScroll: true });
      else trigger.focus({ preventScroll: true });
    };

    const render = ({ focus = false, announce = false } = {}) => {
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
          slide.tabIndex = -1;
        } else {
          slide.removeAttribute("aria-current");
          slide.removeAttribute("aria-label");
          if (!state.active) slide.tabIndex = 0;
          else slide.removeAttribute("tabindex");
        }
      });
      const final = state.index === slides.length - 1;
      const progressText = `${state.index + 1} / ${slides.length}`;
      controls.progress.forEach((progress) => { progress.textContent = progressText; });
      if (controls.previous) controls.previous.disabled = state.index === 0;
      if (controls.next) {
        controls.next.disabled = final;
        controls.next.setAttribute("aria-label", final ? "Final slide reached" : "Next slide");
      }
      if (controls.fullscreen) {
        const supported = Boolean(root.requestFullscreen && document.fullscreenEnabled);
        controls.fullscreen.hidden = !supported;
        const fullscreen = document.fullscreenElement === root;
        controls.fullscreen.textContent = fullscreen ? "Exit fullscreen" : "Enter fullscreen";
        controls.fullscreen.setAttribute("aria-pressed", String(fullscreen));
      }
      if (announce && controls.status) controls.status.textContent = `Slide ${state.index + 1} of ${slides.length}${final ? ", final slide" : ""}.`;
      if (focus) slides[state.index].focus({ preventScroll: true });
    };

    const go = (index) => {
      const now = Date.now();
      if (!state.active || index < 0 || index >= slides.length || index === state.index || now - state.lastNavigation < 180) return;
      state.lastNavigation = now;
      closeTooltips();
      state.index = index;
      render({ focus: true, announce: true });
    };

    const exit = async () => {
      if (!state.active) return;
      if (document.fullscreenElement === root) {
        try { await document.exitFullscreen(); } catch (_) { /* Presentation can still exit. */ }
      }
      state.active = false;
      closeTooltips();
      render();
      controls.start?.focus({ preventScroll: true });
    };

    controls.start?.addEventListener("click", () => {
      state.active = true;
      state.index = 0;
      render({ focus: true, announce: true });
      if (root.requestFullscreen && document.fullscreenEnabled && !document.fullscreenElement) {
        const request = root.requestFullscreen();
        if (request?.catch) request.catch(() => {
          if (controls.status) controls.status.textContent = "Fullscreen was unavailable; presentation mode remains active.";
          render();
        });
      }
    });
    controls.previous?.addEventListener("click", () => go(state.index - 1));
    controls.next?.addEventListener("click", () => go(state.index + 1));
    controls.exit?.addEventListener("click", exit);
    controls.fullscreen?.addEventListener("click", async () => {
      try {
        if (document.fullscreenElement === root) await document.exitFullscreen();
        else await root.requestFullscreen();
      } catch (_) {
        if (controls.status) controls.status.textContent = "Fullscreen was unavailable; presentation mode remains active.";
      }
    });

    root.addEventListener("click", (event) => {
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
      if (!slides[state.index].contains(event.target)) return;
      if (event.target.closest(interactiveSelector) || !window.getSelection()?.isCollapsed) return;
      go(state.index + 1);
    });

    root.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      const openTooltipElement = root.querySelector("[data-criterion-tooltip]:not([hidden])");
      if (!openTooltipElement) return;

      // A dialog gets the first opportunity to consume Escape. Browsers may still
      // reserve Escape for leaving native fullscreen, but application handlers
      // must not also advance a slide or exit presentation on this keypress.
      event.preventDefault();
      event.stopImmediatePropagation();
      closeTooltips(null, true);
    }, true);

    root.addEventListener("keydown", (event) => {
      const openTooltipElement = root.querySelector("[data-criterion-tooltip]:not([hidden])");
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
      if (event.altKey || event.ctrlKey || event.metaKey || isEditable(event.target)) return;
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
      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        event.preventDefault();
        go(state.index + (event.key === "ArrowRight" ? 1 : -1));
      }
    });
    document.addEventListener("fullscreenchange", () => {
      if (state.active) render();
    });
    render();
    return state;
  }

  document.querySelectorAll("[data-mind-map-presentation]").forEach(initialise);
})();
