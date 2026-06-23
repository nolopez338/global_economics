const resultView = document.getElementById('resultView');
const groupFilter = document.getElementById('groupFilter');
const sortRows = document.getElementById('sortRows');
const sortCols = document.getElementById('sortCols');
const searchBox = document.getElementById('searchBox');
const showNames = document.getElementById('showNames');
const showMissing = document.getElementById('showMissing');
const stats = document.getElementById('stats');
const activeSummary = document.getElementById('activeSummary');
const namesEl = document.getElementById('names');
const heatmapEl = document.getElementById('heatmap');
const topBarsEl = document.getElementById('topBars');
const topBarsContent = document.getElementById('topBarsContent') || topBarsEl;
const rightBarsEl = document.getElementById('rightBars');
const rightBarsContent = document.getElementById('rightBarsContent') || rightBarsEl;
const gridEl = document.getElementById('dashboardGrid');
const tooltip = document.getElementById('tooltip');
const vizPanel = document.querySelector('.vizPanel');
const vizToolbar = document.getElementById('vizToolbar');
const vizToolbarCollapseBtn = document.getElementById('vizToolbarCollapseBtn');
const fullscreenBtn = document.getElementById('fullscreenBtn');
const dashboardScroll = document.querySelector('.dashboardScroll');
const questionOverviewBtn = document.getElementById('questionOverviewBtn');
const studentOverviewBtn = document.getElementById('studentOverviewBtn');

let questionOverviewMode = false;
let studentOverviewMode = false;

function cloneRows(rows) {
  return rows.map(row => ({
    ...row,
    answers: [...row.answers]
  }));
}

function normalizeMatricula(value) {
  return String(value ?? '').trim();
}

function nullAnswers(length) {
  return Array.from({ length }, () => null);
}

function orderedDatasetIds() {
  return Object.keys(DATASETS);
}

function prefixedQuestions(datasetIds) {
  return datasetIds.flatMap((paperId, index) => {
    const prefix = `P${index + 1}`;
    return DATASETS[paperId].questions.map(question => `${prefix}-${question}`);
  });
}

function buildAccumulatedDataset() {
  const datasetIds = orderedDatasetIds();
  const records = new Map();
  const nameIndex = new Map();

  datasetIds.forEach(paperId => {
    const dataset = DATASETS[paperId];
    dataset.rows.forEach(row => {
      const matricula = normalizeMatricula(row.matricula);
      const matriculaKey = matricula ? `m:${matricula}` : '';
      const nameKey = `n:${row.name}`;
      let key = '';

      if (matriculaKey && records.has(matriculaKey)) key = matriculaKey;
      else if (nameIndex.has(row.name)) key = nameIndex.get(row.name);
      else key = matriculaKey || nameKey;

      if (!records.has(key)) {
        records.set(key, {
          curso: row.curso,
          grupo: row.grupo,
          no: row.no,
          matricula: row.matricula,
          name: row.name,
          papers: {}
        });
        nameIndex.set(row.name, key);
      }

      const record = records.get(key);
      record.curso = record.curso || row.curso;
      record.grupo = record.grupo || row.grupo;
      record.no = record.no || row.no;
      record.matricula = record.matricula || row.matricula;
      record.name = record.name || row.name;
      record.papers[paperId] = [...row.answers];
    });
  });

  const rows = Array.from(records.values()).map(record => {
    const answers = datasetIds.flatMap(paperId => {
      const dataset = DATASETS[paperId];
      return record.papers[paperId] || nullAnswers(dataset.questions.length);
    });
    const c = counts(answers);
    return {
      curso: record.curso,
      grupo: record.grupo,
      no: record.no,
      matricula: record.matricula,
      name: record.name,
      answers,
      bien: c.pos,
      mal: c.neg,
      nr: c.zero + c.miss
    };
  });

  return {
    label: 'Accumulated: Paper 1 + Paper 2',
    questions: prefixedQuestions(datasetIds),
    rows
  };
}

