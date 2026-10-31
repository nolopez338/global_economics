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
      const y = Number.isFinite(yValue) ? yValue : 0;
      samples.push({ x, y });
    }

    return samples;
  }

  function resolveYLimits(samples, config) {
    if (Number.isFinite(config.yMin) && Number.isFinite(config.yMax) && config.yMax > config.yMin) {
      return [config.yMin, config.yMax];
    }

    const finiteValues = samples.map((sample) => sample.y).filter((y) => Number.isFinite(y));
    let sampleMin = finiteValues.length ? Math.min(...finiteValues) : 0;
    let sampleMax = finiteValues.length ? Math.max(...finiteValues) : 1;

    if (!Number.isFinite(sampleMin)) {
      sampleMin = 0;
    }
    if (!Number.isFinite(sampleMax)) {
      sampleMax = 1;
    }

    if (sampleMin === sampleMax) {
      const pad = Math.max(Math.abs(sampleMax) * 0.12, 1);
      sampleMin -= pad;
      sampleMax += pad;
    } else {
      const pad = (sampleMax - sampleMin) * (config.yPaddingFactor || 0.12);
      sampleMin -= pad;
      sampleMax += pad;
    }

    if (sampleMin > 0) {
      sampleMin = 0;
    }

    if (Number.isFinite(config.yMin)) {
      sampleMin = config.yMin;
    }
    if (Number.isFinite(config.yMax)) {
      sampleMax = config.yMax;
    }

    return [sampleMin, sampleMax];
  }

  function createScale(domain, samples, plotWidth, plotHeight, config = {}) {
    const [xMin, xMax] = domain;
    const [yMin, yMax] = resolveYLimits(samples, config);

    const xToPx = (x) => ((x - xMin) / (xMax - xMin)) * plotWidth;
    const yToPx = (y) => plotHeight - ((y - yMin) / (yMax - yMin)) * plotHeight;
    const pxToX = (px) => xMin + (px / plotWidth) * (xMax - xMin);

    return { xToPx, yToPx, pxToX, xMin, xMax, yMin, yMax };
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
      yMin,
      yMax,
      xToPx,
      yToPx,
      plotWidth,
      plotHeight,
      xAxisY,
      yAxisX,
      xTickCount = 5,
      yTickCount = 4,
      xLabel = "x",
      yLabel = "f(x)"
    } = options;

    rootGroup.appendChild(createSvgElement("line", { class: "axis", x1: 0, y1: xAxisY, x2: plotWidth, y2: xAxisY }));
    rootGroup.appendChild(createSvgElement("line", { class: "axis", x1: yAxisX, y1: plotHeight, x2: yAxisX, y2: 0 }));

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
      const yValue = yMin + (i / yTickCount) * (yMax - yMin);
      const y = yToPx(yValue);
      const tickGroup = createSvgElement("g", { class: "tick" });
      tickGroup.appendChild(createSvgElement("line", { x1: yAxisX - 8, y1: y, x2: yAxisX, y2: y }));
      const text = createSvgElement("text", { x: yAxisX - 12, y: y + 4, "text-anchor": "end" });
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
      x: yAxisX - 24,
      y: -4
    });
    yLabelElement.textContent = yLabel;
    rootGroup.appendChild(yLabelElement);
  }

  function getRoundedValue(value, precision = 3) {
    return Number(value.toFixed(precision));
  }

  function createAxisControlPanel(targetElement, state, onChange) {
    const panel = document.createElement("div");
    panel.className = "graph-axis-controls";
    panel.style.display = "grid";
    panel.style.gridTemplateColumns = "repeat(4, minmax(70px, 1fr))";
    panel.style.gap = "6px 8px";
    panel.style.marginBottom = "8px";

    const controlMap = [
      { key: "xMin", label: "x min" },
      { key: "xMax", label: "x max" },
      { key: "yMin", label: "y min" },
      { key: "yMax", label: "y max" }
    ];

    controlMap.forEach(({ key, label }) => {
      const wrap = document.createElement("label");
      wrap.className = "graph-axis-control";
      wrap.style.display = "flex";
      wrap.style.flexDirection = "column";
      wrap.style.fontSize = "0.8rem";
      wrap.style.gap = "2px";

      const text = document.createElement("span");
      text.textContent = label;

      const input = document.createElement("input");
      input.type = "number";
      input.step = "any";
      input.value = String(getRoundedValue(state[key], 4));
      input.dataset.axisKey = key;
      input.addEventListener("change", () => onChange(input));
      input.addEventListener("blur", () => onChange(input));
      input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          onChange(input);
        }
      });

      wrap.appendChild(text);
      wrap.appendChild(input);
      panel.appendChild(wrap);
    });

    targetElement.appendChild(panel);
    return panel;
  }

  function createHoverLayer(rootGroup, plotWidth, plotHeight) {
    const hoverGroup = createSvgElement("g", { class: "graph-hover-layer" });
    const marker = createSvgElement("circle", {
      class: "graph-hover-marker",
      r: 4,
      cx: -9999,
      cy: -9999,
      style: "pointer-events:none"
    });

    const hoverLabel = createSvgElement("text", {
      class: "graph-hover-label",
      x: 10,
      y: 18,
      style: "pointer-events:none"
    });

    const hoverHitRect = createSvgElement("rect", {
      class: "graph-hover-hitbox",
      x: 0,
      y: 0,
      width: plotWidth,
      height: plotHeight,
      fill: "transparent"
    });

    hoverGroup.appendChild(hoverHitRect);
    hoverGroup.appendChild(marker);
    hoverGroup.appendChild(hoverLabel);
    rootGroup.appendChild(hoverGroup);

    return { hoverGroup, marker, hoverLabel, hoverHitRect };
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
    const showHoverCoordinates = Boolean(config.showHoverCoordinates);
    const showAxisControls = Boolean(config.showAxisControls);

    const graphState = {
      xMin: Number.isFinite(config.initialXMin) ? config.initialXMin : domain[0],
      xMax: Number.isFinite(config.initialXMax) ? config.initialXMax : domain[1],
      yMin: Number.isFinite(config.initialYMin) ? config.initialYMin : undefined,
      yMax: Number.isFinite(config.initialYMax) ? config.initialYMax : undefined
    };

    const bootSamples = sampleFunction(fn, [graphState.xMin, graphState.xMax], sampleCount);
    const bootScale = createScale([graphState.xMin, graphState.xMax], bootSamples, plotWidth, plotHeight, {
      yMin: graphState.yMin,
      yMax: graphState.yMax,
      yPaddingFactor: config.yPaddingFactor
    });
    if (!Number.isFinite(graphState.yMin)) {
      graphState.yMin = bootScale.yMin;
    }
    if (!Number.isFinite(graphState.yMax)) {
      graphState.yMax = bootScale.yMax;
    }

    targetElement.textContent = "";

    const updateGraph = () => {
      const currentDomain = [graphState.xMin, graphState.xMax];
      const samples = sampleFunction(fn, currentDomain, sampleCount);
      const scale = createScale(currentDomain, samples, plotWidth, plotHeight, {
        yMin: graphState.yMin,
        yMax: graphState.yMax,
        yPaddingFactor: config.yPaddingFactor
      });

      const [highlightStart, highlightEnd] = clampHighlightInterval(currentDomain, highlightInterval);
      const xAxisY = Math.max(0, Math.min(plotHeight, scale.yToPx(0)));
      const yAxisX = Math.max(0, Math.min(plotWidth, scale.xToPx(0)));

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
        yMin: scale.yMin,
        yMax: scale.yMax,
        xToPx: scale.xToPx,
        yToPx: scale.yToPx,
        plotWidth,
        plotHeight,
        xAxisY,
        yAxisX,
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

      if (showHoverCoordinates) {
        const { marker, hoverLabel, hoverHitRect } = createHoverLayer(rootGroup, plotWidth, plotHeight);
        const precision = Number.isFinite(config.hoverPrecision) ? config.hoverPrecision : 3;

        const hideHover = () => {
          marker.setAttribute("cx", "-9999");
          marker.setAttribute("cy", "-9999");
          hoverLabel.textContent = "";
        };

        hoverHitRect.addEventListener("mousemove", (event) => {
          const bounds = svg.getBoundingClientRect();
          const localX = event.clientX - bounds.left - margin.left;
          if (localX < 0 || localX > plotWidth) {
            hideHover();
            return;
          }

          const hoveredX = scale.pxToX(localX);
          const yValueRaw = Number(fn(hoveredX));
          if (!Number.isFinite(yValueRaw)) {
            hideHover();
            return;
          }

          const markerX = scale.xToPx(hoveredX);
          const markerY = scale.yToPx(yValueRaw);
          if (markerY < 0 || markerY > plotHeight) {
            hideHover();
            return;
          }

          marker.setAttribute("cx", String(markerX));
          marker.setAttribute("cy", String(markerY));
          hoverLabel.setAttribute("x", String(Math.min(plotWidth - 120, markerX + 10)));
          hoverLabel.setAttribute("y", String(Math.max(18, markerY - 10)));
          hoverLabel.textContent = `(${getRoundedValue(hoveredX, precision)}, ${getRoundedValue(yValueRaw, precision)})`;
        });

        hoverHitRect.addEventListener("mouseleave", hideHover);
      }

      const existingSvg = targetElement.querySelector("svg");
      if (existingSvg) {
        targetElement.replaceChild(svg, existingSvg);
      } else {
        targetElement.appendChild(svg);
      }
    };

    if (showAxisControls) {
      createAxisControlPanel(targetElement, graphState, (input) => {
        const key = input.dataset.axisKey;
        const value = Number(input.value);
        if (!Number.isFinite(value)) {
          return;
        }

        graphState[key] = value;
        if (graphState.xMax <= graphState.xMin) {
          graphState.xMax = graphState.xMin + 0.0001;
        }
        if (Number.isFinite(graphState.yMin) && Number.isFinite(graphState.yMax) && graphState.yMax <= graphState.yMin) {
          graphState.yMax = graphState.yMin + 0.0001;
        }

        const controls = targetElement.querySelectorAll(".graph-axis-controls input[data-axis-key]");
        controls.forEach((control) => {
          const axisKey = control.dataset.axisKey;
          if (axisKey && Number.isFinite(graphState[axisKey])) {
            control.value = String(getRoundedValue(graphState[axisKey], 4));
          }
        });

        updateGraph();
      });
    }

    updateGraph();
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
