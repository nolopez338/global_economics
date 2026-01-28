(function () {
  function updateState(button, expanded) {
    const icon = button.querySelector('.toggle-icon');
    button.setAttribute('aria-expanded', expanded);
    if (icon) {
      icon.textContent = expanded ? '−' : '+';
    }
  }

  function getSectionButton(section) {
    if (section.classList.contains('subsection-minimize')) {
      return section.querySelector('.subsection-toggle');
    }
    return section.querySelector('.collapse-toggle');
  }

  function setSectionExpanded(section, expanded) {
    const button = getSectionButton(section);
    if (!button) return;
    section.classList.toggle('collapsed', !expanded);
    updateState(button, expanded);
  }

  function toggleSection(section) {
    const button = getSectionButton(section);
    if (!button) return;
    const collapsed = section.classList.toggle('collapsed');
    updateState(button, !collapsed);
  }

  function getDefaultExpanded(section, button) {
    const ariaExpanded = button.getAttribute('aria-expanded');
    if (ariaExpanded === 'true') return true;
    if (ariaExpanded === 'false') return false;
    if (section.classList.contains('collapsed')) return false;
    return section.id === 'table-of-contents'
      || section.querySelector('.section-toc');
  }

  function handleToggleActivation(toggleTarget, event) {
    const section = toggleTarget.closest('.collapsible, .subsection-minimize');
    if (!section) return;
    const button = getSectionButton(section);
    if (!button) return;
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    toggleSection(section);
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

    const defaultExpanded = getDefaultExpanded(section, button);
    section.classList.toggle('collapsed', !defaultExpanded);
    updateState(button, defaultExpanded);

    button.addEventListener('click', () => {
      toggleSection(section);
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

    const defaultExpanded = getDefaultExpanded(section, button);
    section.classList.toggle('collapsed', !defaultExpanded);
    updateState(button, defaultExpanded);

    button.addEventListener('click', () => {
      toggleSection(section);
    });
  }

  function expandSection(section) {
    if (!section.classList.contains('collapsed')) return;
    setSectionExpanded(section, true);
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

  function expandMainSectionFromTarget(target) {
    const mainSection = target.closest('.content-card.collapsible');
    if (!mainSection) return;
    expandSection(mainSection);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.classList.add('js-enabled');
    const sections = Array.from(document.querySelectorAll('.collapsible'));
    sections.forEach((section, index) => setupCollapsible(section, index));

    const subsections = Array.from(document.querySelectorAll('.subsection-minimize'));
    subsections.forEach((section, index) => setupSubsection(section, index));

    document.querySelectorAll('.toggle-label, .toggle-icon').forEach((element) => {
      if (element.closest('.collapse-toggle, .subsection-toggle')) return;
      element.setAttribute('role', 'button');
      element.setAttribute('tabindex', '0');
    });

    document.addEventListener('click', (event) => {
      const toggleTarget = event.target.closest('.toggle-label, .toggle-icon');
      if (!toggleTarget) return;
      handleToggleActivation(toggleTarget, event);
    }, true);

    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      const toggleTarget = event.target.closest('.toggle-label, .toggle-icon');
      if (!toggleTarget) return;
      if (toggleTarget.closest('.collapse-toggle, .subsection-toggle')) return;
      handleToggleActivation(toggleTarget, event);
    });

    document.addEventListener('click', (event) => {
      const link = event.target.closest('.section-toc a[href^="#"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || href.length < 2) return;
      const target = document.getElementById(href.slice(1));
      if (!target) return;
      expandAncestorSections(target);
    });

    const mainToc = document.getElementById('table-of-contents');
    if (mainToc) {
      mainToc.addEventListener('click', (event) => {
        const link = event.target.closest('a[href^="#"]');
        if (!link || !mainToc.contains(link)) return;
        const href = link.getAttribute('href');
        if (!href || href.length < 2) return;
        const target = document.getElementById(href.slice(1));
        if (!target) return;
        expandMainSectionFromTarget(target);
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (history.pushState) {
          history.pushState(null, '', href);
        } else {
          window.location.hash = href;
        }
      });
    }
  });
})();
