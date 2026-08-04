(() => {
  "use strict";

  const maps = document.querySelectorAll("[data-mind-map]");

  maps.forEach((map) => {
    const steps = Array.from(map.querySelectorAll(":scope > .mind-map-step"));
    if (!steps.length) return;

    map.classList.add("mind-map--enhanced");
    const help = map.parentElement.querySelector("[data-mind-map-help]");
    if (help) help.hidden = false;

    const selectStep = (selectedStep, moveFocus = false) => {
      steps.forEach((step) => {
        if (step === selectedStep) step.setAttribute("aria-current", "step");
        else step.removeAttribute("aria-current");
      });
      if (moveFocus) selectedStep.focus();
    };

    steps.forEach((step, index) => {
      step.tabIndex = 0;
      step.addEventListener("click", () => selectStep(step));
      step.addEventListener("keydown", (event) => {
        let nextIndex;
        if (event.key === "ArrowDown" || event.key === "ArrowRight") nextIndex = index + 1;
        else if (event.key === "ArrowUp" || event.key === "ArrowLeft") nextIndex = index - 1;
        else if (event.key === "Home") nextIndex = 0;
        else if (event.key === "End") nextIndex = steps.length - 1;
        else if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          selectStep(step);
          return;
        } else return;

        event.preventDefault();
        const wrappedIndex = (nextIndex + steps.length) % steps.length;
        selectStep(steps[wrappedIndex], true);
      });
    });
  });
})();
