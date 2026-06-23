const resultView = document.getElementById('resultView');
const groupFilter = document.getElementById('groupFilter');
const sortRows = document.getElementById('sortRows');
const sortCols = document.getElementById('sortCols');
const sortRowsAscBtn = document.getElementById('sortRowsAscBtn');
const sortRowsDescBtn = document.getElementById('sortRowsDescBtn');
const sortColsAscBtn = document.getElementById('sortColsAscBtn');
const sortColsDescBtn = document.getElementById('sortColsDescBtn');
const searchBox = document.getElementById('searchBox');
const showNames = document.getElementById('showNames');
const showMissing = document.getElementById('showMissing');
const stats = document.getElementById('stats');
const activeSummary = document.getElementById('activeSummary');
const namesEl = document.getElementById('names');
const heatmapEl = document.getElementById('heatmap');
const topBarsEl = document.getElementById('topBars');
const topBarsContentEl = document.getElementById('topBarsContent') || topBarsEl;
const rightBarsEl = document.getElementById('rightBars');
const rightBarsContentEl = document.getElementById('rightBarsContent') || rightBarsEl;
const gridEl = document.getElementById('dashboardGrid');
const tooltip = document.getElementById('tooltip');
const cellQuestionTooltip = document.getElementById('cellQuestionTooltip');
const cellStudentTooltip = document.getElementById('cellStudentTooltip');
const vizPanel = document.querySelector('.vizPanel');
const vizToolbar = document.getElementById('vizToolbar');
const vizToolbarCollapseBtn = document.getElementById('vizToolbarCollapseBtn');
const fullscreenBtn = document.getElementById('fullscreenBtn');
const dashboardScroll = document.querySelector('.dashboardScroll');
const questionOverviewBtn = document.getElementById('questionOverviewBtn');
const studentOverviewBtn = document.getElementById('studentOverviewBtn');

let questionOverviewMode = false;
let studentOverviewMode = false;
let sortRowsDirection = 'desc';
let sortColsDirection = 'desc';

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

function ratioSortConfig(sortValue) {
  const configs = {
    posNegRatioDesc: {
      numerator: 'pos',
      denominator: 'neg',
      label: 'Positive / Negative ratio'
    },
    posZeroRatioDesc: {
      numerator: 'pos',
      denominator: 'zero',
      label: 'Positive / Non responses ratio'
    },
    negZeroRatioDesc: {
      numerator: 'neg',
      denominator: 'zero',
      label: 'Negative / Non responses ratio'
    }
  };

  return configs[sortValue] || null;
}

function ratioValue(countsObject, config) {
  if (!config) return null;

  const numerator = countsObject[config.numerator] || 0;
  const denominator = countsObject[config.denominator] || 0;

  if (denominator === 0) return null;

  return numerator / denominator;
}

function formatRatio(value) {
  return value === null || value === undefined || Number.isNaN(value)
    ? '—'
    : value.toFixed(2);
}

function isOriginalSort(value) {
  return value === 'original';
}

function directionMultiplier(direction) {
  return direction === 'asc' ? 1 : -1;
}

function compareMetric(aValue, bValue, direction) {
  if (aValue === null && bValue === null) return 0;
  if (aValue === null) return 1;
  if (bValue === null) return -1;

  return direction === 'asc'
    ? aValue - bValue
    : bValue - aValue;
}

function updateSortDirectionButtons() {
  const rowsOriginal = isOriginalSort(sortRows.value);
  const colsOriginal = isOriginalSort(sortCols.value);

  sortRowsAscBtn.disabled = rowsOriginal;
  sortRowsDescBtn.disabled = rowsOriginal;
  sortColsAscBtn.disabled = colsOriginal;
  sortColsDescBtn.disabled = colsOriginal;

  sortRowsAscBtn.classList.toggle('isActive', !rowsOriginal && sortRowsDirection === 'asc');
  sortRowsDescBtn.classList.toggle('isActive', !rowsOriginal && sortRowsDirection === 'desc');

  sortColsAscBtn.classList.toggle('isActive', !colsOriginal && sortColsDirection === 'asc');
  sortColsDescBtn.classList.toggle('isActive', !colsOriginal && sortColsDirection === 'desc');
}

