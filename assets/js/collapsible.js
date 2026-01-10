(function () {
  function updateState(button, expanded) {
    const icon = button.querySelector('.toggle-icon');
    button.setAttribute('aria-expanded', expanded);
    if (icon) {
      icon.textContent = expanded ? '−' : '+';
    }
  }

  function setupCollapsible(section, index, selectors, idPrefix) {
    const button = section.querySelector(selectors.toggle);
    const content = section.querySelector(selectors.content);

    if (!button || !content) return;

    const contentId = content.id || `${idPrefix}-${index}`;
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
    const collapsibleSections = Array.from(document.querySelectorAll('.collapsible'));
    collapsibleSections.forEach((section, index) => setupCollapsible(
      section,
      index,
      { toggle: '.collapse-toggle', content: '.collapsible-content' },
      'collapsible-content'
    ));

    const subsections = Array.from(document.querySelectorAll('.subsection-minimize'));
    subsections.forEach((section, index) => setupCollapsible(
      section,
      index,
      { toggle: '.subsection-toggle', content: '.subsection-content' },
      'subsection-content'
    ));
  });
})();
