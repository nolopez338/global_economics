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

    if (!button.id) {
      button.id = `collapsible-toggle-${index}`;
    }

    const contentId = content.id || `collapsible-content-${index}`;
    content.id = contentId;
    button.setAttribute('aria-controls', contentId);
    content.setAttribute('role', 'region');
    content.setAttribute('aria-labelledby', button.id);

    const defaultExpanded = section.id === 'table-of-contents'
      || section.querySelector('.section-toc');
    section.classList.toggle('collapsed', !defaultExpanded);
    updateState(button, defaultExpanded);

    button.addEventListener('click', () => {
      const nextState = section.classList.toggle('collapsed');
      updateState(button, !nextState);
    });
  }

  function setupSubsection(section, index) {
    const button = section.querySelector('.subsection-toggle');
    const content = section.querySelector('.subsection-content');

    if (!button || !content) return;

    if (!button.id) {
      button.id = `subsection-toggle-${index}`;
    }

    const contentId = content.id || `subsection-content-${index}`;
    content.id = contentId;
    button.setAttribute('aria-controls', contentId);
    content.setAttribute('role', 'region');
    content.setAttribute('aria-labelledby', button.id);

    const defaultExpanded = section.id === 'table-of-contents'
      || section.querySelector('.section-toc');
    section.classList.toggle('collapsed', !defaultExpanded);
    updateState(button, defaultExpanded);

    button.addEventListener('click', () => {
      const collapsed = section.classList.toggle('collapsed');
      updateState(button, !collapsed);
    });
  }

  function expandSection(section) {
    if (!section.classList.contains('collapsed')) return;
    section.classList.remove('collapsed');
    const button = section.classList.contains('subsection-minimize')
      ? section.querySelector('.subsection-toggle')
      : section.querySelector('.collapse-toggle');
    if (button) {
      updateState(button, true);
    }
  }

  function expandAncestorSections(target) {
    const sections = [];
    let node = target;
    while (node) {
      if (node.classList?.contains('collapsible') || node.classList?.contains('subsection-minimize')) {
        sections.push(node);
      }
      node = node.parentElement;
    }
    sections.reverse().forEach(expandSection);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.classList.add('js-enabled');
    const sections = Array.from(document.querySelectorAll('.collapsible'));
    sections.forEach((section, index) => setupCollapsible(section, index));

    const subsections = Array.from(document.querySelectorAll('.subsection-minimize'));
    subsections.forEach((section, index) => setupSubsection(section, index));

    document.addEventListener('click', (event) => {
      const link = event.target.closest('.section-toc a[href^="#"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || href.length < 2) return;
      const target = document.getElementById(href.slice(1));
      if (!target) return;
      expandAncestorSections(target);
    });
  });
})();