function ratioTooltipRows(c) {
  return `<div class='tipRows'>${[
    ['pos', 'Positive units', c.pos],
    ['zero', 'Non Responses', c.zero],
    ['neg', 'Negative units', c.neg]
  ].map(([key, label, value]) => `
    <div class='tipRow'>
      <span><i class='tipMiniSwatch ${key}'></i>${label}</span>
      <span>${value}</span>
    </div>
  `).join('')}</div>`;
}

function ratioBarTooltip(title, c, ratioConfig, ratio) {
  return `<b>${safe(title)}</b><br><span>${safe(ratioConfig.label)}: ${formatRatio(ratio)}</span>${ratioTooltipRows(c)}`;
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
  const visibleTotal = total || c.pos + c.zero + c.neg || 1;
  const rows = [
    ['pos', 'Positive units', c.pos],
    ['zero', 'Non Responses', c.zero],
    ['neg', 'Negative units', c.neg]
  ];
  return `<div class='tipRows'>${rows.map(([key, label, value]) => `
    <div class='tipRow'>
      <span><i class='tipMiniSwatch ${key}'></i>${label}</span>
      <span>${value} · ${pct(value, visibleTotal)}%</span>
    </div>
  `).join('')}</div>`;
}

function expandedBarTooltip(title, c, orientation = 'vertical', subtitle = 'Expanded stacked bar') {
  const total = c.pos + c.zero + c.neg || 1;
  const parts = [
    ['pos', c.pos],
    ['zero', c.zero],
    ['neg', c.neg]
  ];
  const segments = parts.map(([key, value]) => {
    const size = Math.max(value > 0 ? pct(value, total) : 0, value > 0 ? 1 : 0);
    const dim = orientation === 'vertical' ? `height:${size}%` : `width:${size}%`;
    return `<span class='tipSeg ${key}' style='${dim}'></span>`;
  }).join('');
  if (orientation === 'vertical') {
    return `<b>${safe(title)}</b><br><span>${subtitle}</span>
      <div class='tipGrid'>
        <div class='tipVBar'>${segments}</div>
        ${tooltipRows(c, total)}
      </div>`;
  }
  return `<b>${safe(title)}</b><br><span>${subtitle}</span>
    <div class='tipHBar'>${segments}</div>
    ${tooltipRows(c, total)}`;
}

function questionTooltipHtml(dataset, rows, colIndex) {
  const question = dataset.questions[colIndex];
  const c = colCounts(rows, colIndex);
  return expandedBarTooltip(`Question ${question}`, c, 'vertical');
}

function studentTooltipHtml(row, colOrder) {
  const c = rowCounts(row, colOrder);
  return studentBarTooltip(row, c);
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
  const tooltipEls = [tooltip, cellQuestionTooltip, cellStudentTooltip].filter(Boolean);
  if (!tooltipEls.length) return;

  const fullscreenRoot = document.fullscreenElement;
  if (fullscreenRoot && vizPanel && fullscreenRoot.contains(vizPanel)) {
    tooltipEls.forEach(el => {
      if (el.parentElement !== fullscreenRoot) fullscreenRoot.appendChild(el);
    });
  } else if (!fullscreenRoot) {
    tooltipEls.forEach(el => {
      if (el.parentElement !== document.body) document.body.appendChild(el);
    });
  }
}