function getActiveDataset() {
  if (resultView.value === 'accumulated') return buildAccumulatedDataset();
  const dataset = DATASETS[resultView.value] || DATASETS.paper1;
  return {
    label: dataset.label,
    questions: [...dataset.questions],
    rows: cloneRows(dataset.rows)
  };
}

function counts(values) {
  return values.reduce((acc, value) => {
    if (value === null || value === undefined || Number.isNaN(value)) acc.miss += 1;
    else if (value > 0) acc.pos += Number(value);
    else if (value === 0) acc.zero += 1;
    else acc.neg += 1;
    return acc;
  }, { pos: 0, zero: 0, neg: 0, miss: 0 });
}

function rowCounts(row, colOrder) {
  return counts(colOrder.map(i => row.answers[i]));
}

function hasMissingValues(row, colOrder) {
  return colOrder.some(i => {
    const value = row.answers[i];
    return value === null || value === undefined || Number.isNaN(value);
  });
}

function colCounts(rows, colIndex) {
  return counts(rows.map(r => r.answers[colIndex]));
}

function pct(n, total) {
  return total ? Math.round((n / total) * 1000) / 10 : 0;
}

function safe(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[char]));
}

function attrSafe(value) {
  return String(value).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
}

function tooltipRows(c, total) {
  const rows = [
    ['pos', 'Positive units', c.pos],
    ['zero', 'Zero', c.zero],
    ['neg', 'Negative', c.neg],
    ['miss', 'Missing', c.miss]
  ];
  return `<div class='tipRows'>${rows.map(([key, label, value]) => `
    <div class='tipRow'>
      <span><i class='tipMiniSwatch ${key}'></i>${label}</span>
      <span>${value} · ${pct(value, total)}%</span>
    </div>
  `).join('')}</div>`;
}

function expandedBarTooltip(title, c, orientation = 'vertical') {
  const total = c.pos + c.zero + c.neg + c.miss || 1;
  const parts = [
    ['pos', c.pos],
    ['zero', c.zero],
    ['neg', c.neg],
    ['miss', c.miss]
  ];
  const segments = parts.map(([key, value]) => {
    const size = Math.max(value > 0 ? pct(value, total) : 0, value > 0 ? 1 : 0);
    const dim = orientation === 'vertical' ? `height:${size}%` : `width:${size}%`;
    return `<span class='tipSeg ${key}' style='${dim}'></span>`;
  }).join('');
  if (orientation === 'vertical') {
    return `<b>${safe(title)}</b><br><span>Expanded stacked bar</span>
      <div class='tipGrid'>
        <div class='tipVBar'>${segments}</div>
        ${tooltipRows(c, total)}
      </div>`;
  }
  return `<b>${safe(title)}</b><br><span>Expanded stacked bar</span>
    <div class='tipHBar'>${segments}</div>
    ${tooltipRows(c, total)}`;
}

function labelForValue(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return 'Missing';
  if (value > 0) return 'Positive';
  if (value === 0) return 'Zero';
  return 'Negative';
}

function colorForValue(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return colors.miss;
  if (value > 0) return colors.pos;
  if (value === 0) return colors.zero;
  return colors.neg;
}

function ensureTooltipInFullscreenContext() {
  if (!tooltip) return;

  const fullscreenRoot = document.fullscreenElement;
  if (fullscreenRoot && vizPanel && fullscreenRoot.contains(vizPanel)) {
    if (tooltip.parentElement !== fullscreenRoot) fullscreenRoot.appendChild(tooltip);
  } else if (!fullscreenRoot && tooltip.parentElement !== document.body) {
    document.body.appendChild(tooltip);
  }
}

function showTip(html, event) {
  ensureTooltipInFullscreenContext();
  tooltip.innerHTML = html;
  tooltip.style.opacity = 1;
  moveTip(event);
}

