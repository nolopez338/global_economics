window.MathJax = {
  tex: {
    inlineMath: [["$", "$"], ["\\(", "\\)"]],
    displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    processEscapes: true
  }
};

(() => {
  const SVG_NS = "http://www.w3.org/2000/svg";

  function createSvgElement(tagName, attributes = {}) {
    const element = document.createElementNS(SVG_NS, tagName);
    Object.entries(attributes).forEach(([key, value]) => {
      element.setAttribute(key, String(value));
    });
    return element;
  }

  function formatTick(value) {
    if (Math.abs(value) < 1e-10) {
      return "0";
    }
    if (Math.abs(value) >= 1 || Number.isInteger(value)) {
      return Number(value.toFixed(2)).toString();
    }
    return Number(value.toFixed(3)).toString();
  }

  function buildPath(points) {
    return points
      .map((point, index) => `${index === 0 ? "M" : "L"}${point[0]},${point[1]}`)
      .join(" ");
  }

  function sampleFunction(fn, domain, sampleCount = 360) {
    const [xMin, xMax] = domain;
    const samples = [];

    for (let i = 0; i <= sampleCount; i += 1) {
      const x = xMin + (i / sampleCount) * (xMax - xMin);
      const yValue = Number(fn(x));
      const y = Number.isFinite(yValue) ? Math.max(0, yValue) : 0;
      samples.push({ x, y });
    }

    return samples;
  }

  function createScale(domain, samples, plotWidth, plotHeight, yPaddingFactor = 1.12) {
    const [xMin, xMax] = domain;
    const yMax = Math.max(...samples.map((sample) => sample.y), 1);
    const yLimit = yMax * yPaddingFactor;

    const xToPx = (x) => ((x - xMin) / (xMax - xMin)) * plotWidth;
    const yToPx = (y) => plotHeight - (y / yLimit) * plotHeight;

    return { xToPx, yToPx, yLimit, xMin, xMax };
  }

  function createGrid({ plotWidth, plotHeight, gridXCount = 6, gridYCount = 5 }) {
    const gridGroup = createSvgElement("g", { class: "graph-grid" });

    for (let i = 0; i <= gridYCount; i += 1) {
      const y = (i / gridYCount) * plotHeight;
      gridGroup.appendChild(createSvgElement("line", { x1: 0, y1: y, x2: plotWidth, y2: y }));
    }

    for (let i = 0; i <= gridXCount; i += 1) {
      const x = (i / gridXCount) * plotWidth;
      gridGroup.appendChild(createSvgElement("line", { x1: x, y1: 0, x2: x, y2: plotHeight }));
    }

    return gridGroup;
  }

  function clampHighlightInterval(domain, highlightInterval) {
    const [xMin, xMax] = domain;
    const [rawStart, rawEnd] = highlightInterval;
    const start = Math.max(xMin, Math.min(rawStart, rawEnd));
    const end = Math.min(xMax, Math.max(rawStart, rawEnd));
    return [start, end];
  }

  function createCurvePath(samples, xToPx, yToPx) {
    const curvePoints = samples.map((sample) => [xToPx(sample.x), yToPx(sample.y)]);
    return buildPath(curvePoints);
  }

  function createHighlightAreaPath(samples, interval, xToPx, yToPx, xAxisY) {
    const [highlightStart, highlightEnd] = interval;
    if (highlightEnd <= highlightStart) {
      return "";
    }

    const highlightPoints = samples
      .filter((sample) => sample.x >= highlightStart && sample.x <= highlightEnd)
      .map((sample) => [xToPx(sample.x), yToPx(sample.y)]);

    if (highlightPoints.length < 2) {
      return "";
    }

    return `${buildPath([
      [xToPx(highlightStart), xAxisY],
      ...highlightPoints,
      [xToPx(highlightEnd), xAxisY]
    ])} Z`;
  }

  function createAxesAndTicks(rootGroup, options) {
    const {
      xMin,
      xMax,
      yLimit,
      xToPx,
      yToPx,
      plotWidth,
      plotHeight,
      xAxisY,
      xTickCount = 5,
      yTickCount = 4,
      xLabel = "x",
      yLabel = "f(x)"
    } = options;

    rootGroup.appendChild(createSvgElement("line", { class: "axis", x1: 0, y1: xAxisY, x2: plotWidth, y2: xAxisY }));
    rootGroup.appendChild(createSvgElement("line", { class: "axis", x1: 0, y1: plotHeight, x2: 0, y2: 0 }));

    for (let i = 0; i <= xTickCount; i += 1) {
      const xValue = xMin + (i / xTickCount) * (xMax - xMin);
      const x = xToPx(xValue);
      const tickGroup = createSvgElement("g", { class: "tick" });
      tickGroup.appendChild(createSvgElement("line", { x1: x, y1: xAxisY, x2: x, y2: xAxisY + 8 }));
      const text = createSvgElement("text", { x, y: xAxisY + 26, "text-anchor": "middle" });
      text.textContent = formatTick(xValue);
      tickGroup.appendChild(text);
      rootGroup.appendChild(tickGroup);
    }

    for (let i = 0; i <= yTickCount; i += 1) {
      const yValue = (i / yTickCount) * yLimit;
      const y = yToPx(yValue);
      const tickGroup = createSvgElement("g", { class: "tick" });
      tickGroup.appendChild(createSvgElement("line", { x1: -8, y1: y, x2: 0, y2: y }));
      const text = createSvgElement("text", { x: -12, y: y + 4, "text-anchor": "end" });
      text.textContent = formatTick(yValue);
      tickGroup.appendChild(text);
      rootGroup.appendChild(tickGroup);
    }

    const xLabelElement = createSvgElement("text", {
      class: "axis-label domain-label",
      x: plotWidth + 10,
      y: xAxisY + 5
    });
    xLabelElement.textContent = xLabel;
    rootGroup.appendChild(xLabelElement);

    const yLabelElement = createSvgElement("text", {
      class: "axis-label domain-label",
      x: -24,
      y: -4
    });
    yLabelElement.textContent = yLabel;
    rootGroup.appendChild(yLabelElement);
  }

  function renderProbabilityGraph(targetElement, fn, domain, highlightInterval, config = {}) {
    if (!targetElement) {
      return;
    }

    const width = config.width || 760;
    const height = config.height || 320;
    const margin = config.margin || { top: 20, right: 60, bottom: 40, left: 80 };
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;
    const sampleCount = config.sampleCount || 360;

    const samples = sampleFunction(fn, domain, sampleCount);
    const scale = createScale(domain, samples, plotWidth, plotHeight, config.yPaddingFactor || 1.12);
    const [highlightStart, highlightEnd] = clampHighlightInterval(domain, highlightInterval);
    const xAxisY = scale.yToPx(0);

    const svg = createSvgElement("svg", {
      viewBox: `0 0 ${width} ${height}`,
      role: "img",
      "aria-label": targetElement.dataset.graphLabel || config.ariaLabel || "Probability density graph"
    });

    const rootGroup = createSvgElement("g", { transform: `translate(${margin.left},${margin.top})` });
    svg.appendChild(rootGroup);

    rootGroup.appendChild(createGrid({
      plotWidth,
      plotHeight,
      gridXCount: config.gridXCount || 6,
      gridYCount: config.gridYCount || 5
    }));

    rootGroup.appendChild(createSvgElement("rect", {
      class: "support-region",
      x: 0,
      y: 0,
      width: plotWidth,
      height: plotHeight
    }));

    const highlightPath = createHighlightAreaPath(samples, [highlightStart, highlightEnd], scale.xToPx, scale.yToPx, xAxisY);
    if (highlightPath) {
      rootGroup.appendChild(createSvgElement("path", { class: "highlight-region", d: highlightPath }));
    }

    rootGroup.appendChild(createSvgElement("path", {
      class: "density-curve",
      d: createCurvePath(samples, scale.xToPx, scale.yToPx)
    }));

    createAxesAndTicks(rootGroup, {
      xMin: scale.xMin,
      xMax: scale.xMax,
      yLimit: scale.yLimit,
      xToPx: scale.xToPx,
      yToPx: scale.yToPx,
      plotWidth,
      plotHeight,
      xAxisY,
      xTickCount: config.xTickCount || 5,
      yTickCount: config.yTickCount || 4,
      xLabel: config.xLabel || "x",
      yLabel: config.yLabel || "f(x)"
    });

    const note = createSvgElement("text", {
      class: "graph-note",
      x: scale.xToPx(Math.min(highlightStart, scale.xMax)),
      y: 18
    });
    note.textContent = `highlighted interval: ${formatTick(highlightStart)} ≤ x ≤ ${formatTick(highlightEnd)}`;
    rootGroup.appendChild(note);

    targetElement.textContent = "";
    targetElement.appendChild(svg);
  }

  window.MathRender = {
    createSvgElement,
    formatTick,
    buildPath,
    sampleFunction,
    createCurvePath,
    createHighlightAreaPath,
    createAxesAndTicks,
    renderProbabilityGraph
  };
})();