function showTip(html, event) {
  ensureTooltipInFullscreenContext();
  hideCellContextTips();
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

function showCellContextTips(questionHtml, studentHtml, event) {
  ensureTooltipInFullscreenContext();
  hideTip();

  cellQuestionTooltip.innerHTML = questionHtml;
  cellStudentTooltip.innerHTML = studentHtml;

  cellQuestionTooltip.style.opacity = 1;
  cellStudentTooltip.style.opacity = 1;

  moveCellContextTips(event);
}

function moveCellContextTips(event) {
  const pad = 12;

  const qRect = cellQuestionTooltip.getBoundingClientRect();
  const sRect = cellStudentTooltip.getBoundingClientRect();

  let qX = event.clientX - qRect.width / 2;
  let qY = event.clientY - qRect.height - pad;

  let sX = event.clientX + pad;
  let sY = event.clientY - sRect.height / 2;

  qX = Math.max(8, Math.min(qX, window.innerWidth - qRect.width - 8));
  qY = Math.max(8, Math.min(qY, window.innerHeight - qRect.height - 8));

  if (sX + sRect.width > window.innerWidth - 8) {
    sX = event.clientX - sRect.width - pad;
  }
  sY = Math.max(8, Math.min(sY, window.innerHeight - sRect.height - 8));

  cellQuestionTooltip.style.left = qX + 'px';
  cellQuestionTooltip.style.top = qY + 'px';

  cellStudentTooltip.style.left = sX + 'px';
  cellStudentTooltip.style.top = sY + 'px';
}

function hideCellContextTips() {
  if (cellQuestionTooltip) cellQuestionTooltip.style.opacity = 0;
  if (cellStudentTooltip) cellStudentTooltip.style.opacity = 0;
}

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
  const ratioConfig = ratioSortConfig(sort);

  if (ratioConfig) {
    sorted.sort((a, b) => {
      const aRatio = ratioValue(rowCounts(a, colOrder), ratioConfig);
      const bRatio = ratioValue(rowCounts(b, colOrder), ratioConfig);

      return compareMetric(aRatio, bRatio, sortRowsDirection) || a.name.localeCompare(b.name, 'es');
    });
  } else {
    if (sort === 'nameAsc') {
      sorted.sort((a, b) => sortRowsDirection === 'asc'
        ? a.name.localeCompare(b.name, 'es')
        : b.name.localeCompare(a.name, 'es'));
    }
    if (sort === 'positiveDesc') sorted.sort((a, b) => compareMetric(rowCounts(a, colOrder).pos, rowCounts(b, colOrder).pos, sortRowsDirection) || a.name.localeCompare(b.name, 'es'));
    if (sort === 'negativeDesc') sorted.sort((a, b) => compareMetric(rowCounts(a, colOrder).neg, rowCounts(b, colOrder).neg, sortRowsDirection) || a.name.localeCompare(b.name, 'es'));
    if (sort === 'zeroDesc') sorted.sort((a, b) => compareMetric(rowCounts(a, colOrder).zero, rowCounts(b, colOrder).zero, sortRowsDirection) || a.name.localeCompare(b.name, 'es'));
  }
  return sorted;
}

function sortedCols(dataset, rows) {
  const cols = dataset.questions.map((q, i) => i);
  const sort = sortCols.value;
  const ratioConfig = ratioSortConfig(sort);

  if (ratioConfig) {
    cols.sort((a, b) => {
      const aRatio = ratioValue(colCounts(rows, a), ratioConfig);
      const bRatio = ratioValue(colCounts(rows, b), ratioConfig);

      return compareMetric(aRatio, bRatio, sortColsDirection) || a - b;
    });
  } else {
    if (sort === 'positiveDesc') cols.sort((a, b) => compareMetric(colCounts(rows, a).pos, colCounts(rows, b).pos, sortColsDirection) || a - b);
    if (sort === 'negativeDesc') cols.sort((a, b) => compareMetric(colCounts(rows, a).neg, colCounts(rows, b).neg, sortColsDirection) || a - b);
    if (sort === 'zeroDesc') cols.sort((a, b) => compareMetric(colCounts(rows, a).zero, colCounts(rows, b).zero, sortColsDirection) || a - b);
  }
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
    ['Result View', dataset.label, ''],
    ['Students', rows.length, '']
  ].map(card).join('');

  const responseCards = [
    ['Positive Units', c.pos, ''],
    ['Negative Units', c.neg, ''],
    ['Non Responses', c.zero, '']
  ].map(card).join('');

  stats.innerHTML = `
    <div class="statGroup selectionGroup">
      <div class="statGroupTitle">Selection</div>
      <div class="statGroupCards">${selectionCards}</div>
    </div>
    <div class="statGroup responseGroup">
      <div class="statGroupTitle">Summary</div>
      <div class="statGroupCards">${responseCards}</div>
    </div>
  `;

  activeSummary.textContent = `${dataset.label} · ${dataset.questions.length} questions · ${rows.length} students`;
}