function moveTip(event) {
  const pad = 14;
  const rect = tooltip.getBoundingClientRect();
  let x = event.clientX + pad;
  let y = event.clientY + pad;
  if (x + rect.width > window.innerWidth - 8) x = event.clientX - rect.width - pad;
  if (y + rect.height > window.innerHeight - 8) y = event.clientY - rect.height - pad;
  tooltip.style.left = x + 'px';
  tooltip.style.top = y + 'px';
}

function hideTip() { tooltip.style.opacity = 0; }

function firstLastName(name) {
  return String(name || '').trim().split(/\s+/)[0] || '';
}

function measureTextWidth(text) {
  if (!measureTextWidth.canvas) {
    measureTextWidth.canvas = document.createElement('canvas');
    measureTextWidth.context = measureTextWidth.canvas.getContext('2d');
  }
  const context = measureTextWidth.context;
  if (context) {
    context.font = '12px Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    return context.measureText(String(text || '')).width;
  }
  return String(text || '').length * 8;
}

function compactNameColumnWidth(rows) {
  const names = rows.map(row => firstLastName(row.name));
  const maxTextWidth = names.reduce((max, name) => Math.max(max, measureTextWidth(name)), 0);
  const badgeWidth = 26;
  const gap = 8;
  const horizontalPadding = 20;
  const safetyPadding = 14;
  return Math.ceil(badgeWidth + gap + horizontalPadding + safetyPadding + maxTextWidth);
}

function filteredRows(dataset) {
  const group = groupFilter.value;
  const query = searchBox.value.trim().toLowerCase();
  let rows = dataset.rows.filter(row => group === 'all' || row.grupo === group);
  if (query) {
    rows = rows.filter(row => (row.name + ' ' + row.matricula).toLowerCase().includes(query));
  }
  return rows;
}

function sortedRows(rows, colOrder) {
  const sorted = [...rows];
  const sort = sortRows.value;
  if (sort === 'nameAsc') sorted.sort((a, b) => a.name.localeCompare(b.name, 'es'));
  if (sort === 'positiveDesc') sorted.sort((a, b) => rowCounts(b, colOrder).pos - rowCounts(a, colOrder).pos || a.name.localeCompare(b.name, 'es'));
  if (sort === 'negativeDesc') sorted.sort((a, b) => rowCounts(b, colOrder).neg - rowCounts(a, colOrder).neg || a.name.localeCompare(b.name, 'es'));
  if (sort === 'zeroDesc') sorted.sort((a, b) => rowCounts(b, colOrder).zero - rowCounts(a, colOrder).zero || a.name.localeCompare(b.name, 'es'));
  return sorted;
}

function sortedCols(dataset, rows) {
  const cols = dataset.questions.map((q, i) => i);
  const sort = sortCols.value;
  if (sort === 'positiveDesc') cols.sort((a, b) => colCounts(rows, b).pos - colCounts(rows, a).pos || a - b);
  if (sort === 'negativeDesc') cols.sort((a, b) => colCounts(rows, b).neg - colCounts(rows, a).neg || a - b);
  if (sort === 'zeroDesc') cols.sort((a, b) => colCounts(rows, b).zero - colCounts(rows, a).zero || a - b);
  return cols;
}

function renderStats(dataset, rows, colOrder) {
  const allValues = rows.flatMap(row => colOrder.map(i => row.answers[i]));
  const c = counts(allValues);

  const card = ([label, value, note]) => `
    <div class="card">
      <div class="label">${label}</div>
      <div class="value">${value}</div>
      <div class="note">${note}</div>
    </div>
  `;

  const selectionCards = [
    ['Result View', dataset.label, 'Current dataset'],
    ['Students', rows.length, 'Visible after filters']
  ].map(card).join('');

  const responseCards = [
    ['Positive Units', c.pos, 'Visible positive units'],
    ['Negative Units', c.neg, 'Visible negative units'],
    ['Non Responses', c.zero, 'Visible non-response units']
  ].map(card).join('');

  stats.innerHTML = `
    <div class="statGroup selectionGroup">
      <div class="statGroupTitle">Selection</div>
      <div class="statGroupCards">${selectionCards}</div>
    </div>
    <div class="statGroup responseGroup">
      <div class="statGroupTitle">Response Summary</div>
      <div class="statGroupCards">${responseCards}</div>
    </div>
  `;

  activeSummary.textContent = showMissing.checked
    ? `${dataset.label} · ${dataset.questions.length} questions · ${rows.length} visible students · ${c.miss} missing`
    : `${dataset.label} · ${dataset.questions.length} questions · ${rows.length} visible students · missing hidden`;
}

