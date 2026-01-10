(function () {
  function buildList(listElement, items) {
    if (!Array.isArray(items)) return;
    listElement.innerHTML = "";

    items.forEach((item) => {
      if (!item?.href || !item?.label) return;
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = item.href;
      link.textContent = item.label;
      li.appendChild(link);
      listElement.appendChild(li);
    });
  }

  async function initExampleTocs() {
    const inlineGroups = window.exampleTocGroups;
    if (inlineGroups) {
      document.querySelectorAll("[data-example-toc]").forEach((listElement) => {
        const key = listElement.getAttribute("data-example-toc");
        buildList(listElement, inlineGroups[key]);
      });
      return;
    }

    const src = document.body?.dataset?.exampleTocSrc;
    if (!src) return;

    try {
      const response = await fetch(src);
      if (!response.ok) return;
      const data = await response.json();
      const groups = data?.tocGroups ?? {};

      document.querySelectorAll("[data-example-toc]").forEach((listElement) => {
        const key = listElement.getAttribute("data-example-toc");
        buildList(listElement, groups[key]);
      });
    } catch (error) {
      console.error("Failed to load example TOC data", error);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    void initExampleTocs();
  });
})();