function renderQuestionRatioHistogram(dataset, rows, colOrder, effectiveCellW) {
  const ratioConfig = ratioSortConfig(sortCols.value);
  if (!ratioConfig) return false;

  const width = colOrder.length * effectiveCellW;
  const values = colOrder.map(colIndex => {
    const c = colCounts(rows, colIndex);
    return { colIndex, counts: c, ratio: ratioValue(c, ratioConfig) };
  });
  const maxRatio = Math.max(1, ...values.map(item => item.ratio ?? 0));
  const barMaxH = 64;
  const baseY = 82;
  const labelY = questionOverviewMode ? 103 : 102;
  const fontSize = questionOverviewMode ? (effectiveCellW < 14 ? 8 : effectiveCellW < 22 ? 9 : 10) : 11;
  const rotate = questionOverviewMode && effectiveCellW < 24;
  let svg = `<svg width="${width}" height="${topH}" role="img" aria-label="Question ratio histogram">`;

  values.forEach((item, visualIndex) => {
    const q = dataset.questions[item.colIndex];
    const x = questionOverviewMode
      ? visualIndex * effectiveCellW
      : visualIndex * effectiveCellW + Math.min(5, Math.max(1, effectiveCellW * 0.15));
    const barW = questionOverviewMode
      ? Math.max(1, effectiveCellW - 1)
      : Math.max(1, effectiveCellW - Math.min(10, Math.max(2, effectiveCellW * 0.3)));
    const h = item.ratio === null ? 0 : (item.ratio / maxRatio) * barMaxH;
    const y = baseY - h;
    const tip = attrSafe(ratioBarTooltip(`Question ${q}`, item.counts, ratioConfig, item.ratio));

    if (h > 0) svg += `<rect x="${x}" y="${y}" width="${barW}" height="${h}" fill="${colors.ratio}" rx="2" data-tip="${tip}" />`;
    svg += `<rect x="${visualIndex * effectiveCellW}" y="${baseY - barMaxH}" width="${effectiveCellW}" height="${barMaxH}" fill="transparent" data-tip="${tip}" />`;
    svg += questionOverviewMode
      ? `<line x1="${visualIndex * effectiveCellW}" y1="82" x2="${visualIndex * effectiveCellW}" y2="88" stroke="#94a3b8" stroke-width="1" />`
      : `<line x1="${visualIndex * effectiveCellW}" y1="82" x2="${visualIndex * effectiveCellW + effectiveCellW}" y2="82" stroke="#d7dde8" />`;
    const labelX = visualIndex * effectiveCellW + effectiveCellW / 2;
    if (rotate) {
      svg += `<text x="${labelX}" y="${labelY}" font-size="${fontSize}" text-anchor="end" fill="#334155" font-weight="700" transform="rotate(-55 ${labelX} ${labelY})">${safe(q)}</text>`;
    } else {
      svg += `<text x="${labelX}" y="${labelY}" font-size="${fontSize}" text-anchor="middle" fill="#334155" font-weight="700">${safe(q)}</text>`;
    }
  });
  svg += `<line x1="0" y1="82" x2="${width}" y2="82" stroke="#d7dde8" />`;
  svg += '</svg>';
  topBarsContentEl.innerHTML = svg;
  attachSvgTips(topBarsContentEl);
  return true;
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
  topBarsContentEl.innerHTML = svg;
  attachSvgTips(topBarsContentEl);
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
      const fill = colorForValue(value);
      const textColor = value === 0 ? '#3c3108' : '#ffffff';
      const isMissing = value === null || value === undefined || Number.isNaN(value);
      const shown = isMissing ? '' : value;
      if (isMissing) {
        svg += `<rect x="${x}" y="${y}" width="${effectiveCellW}" height="${effectiveCellH}" fill="${fill}" stroke="#ffffff" stroke-width="1" />`;
      } else {
        const questionTip = attrSafe(questionTooltipHtml(dataset, rows, colIndex));
        const studentTip = attrSafe(studentTooltipHtml(row, colOrder));
        svg += `<rect x="${x}" y="${y}" width="${effectiveCellW}" height="${effectiveCellH}" fill="${fill}" stroke="#ffffff" stroke-width="1" data-question-tip="${questionTip}" data-student-tip="${studentTip}" />`;
      }
      if (showCellText && shown !== '') svg += `<text x="${x + effectiveCellW / 2}" y="${y + effectiveCellH / 2 + 4}" font-size="11" text-anchor="middle" fill="${textColor}" font-weight="750" pointer-events="none">${shown}</text>`;
    });
  });
  svg += '</svg>';
  heatmapEl.innerHTML = svg;
  attachHeatmapCellTips(heatmapEl);
}

function studentBarTooltip(row, c) {
  return expandedBarTooltip(
    row.name,
    c,
    'horizontal',
    `Group: ${safe(row.grupo)} · No. ${safe(row.no || '—')}`
  );
}


