(function () {
  "use strict";
  const tablist = document.querySelector('.main-tabs');
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));

  function selectTab(selected) {
    tabs.forEach(tab => {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    });
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      switch (event.key) {
        case 'ArrowRight': next = (index + 1) % tabs.length; break;
        case 'ArrowLeft': next = (index + tabs.length - 1) % tabs.length; break;
        case 'Home': next = 0; break;
        case 'End': next = tabs.length - 1; break;
        default: return;
      }
      event.preventDefault();
      selectTab(tabs[next]);
      tabs[next].focus();
    });
  });

  // Today's assignments live only in this closure and the rendered text.
  // Tab changes hide panels without recreating them; a reload starts fresh.
  const monitorSeats = Array.from(document.querySelectorAll('.monitor-seat'));
  const monitorNames = monitorSeats.map(() => '');
  const editor = document.getElementById('monitor-editor');
  const nameInput = document.getElementById('monitor-name-input');
  const editorHeading = document.getElementById('monitor-editor-heading');
  let editingIndex = null;

  function openEditor(row) {
    if (editor.open) return;
    editingIndex = Number(row) - 1;
    editorHeading.textContent = `Row ${row} monitor`;
    nameInput.value = monitorNames[editingIndex];
    editor.showModal();
    nameInput.focus();
    nameInput.select();
  }

  function saveMonitor(name) {
    if (editingIndex === null) return;
    const seat = monitorSeats[editingIndex];
    monitorNames[editingIndex] = name.trim();
    const label = monitorNames[editingIndex] || 'Unassigned';
    seat.querySelector('.monitor-name').textContent = monitorNames[editingIndex] || '—';
    seat.setAttribute('aria-label', `Row ${seat.dataset.row} monitor: ${label}`);
    closeEditor();
  }

  function closeEditor() {
    editingIndex = null;
    editor.close();
  }

  monitorSeats.forEach(seat => {
    seat.addEventListener('dblclick', () => openEditor(seat.dataset.row));
    seat.addEventListener('keydown', event => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      openEditor(seat.dataset.row);
    });
    // Assistive technology can activate a button without pointer clicks.
    seat.addEventListener('click', event => {
      if (event.detail === 0) openEditor(seat.dataset.row);
    });
  });
  document.querySelectorAll('.edit-monitor').forEach(button => {
    button.addEventListener('click', () => openEditor(button.dataset.row));
  });
  document.getElementById('monitor-editor-form').addEventListener('submit', event => {
    event.preventDefault();
    saveMonitor(nameInput.value);
  });
  document.getElementById('clear-monitor').addEventListener('click', () => saveMonitor(''));
  document.getElementById('cancel-monitor').addEventListener('click', closeEditor);
  // Native dialog cancellation handles Escape and restores the opener's focus.
  editor.addEventListener('cancel', () => { editingIndex = null; });
})();
