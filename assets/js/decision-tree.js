(function () {
  const VIEW_H = 720;
  const margin = { top: 24, right: 40, bottom: 24, left: 40 };

  function moneyShort(n) {
    const sign = n < 0 ? "-" : "";
    const abs = Math.abs(n);

    if (abs >= 1_000_000) return sign + (abs / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M";
    if (abs >= 1_000)     return sign + Math.round(abs / 1_000) + "k";
    return sign + abs;
  }

  function createDecisionTree({ canvasId, svgId, data }) {
    const svg = d3.select(`#${svgId}`);
    const canvas = document.getElementById(canvasId);

    if (!svg.node() || !canvas) return;

    const gRoot = svg.append("g");
    const gLinks = gRoot.append("g").attr("class", "links");
    const gNodes = gRoot.append("g").attr("class", "nodes");

    const svgNode = svg.node();
    svgNode.addEventListener("gesturestart", (event) => event.preventDefault(), { passive: false });
    svgNode.addEventListener("gesturechange", (event) => event.preventDefault(), { passive: false });
    svgNode.addEventListener("gestureend", (event) => event.preventDefault(), { passive: false });

    const root = d3.hierarchy(data);
    expandAll(root);

    const cssVar = {
      decision: "var(--decision)",
      strategy: "var(--strategy)",
      outcome: "var(--outcome)"
    };

    function w() { return canvas.clientWidth; }
    function h() { return VIEW_H; }

    function onEnterOrSpace(event, action) {
      const key = event.key;
      if (key !== "Enter" && key !== " ") return;
      event.preventDefault();
      action();
    }

    function textWidth(node) {
      return node?.getComputedTextLength ? node.getComputedTextLength() : 0;
    }

    function linkPath(source, target) {
      const midY = (source.y + target.y) / 2;
      return `M${source.y},${source.x} C${midY},${source.x} ${midY},${target.x} ${target.y},${target.x}`;
    }

    function expandAll(node) {
      if (!node) return;
      if (node._children) {
        node.children = node._children;
        node._children = null;
      }
      (node.children || []).forEach(expandAll);
    }

    function toggleNode(node) {
      if (!node.children && !node._children) return;

      if (node.children) {
        node._children = node.children;
        node.children = null;
      } else {
        node.children = node._children;
        node._children = null;
      }

      render();
      fitView();
    }

    function layoutTree() {
      const W = w();
      const H = h();

      svg.attr("viewBox", [0, 0, W, H]);

      const thirdLayerCount = root.descendants().filter((d) => d.depth === 2).length;
      const spacingMultiplier = Math.max(thirdLayerCount / 9, 1);
      const thirdLayerSeparation = 1.4 * spacingMultiplier;
      const thirdLayerHorizontalGap = 120;

      d3.tree()
        .nodeSize([110, 280])
        .separation((a, b) => (a.depth === 2 && b.depth === 2 ? thirdLayerSeparation : 1))
        (root);

      const nodes = root.descendants();
      const links = root.links();

      let xMin = Infinity;
      let xMax = -Infinity;
      for (const d of nodes) {
        xMin = Math.min(xMin, d.x);
        xMax = Math.max(xMax, d.x);
      }

      const innerH = H - margin.top - margin.bottom;
      const innerW = W - margin.left - margin.right;

      const xSpan = (xMax - xMin) || 1;
      const yMax = d3.max(nodes, (d) => d.y) || 1;
      const yScale = Math.min(1, innerW / (yMax + 320));

      for (const d of nodes) {
        d.x = margin.top + ((d.x - xMin) / xSpan) * innerH;
        d.y = margin.left + d.y * yScale;
        if (d.depth >= 2) {
          d.y += thirdLayerHorizontalGap;
        }
      }

      return { nodes, links };
    }

    function buildNodeMarkup(sel) {
      sel.append("rect").attr("class", "pill");

      sel.append("rect")
        .attr("class", "typebox")
        .attr("rx", 3).attr("ry", 3);

      sel.append("text").attr("class", "label");
      sel.append("text").attr("class", "meta");

      sel.append("line")
        .attr("class", "divider tableTop")
        .style("display", (d) => (d.data.type === "outcome" ? null : "none"));

      sel.append("text")
        .attr("class", "cellHead pHead")
        .style("display", (d) => (d.data.type === "outcome" ? null : "none"))
        .text("p");

      sel.append("text")
        .attr("class", "cellHead vHead")
        .style("display", (d) => (d.data.type === "outcome" ? null : "none"))
        .text("payoff");

      sel.append("text")
        .attr("class", "cell pVal")
        .style("display", (d) => (d.data.type === "outcome" ? null : "none"));

      sel.append("text")
        .attr("class", "cell vVal")
        .style("display", (d) => (d.data.type === "outcome" ? null : "none"));

      sel.append("text")
        .attr("class", "toggleglyph")
        .attr("text-anchor", "middle")
        .attr("font-size", 18)
        .attr("fill", "#9ca3af");
    }

    function paintNode(g, d) {
      const type = d.data.type;

      g.select("rect.typebox").attr("fill", cssVar[type] || cssVar.outcome);
      g.select("text.label").text(d.data.name || "");

      const isStrategy = type === "strategy";
      g.select("text.meta")
        .text(isStrategy ? (d.data.subtitle || "") : "")
        .style("display", isStrategy ? null : "none");

      if (type === "outcome") {
        g.select("text.pVal").text(d.data.prob ?? "");
        g.select("text.vVal").text(moneyShort(d.data.payoff ?? 0));
      }

      const canToggle = Boolean(d.children || d._children);
      const glyph = canToggle ? (d.children ? "−" : "+") : "";
      g.select("text.toggleglyph").text(glyph);
    }

    function computeNodeLayout(g, d) {
      const PAD_X = 14;
      const PAD_Y = 10;
      const TYPE_SQ = 12;
      const TYPE_GAP = 10;
      const colGap = 18;

      const isOutcome = d.data.type === "outcome";

      const wLabel = textWidth(g.select("text.label").node());
      const wMeta  = textWidth(g.select("text.meta").node());

      let pColW = 0, vColW = 0, tableW = 0;
      if (isOutcome) {
        pColW = Math.max(
          textWidth(g.select("text.pHead").node()),
          textWidth(g.select("text.pVal").node())
        ) + 8;

        vColW = Math.max(
          textWidth(g.select("text.vHead").node()),
          textWidth(g.select("text.vVal").node())
        ) + 8;

        tableW = pColW + colGap + vColW;
      }

      const leftInset = PAD_X + TYPE_SQ + TYPE_GAP;
      const contentW = Math.max(wLabel, wMeta, tableW);
      const width = leftInset + contentW + PAD_X;

      const hasMeta = (g.select("text.meta").text() || "").trim().length > 0;
      const height = isOutcome ? 80 : (hasMeta ? 56 : 44);

      return {
        width,
        height,
        hasMeta,
        isOutcome,
        leftInset,
        colGap,
        pColW,
        vColW,
        tableW,
        PAD_X,
        PAD_Y,
        TYPE_SQ,
        TYPE_GAP
      };
    }

    function sizeAndPlaceNode(g, d, layerWidth) {
      const {
        width: baseWidth,
        height,
        hasMeta,
        isOutcome,
        leftInset,
        colGap,
        pColW,
        vColW,
        tableW,
        PAD_X,
        PAD_Y,
        TYPE_SQ
      } = d._layout;

      const width = layerWidth ?? baseWidth;

      g.select("rect.pill")
        .attr("x", -width / 2)
        .attr("y", -height / 2)
        .attr("width", width)
        .attr("height", height);

      g.select("rect.typebox")
        .attr("x", -width / 2 + PAD_X)
        .attr("y", -height / 2 + PAD_Y)
        .attr("width", TYPE_SQ)
        .attr("height", TYPE_SQ);

      const startX = -width / 2 + leftInset;

      g.select("text.label")
        .attr("x", startX)
        .attr("y", isOutcome ? (-height / 2 + PAD_Y + 6) : (hasMeta ? -6 : 0));

      g.select("text.meta")
        .attr("x", startX)
        .attr("y", 16);

      if (isOutcome) {
        const titleBaselineY = (-height / 2 + PAD_Y + 6);
        const dividerY = titleBaselineY + 12;
        const tableTop = dividerY + 14;

        const pX = startX;
        const vX = startX + pColW + colGap;

        g.select("line.tableTop")
          .attr("x1", startX).attr("x2", startX + tableW)
          .attr("y1", dividerY).attr("y2", dividerY);

        g.select("text.pHead").attr("x", pX).attr("y", tableTop);
        g.select("text.vHead").attr("x", vX).attr("y", tableTop);
        g.select("text.pVal").attr("x", pX).attr("y", tableTop + 18);
        g.select("text.vVal").attr("x", vX).attr("y", tableTop + 18);
      }

      g.select("text.toggleglyph")
        .attr("x", width / 2 - 16)
        .attr("y", 4);
    }

    function render() {
      const { nodes, links } = layoutTree();

      gLinks.selectAll("path.link")
        .data(links, (d) => `${d.target.data.name}-${d.target.depth}`)
        .join(
          (enter) => enter.append("path").attr("class", "link"),
          (update) => update,
          (exit) => exit.remove()
        )
        .attr("d", (d) => linkPath(d.source, d.target));

      const nodeJoin = gNodes.selectAll("g.node")
        .data(nodes, (d) => `${d.data.name}-${d.depth}`)
        .join(
          (enter) => {
            const g = enter.append("g")
              .attr("class", "node focus-ring")
              .attr("tabindex", 0)
              .on("click", (e, d) => toggleNode(d))
              .on("keydown", (e, d) => onEnterOrSpace(e, () => toggleNode(d)));

            buildNodeMarkup(g);
            return g;
          },
          (update) => update,
          (exit) => exit.remove()
        );

      nodeJoin
        .attr("transform", (d) => `translate(${d.y},${d.x})`)
        .each(function(d) {
          const g = d3.select(this);
          paintNode(g, d);
          d._layout = computeNodeLayout(g, d);
        });

      const layerWidths = new Map();
      nodes.forEach((d) => {
        const width = d._layout?.width ?? 0;
        layerWidths.set(d.depth, Math.max(layerWidths.get(d.depth) || 0, width));
      });

      nodeJoin.each(function(d) {
        const g = d3.select(this);
        sizeAndPlaceNode(g, d, layerWidths.get(d.depth));
      });
    }

    function fitView() {
      const W = w();
      const H = h();

      const box = gRoot.node().getBBox();
      const ok = isFinite(box.width) && isFinite(box.height) && box.width > 0 && box.height > 0;
      if (!ok) return;

      const padding = 36;
      const fullW = box.width + padding * 2;
      const fullH = box.height + padding * 2;

      const scale = Math.min(W / fullW, H / fullH);

      const centerX = box.x + box.width / 2;
      const centerY = box.y + box.height / 2;

      const translateX = W / 2 - scale * centerX;
      const translateY = H / 2 - scale * centerY;
      gRoot.attr("transform", `translate(${translateX},${translateY}) scale(${scale})`);
    }

    function rerenderAndFit() {
      render();
      requestAnimationFrame(fitView);
    }

    rerenderAndFit();

    new ResizeObserver(rerenderAndFit).observe(canvas);
  }

  async function initDecisionTrees() {
    const src = document.body?.dataset?.decisionTreeSrc;
    if (!src) return;

    try {
      const response = await fetch(src);
      if (!response.ok) return;
      const decisionTrees = await response.json();
      decisionTrees.forEach(createDecisionTree);
    } catch (error) {
      console.error("Failed to load decision tree data", error);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    void initDecisionTrees();
  });
})();