function renderStudentRatioHistogram(rows, colOrder, effectiveCellH) {
  const ratioConfig = ratioSortConfig(sortRows.value);
  if (!ratioConfig) return false;

  const width = studentOverviewMode ? 198 : 180;
  const barW = studentOverviewMode ? 172 : 132;
  const values = rows.map(row => {
    const c = rowCounts(row, colOrder);
    return { row, counts: c, ratio: ratioValue(c, ratioConfig) };
  });
  const maxRatio = Math.max(1, ...values.map(item => item.ratio ?? 0));

  if (studentOverviewMode) {
    const height = rows.length * effectiveCellH;
    let svg = `<svg width="${width}" height="${height}" role="img" aria-label="Student ratio histogram">`;
    values.forEach((item, index) => {
      const y = index * effectiveCellH;
      const h = Math.max(1, effectiveCellH - 1);
      const w = item.ratio === null ? 0 : (item.ratio / maxRatio) * barW;
      const tip = attrSafe(ratioBarTooltip(`${item.row.name} · Group: ${item.row.grupo}`, item.counts, ratioConfig, item.ratio));
      if (w > 0) svg += `<rect x="0" y="${y}" width="${Math.max(1, w)}" height="${h}" fill="${colors.ratio}" data-tip="${tip}" />`;
      svg += `<rect x="0" y="${y}" width="${barW}" height="${h}" fill="transparent" data-tip="${tip}" />`;
      svg += `<line x1="${barW + 4}" y1="${y}" x2="${barW + 14}" y2="${y}" stroke="#94a3b8" stroke-width="1" />`;
    });
    svg += '</svg>';
    rightBarsContentEl.innerHTML = svg;
    attachSvgTips(rightBarsContentEl);
    return true;
  }

  rightBarsContentEl.style.setProperty('--cellH', effectiveCellH + 'px');
  rightBarsContentEl.innerHTML = values.map(item => {
    const w = item.ratio === null ? 0 : (item.ratio / maxRatio) * 100;
    const tip = attrSafe(ratioBarTooltip(`${item.row.name} · Group: ${item.row.grupo}`, item.counts, ratioConfig, item.ratio));
    return `
      <div class="rowBar" data-tip="${tip}">
        <div class="stack" style="background:#edf2f7">
          <div class="segment" style="width:${w}%;background:${colors.ratio}"></div>
        </div>
        <div class="barText">${formatRatio(item.ratio)}</div>
      </div>
    `;
  }).join('');
  attachHtmlTips(rightBarsContentEl);
  return true;
}