function renderTopBars(dataset, rows, colOrder, effectiveCellW) {
  const width = colOrder.length * effectiveCellW;
  const maxRows = Math.max(1, ...colOrder.map(colIndex => {
    const c = colCounts(rows, colIndex);
    return c.pos + c.zero + c.neg + c.miss;
  }));
  const barMaxH = 64;
  const labelY = 102;
  let svg = `<svg width="${width}" height="${topH}" role="img" aria-label="Column stacked bar accumulations">`;
  colOrder.forEach((colIndex, visualIndex) => {
    const q = dataset.questions[colIndex];
    const c = colCounts(rows, colIndex);
    const x = visualIndex * effectiveCellW + Math.min(5, Math.max(1, effectiveCellW * 0.15));
    const barW = Math.max(1, effectiveCellW - Math.min(10, Math.max(2, effectiveCellW * 0.3)));
    let y = 78;
    const parts = [
      ['pos', c.pos],
      ['zero', c.zero],
      ['neg', c.neg],
      ['miss', c.miss]
    ];
    const tip = attrSafe(expandedBarTooltip(`Question ${q}`, c, 'vertical'));
    parts.forEach(([key, value]) => {
      const h = (value / maxRows) * barMaxH;
      y -= h;
      if (h > 0) svg += `<rect x="${x}" y="${y}" width="${barW}" height="${h}" fill="${colors[key]}" rx="2" data-tip="${tip}" />`;
    });
    svg += `<line x1="${visualIndex * effectiveCellW}" y1="82" x2="${visualIndex * effectiveCellW + effectiveCellW}" y2="82" stroke="#d7dde8" />`;
    svg += `<text x="${visualIndex * effectiveCellW + effectiveCellW / 2}" y="${labelY}" font-size="11" text-anchor="middle" fill="#334155" font-weight="700">${safe(q)}</text>`;
  });
  svg += '</svg>';
  topBarsContent.innerHTML = svg;
  attachSvgTips(topBarsContent);
}

function renderNames(rows, effectiveCellH) {
  const compact = !showNames.checked;
  namesEl.style.setProperty('--cellH', effectiveCellH + 'px');
  namesEl.innerHTML = rows.map(row => {
    const displayName = compact ? firstLastName(row.name) : row.name;
    return `
      <div class="nameCell" title="${attrSafe(row.name)}">
        <span class="groupBadge">${safe(row.grupo)}</span>
        <span class="nameText">${safe(displayName)}</span>
      </div>
    `;
  }).join('');
}

