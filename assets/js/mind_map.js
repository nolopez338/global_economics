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
    if (instances.has(root)) return instances.get(root);

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
      progress: root.querySelector("[data-presentation-progress]"),
      status: root.querySelector("[data-presentation-status]")
    };
    const state = { active: false, index: 0, lastNavigation: 0 };
    instances.set(root, state);
    root.classList.add("mind-map-presentation--enhanced");
    map.classList.add("mind-map--enhanced");
    root.querySelectorAll("[data-criterion-tooltip]").forEach((tip) => { tip.hidden = true; });

    const closeTooltips = (except = null) => {
      root.querySelectorAll("[data-criterion-trigger][aria-expanded='true']").forEach((trigger) => {
        if (trigger === except) return;
        trigger.setAttribute("aria-expanded", "false");
        const tip = root.querySelector(`#${CSS.escape(trigger.getAttribute("aria-controls"))}`);
        if (tip) tip.hidden = true;
      });
    };

    const render = ({ focus = false, announce = false } = {}) => {
      root.classList.toggle("is-presenting", state.active);
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
      const progressText = `${state.index + 1} / ${slides.length}${final ? " · Final slide" : ""}`;
      if (controls.progress) controls.progress.textContent = progressText;
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
        const opening = trigger.getAttribute("aria-expanded") !== "true";
        closeTooltips(trigger);
        trigger.setAttribute("aria-expanded", String(opening));
        const tip = root.querySelector(`#${CSS.escape(trigger.getAttribute("aria-controls"))}`);
        if (tip) tip.hidden = !opening;
        return;
      }
      if (!event.target.closest("[data-criterion-tooltip]")) closeTooltips();
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
