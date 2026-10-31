(() => {
  "use strict";
  const registry = window.MindMapEffects;
  if (!registry) return;
  const words = (slide) => { slide.querySelectorAll("[data-mind-map-effect-word]").forEach((node) => node.replaceWith(document.createTextNode(node.textContent))); slide.normalize(); };
  const elements = (slide) => slide.querySelectorAll("[data-mind-map-effect-element]").forEach((node) => {
    node.classList.remove("mind-map-effect-element", "is-highlighted");
    node.removeAttribute("data-mind-map-effect-element"); node.removeAttribute("data-highlight-color");
  });
  const findWord = (slide, target, occurrence) => {
    const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT, { acceptNode: (node) => node.parentElement?.closest("script, style, [data-mind-map-effect-word]") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    const expression = new RegExp(target.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi"); let count = 0, node;
    while ((node = walker.nextNode())) { let match; while ((match = expression.exec(node.nodeValue))) if (++count === occurrence) { const span=document.createElement("span"); span.className="mind-map-effect-word"; span.dataset.mindMapEffectWord=target.toLowerCase(); span.textContent=match[0]; const rest=node.splitText(match.index); rest.splitText(match[0].length); rest.replaceWith(span); return span; } }
  };
  registry.register("word-highlight", async ({ slide, effect, signal }) => {
    const target=String(effect.target||""); const node=slide.querySelector(`[data-mind-map-effect-word="${CSS.escape(target.toLowerCase())}"]`) || findWord(slide,target,Number(effect.occurrence)||1);
    if (!node || signal?.aborted) return; node.dataset.highlightColor=effect.color||"green"; void node.offsetWidth; node.classList.add("is-highlighted");
  }, ({slide}) => words(slide));
  registry.register("element-highlight", async ({slide,effect,signal}) => { if(signal?.aborted||typeof effect.selector!=="string")return; let nodes; try{nodes=slide.querySelectorAll(effect.selector)}catch(_){console.warn("Ignoring invalid element-highlight selector.");return} nodes.forEach(node=>{node.classList.add("mind-map-effect-element");node.dataset.mindMapEffectElement="";node.dataset.highlightColor=effect.color||"green";void node.offsetWidth;node.classList.add("is-highlighted")}); }, ({slide})=>elements(slide));
  registry.register("clear-highlights", async ({slide})=>{words(slide);elements(slide)}, ({slide})=>{words(slide);elements(slide)});
})();