function renderHeatmap(dataset, rows, colOrder, effectiveCellW, effectiveCellH) {
  const width = colOrder.length * effectiveCellW;
  const height = rows.length * effectiveCellH;
  const showCellText = !questionOverviewMode && !studentOverviewMode;
  let svg = `<svg width="${width}" height="${height}" role="img" aria-label="Raw answer heatmap">`;
  rows.forEach((row, r) => {
    colOrder.forEach((colIndex, c) => {
      const value = row.answers[colIndex];
      const x = c * effectiveCellW;
      const y = r * effectiveCellH;
      const q = dataset.questions[colIndex];
      const fill = colorForValue(value);
      const textColor = value === 0 ? '#3c3108' : '#ffffff';
      const shown = value === null || value === undefined || Number.isNaN(value) ? '' : value;
      const tip = attrSafe(`<b>${safe(row.name)}</b><br>View: ${safe(dataset.label)}<br>Group: ${safe(row.grupo)} · No. ${safe(row.no || '—')}<br>Question: ${safe(q)}<br>Value: ${shown === '' ? 'Missing' : safe(shown)}<br>Class: ${labelForValue(value)}`);
      svg += `<rect x="${x}" y="${y}" width="${effectiveCellW}" height="${effectiveCellH}" fill="${fill}" stroke="#ffffff" stroke-width="1" data-tip="${tip}" />`;
      if (showCellText && shown !== '') svg += `<text x="${x + effectiveCellW / 2}" y="${y + effectiveCellH / 2 + 4}" font-size="11" text-anchor="middle" fill="${textColor}" font-weight="750" pointer-events="none">${shown}</text>`;
    });
  });
  svg += '</svg>';
  heatmapEl.innerHTML = svg;
  attachSvgTips(heatmapEl);
}

function renderRightBars(rows, colOrder, effectiveCellH) {
  rightBarsContent.style.setProperty('--cellH', effectiveCellH + 'px');
  rightBarsContent.innerHTML = rows.map(row => {
    const c = rowCounts(row, colOrder);
    const total = c.pos + c.zero + c.neg + c.miss || 1;
    const tip = attrSafe(expandedBarTooltip(row.name, c, 'horizontal'));
    return `
      <div class="rowBar" data-tip="${tip}">
        <div class="stack">
          <div class="segment pos" style="width:${pct(c.pos, total)}%"></div>
          <div class="segment zero" style="width:${pct(c.zero, total)}%"></div>
          <div class="segment neg" style="width:${pct(c.neg, total)}%"></div>
          <div class="segment miss" style="width:${pct(c.miss, total)}%"></div>
        </div>
        <div class="barText">${c.pos}/${c.zero}/${c.neg}</div>
      </div>
    `;
  }).join('');
  attachHtmlTips(rightBarsContent);
}

function renderQuestionOverviewHistogram(dataset, rows, colOrder, effectiveCellW) {
  const width = colOrder.length * effectiveCellW;
  const maxRows = Math.max(1, ...colOrder.map(colIndex => {
    const c = colCounts(rows, colIndex);
    return c.pos + c.zero + c.neg + c.miss;
  }));
  const barMaxH = 66;
  const baseY = 78;
  const labelY = 103;
  const fontSize = effectiveCellW < 14 ? 8 : effectiveCellW < 22 ? 9 : 10;
  const rotate = effectiveCellW < 24;
  let svg = `<svg width="${width}" height="${topH}" role="img" aria-label="Compressed question overview histogram">`;
  colOrder.forEach((colIndex, visualIndex) => {
    const q = dataset.questions[colIndex];
    const c = colCounts(rows, colIndex);
    const x = visualIndex * effectiveCellW;
    const barW = Math.max(1, effectiveCellW - 1);
    let y = baseY;
    const tip = attrSafe(expandedBarTooltip(`Question ${q}`, c, 'vertical'));
    [['pos', c.pos], ['zero', c.zero], ['neg', c.neg], ['miss', c.miss]].forEach(([key, value]) => {
      const h = (value / maxRows) * barMaxH;
      y -= h;
      if (h > 0) svg += `<rect x="${x}" y="${y}" width="${barW}" height="${h}" fill="${colors[key]}" data-tip="${tip}" />`;
    });
    svg += `<line x1="${x}" y1="82" x2="${x}" y2="88" stroke="#94a3b8" stroke-width="1" />`;
    const labelX = x + effectiveCellW / 2;
    if (rotate) {
      svg += `<text x="${labelX}" y="${labelY}" font-size="${fontSize}" text-anchor="end" fill="#334155" font-weight="700" transform="rotate(-55 ${labelX} ${labelY})">${safe(q)}</text>`;
    } else {
      svg += `<text x="${labelX}" y="${labelY}" font-size="${fontSize}" text-anchor="middle" fill="#334155" font-weight="700">${safe(q)}</text>`;
    }
  });
  svg += `<line x1="0" y1="82" x2="${width}" y2="82" stroke="#d7dde8" />`;
  svg += '</svg>';
  topBarsContent.innerHTML = svg;
  attachSvgTips(topBarsContent);
}

