(() => {
  "use strict";

  const practiceData = {
    labelDefinitions: [
      { key: "name", label: "Problem" },
      { key: "payoffType", label: "Payoff Type" }
    ],
    problems: [
      {
        id: "problem-1",
        labels: {
          name: "Local Café Investment",
          payoffType: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
          <p>A small café is deciding whether to launch a new line of artisan desserts. The transaction is daily café sales, and profit is earned from dessert plates sold.</p>
          <p>The owner is comparing these alternatives and outcomes (all profits are in thousand USD):</p>
          <ol>
            <li><strong>Launch the dessert line</strong>
              <ul><li>High traffic: 42</li><li>Low traffic: 8</li></ul>
            </li>
            <li><strong>Keep the current menu</strong>
              <ul><li>High traffic: 28</li><li>Low traffic: 20</li></ul>
            </li>
          </ol>
          <h4>Tasks</h4>
          <ol>
            <li><strong>C1:</strong> Interpret the decision alternatives, events, consequences, and states.</li>
            <li><strong>C2:</strong> Build the payoff table.</li>
          </ol>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
              <div class="table-card"><table class="data-table">
                <caption>Decision elements for the café investment</caption>
                <thead><tr><th scope="col">Decision element</th><th scope="col">Content</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Alternatives</th><td>Launch dessert line; Keep current menu</td></tr>
                  <tr><th scope="row">States of nature</th><td>High traffic; Low traffic</td></tr>
                  <tr><th scope="row">Uncertain event</th><td>Actual foot traffic after the decision</td></tr>
                  <tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each alternative–state pair</td></tr>
                </tbody>
              </table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
              <p>All payoffs are measured in <strong>thousand USD</strong>.</p>
              <div class="table-card"><table class="data-table">
                <caption>Café payoff table (thousand USD)</caption>
                <thead><tr><th scope="col">Alternative</th><th scope="col">High traffic</th><th scope="col">Low traffic</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Launch dessert line</th><td>42</td><td>8</td></tr>
                  <tr><th scope="row">Keep current menu</th><td>28</td><td>20</td></tr>
                </tbody>
              </table></div>
            `
          }
        ]
      },
      {
        id: "problem-2",
        labels: {
          name: "Green Energy Production Mix",
          payoffType: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
          <p>A renewable-energy company must select an electricity-generation mix. The transaction is annual electricity sales, and profit is earned per megawatt-hour generated and sold.</p>
          <p>The three possible weather states are:</p>
          <ol><li>Windy</li><li>Sunny</li><li>Cloudy</li></ol>
          <p>The company is comparing three strategies:</p>
          <ol><li>Build wind turbines</li><li>Build solar farms</li><li>Build a balanced hybrid system</li></ol>
          <p>Modeled profits in thousand USD are:</p>
          <ul>
            <li><strong>Wind turbines:</strong> 90 under Windy, 45 under Sunny, and 30 under Cloudy.</li>
            <li><strong>Solar farms:</strong> 35 under Windy, 95 under Sunny, and 25 under Cloudy.</li>
            <li><strong>Hybrid system:</strong> 70 under Windy, 65 under Sunny, and 60 under Cloudy.</li>
          </ul>
          <h4>Tasks</h4>
          <ol>
            <li><strong>C1:</strong> Interpret the decision alternatives, events, consequences, and states.</li>
            <li><strong>C2:</strong> Build the payoff table.</li>
          </ol>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
              <div class="table-card"><table class="data-table">
                <caption>Decision elements for the energy production mix</caption>
                <thead><tr><th scope="col">Decision element</th><th scope="col">Content</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Alternatives</th><td>Wind turbines; Solar farms; Hybrid system</td></tr>
                  <tr><th scope="row">States of nature</th><td>Windy; Sunny; Cloudy</td></tr>
                  <tr><th scope="row">Uncertain event</th><td>Weather outcome affecting generation</td></tr>
                  <tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each strategy–weather combination</td></tr>
                </tbody>
              </table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
              <p>All payoffs are measured in <strong>thousand USD</strong>.</p>
              <div class="table-card"><table class="data-table">
                <caption>Energy production payoff table (thousand USD)</caption>
                <thead><tr><th scope="col">Strategy</th><th scope="col">Windy</th><th scope="col">Sunny</th><th scope="col">Cloudy</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Wind turbines</th><td>90</td><td>45</td><td>30</td></tr>
                  <tr><th scope="row">Solar farms</th><td>35</td><td>95</td><td>25</td></tr>
                  <tr><th scope="row">Hybrid system</th><td>70</td><td>65</td><td>60</td></tr>
                </tbody>
              </table></div>
            `
          }
        ]
      },
      {
        id: "problem-3",
        labels: {
          name: "Global Shipping Network Design",
          payoffType: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
          <p>A multinational logistics firm is choosing between two shipping-network designs for long-term freight contracts. The transaction is global freight services, and profit is earned per contract delivered on schedule.</p>
          <p>The two alternatives are:</p>
          <ol><li>Centralized mega-hub network</li><li>Regional multi-hub network</li></ol>
          <p>The four possible trade conditions are:</p>
          <ol><li>Trade boom</li><li>Stable trade</li><li>Moderate disruptions</li><li>Severe disruptions</li></ol>
          <p>Modeled profits in thousand USD are:</p>
          <ul>
            <li><strong>Centralized network:</strong> 220, 140, 40, and −30 for the four states in the stated order.</li>
            <li><strong>Regional network:</strong> 180, 160, 110, and 60 for the four states in the stated order.</li>
          </ul>
          <h4>Tasks</h4>
          <ol>
            <li><strong>C1:</strong> Interpret the decision alternatives, events, consequences, and states.</li>
            <li><strong>C2:</strong> Build the payoff table.</li>
          </ol>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
              <div class="table-card"><table class="data-table">
                <caption>Decision elements for the shipping network</caption>
                <thead><tr><th scope="col">Decision element</th><th scope="col">Content</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Alternatives</th><td>Centralized mega-hub; Regional multi-hub</td></tr>
                  <tr><th scope="row">States of nature</th><td>Boom; Stable; Moderate disruptions; Severe disruptions</td></tr>
                  <tr><th scope="row">Uncertain event</th><td>Trade conditions realized during the planning horizon</td></tr>
                  <tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each network–state pair</td></tr>
                </tbody>
              </table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
              <p>All payoffs are measured in <strong>thousand USD</strong>.</p>
              <div class="table-card"><table class="data-table">
                <caption>Shipping network payoff table (thousand USD)</caption>
                <thead><tr><th scope="col">Network</th><th scope="col">Boom</th><th scope="col">Stable</th><th scope="col">Moderate disruptions</th><th scope="col">Severe disruptions</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Centralized mega-hub</th><td>220</td><td>140</td><td>40</td><td>-30</td></tr>
                  <tr><th scope="row">Regional multi-hub</th><td>180</td><td>160</td><td>110</td><td>60</td></tr>
                </tbody>
              </table></div>
            `
          }
        ]
      }
    ]
  };

  function validateData(data) {
    if (!Array.isArray(data.labelDefinitions) || data.labelDefinitions.length < 1 || data.labelDefinitions.length > 4) {
      throw new Error("Practice data must define between one and four label dimensions.");
    }
    if (data.labelDefinitions[0]?.key !== "name") {
      throw new Error('The first practice label must use the key "name".');
    }

    const keys = data.labelDefinitions.map(({ key, label }) => {
      if (typeof key !== "string" || !key.trim() || typeof label !== "string" || !label.trim()) {
        throw new Error("Every practice label definition needs a non-empty key and label.");
      }
      return key;
    });
    if (new Set(keys).size !== keys.length) {
      throw new Error("Practice label keys must be unique.");
    }
    if (!Array.isArray(data.problems)) {
      throw new Error("Practice problems must be an array.");
    }

    const ids = new Set();
    const names = new Set();
    data.problems.forEach((problem, problemIndex) => {
      const prefix = `Problem ${problemIndex + 1}`;
      if (!problem || typeof problem.id !== "string" || !problem.id.trim() || ids.has(problem.id)) {
        throw new Error(`${prefix} must have a unique, non-empty ID.`);
      }
      ids.add(problem.id);
      if (!problem.labels || typeof problem.labels !== "object" || Array.isArray(problem.labels)) {
        throw new Error(`${prefix} must provide a labels object.`);
      }
      const suppliedKeys = Object.keys(problem.labels);
      if (suppliedKeys.length !== keys.length || keys.some((key) => !suppliedKeys.includes(key))) {
        throw new Error(`${prefix} must provide exactly one value for every configured label.`);
      }
      keys.forEach((key) => {
        if (typeof problem.labels[key] !== "string" || !problem.labels[key].trim()) {
          throw new Error(`${prefix} has an empty or invalid "${key}" label.`);
        }
      });
      if (names.has(problem.labels.name)) {
        throw new Error(`Problem names must be unique: "${problem.labels.name}".`);
      }
      names.add(problem.labels.name);
      if (typeof problem.descriptionHtml !== "string") {
        throw new Error(`${prefix} must provide descriptionHtml.`);
      }
      if (!Array.isArray(problem.solutionSections)) {
        throw new Error(`${prefix} solutionSections must be an ordered array.`);
      }
      problem.solutionSections.forEach((section, sectionIndex) => {
        if (!section || typeof section.title !== "string" || !section.title.trim()
          || typeof section.contentHtml !== "string" || !section.contentHtml.trim()) {
          throw new Error(`${prefix}, solution subsection ${sectionIndex + 1}, needs both a title and content.`);
        }
      });
    });
  }

  const escapeHtml = (value) => String(value).replace(/[&<>"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
  })[character]);

  const uniqueValues = (problems, key) => [...new Set(problems.map((problem) => problem.labels[key]))];

  function allOptionText(label) {
    const lowerLabel = label.toLowerCase();
    if (lowerLabel.endsWith("y")) return `All ${lowerLabel.slice(0, -1)}ies`;
    return `All ${lowerLabel}s`;
  }

  function initializePracticePage() {
    const controls = document.getElementById("practice-selector-controls");
    const status = document.getElementById("practice-selector-status");
    const region = document.getElementById("selected-problem");
    if (!controls || !status || !region) return;

    try {
      validateData(practiceData);
    } catch (error) {
      console.error(error);
      controls.replaceChildren();
      status.textContent = `Practice data error: ${error.message}`;
      region.hidden = true;
      return;
    }

    if (practiceData.problems.length === 0) {
      status.textContent = "No practice problems are available.";
      region.hidden = true;
    }

    const selects = new Map();
    practiceData.labelDefinitions.forEach((definition, index) => {
      const field = document.createElement("div");
      field.className = "practice-selector__field";
      const label = document.createElement("label");
      const select = document.createElement("select");
      select.id = `practice-filter-${definition.key}`;
      select.dataset.labelKey = definition.key;
      label.htmlFor = select.id;
      label.textContent = definition.label;

      if (index === 0) {
        select.add(new Option("Select a problem", ""));
      } else {
        select.add(new Option(allOptionText(definition.label), ""));
        uniqueValues(practiceData.problems, definition.key).forEach((value) => select.add(new Option(value, value)));
      }
      field.append(label, select);
      controls.append(field);
      selects.set(definition.key, select);
    });

    const nameSelect = selects.get("name");

    function matchingProblems() {
      return practiceData.problems.filter((problem) => practiceData.labelDefinitions.slice(1).every(({ key }) => {
        const selectedValue = selects.get(key).value;
        return !selectedValue || problem.labels[key] === selectedValue;
      }));
    }

    function renderProblem(problem) {
      const metadata = practiceData.labelDefinitions.slice(1).map(({ key, label }) =>
        `<li><strong>${escapeHtml(label)}:</strong> ${escapeHtml(problem.labels[key])}</li>`
      ).join("");
      const contents = problem.solutionSections.map((section, index) =>
        `<li><a href="#${problem.id}-solution-${index + 1}">${escapeHtml(section.title)}</a></li>`
      ).join("");
      const sections = problem.solutionSections.map((section, index) => {
        const sectionId = `${problem.id}-solution-${index + 1}`;
        return `
          <div class="subsection-minimize collapsed" data-region="subsection">
            <button class="subsection-toggle" type="button" aria-expanded="false" id="${sectionId}-toggle" aria-controls="${sectionId}">
              <span class="toggle-label">${escapeHtml(section.title)}</span><span class="toggle-icon" aria-hidden="true">+</span>
            </button>
            <div class="subsection-content" id="${sectionId}" role="region" aria-labelledby="${sectionId}-toggle">
              <div class="content-block">${section.contentHtml}</div>
              <div class="subsection-footer"><a class="subsection-back-link" href="#${problem.id}-solution-list" aria-label="Back to solution contents">↑</a></div>
            </div>
          </div>`;
      }).join("");

      region.id = problem.id;
      region.innerHTML = `
        <h2>${escapeHtml(problem.labels.name)}</h2>
        ${metadata ? `<ul class="practice-problem__metadata" aria-label="Problem properties">${metadata}</ul>` : ""}
        <div class="example">
          <h3>Problem description</h3>
          <div class="content-block">${problem.descriptionHtml}</div>
          <nav class="practice-problem__contents" aria-label="Solution contents">
            <h3 id="${problem.id}-solution-list">Solution sections</h3>
            <ol>${contents}</ol>
          </nav>
          ${sections}
        </div>
        <div class="back-to-top"><a class="back-to-top-button" href="#practice-selector"><span class="back-to-top-icon" aria-hidden="true">↑</span>Back to Problem Selector</a></div>`;
      region.hidden = false;
      if (window.MathJax?.typesetPromise) {
        window.MathJax.typesetPromise([region]).catch((error) => console.error("MathJax typesetting failed:", error));
      }
      status.textContent = `${problem.labels.name} selected.`;
    }

    function hideProblem() {
      region.replaceChildren();
      region.id = "selected-problem";
      region.hidden = true;
    }

    function updateNameOptions() {
      const previousName = nameSelect.value;
      const matches = matchingProblems();
      nameSelect.replaceChildren(new Option(matches.length ? "Select a problem" : "No matching problems", ""));
      nameSelect.options[0].disabled = matches.length === 0;
      matches.forEach((problem) => nameSelect.add(new Option(problem.labels.name, problem.id)));

      const selectedProblem = matches.find((problem) => problem.id === previousName);
      if (selectedProblem) {
        nameSelect.value = previousName;
      } else {
        nameSelect.value = "";
        hideProblem();
      }
      status.textContent = matches.length ? "Select a problem to display it." : "No matching problems.";
    }

    practiceData.labelDefinitions.slice(1).forEach(({ key }) => {
      selects.get(key).addEventListener("change", updateNameOptions);
    });
    nameSelect.addEventListener("change", () => {
      const problem = practiceData.problems.find(({ id }) => id === nameSelect.value);
      if (problem && matchingProblems().includes(problem)) renderProblem(problem);
      else {
        hideProblem();
        status.textContent = "Select a problem to display it.";
      }
    });
    region.addEventListener("click", (event) => {
      const button = event.target.closest(".subsection-toggle");
      if (!button || !region.contains(button)) return;
      const subsection = button.closest(".subsection-minimize");
      const expanded = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(expanded));
      button.querySelector(".toggle-icon").textContent = expanded ? "−" : "+";
      subsection.classList.toggle("collapsed", !expanded);
    });

    updateNameOptions();
  }

  initializePracticePage();
})();