function renderRightBars(rows, colOrder, effectiveCellH) {
  rightBarsContentEl.style.setProperty('--cellH', effectiveCellH + 'px');
  rightBarsContentEl.innerHTML = rows.map(row => {
    const c = rowCounts(row, colOrder);
    const total = c.pos + c.zero + c.neg + c.miss || 1;
    const tip = attrSafe(studentBarTooltip(row, c));
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
  attachHtmlTips(rightBarsContentEl);
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
  topBarsContentEl.innerHTML = svg;
  attachSvgTips(topBarsContentEl);
}

function renderStudentOverviewHistogram(rows, colOrder, effectiveCellH) {
  const width = 198;
  const height = rows.length * effectiveCellH;
  const barW = 172;
  const maxTotal = Math.max(1, ...rows.map(row => {
    const c = rowCounts(row, colOrder);
    return c.pos + c.zero + c.neg + c.miss;
  }));
  let svg = `<svg width="${width}" height="${height}" role="img" aria-label="Compressed student overview histogram">`;
  rows.forEach((row, index) => {
    const c = rowCounts(row, colOrder);
    const total = c.pos + c.zero + c.neg + c.miss || 1;
    const y = index * effectiveCellH;
    const h = Math.max(1, effectiveCellH - 1);
    let x = 0;
    const scaledW = Math.max(1, (total / maxTotal) * barW);
    const tip = attrSafe(studentBarTooltip(row, c));
    [['pos', c.pos], ['zero', c.zero], ['neg', c.neg], ['miss', c.miss]].forEach(([key, value]) => {
      const w = (value / total) * scaledW;
      if (w > 0) svg += `<rect x="${x}" y="${y}" width="${Math.max(1, w)}" height="${h}" fill="${colors[key]}" data-tip="${tip}" />`;
      x += w;
    });
    svg += `<line x1="${barW + 4}" y1="${y}" x2="${barW + 14}" y2="${y}" stroke="#94a3b8" stroke-width="1" />`;
  });
  svg += '</svg>';
  rightBarsContentEl.innerHTML = svg;
  attachSvgTips(rightBarsContentEl);
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

function attachHeatmapCellTips(root) {
  root.querySelectorAll('[data-question-tip][data-student-tip]').forEach(el => {
    el.addEventListener('mouseenter', event => {
      showCellContextTips(
        el.getAttribute('data-question-tip'),
        el.getAttribute('data-student-tip'),
        event
      );
    });
    el.addEventListener('mousemove', moveCellContextTips);
    el.addEventListener('mouseleave', hideCellContextTips);
  });
}


function updateQuestionOverviewButtonPosition() {
  if (!dashboardScroll || !questionOverviewBtn) return;

  const left = Math.max(8, dashboardScroll.scrollLeft + dashboardScroll.clientWidth - questionOverviewBtn.offsetWidth - 8);
  const top = Math.max(8, dashboardScroll.scrollTop + 8);
  questionOverviewBtn.style.transform = `translate(${left}px, ${top}px)`;
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
  gridEl.classList.toggle('studentOverviewActive', studentOverviewMode);
  const nameColumnWidth = studentOverviewMode ? 0 : (showNames.checked ? 260 : compactNameColumnWidth(rows));
  const rightColumnWidth = studentOverviewMode ? 210 : 180;
  const availableHeatmapWidth = Math.max(120, (dashboardScroll?.clientWidth || window.innerWidth) - nameColumnWidth - rightColumnWidth);
  const availableHeatmapHeight = Math.max(180, (dashboardScroll?.clientHeight || window.innerHeight - 360) - topH);
  const effectiveCellW = questionOverviewMode && colOrder.length
    ? Math.max(4, Math.floor(availableHeatmapWidth / colOrder.length))
    : cellW;
  const effectiveCellH = studentOverviewMode && rows.length
    ? Math.max(4, Math.floor(availableHeatmapHeight / rows.length))
    : cellH;
  const heatmapWidth = colOrder.length * effectiveCellW;
  gridEl.style.gridTemplateColumns = `${nameColumnWidth}px ${heatmapWidth}px ${rightColumnWidth}px`;
  renderStats(dataset, rows, colOrder);
  if (!renderQuestionRatioHistogram(dataset, rows, colOrder, effectiveCellW)) {
    if (questionOverviewMode) renderQuestionOverviewHistogram(dataset, rows, colOrder, effectiveCellW);
    else renderTopBars(dataset, rows, colOrder, effectiveCellW);
  }
  renderNames(rows, effectiveCellH);
  renderHeatmap(dataset, rows, colOrder, effectiveCellW, effectiveCellH);
  if (!renderStudentRatioHistogram(rows, colOrder, effectiveCellH)) {
    if (studentOverviewMode) renderStudentOverviewHistogram(rows, colOrder, effectiveCellH);
    else renderRightBars(rows, colOrder, effectiveCellH);
  }
  updateQuestionOverviewButtonPosition();
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

[resultView, groupFilter, searchBox, showNames, showMissing].forEach(control => control.addEventListener('input', render));
sortRows.addEventListener('input', () => {
  updateSortDirectionButtons();
  render();
});
sortCols.addEventListener('input', () => {
  updateSortDirectionButtons();
  render();
});
sortRowsAscBtn.addEventListener('click', () => {
  if (isOriginalSort(sortRows.value)) return;
  sortRowsDirection = 'asc';
  updateSortDirectionButtons();
  render();
});
sortRowsDescBtn.addEventListener('click', () => {
  if (isOriginalSort(sortRows.value)) return;
  sortRowsDirection = 'desc';
  updateSortDirectionButtons();
  render();
});
sortColsAscBtn.addEventListener('click', () => {
  if (isOriginalSort(sortCols.value)) return;
  sortColsDirection = 'asc';
  updateSortDirectionButtons();
  render();
});
sortColsDescBtn.addEventListener('click', () => {
  if (isOriginalSort(sortCols.value)) return;
  sortColsDirection = 'desc';
  updateSortDirectionButtons();
  render();
});
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
if (dashboardScroll) dashboardScroll.addEventListener('scroll', updateQuestionOverviewButtonPosition, { passive: true });
document.addEventListener('fullscreenchange', () => {
  updateFullscreenButton();
  ensureTooltipInFullscreenContext();
});
updateFullscreenButton();
updateSortDirectionButtons();
setVizToolbarCollapsed(false);
render();