function renderStudentOverviewHistogram(rows, colOrder, effectiveCellH) {
  const width = 180;
  const height = rows.length * effectiveCellH;
  const barW = 118;
  const labelX = 124;
  const maxTotal = Math.max(1, ...rows.map(row => {
    const c = rowCounts(row, colOrder);
    return c.pos + c.zero + c.neg + c.miss;
  }));
  const fontSize = effectiveCellH < 12 ? 8 : effectiveCellH < 18 ? 9 : 10;
  const every = Math.max(1, Math.ceil(rows.length / Math.max(1, Math.floor(height / Math.max(10, fontSize + 2)))));
  let svg = `<svg width="${width}" height="${height}" role="img" aria-label="Compressed student overview histogram">`;
  rows.forEach((row, index) => {
    const c = rowCounts(row, colOrder);
    const total = c.pos + c.zero + c.neg + c.miss || 1;
    const y = index * effectiveCellH;
    const h = Math.max(1, effectiveCellH - 1);
    let x = 0;
    const scaledW = Math.max(1, (total / maxTotal) * barW);
    const tip = attrSafe(expandedBarTooltip(row.name, c, 'horizontal'));
    [['pos', c.pos], ['zero', c.zero], ['neg', c.neg], ['miss', c.miss]].forEach(([key, value]) => {
      const w = (value / total) * scaledW;
      if (w > 0) svg += `<rect x="${x}" y="${y}" width="${Math.max(1, w)}" height="${h}" fill="${colors[key]}" data-tip="${tip}" />`;
      x += w;
    });
    svg += `<line x1="${barW + 2}" y1="${y}" x2="${barW + 8}" y2="${y}" stroke="#94a3b8" stroke-width="1" />`;
    if (index % every === 0) svg += `<text x="${labelX}" y="${y + Math.max(fontSize, effectiveCellH / 2 + fontSize / 3)}" font-size="${fontSize}" fill="#334155" font-weight="700">${safe(firstLastName(row.name))}</text>`;
  });
  svg += '</svg>';
  rightBarsContent.innerHTML = svg;
  attachSvgTips(rightBarsContent);
}

function attachSvgTips(root) {
  root.querySelectorAll('[data-tip]').forEach(el => {
    el.addEventListener('mouseenter', event => showTip(el.getAttribute('data-tip'), event));
    el.addEventListener('mousemove', moveTip);
    el.addEventListener('mouseleave', hideTip);
  });
}

function attachHtmlTips(root) {
  root.querySelectorAll('[data-tip]').forEach(el => {
    el.addEventListener('mouseenter', event => showTip(el.getAttribute('data-tip'), event));
    el.addEventListener('mousemove', moveTip);
    el.addEventListener('mouseleave', hideTip);
  });
}

