(function () {
  function updateState(button, expanded) {
    const icon = button.querySelector('.toggle-icon');
    button.setAttribute('aria-expanded', expanded);
    if (icon) {
      icon.textContent = expanded ? '−' : '+';
    }
  }

  function setupCollapsible(section, index) {
    const button = section.querySelector('.collapse-toggle');
    const content = section.querySelector('.collapsible-content');

    if (!button || !content) return;

    const contentId = content.id || `collapsible-content-${index}`;
    content.id = contentId;
    button.setAttribute('aria-controls', contentId);

    const isCollapsed = section.classList.contains('collapsed');
    updateState(button, !isCollapsed);

    button.addEventListener('click', () => {
      const nextState = section.classList.toggle('collapsed');
      updateState(button, !nextState);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const sections = Array.from(document.querySelectorAll('.collapsible'));
    sections.forEach((section, index) => setupCollapsible(section, index));
  });
})();