function render() {
  const dataset = getActiveDataset();
  const fullColOrder = dataset.questions.map((_, i) => i);
  let rowsPreSort = filteredRows(dataset);

  if (!showMissing.checked) {
    rowsPreSort = rowsPreSort.filter(row => !hasMissingValues(row, fullColOrder));
  }

  const colOrder = sortedCols(dataset, rowsPreSort);
  const rows = sortedRows(rowsPreSort, colOrder);
  const nameColumnWidth = showNames.checked ? 260 : compactNameColumnWidth(rows);
  const availableHeatmapWidth = Math.max(120, (dashboardScroll?.clientWidth || window.innerWidth) - nameColumnWidth - 180);
  const availableHeatmapHeight = Math.max(180, (dashboardScroll?.clientHeight || window.innerHeight - 360) - topH);
  const effectiveCellW = questionOverviewMode && colOrder.length
    ? Math.max(4, Math.floor(availableHeatmapWidth / colOrder.length))
    : cellW;
  const effectiveCellH = studentOverviewMode && rows.length
    ? Math.max(4, Math.floor(availableHeatmapHeight / rows.length))
    : cellH;
  const heatmapWidth = colOrder.length * effectiveCellW;
  gridEl.style.gridTemplateColumns = `${nameColumnWidth}px ${heatmapWidth}px 180px`;
  renderStats(dataset, rows, colOrder);
  if (questionOverviewMode) renderQuestionOverviewHistogram(dataset, rows, colOrder, effectiveCellW);
  else renderTopBars(dataset, rows, colOrder, effectiveCellW);
  renderNames(rows, effectiveCellH);
  renderHeatmap(dataset, rows, colOrder, effectiveCellW, effectiveCellH);
  if (studentOverviewMode) renderStudentOverviewHistogram(rows, colOrder, effectiveCellH);
  else renderRightBars(rows, colOrder, effectiveCellH);
}

function isVizPanelFullscreen() {
  return document.fullscreenElement === vizPanel;
}

function setVizToolbarCollapsed(collapsed) {
  if (!vizToolbar || !vizToolbarCollapseBtn) return;

  vizToolbar.classList.toggle('isCollapsed', collapsed);
  vizToolbarCollapseBtn.setAttribute('aria-expanded', String(!collapsed));
  vizToolbarCollapseBtn.setAttribute(
    'title',
    collapsed ? 'Expand visualization controls' : 'Collapse visualization controls'
  );

  const icon = vizToolbarCollapseBtn.querySelector('.collapseIcon');
  if (icon) icon.textContent = collapsed ? '▸' : '▾';
}

function updateFullscreenButton() {
  if (!fullscreenBtn) return;

  const active = isVizPanelFullscreen();
  fullscreenBtn.setAttribute(
    'aria-label',
    active ? 'Exit fullscreen' : 'Open visualization in fullscreen'
  );
  fullscreenBtn.setAttribute(
    'title',
    active ? 'Exit fullscreen' : 'Fullscreen'
  );
  fullscreenBtn.textContent = active ? '×' : '⛶';
}

async function toggleFullscreen() {
  if (!vizPanel) return;

  try {
    if (isVizPanelFullscreen()) {
      await document.exitFullscreen();
    } else {
      await vizPanel.requestFullscreen();
    }
  } catch (error) {
    console.warn('Fullscreen mode could not be toggled:', error);
  }
}

[resultView, groupFilter, sortRows, sortCols, searchBox, showNames, showMissing].forEach(control => control.addEventListener('input', render));
if (questionOverviewBtn) questionOverviewBtn.addEventListener('click', () => {
  questionOverviewMode = !questionOverviewMode;
  questionOverviewBtn.setAttribute('aria-pressed', String(questionOverviewMode));
  render();
});
if (studentOverviewBtn) studentOverviewBtn.addEventListener('click', () => {
  studentOverviewMode = !studentOverviewMode;
  studentOverviewBtn.setAttribute('aria-pressed', String(studentOverviewMode));
  render();
});
if (fullscreenBtn) fullscreenBtn.addEventListener('click', toggleFullscreen);
if (vizToolbarCollapseBtn) vizToolbarCollapseBtn.addEventListener('click', () => {
  if (!vizToolbar) return;
  setVizToolbarCollapsed(!vizToolbar.classList.contains('isCollapsed'));
});
window.addEventListener('resize', render);
document.addEventListener('fullscreenchange', () => {
  updateFullscreenButton();
  ensureTooltipInFullscreenContext();
});
updateFullscreenButton();
setVizToolbarCollapsed(false);
render();
