(() => {
  "use strict";

  const practiceData = {
    selectors: [
      {
        key: "layer1",
        label: "Number of components",
        type: "filter",
        multiple: true,
        options: ["Direct", "1 component", "2 components", "3 components", "4 components"]
      },
      {
        key: "layer2",
        label: "Component structure",
        type: "filter",
        multiple: true,
        options: ["AV", "SV", "AF", "SF"],
        descriptions: {
          AV: "Alternative-based Variable",
          SV: "State-based Variable",
          AF: "Alternative-based Fixed",
          SF: "State-based Fixed"
        }
      }
    ],
    problems: [
      {
        id: "problem-1",
        layer1: "Direct",
        layer2: [],
        labels: {
          name: "Introductory General Problem (C1--C2)",
          section: "Introduction"
        },
        descriptionHtml: String.raw`
<p>A decision-maker chooses between generic alternatives $A_1$ and $A_2$. After the choice, one uncertain event produces either state $S_1$ or state $S_2$. The payoffs, in thousand USD, are supplied directly:</p>
$$
P_{11}=10,\quad P_{12}=4,\quad P_{21}=7,\quad P_{22}=8.
$$
<p>The first subscript identifies the alternative (the row), and the second identifies the state (the column). The four combinations are</p>
$$
(A_1,S_1),\quad(A_1,S_2),\quad(A_2,S_1),\quad(A_2,S_2).
$$
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>$A_1$; $A_2$</td></tr><tr><th scope="row">States of nature</th><td>$S_1$; $S_2$</td></tr><tr><th scope="row">Uncertain event</th><td>The uncertain event that produces either $S_1$ or $S_2$</td></tr><tr><th scope="row">Consequences/payoffs</th><td>The consequence and its payoff in thousand USD for each pair $(A_i,S_j)$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th></tr></thead>
<tbody>
<tr><th scope="row">$A_1$</th><td>10</td><td>4</td></tr>
<tr><th scope="row">$A_2$</th><td>7</td><td>8</td></tr>
</tbody></table></div>
<p>Because $P_{11}$ belongs to row $A_1$ and column $S_1$, 10 goes in the first payoff cell. Similarly, $P_{12}=4$ goes in row $A_1$, column $S_2$; $P_{21}=7$ goes in row $A_2$, column $S_1$; and $P_{22}=8$ goes in row $A_2$, column $S_2$.</p>
            `
          }
        ]
      },
      {
        id: "problem-2",
        layer1: "4 components",
        layer2: ["AV","SV","AF","SF"],
        labels: {
          name: "Advanced General Problem (C1--C2)",
          section: "Introduction"
        },
        descriptionHtml: String.raw`
<p>A decision-maker chooses $A_1$ or $A_2$ before an uncertain event produces $S_1$ or $S_2$. All monetary values below are in thousand USD, with variable values stated per item:</p>
$$
v_1^A=2,\quad v_2^A=3,\qquad f_1^A=5,\quad f_2^A=6,
$$
$$
v_1^S=1,\quad v_2^S=2,\qquad f_1^S=1,\quad f_2^S=2.
$$
<p>The alternative--state quantities are:</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th></tr></thead>
<tbody>
<tr><th scope="row">$A_1$</th><td>$q_{11}=2$</td><td>$q_{12}=3$</td></tr>
<tr><th scope="row">$A_2$</th><td>$q_{21}=4$</td><td>$q_{22}=5$</td></tr>
</tbody></table></div>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>$A_1$; $A_2$</td></tr><tr><th scope="row">States of nature</th><td>$S_1$; $S_2$</td></tr><tr><th scope="row">Uncertain event</th><td>The uncertain event that produces either $S_1$ or $S_2$</td></tr><tr><th scope="row">Consequences/payoffs</th><td>The total payoff in thousand USD for each pair $(A_i,S_j)$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Every cell uses the complete formula</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_i^A+f_j^S.
$$
<p>The values carrying $i$ change by alternative and therefore by row. The values carrying $j$ change by state and therefore by column. The quantity $q_{ij}$ carries both indices and can change in every cell.</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Payoff</th><th scope="col">Complete numerical substitution</th><th scope="col">Result</th></tr></thead>
<tbody>
<tr><th scope="row">$P_{11}$</th><td>$q_{11}(v_1^A+v_1^S)+f_1^A+f_1^S=2(2+1)+5+1$</td><td>12</td></tr>
<tr><th scope="row">$P_{12}$</th><td>$q_{12}(v_1^A+v_2^S)+f_1^A+f_2^S=3(2+2)+5+2$</td><td>19</td></tr>
<tr><th scope="row">$P_{21}$</th><td>$q_{21}(v_2^A+v_1^S)+f_2^A+f_1^S=4(3+1)+6+1$</td><td>23</td></tr>
<tr><th scope="row">$P_{22}$</th><td>$q_{22}(v_2^A+v_2^S)+f_2^A+f_2^S=5(3+2)+6+2$</td><td>33</td></tr>
</tbody></table></div>
<p>Each line displays separately the alternative--state quantity, alternative-based variable value, state-based variable value, alternative-based fixed value, and state-based fixed value before they are combined.</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th></tr></thead>
<tbody>
<tr><th scope="row">$A_1$</th><td>12</td><td>19</td></tr>
<tr><th scope="row">$A_2$</th><td>23</td><td>33</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-3",
        layer1: "Direct",
        layer2: [],
        labels: {
          name: "Local Café Investment (C1--C2)",
          section: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
<p>A small café is deciding whether to launch a new line of artisan desserts. The transaction is daily café sales, where profit is earned from each dessert plate sold. The owner has two options:</p>
<ol>
<li><strong>Launch the dessert line</strong>, with profit outcomes depending on foot traffic:
<ol>
<li>High traffic $\to 42$ thousand USD
</li><li>Low traffic $\to 8$ thousand USD
</li></ol>
</li><li><strong>Keep the current menu</strong>, with profit outcomes based on historical data:
<ol>
<li>High traffic $\to 28$ thousand USD
</li><li>Low traffic $\to 20$ thousand USD
</li></ol>
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A small café is deciding whether to introduce a line of artisan desserts or keep its current menu. The payoff represents estimated daily profit from café sales. The projections combine recent sales records with expected ingredient, staffing, and preparation costs.</p>
<p>The result depends on customer traffic, which may be high or low. If the café launches the dessert line, the projected profit is 42 thousand USD under high traffic and 8 thousand USD under low traffic. The large difference reflects the additional sales possible when demand is strong and the risk of unsold ingredients when demand is weak.</p>
<p>If the café keeps its current menu, the projected profit is 28 thousand USD under high traffic and 20 thousand USD under low traffic. This alternative offers less growth potential but produces more stable outcomes because it avoids most of the new operating costs.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Launch dessert line; Keep current menu</td></tr><tr><th scope="row">States of nature</th><td>High traffic; Low traffic</td></tr><tr><th scope="row">Uncertain event</th><td>Actual foot traffic after the decision</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High traffic</th><th scope="col">Low traffic</th></tr></thead>
<tbody>
<tr><th scope="row">Launch dessert line</th><td>42</td><td>8</td></tr>
<tr><th scope="row">Keep menu</th><td>28</td><td>20</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-4",
        layer1: "Direct",
        layer2: [],
        labels: {
          name: "Green Energy Production Mix (C1--C2)",
          section: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
<p>A renewable-energy company must select an electricity generation mix. The transaction is annual electricity sales, where profit is earned per megawatt-hour generated and sold.</p>
<p>Three weather states are possible:</p>
<ol>
<li>Windy
</li><li>Sunny
</li><li>Cloudy
</li></ol>
<p>The company is comparing three strategies:</p>
<ol>
<li>Build wind turbines
</li><li>Build solar farms
</li><li>Build a balanced hybrid system
</li></ol>
<p>Modeled profits in thousand USD:</p>
<ol>
<li>Wind turbines $\to 90$ (Windy), $45$ (Sunny), $30$ (Cloudy)
</li><li>Solar farms $\to 35$ (Windy), $95$ (Sunny), $25$ (Cloudy)
</li><li>Hybrid system $\to 70$ (Windy), $65$ (Sunny), $60$ (Cloudy)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A renewable-energy company must choose among building wind turbines, developing solar farms, or installing a balanced hybrid system. The payoff represents projected annual profit from electricity generation and sales. The estimates are based on expected production capacity, electricity prices, and operating and maintenance costs.</p>
<p>Profit depends on whether conditions are windy, sunny, or cloudy. For the wind-turbine strategy, the projected profits are 90 thousand USD under windy conditions, 45 thousand USD under sunny conditions, and 30 thousand USD under cloudy conditions.</p>
<p>For the solar-farm strategy, the projected profits are 35 thousand USD under windy conditions, 95 thousand USD under sunny conditions, and 25 thousand USD under cloudy conditions. The hybrid system is expected to produce 70 thousand USD under windy conditions, 65 thousand USD under sunny conditions, and 60 thousand USD under cloudy conditions.</p>
<p>The specialized wind and solar systems perform best under favorable weather but decline sharply under less suitable conditions. The hybrid system does not achieve the highest possible payoff, but its outcomes are more stable because it combines two energy sources.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Wind turbines; Solar farms; Hybrid system</td></tr><tr><th scope="row">States of nature</th><td>Windy; Sunny; Cloudy</td></tr><tr><th scope="row">Uncertain event</th><td>Weather outcome affecting generation</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each strategy--weather combination</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Strategy</th><th scope="col">Windy</th><th scope="col">Sunny</th><th scope="col">Cloudy</th></tr></thead>
<tbody>
<tr><th scope="row">Wind turbines</th><td>90</td><td>45</td><td>30</td></tr>
<tr><th scope="row">Solar farms</th><td>35</td><td>95</td><td>25</td></tr>
<tr><th scope="row">Hybrid system</th><td>70</td><td>65</td><td>60</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-5",
        layer1: "Direct",
        layer2: [],
        labels: {
          name: "Global Shipping Network Design (C1--C2)",
          section: "Direct Alternative--State Payoffs"
        },
        descriptionHtml: String.raw`
<p>A multinational logistics firm is choosing between two shipping network designs for long-term freight contracts. The transaction is global freight services, where profit is earned per contract delivered on schedule.</p>
<p>Management is considering:</p>
<ol>
<li><strong>Centralized mega-hub network</strong>
</li><li><strong>Regional multi-hub network</strong>
</li></ol>
<p>The firm models four trade conditions:</p>
<ol>
<li>Trade boom
</li><li>Stable trade
</li><li>Moderate disruptions
</li><li>Severe disruptions
</li></ol>
<p>Modeled profits in thousand USD are:</p>
<ol>
<li>Centralized network $\to 220, 140, 40, -30$
</li><li>Regional network $\to 180, 160, 110, 60$
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A multinational logistics firm must choose between a centralized mega-hub network and a regional multi-hub network for its long-term freight contracts. The payoff represents projected profit after transportation, storage, coordination, and delay costs. Management developed the estimates from previous contracts, expected freight volumes, and simulated disruption scenarios.</p>
<p>The firm considers four possible trade conditions: a trade boom, stable trade, moderate disruptions, and severe disruptions. Under the centralized network, projected profits are 220 thousand USD during a trade boom, 140 thousand USD during stable trade, and 40 thousand USD during moderate disruptions; severe disruptions would produce a loss of 30 thousand USD. This design benefits from economies of scale when trade is strong but becomes vulnerable when disruptions affect the main hub.</p>
<p>Under the regional network, projected profits are 180, 160, 110, and 60 thousand USD under the same four conditions. Operating several hubs limits the highest possible profit, but the network remains more resilient because freight can be redirected when disruptions occur.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Centralized mega-hub; Regional multi-hub</td></tr><tr><th scope="row">States of nature</th><td>Boom; Stable; Moderate disruptions; Severe disruptions</td></tr><tr><th scope="row">Uncertain event</th><td>Trade conditions realized during the planning horizon</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD for each network--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Network</th><th scope="col">Boom</th><th scope="col">Stable</th><th scope="col">Moderate disruptions</th><th scope="col">Severe disruptions</th></tr></thead>
<tbody>
<tr><th scope="row">Centralized mega-hub</th><td>220</td><td>140</td><td>40</td><td>-30</td></tr>
<tr><th scope="row">Regional multi-hub</th><td>180</td><td>160</td><td>110</td><td>60</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-6",
        layer1: "1 component",
        layer2: ["AV"],
        labels: {
          name: "Community Bakery Lunch Boxes (C1--C2)",
          section: "Alternative-Based Variable Payoff: Profit per Item Times Number of Items"
        },
        descriptionHtml: String.raw`
<p>A community bakery is bidding on office lunch-box contracts. The transaction is meal box sales, where profit is earned per lunch box delivered.</p>
<p>The bakery can choose one pricing strategy:</p>
<ol>
<li><strong>Standard packaging</strong> with a profit of $0.04$ thousand USD per lunch box
</li><li><strong>Premium packaging</strong> with a profit of $0.07$ thousand USD per lunch box
</li></ol>
<p>Demand states:</p>
<ol>
<li>High office demand
</li><li>Low office demand
</li></ol>
<p>Modeled number of lunch boxes:</p>
<ol>
<li>Standard packaging $\to 900$ (High), $550$ (Low)
</li><li>Premium packaging $\to 650$ (High), $250$ (Low)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A community bakery is bidding for office lunch-box contracts and must choose between standard and premium packaging. The payoff depends on the profit earned per lunch box and the number of boxes sold. The bakery estimates demand using recent office orders, client inquiries, and projected packaging costs.</p>
<p>Standard packaging generates a profit of 0.04 thousand USD per lunch box. The bakery expects to sell 900 boxes under high office demand and 550 boxes under low demand. Premium packaging generates a higher profit of 0.07 thousand USD per box, but its higher price is expected to reduce sales to 650 boxes under high demand and 250 boxes under low demand.</p>
<p>The premium option earns more per sale but is more sensitive to weak demand, while standard packaging attracts a larger number of customers in both demand states.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Standard packaging; Premium packaging</td></tr><tr><th scope="row">States of nature</th><td>High demand; Low demand</td></tr><tr><th scope="row">Uncertain event</th><td>Actual number of lunch-box contracts realized</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD, based on boxes $\times$ profit per box</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{number of lunch boxes}\times\text{profit per lunch box}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Standard packaging</th><td>$900 \times 0.04 = 36$</td><td>$550 \times 0.04 = 22$</td></tr>
<tr><th scope="row">Premium packaging</th><td>$650 \times 0.07 = 45.5$</td><td>$250 \times 0.07 = 17.5$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Standard packaging</th><td>36</td><td>22</td></tr>
<tr><th scope="row">Premium packaging</th><td>45.5</td><td>17.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-7",
        layer1: "1 component",
        layer2: ["AV"],
        labels: {
          name: "Rural Internet Subscriptions (C1--C2)",
          section: "Alternative-Based Variable Payoff: Profit per Item Times Number of Items"
        },
        descriptionHtml: String.raw`
<p>A rural internet provider is selecting a subscription plan mix. The transaction is monthly broadband subscriptions, where profit is earned per subscription sold.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Basic plan</strong> with profit of $0.03$ thousand USD per subscription
</li><li><strong>Plus plan</strong> with profit of $0.05$ thousand USD per subscription
</li><li><strong>Pro plan</strong> with profit of $0.08$ thousand USD per subscription
</li></ol>
<p>Enrollment states:</p>
<ol>
<li>High enrollment
</li><li>Low enrollment
</li></ol>
<p>Modeled subscriptions sold:</p>
<ol>
<li>Basic $\to 1400$ (High), $900$ (Low)
</li><li>Plus $\to 1000$ (High), $700$ (Low)
</li><li>Pro $\to 600$ (High), $300$ (Low)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A rural internet provider must decide whether to promote its Basic, Plus, or Pro subscription plan. The payoff depends on the profit earned per subscription and the number of customers who enroll. The estimates are based on previous enrollment patterns, local market surveys, and projected service and installation costs.</p>
<p>The Basic plan generates a profit of 0.03 thousand USD per subscription and is expected to attract 1400 customers under high enrollment and 900 under low enrollment. The Plus plan generates 0.05 thousand USD per subscription, with projected sales of 1000 under high enrollment and 700 under low enrollment.</p>
<p>The Pro plan produces the highest profit per subscription, at 0.08 thousand USD, but is expected to attract only 600 customers under high enrollment and 300 under low enrollment. The pattern reflects the trade-off between higher profit per customer and lower demand for more expensive plans.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Basic plan; Plus plan; Pro plan</td></tr><tr><th scope="row">States of nature</th><td>High enrollment; Low enrollment</td></tr><tr><th scope="row">Uncertain event</th><td>Actual subscription uptake after plan selection</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD based on subscriptions $\times$ profit per subscription</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{subscriptions sold}\times\text{profit per subscription}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High enrollment</th><th scope="col">Low enrollment</th></tr></thead>
<tbody>
<tr><th scope="row">Basic plan</th><td>$1400 \times 0.03 = 42$</td><td>$900 \times 0.03 = 27$</td></tr>
<tr><th scope="row">Plus plan</th><td>$1000 \times 0.05 = 50$</td><td>$700 \times 0.05 = 35$</td></tr>
<tr><th scope="row">Pro plan</th><td>$600 \times 0.08 = 48$</td><td>$300 \times 0.08 = 24$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High enrollment</th><th scope="col">Low enrollment</th></tr></thead>
<tbody>
<tr><th scope="row">Basic plan</th><td>42</td><td>27</td></tr>
<tr><th scope="row">Plus plan</th><td>50</td><td>35</td></tr>
<tr><th scope="row">Pro plan</th><td>48</td><td>24</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-8",
        layer1: "1 component",
        layer2: ["SV"],
        labels: {
          name: "Coffee Export Routes (C1--C2)",
          section: "State-Based Variable Payoff: Profit per Item Times Number of Items"
        },
        descriptionHtml: String.raw`
<p>A coffee exporter must choose a shipping route. The transaction is exporting coffee shipments, where profit is earned per shipment delivered.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Route through Port A</strong>
</li><li><strong>Route through Port B</strong>
</li></ol>
<p>Exchange-rate states:</p>
<ol>
<li>Favorable rate
</li><li>Unfavorable rate
</li></ol>
<p>Profit per shipment depends on the exchange rate:</p>
<ol>
<li>Favorable $\to 6$ thousand USD per shipment
</li><li>Unfavorable $\to 2$ thousand USD per shipment
</li></ol>
<p>Modeled shipments:</p>
<ol>
<li>Port A $\to 40$ (Favorable), $28$ (Unfavorable)
</li><li>Port B $\to 32$ (Favorable), $30$ (Unfavorable)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A coffee exporter must choose whether to ship its products through Port A or Port B. The payoff depends on the profit earned per shipment and the number of shipments delivered. Management developed the estimates from previous export volumes, transportation costs, port capacity, and exchange-rate scenarios.</p>
<p>The exchange rate may be favorable or unfavorable. A favorable rate produces a profit of 6 thousand USD per shipment, while an unfavorable rate reduces the profit to 2 thousand USD per shipment.</p>
<p>Through Port A, the exporter expects to deliver 40 shipments under a favorable exchange rate and 28 under an unfavorable rate. Through Port B, it expects to deliver 32 shipments under a favorable rate and 30 under an unfavorable rate. Port A offers greater capacity in favorable conditions, while Port B maintains more stable shipment volumes across both states.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Port A route; Port B route</td></tr><tr><th scope="row">States of nature</th><td>Favorable rate; Unfavorable rate</td></tr><tr><th scope="row">Uncertain event</th><td>Exchange-rate level that affects profit per shipment</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD based on shipments $\times$ profit per shipment</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{shipments}\times\text{profit per shipment}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Route</th><th scope="col">Favorable rate</th><th scope="col">Unfavorable rate</th></tr></thead>
<tbody>
<tr><th scope="row">Port A</th><td>$40 \times 6 = 240$</td><td>$28 \times 2 = 56$</td></tr>
<tr><th scope="row">Port B</th><td>$32 \times 6 = 192$</td><td>$30 \times 2 = 60$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Route</th><th scope="col">Favorable rate</th><th scope="col">Unfavorable rate</th></tr></thead>
<tbody>
<tr><th scope="row">Port A</th><td>240</td><td>56</td></tr>
<tr><th scope="row">Port B</th><td>192</td><td>60</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-9",
        layer1: "1 component",
        layer2: ["SV"],
        labels: {
          name: "Lake Ferry Tourism (C1--C2)",
          section: "State-Based Variable Payoff: Profit per Item Times Number of Items"
        },
        descriptionHtml: String.raw`
<p>A lake tourism operator is choosing boat sizes for sightseeing tours. The transaction is tour ticket sales, where profit is earned per ticket sold.</p>
<p>Alternatives:</p>
<ol>
<li><strong>Operate small ferries</strong>
</li><li><strong>Operate large ferries</strong>
</li></ol>
<p>Seasonal states:</p>
<ol>
<li>Peak season
</li><li>Normal season
</li><li>Rainy season
</li></ol>
<p>Profit per ticket depends on the season:</p>
<ol>
<li>Peak $\to 0.05$ thousand USD
</li><li>Normal $\to 0.04$ thousand USD
</li><li>Rainy $\to 0.03$ thousand USD
</li></ol>
<p>Modeled tickets sold:</p>
<ol>
<li>Small ferries $\to 2200$ (Peak), $1600$ (Normal), $1000$ (Rainy)
</li><li>Large ferries $\to 2600$ (Peak), $1800$ (Normal), $800$ (Rainy)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A lake tourism operator must decide whether to use small ferries or large ferries for sightseeing tours. The payoff depends on the profit earned per ticket and the number of tickets sold. The estimates are based on previous passenger demand, seasonal ticket prices, and projected operating costs.</p>
<p>The operator considers peak season, normal season, and rainy season. Profit per ticket is 0.05 thousand USD during peak season, 0.04 thousand USD during normal season, and 0.03 thousand USD during rainy season.</p>
<p>Small ferries are expected to sell 2200 tickets in peak season, 1600 in normal season, and 1000 in rainy season. Large ferries are expected to sell 2600, 1800, and 800 tickets under the same respective conditions. Large ferries can serve more passengers when demand is strong, but their ticket sales fall below those of small ferries during the rainy season.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Small ferries; Large ferries</td></tr><tr><th scope="row">States of nature</th><td>Peak; Normal; Rainy</td></tr><tr><th scope="row">Uncertain event</th><td>Tourism season and ticket price level</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD based on tickets $\times$ profit per ticket</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{tickets sold}\times\text{profit per ticket}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Peak</th><th scope="col">Normal</th><th scope="col">Rainy</th></tr></thead>
<tbody>
<tr><th scope="row">Small ferries</th><td>$2200 \times 0.05 = 110$</td><td>$1600 \times 0.04 = 64$</td><td>$1000 \times 0.03 = 30$</td></tr>
<tr><th scope="row">Large ferries</th><td>$2600 \times 0.05 = 130$</td><td>$1800 \times 0.04 = 72$</td><td>$800 \times 0.03 = 24$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Peak</th><th scope="col">Normal</th><th scope="col">Rainy</th></tr></thead>
<tbody>
<tr><th scope="row">Small ferries</th><td>110</td><td>64</td><td>30</td></tr>
<tr><th scope="row">Large ferries</th><td>130</td><td>72</td><td>24</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-10",
        layer1: "1 component",
        layer2: ["AF"],
        labels: {
          name: "School Meal Service Contracts (C1--C2)",
          section: "Alternative-Based Fixed Payoff Only"
        },
        descriptionHtml: String.raw`
<p>A school cafeteria provider is choosing a meal-service contract for a short academic program. The transaction is a fixed service contract, where the recorded payoff is tied only to the selected contract type.</p>
<p>Decision alternatives with fixed payoff components:</p>
<ol>
<li><strong>Basic meal contract</strong> $\to 18$ thousand USD
</li><li><strong>Extended meal contract</strong> $\to 32$ thousand USD
</li></ol>
<p>Participation states:</p>
<ol>
<li>Regular participation
</li><li>High participation
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A school cafeteria provider must choose a basic or extended meal contract for a short academic program. After projected food, staffing, and operating costs, the agreed service fee leaves 18 thousand USD under the basic contract and 32 thousand USD under the extended contract.</p>
<p>Participation may be regular or high, but the contracts were negotiated in advance, so their financial results do not change with participation.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Basic meal; Extended meal</td></tr><tr><th scope="row">States of nature</th><td>Regular participation; High participation</td></tr><tr><th scope="row">Uncertain event</th><td>Participation level observed after the contract choice</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Fixed payoff in thousand USD tied only to the selected contract</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Regular participation</th><th scope="col">High participation</th></tr></thead>
<tbody>
<tr><th scope="row">Basic meal</th><td>18</td><td>18</td></tr>
<tr><th scope="row">Extended meal</th><td>32</td><td>32</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-11",
        layer1: "1 component",
        layer2: ["AF"],
        labels: {
          name: "Mobile Clinic Service Contracts (C1--C2)",
          section: "Alternative-Based Fixed Payoff Only"
        },
        descriptionHtml: String.raw`
<p>A health nonprofit is choosing a service contract for mobile clinics. The transaction is a fixed service contract, where the recorded payoff is tied only to the selected contract type.</p>
<p>Decision alternatives with fixed payoff components:</p>
<ol>
<li><strong>Basic outreach contract</strong> $\to 24$ thousand USD
</li><li><strong>Extended outreach contract</strong> $\to 38$ thousand USD
</li><li><strong>Full regional contract</strong> $\to 52$ thousand USD
</li></ol>
<p>Community-need states:</p>
<ol>
<li>Regular need
</li><li>High need
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A health nonprofit must select a basic outreach, extended outreach, or full regional contract for mobile clinics. After expected staffing, transportation, equipment, and operating costs, contracted funding leaves 24 thousand USD for basic outreach, 38 thousand USD for extended outreach, and 52 thousand USD for full regional service.</p>
<p>Community need may be regular or high, but the funding was agreed before need is observed, so the financial result for each contract remains unchanged.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Basic outreach; Extended outreach; Full regional</td></tr><tr><th scope="row">States of nature</th><td>Regular need; High need</td></tr><tr><th scope="row">Uncertain event</th><td>Community-need level observed after the contract choice</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Fixed payoff in thousand USD tied only to the selected contract</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{contract fixed payoff}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Regular need</th><th scope="col">High need</th></tr></thead>
<tbody>
<tr><th scope="row">Basic outreach</th><td>$24$</td><td>$24$</td></tr>
<tr><th scope="row">Extended outreach</th><td>$38$</td><td>$38$</td></tr>
<tr><th scope="row">Full regional</th><td>$52$</td><td>$52$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Regular need</th><th scope="col">High need</th></tr></thead>
<tbody>
<tr><th scope="row">Basic outreach</th><td>24</td><td>24</td></tr>
<tr><th scope="row">Extended outreach</th><td>38</td><td>38</td></tr>
<tr><th scope="row">Full regional</th><td>52</td><td>52</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-12",
        layer1: "1 component",
        layer2: ["SF"],
        labels: {
          name: "Neighborhood Shelter Support (C1--C2)",
          section: "State-Based Fixed Payoff Only"
        },
        descriptionHtml: String.raw`
<p>A municipal office is deciding how to prepare a temporary shelter service for short emergency responses. The transaction is public-service shelter support, where the recorded payoff is a fixed municipal support amount tied only to the emergency state.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Open the school gym</strong>
</li><li><strong>Open the sports center</strong>
</li></ol>
<p>Emergency states with fixed payoff components:</p>
<ol>
<li>Minor emergency $\to 12$ thousand USD
</li><li>Major emergency $\to 30$ thousand USD
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A municipal office must decide whether to open a school gym or a sports center as a temporary shelter. Its emergency budget provides 12 thousand USD during a minor emergency and 30 thousand USD during a major emergency, based on expected shelter operating requirements.</p>
<p>The same support is available for either facility because funding depends on emergency severity, and the larger response receives more support.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>School gym; Sports center</td></tr><tr><th scope="row">States of nature</th><td>Minor emergency; Major emergency</td></tr><tr><th scope="row">Uncertain event</th><td>Emergency level realized after the shelter decision</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Fixed payoff in thousand USD tied only to the emergency state</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Minor emergency</th><th scope="col">Major emergency</th></tr></thead>
<tbody>
<tr><th scope="row">School gym</th><td>12</td><td>30</td></tr>
<tr><th scope="row">Sports center</th><td>12</td><td>30</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-13",
        layer1: "1 component",
        layer2: ["SF"],
        labels: {
          name: "Community Hall Emergency Rentals (C1--C2)",
          section: "State-Based Fixed Payoff Only"
        },
        descriptionHtml: String.raw`
<p>A city council is choosing how to reserve community halls for emergency use. The transaction is public-service facility rental, where the recorded payoff is a fixed municipal support amount tied only to the emergency state.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Reserve one central hall</strong>
</li><li><strong>Reserve two neighborhood halls</strong>
</li></ol>
<p>Emergency states with fixed payoff components:</p>
<ol>
<li>Mild emergency $\to 18$ thousand USD
</li><li>Serious emergency $\to 35$ thousand USD
</li><li>Major emergency $\to 50$ thousand USD
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A city council must decide whether to reserve one central hall or two neighborhood halls for emergency use. Budget forecasts provide 18 thousand USD of facility-rental support during a mild emergency, 35 thousand USD during a serious emergency, and 50 thousand USD during a major emergency.</p>
<p>These amounts apply to either reservation strategy because the support depends on the scale of emergency services required, not the halls selected.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>One central hall; Two neighborhood halls</td></tr><tr><th scope="row">States of nature</th><td>Mild emergency; Serious emergency; Major emergency</td></tr><tr><th scope="row">Uncertain event</th><td>Emergency level realized after the reservation decision</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Fixed payoff in thousand USD tied only to the emergency state</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{emergency-state fixed payoff}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Mild emergency</th><th scope="col">Serious emergency</th><th scope="col">Major emergency</th></tr></thead>
<tbody>
<tr><th scope="row">One central hall</th><td>$18$</td><td>$35$</td><td>$50$</td></tr>
<tr><th scope="row">Two neighborhood halls</th><td>$18$</td><td>$35$</td><td>$50$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Mild emergency</th><th scope="col">Serious emergency</th><th scope="col">Major emergency</th></tr></thead>
<tbody>
<tr><th scope="row">One central hall</th><td>18</td><td>35</td><td>50</td></tr>
<tr><th scope="row">Two neighborhood halls</th><td>18</td><td>35</td><td>50</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-14",
        layer1: "2 components",
        layer2: ["AV","SV"],
        labels: {
          name: "Recycling Collection Contract (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff"
        },
        descriptionHtml: String.raw`
<p>A municipal contractor chooses a collection fleet for a two-month recycling service contract.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Electric fleet
</li><li>Diesel fleet
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>High recovery
</li><li>Low recovery
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Electric fleet: $0.6$ thousand USD
</li><li>Diesel fleet: $0.4$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>High recovery: $0.3$ thousand USD
</li><li>Low recovery: $0.1$ thousand USD
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Electric fleet: 80 under High recovery, 55 under Low recovery
</li><li>Diesel fleet: 95 under High recovery, 65 under Low recovery
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A municipal contractor must choose an electric or diesel fleet for a two-month recycling collection contract. Supplier quotes and operating budgets indicate that each item collected by the electric fleet earns 0.6 thousand USD after fleet expenses, while each item collected by the diesel fleet earns 0.4 thousand USD. Revenue from recovered material adds 0.3 thousand USD for every item when recovery is high and 0.1 thousand USD when recovery is low.</p>
<p>The electric fleet is expected to collect 80 items under high recovery and 55 under low recovery. The diesel fleet is expected to collect 95 items under high recovery and 65 under low recovery. The diesel fleet processes more items, while the electric fleet earns more from each collection before recovery revenue is included.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Electric fleet; Diesel fleet</td></tr><tr><th scope="row">States of nature</th><td>High recovery; Low recovery</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right).
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High recovery</th><th scope="col">Low recovery</th></tr></thead>
<tbody>
<tr><th scope="row">Electric fleet</th><td>$80\times(0.6+0.3)=72$</td><td>$55\times(0.6+0.1)=38.5$</td></tr>
<tr><th scope="row">Diesel fleet</th><td>$95\times(0.4+0.3)=66.5$</td><td>$65\times(0.4+0.1)=32.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High recovery</th><th scope="col">Low recovery</th></tr></thead>
<tbody>
<tr><th scope="row">Electric fleet</th><td>72</td><td>38.5</td></tr>
<tr><th scope="row">Diesel fleet</th><td>66.5</td><td>32.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-15",
        layer1: "2 components",
        layer2: ["AV","SV"],
        labels: {
          name: "Museum Ticket Platform (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff"
        },
        descriptionHtml: String.raw`
<p>A museum consortium selects a ticket platform; the transaction is batches of one thousand admissions processed.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Mobile platform
</li><li>Kiosk platform
</li><li>Hybrid platform
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Peak season
</li><li>Regular season
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Mobile platform: $0.5$ thousand USD
</li><li>Kiosk platform: $0.4$ thousand USD
</li><li>Hybrid platform: $0.4$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Peak season: $0.2$ thousand USD
</li><li>Regular season: $0.1$ thousand USD
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Mobile platform: 70 under Peak season, 45 under Regular season
</li><li>Kiosk platform: 60 under Peak season, 50 under Regular season
</li><li>Hybrid platform: 65 under Peak season, 55 under Regular season
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A museum consortium must select a mobile, kiosk, or hybrid ticket platform. Its contracts measure activity in batches of one thousand admissions. After platform operating costs, each batch processed on the mobile platform earns 0.5 thousand USD, while each batch processed on either the kiosk or hybrid platform earns 0.4 thousand USD. Seasonal admission pricing adds 0.2 thousand USD to the earnings from every batch in peak season and 0.1 thousand USD in regular season. These figures come from recent admission volumes, vendor quotes, and processing-revenue forecasts.</p>
<p>The mobile platform is expected to process 70 batches during peak season and 45 during regular season. The kiosk platform is expected to process 60 and 50 batches, respectively. The hybrid platform is expected to process 65 batches during peak season and 55 during regular season. The mobile platform earns the most from each batch before seasonal admission revenue is included, while the hybrid platform is forecast to process the most batches during regular season.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Mobile platform; Kiosk platform; Hybrid platform</td></tr><tr><th scope="row">States of nature</th><td>Peak season; Regular season</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right).
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Peak season</th><th scope="col">Regular season</th></tr></thead>
<tbody>
<tr><th scope="row">Mobile platform</th><td>$70\times(0.5+0.2)=49$</td><td>$45\times(0.5+0.1)=27$</td></tr>
<tr><th scope="row">Kiosk platform</th><td>$60\times(0.4+0.2)=36$</td><td>$50\times(0.4+0.1)=25$</td></tr>
<tr><th scope="row">Hybrid platform</th><td>$65\times(0.4+0.2)=39$</td><td>$55\times(0.4+0.1)=27.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Peak season</th><th scope="col">Regular season</th></tr></thead>
<tbody>
<tr><th scope="row">Mobile platform</th><td>49</td><td>27</td></tr>
<tr><th scope="row">Kiosk platform</th><td>36</td><td>25</td></tr>
<tr><th scope="row">Hybrid platform</th><td>39</td><td>27.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-16",
        layer1: "2 components",
        layer2: ["AV","AF"],
        labels: {
          name: "Local Printing Contracts (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A local printing shop is choosing a contract format for school material packets. The transaction is printing packets, where profit is earned per packet printed plus a fixed profit associated with the chosen printing setup.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Small printer setup</strong> (fixed profit $12$ thousand USD, profit $0.05$ thousand USD per packet)
</li><li><strong>Digital printer setup</strong> (fixed profit $20$ thousand USD, profit $0.04$ thousand USD per packet)
</li></ol>
<p>Demand states:</p>
<ol>
<li>High packet demand
</li><li>Low packet demand
</li></ol>
<p>Modeled packets printed:</p>
<ol>
<li>Small printer $\to 500$ (High), $300$ (Low)
</li><li>Digital printer $\to 700$ (High), $400$ (Low)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A local printing shop must choose a small or digital printer setup for school material packets. Contract terms provide 12 thousand USD of setup income for the small printer and 20 thousand USD for the digital printer. After ink, paper, and labor costs, the small printer earns 0.05 thousand USD per packet and the digital printer earns 0.04 thousand USD. Demand forecasts come from previous school orders.</p>
<p>The small printer is expected to produce 500 packets under high demand and 300 under low demand. The digital printer is expected to produce 700 and 400 packets, respectively.</p>
<p>The small setup earns more per packet, while the digital setup receives more setup income and can process more packets under both demand conditions.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Small printer; Digital printer</td></tr><tr><th scope="row">States of nature</th><td>High demand; Low demand</td></tr><tr><th scope="row">Uncertain event</th><td>Packet demand realized after the printing setup decision</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{packets} \times \text{profit per packet} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{packets printed}\times\text{profit per packet}+\text{setup fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Small printer</th><td>$500 \times 0.05 + 12 = 37$</td><td>$300 \times 0.05 + 12 = 27$</td></tr>
<tr><th scope="row">Digital printer</th><td>$700 \times 0.04 + 20 = 48$</td><td>$400 \times 0.04 + 20 = 36$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Small printer</th><td>37</td><td>27</td></tr>
<tr><th scope="row">Digital printer</th><td>48</td><td>36</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-17",
        layer1: "2 components",
        layer2: ["AV","AF"],
        labels: {
          name: "Cold-Storage Contracts (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A logistics company is leasing cold-storage space for agricultural pallets. The transaction is storage contracts, where profit is earned per pallet stored plus a fixed profit associated with the chosen facility.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Small facility</strong> (fixed profit $40$ thousand USD, profit $0.18$ thousand USD per pallet)
</li><li><strong>Medium facility</strong> (fixed profit $25$ thousand USD, profit $0.12$ thousand USD per pallet)
</li><li><strong>Large facility</strong> (fixed profit $10$ thousand USD, profit $0.08$ thousand USD per pallet)
</li></ol>
<p>Demand states:</p>
<ol>
<li>High storage demand
</li><li>Low storage demand
</li></ol>
<p>Modeled pallets stored:</p>
<ol>
<li>Small $\to 300$ (High), $220$ (Low)
</li><li>Medium $\to 600$ (High), $420$ (Low)
</li><li>Large $\to 900$ (High), $700$ (Low)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A logistics company must choose a small, medium, or large cold-storage facility for agricultural pallets. Existing contracts provide 40 thousand USD of facility income for the small site, 25 thousand USD for the medium site, and 10 thousand USD for the large site. After operating costs, each stored pallet earns 0.18 thousand USD at the small facility, 0.12 thousand USD at the medium facility, and 0.08 thousand USD at the large facility. Volume forecasts use previous contracts and projected demand.</p>
<p>The small facility is expected to store 300 pallets under high demand and 220 under low demand. The medium facility is expected to store 600 and 420 pallets, respectively.</p>
<p>The large facility is expected to store 900 pallets under high demand and 700 under low demand. Larger facilities handle more pallets, while smaller facilities receive more contract income and earn more per pallet.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Small facility; Medium facility; Large facility</td></tr><tr><th scope="row">States of nature</th><td>High demand; Low demand</td></tr><tr><th scope="row">Uncertain event</th><td>Storage demand realized after the lease decision</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{pallets} \times \text{profit per pallet} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{pallets stored}\times\text{profit per pallet}+\text{facility fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Small facility</th><td>$300 \times 0.18 + 40 = 94$</td><td>$220 \times 0.18 + 40 = 79.6$</td></tr>
<tr><th scope="row">Medium facility</th><td>$600 \times 0.12 + 25 = 97$</td><td>$420 \times 0.12 + 25 = 75.4$</td></tr>
<tr><th scope="row">Large facility</th><td>$900 \times 0.08 + 10 = 82$</td><td>$700 \times 0.08 + 10 = 66$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead>
<tbody>
<tr><th scope="row">Small facility</th><td>94</td><td>79.6</td></tr>
<tr><th scope="row">Medium facility</th><td>97</td><td>75.4</td></tr>
<tr><th scope="row">Large facility</th><td>82</td><td>66</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-18",
        layer1: "2 components",
        layer2: ["AV","SF"],
        labels: {
          name: "Urban Landscaping Bids (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A landscaping company is bidding on city maintenance projects. The transaction is completing landscaping projects, where profit is earned per project plus a fixed profit adjustment from grant conditions.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Residential team focus</strong> (profit $0.6$ thousand USD per project)
</li><li><strong>Commercial team focus</strong> (profit $1.0$ thousand USD per project)
</li></ol>
<p>Grant states with fixed profit components:</p>
<ol>
<li>Grant available $\to +10$ thousand USD
</li><li>No grant $\to -5$ thousand USD
</li></ol>
<p>Modeled projects completed:</p>
<ol>
<li>Residential $\to 40$ (Grant available), $25$ (No grant)
</li><li>Commercial $\to 30$ (Grant available), $20$ (No grant)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A landscaping company must focus its bids on residential or commercial city maintenance projects. Each completed project earns a team-specific profit, and grant funding or unreimbursed costs also affect the result. The estimates are based on previous contracts, projected labor and equipment costs, and expected project demand.</p>
<p>The residential team earns 0.6 thousand USD per project and is expected to complete 40 projects if the grant is available and 25 if no grant is available. The commercial team earns 1.0 thousand USD per project and is expected to complete 30 and 20 projects under the same respective states.</p>
<p>If the grant is available, it contributes 10 thousand USD toward either team’s contract profit. Without the grant, either team must absorb 5 thousand USD of unreimbursed equipment and mobilization costs. The residential focus produces more projects, while the commercial focus earns more per project.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Residential; Commercial</td></tr><tr><th scope="row">States of nature</th><td>Grant available; No grant</td></tr><tr><th scope="row">Uncertain event</th><td>Grant outcome affecting the fixed profit adjustment</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{projects} \times \text{profit per project} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{projects completed}\times\text{profit per project}+\text{grant fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Grant available</th><th scope="col">No grant</th></tr></thead>
<tbody>
<tr><th scope="row">Residential focus</th><td>$40 \times 0.6 + 10 = 34$</td><td>$25 \times 0.6 - 5 = 10$</td></tr>
<tr><th scope="row">Commercial focus</th><td>$30 \times 1.0 + 10 = 40$</td><td>$20 \times 1.0 - 5 = 15$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Grant available</th><th scope="col">No grant</th></tr></thead>
<tbody>
<tr><th scope="row">Residential focus</th><td>34</td><td>10</td></tr>
<tr><th scope="row">Commercial focus</th><td>40</td><td>15</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-19",
        layer1: "2 components",
        layer2: ["AV","SF"],
        labels: {
          name: "Solar Installation Bids (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A solar company is bidding on installation contracts. The transaction is installing solar systems, where profit is earned per installation plus a fixed profit adjustment from policy conditions.</p>
<p>Decision alternatives:</p>
<ol>
<li><strong>Residential focus</strong> (profit $0.9$ thousand USD per installation)
</li><li><strong>Commercial focus</strong> (profit $1.6$ thousand USD per installation)
</li><li><strong>Mixed portfolio</strong> (profit $1.2$ thousand USD per installation)
</li></ol>
<p>Policy states with fixed profit components:</p>
<ol>
<li>Rebate continues $\to +20$ thousand USD
</li><li>Rebate ends $\to -10$ thousand USD
</li></ol>
<p>Modeled installations:</p>
<ol>
<li>Residential $\to 80$ (Rebate continues), $50$ (Rebate ends)
</li><li>Commercial $\to 55$ (Rebate continues), $40$ (Rebate ends)
</li><li>Mixed $\to 70$ (Rebate continues), $45$ (Rebate ends)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A solar company must choose a residential, commercial, or mixed portfolio. Each installation earns a portfolio-specific profit, and the government rebate either contributes funding or leaves costs unreimbursed. The estimates reflect recent bids, projected installation costs, and expected customer demand.</p>
<p>The residential focus earns 0.9 thousand USD per installation and is expected to complete 80 installations if the rebate continues and 50 if it ends. The commercial focus earns 1.6 thousand USD per installation, with projected volumes of 55 and 40 installations under the same respective states. The mixed portfolio earns 1.2 thousand USD per installation and is expected to complete 70 installations if the rebate continues and 45 if it ends.</p>
<p>If the rebate continues, it contributes 20 thousand USD to the profit of any portfolio. If it ends, any portfolio must absorb 10 thousand USD of administrative and equipment costs that would otherwise have been reimbursed. The residential strategy produces the largest volume, the commercial strategy earns the most per installation, and the mixed portfolio balances both features.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Residential; Commercial; Mixed portfolio</td></tr><tr><th scope="row">States of nature</th><td>Rebate continues; Rebate ends</td></tr><tr><th scope="row">Uncertain event</th><td>Policy outcome affecting the fixed profit adjustment</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{installs} \times \text{profit per install} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{installations}\times\text{profit per installation}+\text{policy fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Rebate continues</th><th scope="col">Rebate ends</th></tr></thead>
<tbody>
<tr><th scope="row">Residential focus</th><td>$80 \times 0.9 + 20 = 92$</td><td>$50 \times 0.9 - 10 = 35$</td></tr>
<tr><th scope="row">Commercial focus</th><td>$55 \times 1.6 + 20 = 108$</td><td>$40 \times 1.6 - 10 = 54$</td></tr>
<tr><th scope="row">Mixed portfolio</th><td>$70 \times 1.2 + 20 = 104$</td><td>$45 \times 1.2 - 10 = 44$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Rebate continues</th><th scope="col">Rebate ends</th></tr></thead>
<tbody>
<tr><th scope="row">Residential focus</th><td>92</td><td>35</td></tr>
<tr><th scope="row">Commercial focus</th><td>108</td><td>54</td></tr>
<tr><th scope="row">Mixed portfolio</th><td>104</td><td>44</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-20",
        layer1: "2 components",
        layer2: ["SV","AF"],
        labels: {
          name: "Regional Bus Charters (C1--C2)",
          section: "State-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A regional transport firm is choosing a charter fleet for school trips. The transaction is bus charters, where profit is earned per charter plus a fixed profit component tied to the selected fleet arrangement.</p>
<p>Alternatives:</p>
<ol>
<li><strong>Use mini-bus fleet</strong> (fixed profit $15$ thousand USD)
</li><li><strong>Use coach fleet</strong> (fixed profit $25$ thousand USD)
</li></ol>
<p>Fuel-cost states:</p>
<ol>
<li>Regular fuel cost
</li><li>High fuel cost
</li></ol>
<p>Profit per charter depends on fuel costs:</p>
<ol>
<li>Regular fuel $\to 4$ thousand USD
</li><li>High fuel $\to 2$ thousand USD
</li></ol>
<p>Modeled charters:</p>
<ol>
<li>Mini-bus $\to 25$ (Regular), $20$ (High)
</li><li>Coach $\to 18$ (Regular), $16$ (High)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A regional transport firm must choose a mini-bus or coach fleet for school-trip charters. Fleet contracts provide 15 thousand USD of income for mini-buses and 25 thousand USD for coaches, in addition to the profit from completed charters. The estimates are based on previous school contracts, expected bookings, and projected fuel and operating costs.</p>
<p>The mini-bus fleet is expected to complete 25 charters under regular fuel costs and 20 under high fuel costs. The coach fleet has projected volumes of 18 and 16 charters under the same respective states.</p>
<p>Profit per charter is 4 thousand USD when fuel costs are regular and 2 thousand USD when fuel costs are high. The mini-bus fleet completes more charters, while the coach fleet receives more contract income.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Mini-bus fleet; Coach fleet</td></tr><tr><th scope="row">States of nature</th><td>Regular fuel; High fuel</td></tr><tr><th scope="row">Uncertain event</th><td>Fuel costs affecting profit per charter</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{charters} \times \text{profit per charter} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{charters}\times\text{profit per charter}+\text{fleet fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Regular fuel</th><th scope="col">High fuel</th></tr></thead>
<tbody>
<tr><th scope="row">Mini-bus fleet</th><td>$25 \times 4 + 15 = 115$</td><td>$20 \times 2 + 15 = 55$</td></tr>
<tr><th scope="row">Coach fleet</th><td>$18 \times 4 + 25 = 97$</td><td>$16 \times 2 + 25 = 57$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Regular fuel</th><th scope="col">High fuel</th></tr></thead>
<tbody>
<tr><th scope="row">Mini-bus fleet</th><td>115</td><td>55</td></tr>
<tr><th scope="row">Coach fleet</th><td>97</td><td>57</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-21",
        layer1: "2 components",
        layer2: ["SV","AF"],
        labels: {
          name: "Air Cargo Charters (C1--C2)",
          section: "State-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>An air cargo firm is choosing a charter fleet. The transaction is cargo charters, where profit is earned per charter plus a fixed profit component tied to the chosen aircraft lease.</p>
<p>Alternatives:</p>
<ol>
<li><strong>Lease narrow-body aircraft</strong> (fixed profit $30$ thousand USD)
</li><li><strong>Lease wide-body aircraft</strong> (fixed profit $50$ thousand USD)
</li></ol>
<p>Fuel-price states:</p>
<ol>
<li>Low fuel cost
</li><li>Medium fuel cost
</li><li>High fuel cost
</li></ol>
<p>Profit per charter depends on fuel prices:</p>
<ol>
<li>Low fuel $\to 8$ thousand USD
</li><li>Medium fuel $\to 5$ thousand USD
</li><li>High fuel $\to 2$ thousand USD
</li></ol>
<p>Modeled charters:</p>
<ol>
<li>Narrow-body $\to 20$ (Low), $18$ (Medium), $15$ (High)
</li><li>Wide-body $\to 14$ (Low), $12$ (Medium), $9$ (High)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>An air cargo firm must lease narrow-body or wide-body aircraft. Lease contracts provide 30 thousand USD of income for narrow-body aircraft and 50 thousand USD for wide-body aircraft, in addition to profit from completed charters. The estimates reflect previous contracts, expected freight demand, lease costs, and projected fuel expenses.</p>
<p>Narrow-body aircraft are expected to complete 20 charters under low fuel costs, 18 under medium fuel costs, and 15 under high fuel costs. Wide-body aircraft have projected volumes of 14, 12, and 9 charters under the same respective states.</p>
<p>Profit per charter is 8 thousand USD under low fuel costs, 5 thousand USD under medium fuel costs, and 2 thousand USD under high fuel costs. Narrow-body aircraft complete more charters, while wide-body aircraft receive more lease-contract income.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Narrow-body lease; Wide-body lease</td></tr><tr><th scope="row">States of nature</th><td>Low fuel; Medium fuel; High fuel</td></tr><tr><th scope="row">Uncertain event</th><td>Fuel prices affecting profit per charter</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{charters} \times \text{profit per charter} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{charters}\times\text{profit per charter}+\text{aircraft fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Low fuel</th><th scope="col">Medium fuel</th><th scope="col">High fuel</th></tr></thead>
<tbody>
<tr><th scope="row">Narrow-body lease</th><td>$20 \times 8 + 30 = 190$</td><td>$18 \times 5 + 30 = 120$</td><td>$15 \times 2 + 30 = 60$</td></tr>
<tr><th scope="row">Wide-body lease</th><td>$14 \times 8 + 50 = 162$</td><td>$12 \times 5 + 50 = 110$</td><td>$9 \times 2 + 50 = 68$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Low fuel</th><th scope="col">Medium fuel</th><th scope="col">High fuel</th></tr></thead>
<tbody>
<tr><th scope="row">Narrow-body lease</th><td>190</td><td>120</td><td>60</td></tr>
<tr><th scope="row">Wide-body lease</th><td>162</td><td>110</td><td>68</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-22",
        layer1: "2 components",
        layer2: ["SV","SF"],
        labels: {
          name: "Fruit Export Permits (C1--C2)",
          section: "State-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A fruit exporter is choosing an export permit focus. The transaction is exporting fruit crates, where profit is earned per crate plus a fixed profit adjustment tied to seasonal conditions.</p>
<p>Alternatives:</p>
<ol>
<li><strong>Citrus export focus</strong>
</li><li><strong>Berry export focus</strong>
</li></ol>
<p>Seasonal states with fixed profit components:</p>
<ol>
<li>Strong harvest season $\to +12$ thousand USD
</li><li>Weak harvest season $\to -8$ thousand USD
</li></ol>
<p>Profit per crate depends on the season:</p>
<ol>
<li>Strong season $\to 0.4$ thousand USD
</li><li>Weak season $\to 0.2$ thousand USD
</li></ol>
<p>Modeled crates exported:</p>
<ol>
<li>Citrus $\to 200$ (Strong), $150$ (Weak)
</li><li>Berry $\to 180$ (Strong), $120$ (Weak)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A fruit exporter must choose whether to focus its permit on citrus or berry exports. Profit comes from each crate exported, together with supply-contract income or emergency sourcing costs determined by the harvest. The estimates are based on expected export volumes, seasonal yields, transportation costs, and market demand.</p>
<p>During a strong harvest, favorable supply contracts contribute 12 thousand USD to the exporter’s profit, and each crate earns 0.4 thousand USD. During a weak harvest, emergency sourcing costs reduce profit by 8 thousand USD, and each crate earns 0.2 thousand USD.</p>
<p>The citrus focus is expected to export 200 crates in a strong season and 150 in a weak season. The berry focus is expected to export 180 and 120 crates under the same respective conditions. Citrus maintains the larger modeled export volume in both states.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Citrus focus; Berry focus</td></tr><tr><th scope="row">States of nature</th><td>Strong; Weak</td></tr><tr><th scope="row">Uncertain event</th><td>Seasonal conditions affecting prices and fixed profit adjustments</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{crates} \times \text{profit per crate} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{crates exported}\times\text{profit per crate}+\text{season fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong</th><th scope="col">Weak</th></tr></thead>
<tbody>
<tr><th scope="row">Citrus focus</th><td>$200 \times 0.4 + 12 = 92$</td><td>$150 \times 0.2 - 8 = 22$</td></tr>
<tr><th scope="row">Berry focus</th><td>$180 \times 0.4 + 12 = 84$</td><td>$120 \times 0.2 - 8 = 16$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong</th><th scope="col">Weak</th></tr></thead>
<tbody>
<tr><th scope="row">Citrus focus</th><td>92</td><td>22</td></tr>
<tr><th scope="row">Berry focus</th><td>84</td><td>16</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-23",
        layer1: "2 components",
        layer2: ["SV","SF"],
        labels: {
          name: "Seafood Export Licenses (C1--C2)",
          section: "State-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A seafood exporter is choosing a license focus. The transaction is exporting seafood crates, where profit is earned per crate plus a fixed profit adjustment tied to seasonal conditions.</p>
<p>Alternatives:</p>
<ol>
<li><strong>Frozen fillet focus</strong>
</li><li><strong>Fresh export focus</strong>
</li></ol>
<p>Seasonal states with fixed profit components:</p>
<ol>
<li>Strong tourism season $\to +30$ thousand USD
</li><li>Normal season $\to +10$ thousand USD
</li><li>Stormy season $\to -15$ thousand USD
</li></ol>
<p>Profit per crate depends on the season:</p>
<ol>
<li>Strong $\to 0.7$ thousand USD
</li><li>Normal $\to 0.5$ thousand USD
</li><li>Stormy $\to 0.2$ thousand USD
</li></ol>
<p>Modeled crates exported:</p>
<ol>
<li>Frozen fillet $\to 120$ (Strong), $100$ (Normal), $80$ (Stormy)
</li><li>Fresh export $\to 90$ (Strong), $110$ (Normal), $70$ (Stormy)
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A seafood exporter must choose between a frozen-fillet focus and a fresh-export focus. Profit comes from each crate exported, together with advance-purchase income or weather-related costs determined by the season. The estimates reflect expected demand, storage and transportation costs, previous export volumes, and possible weather disruptions.</p>
<p>During a strong tourism season, advance-purchase contracts contribute 30 thousand USD to profit, and each crate earns 0.7 thousand USD. During a normal season, those contracts contribute 10 thousand USD, and each crate earns 0.5 thousand USD. During a stormy season, weather-related storage and rescheduling costs reduce profit by 15 thousand USD, and each crate earns 0.2 thousand USD.</p>
<p>The frozen-fillet focus is expected to export 120 crates in a strong season, 100 in a normal season, and 80 in a stormy season. The fresh-export focus is expected to export 90, 110, and 70 crates under the same respective states. Frozen products perform better in strong and stormy conditions, while fresh exports have the larger modeled volume during a normal season.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Frozen fillet focus; Fresh export focus</td></tr><tr><th scope="row">States of nature</th><td>Strong; Normal; Stormy</td></tr><tr><th scope="row">Uncertain event</th><td>Seasonal conditions affecting prices and fixed profit adjustments</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{crates} \times \text{profit per crate} + \text{fixed profit}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{crates exported}\times\text{profit per crate}+\text{season fixed profit}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong</th><th scope="col">Normal</th><th scope="col">Stormy</th></tr></thead>
<tbody>
<tr><th scope="row">Frozen fillet focus</th><td>$120 \times 0.7 + 30 = 114$</td><td>$100 \times 0.5 + 10 = 60$</td><td>$80 \times 0.2 - 15 = 1$</td></tr>
<tr><th scope="row">Fresh export focus</th><td>$90 \times 0.7 + 30 = 93$</td><td>$110 \times 0.5 + 10 = 65$</td><td>$70 \times 0.2 - 15 = -1$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong</th><th scope="col">Normal</th><th scope="col">Stormy</th></tr></thead>
<tbody>
<tr><th scope="row">Frozen fillet focus</th><td>114</td><td>60</td><td>1</td></tr>
<tr><th scope="row">Fresh export focus</th><td>93</td><td>65</td><td>-1</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-24",
        layer1: "2 components",
        layer2: ["AF","SF"],
        labels: {
          name: "Warehouse Security Agreements (C1--C2)",
          section: "Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A warehouse operator is choosing a security agreement for seasonal inventory protection. The transaction is a fixed security agreement, where the recorded payoff combines a fixed component tied to the agreement and a fixed component tied to the demand season.</p>
<p>Decision alternatives with fixed payoff components:</p>
<ol>
<li><strong>Standard security agreement</strong> $\to 20$ thousand USD
</li><li><strong>Enhanced security agreement</strong> $\to 35$ thousand USD
</li></ol>
<p>Demand-season states with fixed payoff components:</p>
<ol>
<li>Normal season $\to 6$ thousand USD
</li><li>Festival season $\to 14$ thousand USD
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A warehouse operator must choose between a standard and an enhanced security agreement for protecting seasonal inventory. Contract terms provide 20 thousand USD of net income under the standard agreement and 35 thousand USD under the enhanced agreement. Inventory forecasts show that the normal season brings a further 6 thousand USD of security funding, while the festival season brings 14 thousand USD because larger inventories require greater security support.</p>
<p>These agreement amounts and seasonal funding are both included in the operator’s financial result, whichever agreement is selected.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Standard security; Enhanced security</td></tr><tr><th scope="row">States of nature</th><td>Normal season; Festival season</td></tr><tr><th scope="row">Uncertain event</th><td>Demand-season state realized during the security period</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{agreement fixed payoff} + \text{state fixed payoff}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{agreement fixed payoff}+\text{state fixed payoff}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Normal season</th><th scope="col">Festival season</th></tr></thead>
<tbody>
<tr><th scope="row">Standard security</th><td>$20 + 6 = 26$</td><td>$20 + 14 = 34$</td></tr>
<tr><th scope="row">Enhanced security</th><td>$35 + 6 = 41$</td><td>$35 + 14 = 49$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Normal season</th><th scope="col">Festival season</th></tr></thead>
<tbody>
<tr><th scope="row">Standard security</th><td>26</td><td>34</td></tr>
<tr><th scope="row">Enhanced security</th><td>41</td><td>49</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-25",
        layer1: "2 components",
        layer2: ["AF","SF"],
        labels: {
          name: "Harbor Inspection Agreements (C1--C2)",
          section: "Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A port authority is choosing an inspection agreement for harbor facilities. The transaction is a fixed inspection agreement, where the recorded payoff combines a fixed component tied to the agreement and a fixed component tied to the harbor condition state.</p>
<p>Decision alternatives with fixed payoff components:</p>
<ol>
<li><strong>Standard inspection agreement</strong> $\to 28$ thousand USD
</li><li><strong>Rapid-response inspection agreement</strong> $\to 42$ thousand USD
</li></ol>
<p>Harbor condition states with fixed payoff components:</p>
<ol>
<li>Calm season $\to 12$ thousand USD
</li><li>Busy season $\to 5$ thousand USD
</li><li>Storm-repair season $\to -10$ thousand USD
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A port authority must choose between a standard inspection agreement and a rapid-response inspection agreement. Contract terms provide 28 thousand USD of net income under the standard agreement and 42 thousand USD under the rapid-response agreement. Operations forecasts indicate that a calm season adds 12 thousand USD and a busy season adds 5 thousand USD, while storm repairs reduce the result by 10 thousand USD. These amounts apply whichever agreement is chosen.</p>
<p>The harbor estimates come from the inspection contracts, maintenance plans, and staffing requirements for each operating condition.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Standard inspection; Rapid-response inspection</td></tr><tr><th scope="row">States of nature</th><td>Calm season; Busy season; Storm-repair season</td></tr><tr><th scope="row">Uncertain event</th><td>Harbor condition state realized during the inspection period</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Profit in thousand USD $= \text{agreement fixed payoff} + \text{state fixed payoff}$</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>Calculation table in thousand USD:</p>
$$
\text{Payoff}=\text{agreement fixed payoff}+\text{state fixed payoff}
$$
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Calm season</th><th scope="col">Busy season</th><th scope="col">Storm-repair season</th></tr></thead>
<tbody>
<tr><th scope="row">Standard inspection</th><td>$28 + 12 = 40$</td><td>$28 + 5 = 33$</td><td>$28 - 10 = 18$</td></tr>
<tr><th scope="row">Rapid-response inspection</th><td>$42 + 12 = 54$</td><td>$42 + 5 = 47$</td><td>$42 - 10 = 32$</td></tr>
</tbody></table></div>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Calm season</th><th scope="col">Busy season</th><th scope="col">Storm-repair season</th></tr></thead>
<tbody>
<tr><th scope="row">Standard inspection</th><td>40</td><td>33</td><td>18</td></tr>
<tr><th scope="row">Rapid-response inspection</th><td>54</td><td>47</td><td>32</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-26",
        layer1: "3 components",
        layer2: ["AV","SV","AF"],
        labels: {
          name: "Water Treatment Modules (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A utility chooses a portable treatment design for batches of water delivered to remote communities.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Membrane unit
</li><li>Filtration unit
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Dry season
</li><li>Wet season
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Membrane unit: $0.8$ thousand USD
</li><li>Filtration unit: $0.6$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Dry season: $0.3$ thousand USD
</li><li>Wet season: $0.1$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Membrane unit: $8$ thousand USD
</li><li>Filtration unit: $12$ thousand USD
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Membrane unit: 50 under Dry season, 35 under Wet season
</li><li>Filtration unit: 60 under Dry season, 45 under Wet season
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A utility must choose between a membrane unit and a filtration unit for treating batches of water delivered to remote communities. Supplier terms give the membrane unit 8 thousand USD of contract income plus earnings of 0.8 thousand USD for every batch treated. The filtration unit receives 12 thousand USD of contract income plus 0.6 thousand USD for every batch. Seasonal water tariffs add 0.3 thousand USD to the earnings from each batch in the dry season and 0.1 thousand USD in the wet season. The estimates come from supplier quotes, operating budgets, and demand forecasts.</p>
<p>Capacity studies predict that the membrane unit will treat 50 batches in the dry season and 35 in the wet season. They predict 60 and 45 batches, respectively, for the filtration unit.</p>
<p>The membrane unit earns more for each batch before seasonal tariffs, whereas the filtration unit receives more contract income and has greater forecast capacity.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Membrane unit; Filtration unit</td></tr><tr><th scope="row">States of nature</th><td>Dry season; Wet season</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_i^A.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Dry season</th><th scope="col">Wet season</th></tr></thead>
<tbody>
<tr><th scope="row">Membrane unit</th><td>$50\times(0.8+0.3)+8=63$</td><td>$35\times(0.8+0.1)+8=39.5$</td></tr>
<tr><th scope="row">Filtration unit</th><td>$60\times(0.6+0.3)+12=66$</td><td>$45\times(0.6+0.1)+12=43.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Dry season</th><th scope="col">Wet season</th></tr></thead>
<tbody>
<tr><th scope="row">Membrane unit</th><td>63</td><td>39.5</td></tr>
<tr><th scope="row">Filtration unit</th><td>66</td><td>43.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-27",
        layer1: "3 components",
        layer2: ["AV","SV","AF"],
        labels: {
          name: "Freight Locker Network (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff Plus Alternative-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A parcel operator chooses a locker network for shipment batches handled under two demand states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Metro lockers
</li><li>Suburban lockers
</li><li>Mixed network
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Strong demand
</li><li>Steady demand
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Metro lockers: $0.5$ thousand USD
</li><li>Suburban lockers: $0.4$ thousand USD
</li><li>Mixed network: $0.5$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Strong demand: $0.2$ thousand USD
</li><li>Steady demand: $0.1$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Metro lockers: $10$ thousand USD
</li><li>Suburban lockers: $14$ thousand USD
</li><li>Mixed network: $12$ thousand USD
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Metro lockers: 80 under Strong demand, 55 under Steady demand
</li><li>Suburban lockers: 65 under Strong demand, 60 under Steady demand
</li><li>Mixed network: 75 under Strong demand, 65 under Steady demand
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A parcel operator must choose a metro-locker system, a suburban-locker system, or a mixed network. Lease proposals provide 10 thousand USD of contract income for the metro system, 14 thousand USD for the suburban system, and 12 thousand USD for the mixed network. After operating costs, metro and mixed lockers each earn 0.5 thousand USD per shipment batch, while suburban lockers earn 0.4 thousand USD. Strong demand adds 0.2 thousand USD to the earnings from every batch, and steady demand adds 0.1 thousand USD. The estimates come from lease terms, recent parcel volumes, and operating budgets.</p>
<p>Volume forecasts show metro lockers handling 80 batches under strong demand and 55 under steady demand, while suburban lockers handle 65 and 60 batches, respectively.</p>
<p>The mixed network is expected to handle 75 batches under strong demand and 65 under steady demand. The metro network has the highest modeled volume under strong demand, while the mixed network handles the most batches under steady demand.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Metro lockers; Suburban lockers; Mixed network</td></tr><tr><th scope="row">States of nature</th><td>Strong demand; Steady demand</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_i^A.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Steady demand</th></tr></thead>
<tbody>
<tr><th scope="row">Metro lockers</th><td>$80\times(0.5+0.2)+10=66$</td><td>$55\times(0.5+0.1)+10=43$</td></tr>
<tr><th scope="row">Suburban lockers</th><td>$65\times(0.4+0.2)+14=53$</td><td>$60\times(0.4+0.1)+14=44$</td></tr>
<tr><th scope="row">Mixed network</th><td>$75\times(0.5+0.2)+12=64.5$</td><td>$65\times(0.5+0.1)+12=51$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Steady demand</th></tr></thead>
<tbody>
<tr><th scope="row">Metro lockers</th><td>66</td><td>43</td></tr>
<tr><th scope="row">Suburban lockers</th><td>53</td><td>44</td></tr>
<tr><th scope="row">Mixed network</th><td>64.5</td><td>51</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-28",
        layer1: "3 components",
        layer2: ["AV","SV","SF"],
        labels: {
          name: "District Heating Supply (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A district energy provider selects a heat source for units supplied during the winter.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Biomass heat
</li><li>Heat pumps
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Mild winter
</li><li>Cold winter
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Biomass heat: $0.5$ thousand USD
</li><li>Heat pumps: $0.6$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Mild winter: $0.1$ thousand USD
</li><li>Cold winter: $0.3$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Mild winter: $6$ thousand USD
</li><li>Cold winter: $-4$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Biomass heat: 55 under Mild winter, 85 under Cold winter
</li><li>Heat pumps: 65 under Mild winter, 95 under Cold winter
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A district energy provider must choose between biomass heat and heat pumps. Energy-price contracts and operating budgets show earnings of 0.5 thousand USD for each biomass heating unit and 0.6 thousand USD for each heat-pump unit. Winter tariffs add 0.1 thousand USD for every unit in a mild winter and 0.3 thousand USD in a cold winter. A mild-winter service subsidy contributes another 6 thousand USD, while cold-weather emergency expenses reduce profit by 4 thousand USD. Demand forecasts supply the expected volumes.</p>
<p>Biomass heat contributes 0.5 thousand USD per unit and is expected to supply 55 units during a mild winter and 85 during a cold winter. Heat pumps contribute 0.6 thousand USD per unit, with projected volumes of 65 and 95 units under the same respective states.</p>
<p>Heat pumps provide the higher payoff per unit and the larger modeled supply in both winter conditions.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Biomass heat; Heat pumps</td></tr><tr><th scope="row">States of nature</th><td>Mild winter; Cold winter</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Mild winter</th><th scope="col">Cold winter</th></tr></thead>
<tbody>
<tr><th scope="row">Biomass heat</th><td>$55\times(0.5+0.1)+6=39$</td><td>$85\times(0.5+0.3)-4=64$</td></tr>
<tr><th scope="row">Heat pumps</th><td>$65\times(0.6+0.1)+6=51.5$</td><td>$95\times(0.6+0.3)-4=81.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Mild winter</th><th scope="col">Cold winter</th></tr></thead>
<tbody>
<tr><th scope="row">Biomass heat</th><td>39</td><td>64</td></tr>
<tr><th scope="row">Heat pumps</th><td>51.5</td><td>81.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-29",
        layer1: "3 components",
        layer2: ["AV","SV","SF"],
        labels: {
          name: "Port Cold-Chain Service (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus State-Based Variable Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A port authority chooses a cold-chain service model for container batches under three operating states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Automated service
</li><li>Crew service
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Clear flow
</li><li>Congestion
</li><li>Inspection surge
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Automated service: $0.7$ thousand USD
</li><li>Crew service: $0.5$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Clear flow: $0.2$ thousand USD
</li><li>Congestion: $0.1$ thousand USD
</li><li>Inspection surge: $0.3$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Clear flow: $8$ thousand USD
</li><li>Congestion: $-3$ thousand USD (negative adjustment)
</li><li>Inspection surge: $5$ thousand USD
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Automated service: 80 under Clear flow, 60 under Congestion, 45 under Inspection surge
</li><li>Crew service: 70 under Clear flow, 65 under Congestion, 55 under Inspection surge
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A port authority must choose between automated and crew-operated cold-chain service. Cost studies show that automation earns 0.7 thousand USD per refrigerated container batch and crew service earns 0.5 thousand USD. Clear flow adds 0.2 thousand USD to the earnings from each batch and provides 8 thousand USD of scheduling savings. Congestion adds 0.1 thousand USD per batch but creates 3 thousand USD of extra coordination costs. An inspection surge adds 0.3 thousand USD per batch and provides 5 thousand USD of inspection-service income. Volume estimates come from earlier congestion and inspection records.</p>
<p>The automated service contributes 0.7 thousand USD per batch and is expected to handle 80 batches under clear flow, 60 under congestion, and 45 during an inspection surge. The crew service contributes 0.5 thousand USD per batch, with projected volumes of 70, 65, and 55 batches under the same respective states.</p>
<p>Automation handles more batches under clear flow, while the crew service maintains higher volumes under congestion and inspection surges.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Automated service; Crew service</td></tr><tr><th scope="row">States of nature</th><td>Clear flow; Congestion; Inspection surge</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Clear flow</th><th scope="col">Congestion</th><th scope="col">Inspection surge</th></tr></thead>
<tbody>
<tr><th scope="row">Automated service</th><td>$80\times(0.7+0.2)+8=80$</td><td>$60\times(0.7+0.1)-3=45$</td><td>$45\times(0.7+0.3)+5=50$</td></tr>
<tr><th scope="row">Crew service</th><td>$70\times(0.5+0.2)+8=57$</td><td>$65\times(0.5+0.1)-3=36$</td><td>$55\times(0.5+0.3)+5=49$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Clear flow</th><th scope="col">Congestion</th><th scope="col">Inspection surge</th></tr></thead>
<tbody>
<tr><th scope="row">Automated service</th><td>80</td><td>45</td><td>50</td></tr>
<tr><th scope="row">Crew service</th><td>57</td><td>36</td><td>49</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-30",
        layer1: "3 components",
        layer2: ["AV","AF","SF"],
        labels: {
          name: "Pharmacy Delivery Plan (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A pharmacy cooperative chooses a delivery plan for prescription batches served across two traffic states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Cargo bikes
</li><li>Electric vans
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Light traffic
</li><li>Heavy traffic
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Cargo bikes: $0.6$ thousand USD
</li><li>Electric vans: $0.8$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Cargo bikes: $9$ thousand USD
</li><li>Electric vans: $4$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Light traffic: $6$ thousand USD
</li><li>Heavy traffic: $-5$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Cargo bikes: 60 under Light traffic, 45 under Heavy traffic
</li><li>Electric vans: 75 under Light traffic, 55 under Heavy traffic
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A pharmacy cooperative must choose cargo bikes or electric vans for prescription deliveries. The bike contract provides 9 thousand USD of route income and earns 0.6 thousand USD for each batch delivered. The van contract provides 4 thousand USD of route income and earns 0.8 thousand USD per batch. Recent traffic records also indicate 6 thousand USD of scheduling savings in light traffic, while delays in heavy traffic impose 5 thousand USD of extra costs on either plan.</p>
<p>Capacity forecasts estimate that cargo bikes will deliver 60 batches in light traffic and 45 in heavy traffic. Electric vans are expected to deliver 75 and 55 batches, respectively.</p>
<p>The estimates come from vehicle costs, route contracts, delivery capacity, and recent traffic patterns. Vans earn more per batch and carry more batches, whereas bikes receive more route income.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Cargo bikes; Electric vans</td></tr><tr><th scope="row">States of nature</th><td>Light traffic; Heavy traffic</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}v_i^A+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Light traffic</th><th scope="col">Heavy traffic</th></tr></thead>
<tbody>
<tr><th scope="row">Cargo bikes</th><td>$60\times 0.6+9+6=51$</td><td>$45\times 0.6+9-5=31$</td></tr>
<tr><th scope="row">Electric vans</th><td>$75\times 0.8+4+6=70$</td><td>$55\times 0.8+4-5=43$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Light traffic</th><th scope="col">Heavy traffic</th></tr></thead>
<tbody>
<tr><th scope="row">Cargo bikes</th><td>51</td><td>31</td></tr>
<tr><th scope="row">Electric vans</th><td>70</td><td>43</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-31",
        layer1: "3 components",
        layer2: ["AV","AF","SF"],
        labels: {
          name: "Timber Processing Line (C1--C2)",
          section: "Alternative-Based Variable Payoff Plus Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A wood cooperative selects a processing line for lumber batches sold under three market conditions.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Precision line
</li><li>Standard line
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Firm market
</li><li>Normal market
</li><li>Weak market
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Precision line: $0.9$ thousand USD
</li><li>Standard line: $0.6$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Precision line: $7$ thousand USD
</li><li>Standard line: $13$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Firm market: $10$ thousand USD
</li><li>Normal market: $2$ thousand USD
</li><li>Weak market: $-6$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Precision line: 70 under Firm market, 55 under Normal market, 40 under Weak market
</li><li>Standard line: 85 under Firm market, 65 under Normal market, 50 under Weak market
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A wood cooperative must choose a precision or standard lumber-processing line. The precision line’s sales agreement provides 7 thousand USD of income and earnings of 0.9 thousand USD per batch. The standard line’s agreement provides 13 thousand USD and earnings of 0.6 thousand USD per batch. Market contracts add 10 thousand USD when the market is firm and 2 thousand USD when it is normal, while weak-market storage costs reduce profit by 6 thousand USD.</p>
<p>Production records and demand forecasts indicate that the precision line will process 70 batches in a firm market, 55 in a normal market, and 40 in a weak market. The standard line is expected to process 85, 65, and 50 batches under those respective conditions.</p>
<p>The precision line earns more per batch, while the standard line receives more contract income and processes more batches in every market condition.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Precision line; Standard line</td></tr><tr><th scope="row">States of nature</th><td>Firm market; Normal market; Weak market</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}v_i^A+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Firm market</th><th scope="col">Normal market</th><th scope="col">Weak market</th></tr></thead>
<tbody>
<tr><th scope="row">Precision line</th><td>$70\times 0.9+7+10=80$</td><td>$55\times 0.9+7+2=58.5$</td><td>$40\times 0.9+7-6=37$</td></tr>
<tr><th scope="row">Standard line</th><td>$85\times 0.6+13+10=74$</td><td>$65\times 0.6+13+2=54$</td><td>$50\times 0.6+13-6=37$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Firm market</th><th scope="col">Normal market</th><th scope="col">Weak market</th></tr></thead>
<tbody>
<tr><th scope="row">Precision line</th><td>80</td><td>58.5</td><td>37</td></tr>
<tr><th scope="row">Standard line</th><td>74</td><td>54</td><td>37</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-32",
        layer1: "3 components",
        layer2: ["SV","AF","SF"],
        labels: {
          name: "Public Library Outreach (C1--C2)",
          section: "State-Based Variable Payoff Plus Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A library system selects an outreach format for participant groups served under two attendance states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Mobile library
</li><li>Pop-up branches
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>High attendance
</li><li>Low attendance
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>High attendance: $0.7$ thousand USD
</li><li>Low attendance: $0.4$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Mobile library: $8$ thousand USD
</li><li>Pop-up branches: $11$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>High attendance: $5$ thousand USD
</li><li>Low attendance: $-2$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Mobile library: 50 under High attendance, 30 under Low attendance
</li><li>Pop-up branches: 45 under High attendance, 35 under Low attendance
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A library system must choose a mobile library or pop-up branches. The program budget provides 8 thousand USD for the mobile library and 11 thousand USD for pop-up branches. When attendance is high, funding provides 0.7 thousand USD for each group served and a further 5 thousand USD for the program. When attendance is low, it provides 0.4 thousand USD per group, while unrecovered venue and publicity costs reduce the result by 2 thousand USD. The estimates come from earlier participation, operating costs, and the funding schedule.</p>
<p>Attendance forecasts show the mobile library serving 50 groups under high attendance and 30 under low attendance. Pop-up branches are expected to serve 45 and 35 groups, respectively.</p>
<p>The mobile library serves more groups under high attendance, while pop-up branches serve more under low attendance and receive the larger initial program allocation.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Mobile library; Pop-up branches</td></tr><tr><th scope="row">States of nature</th><td>High attendance; Low attendance</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}v_j^S+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High attendance</th><th scope="col">Low attendance</th></tr></thead>
<tbody>
<tr><th scope="row">Mobile library</th><td>$50\times 0.7+8+5=48$</td><td>$30\times 0.4+8-2=18$</td></tr>
<tr><th scope="row">Pop-up branches</th><td>$45\times 0.7+11+5=47.5$</td><td>$35\times 0.4+11-2=23$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">High attendance</th><th scope="col">Low attendance</th></tr></thead>
<tbody>
<tr><th scope="row">Mobile library</th><td>48</td><td>18</td></tr>
<tr><th scope="row">Pop-up branches</th><td>47.5</td><td>23</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-33",
        layer1: "3 components",
        layer2: ["SV","AF","SF"],
        labels: {
          name: "Grain Terminal Schedule (C1--C2)",
          section: "State-Based Variable Payoff Plus Alternative-Based Fixed Payoff Plus State-Based Fixed Payoff"
        },
        descriptionHtml: String.raw`
<p>A grain terminal selects a loading schedule for cargo lots handled under two export states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Day schedule
</li><li>Night schedule
</li><li>Split schedule
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Open channels
</li><li>Restricted channels
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Open channels: $0.6$ thousand USD
</li><li>Restricted channels: $0.3$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Day schedule: $12$ thousand USD
</li><li>Night schedule: $8$ thousand USD
</li><li>Split schedule: $10$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Open channels: $7$ thousand USD
</li><li>Restricted channels: $-3$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Day schedule: 90 under Open channels, 55 under Restricted channels
</li><li>Night schedule: 75 under Open channels, 60 under Restricted channels
</li><li>Split schedule: 85 under Open channels, 65 under Restricted channels
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A grain terminal must choose a day, night, or split loading schedule. Labor contracts provide 12 thousand USD of operating income for the day schedule, 8 thousand USD for the night schedule, and 10 thousand USD for the split schedule. Open export channels earn 0.6 thousand USD per cargo lot and provide 7 thousand USD of priority-access income. Restricted channels earn 0.3 thousand USD per lot and impose 3 thousand USD of rescheduling costs. The estimates come from prior volumes, labor costs, and forecasts of export restrictions.</p>
<p>The day schedule is expected to handle 90 lots with open channels and 55 with restricted channels. The night schedule is expected to handle 75 and 60 lots, respectively, and the split schedule 85 and 65 lots, respectively.</p>
<p>The day schedule handles the most lots when channels are open, while the split schedule handles the most under restricted conditions.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Day schedule; Night schedule; Split schedule</td></tr><tr><th scope="row">States of nature</th><td>Open channels; Restricted channels</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}v_j^S+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Open channels</th><th scope="col">Restricted channels</th></tr></thead>
<tbody>
<tr><th scope="row">Day schedule</th><td>$90\times 0.6+12+7=73$</td><td>$55\times 0.3+12-3=25.5$</td></tr>
<tr><th scope="row">Night schedule</th><td>$75\times 0.6+8+7=60$</td><td>$60\times 0.3+8-3=23$</td></tr>
<tr><th scope="row">Split schedule</th><td>$85\times 0.6+10+7=68$</td><td>$65\times 0.3+10-3=26.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Open channels</th><th scope="col">Restricted channels</th></tr></thead>
<tbody>
<tr><th scope="row">Day schedule</th><td>73</td><td>25.5</td></tr>
<tr><th scope="row">Night schedule</th><td>60</td><td>23</td></tr>
<tr><th scope="row">Split schedule</th><td>68</td><td>26.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-34",
        layer1: "4 components",
        layer2: ["AV","SV","AF","SF"],
        labels: {
          name: "Urban Food Hub (C1--C2)",
          section: "Alternative-Based and State-Based Variable Payoffs Plus Alternative-Based and State-Based Fixed Payoffs"
        },
        descriptionHtml: String.raw`
<p>A city food hub chooses a distribution system for produce crates delivered under two demand states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Electric sorting
</li><li>Manual sorting
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Strong demand
</li><li>Soft demand
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Electric sorting: $0.6$ thousand USD
</li><li>Manual sorting: $0.4$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Strong demand: $0.2$ thousand USD
</li><li>Soft demand: $0.1$ thousand USD
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Electric sorting: $9$ thousand USD
</li><li>Manual sorting: $14$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Strong demand: $6$ thousand USD
</li><li>Soft demand: $-3$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Electric sorting: 70 under Strong demand, 45 under Soft demand
</li><li>Manual sorting: 80 under Strong demand, 55 under Soft demand
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A city food hub must choose electric or manual sorting for produce crates. The electric system’s service contract provides 9 thousand USD of income and earnings of 0.6 thousand USD per crate. Manual sorting receives 14 thousand USD under its contract and earns 0.4 thousand USD per crate. Strong demand adds 0.2 thousand USD to the earnings from each crate and brings 6 thousand USD of distributor incentives. Soft demand adds 0.1 thousand USD per crate, while unused-capacity costs reduce profit by 3 thousand USD. These estimates come from distribution forecasts, labor costs, equipment expenses, and recent demand.</p>
<p>The hub expects electric sorting to process 70 crates under strong demand and 45 under soft demand. Manual sorting is expected to process 80 and 55 crates, respectively.</p>
<p>Electric sorting earns more per crate before demand-related income, while manual sorting receives more contract income and processes more crates under both demand conditions.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Electric sorting; Manual sorting</td></tr><tr><th scope="row">States of nature</th><td>Strong demand; Soft demand</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Soft demand</th></tr></thead>
<tbody>
<tr><th scope="row">Electric sorting</th><td>$70\times(0.6+0.2)+9+6=71$</td><td>$45\times(0.6+0.1)+9-3=37.5$</td></tr>
<tr><th scope="row">Manual sorting</th><td>$80\times(0.4+0.2)+14+6=68$</td><td>$55\times(0.4+0.1)+14-3=38.5$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Soft demand</th></tr></thead>
<tbody>
<tr><th scope="row">Electric sorting</th><td>71</td><td>37.5</td></tr>
<tr><th scope="row">Manual sorting</th><td>68</td><td>38.5</td></tr>
</tbody></table></div>
            `
          }
        ]
      },
      {
        id: "problem-35",
        layer1: "4 components",
        layer2: ["AV","SV","AF","SF"],
        labels: {
          name: "Regional Rail Cargo (C1--C2)",
          section: "Alternative-Based and State-Based Variable Payoffs Plus Alternative-Based and State-Based Fixed Payoffs"
        },
        descriptionHtml: String.raw`
<p>A rail operator selects a cargo service design for freight lots moved under three network states.</p>
<p><strong>Decision alternatives</strong></p>
<ol>
<li>Express service
</li><li>Flexible service
</li></ol>
<p><strong>States of nature</strong></p>
<ol>
<li>Clear network
</li><li>Busy network
</li><li>Disrupted network
</li></ol>
<p><strong>Alternative-based variable payoff per item $v_i^A$</strong></p>
<ol>
<li>Express service: $0.8$ thousand USD
</li><li>Flexible service: $0.6$ thousand USD
</li></ol>
<p><strong>State-based variable payoff per item $v_j^S$</strong></p>
<ol>
<li>Clear network: $0.2$ thousand USD
</li><li>Busy network: $0.1$ thousand USD
</li><li>Disrupted network: $-0.1$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Alternative-based fixed payoff $f_i^A$</strong></p>
<ol>
<li>Express service: $10$ thousand USD
</li><li>Flexible service: $15$ thousand USD
</li></ol>
<p><strong>State-based fixed payoff $f_j^S$</strong></p>
<ol>
<li>Clear network: $5$ thousand USD
</li><li>Busy network: $0$ thousand USD
</li><li>Disrupted network: $-7$ thousand USD (negative adjustment)
</li></ol>
<p><strong>Modeled number of items $q_{ij}$</strong></p>
<ol>
<li>Express service: 85 under Clear network, 65 under Busy network, 40 under Disrupted network
</li><li>Flexible service: 75 under Clear network, 70 under Busy network, 50 under Disrupted network
</li></ol>
<h4>Questions/Tasks</h4>
<ol>
<li><strong>(C1)</strong> Interpreting decision alternatives, events, consequences, and states.
</li><li><strong>(C2)</strong> Building the payoff table.
</li></ol>
        `,
        narrativeDescriptionHtml: String.raw`
<p>A rail operator must choose an express or flexible service for moving freight lots. The express contract provides 10 thousand USD of service income and earnings of 0.8 thousand USD per lot. The flexible contract provides 15 thousand USD and earnings of 0.6 thousand USD per lot. Clear conditions add 0.2 thousand USD to the earnings from each lot and produce 5 thousand USD of on-time-delivery bonuses. Busy conditions add 0.1 thousand USD per lot and bring no additional bonus or cost. Disruptions reduce earnings by 0.1 thousand USD for every lot and impose a further 7 thousand USD of rerouting costs. The estimates come from past volumes, operating costs, and network simulations.</p>
<p>Volume forecasts show the express service moving 85 lots under clear conditions, 65 under busy conditions, and 40 under disrupted conditions. The flexible service is expected to move 75, 70, and 50 lots under those respective conditions.</p>
<p>Express service earns more for each lot before network-related income or costs, while flexible service maintains higher forecast volumes under busy and disrupted conditions.</p>
        `,
        solutionSections: [
          {
            title: "C1: Interpreting decision alternatives, events, consequences, and states",
            contentHtml: String.raw`
<div class="table-card"><table class="data-table"><caption>Decision elements</caption><tbody><tr><th scope="row">Alternatives</th><td>Express service; Flexible service</td></tr><tr><th scope="row">States of nature</th><td>Clear network; Busy network; Disrupted network</td></tr><tr><th scope="row">Uncertain event</th><td>The realized state affecting the transaction</td></tr><tr><th scope="row">Consequences/payoffs</th><td>Payoff in thousand USD for each alternative--state pair</td></tr></tbody></table></div>
            `
          },
          {
            title: "C2: Building the payoff table",
            contentHtml: String.raw`
<p>The applicable payoff formula is</p>
$$
P_{ij}=q_{ij}\left(v_i^A+v_j^S\right)+f_i^A+f_j^S.
$$
<p>Detailed calculations (thousand USD):</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Clear network</th><th scope="col">Busy network</th><th scope="col">Disrupted network</th></tr></thead>
<tbody>
<tr><th scope="row">Express service</th><td>$85\times(0.8+0.2)+10+5=100$</td><td>$65\times(0.8+0.1)+10+0=68.5$</td><td>$40\times(0.8-0.1)+10-7=31$</td></tr>
<tr><th scope="row">Flexible service</th><td>$75\times(0.6+0.2)+15+5=80$</td><td>$70\times(0.6+0.1)+15+0=64$</td><td>$50\times(0.6-0.1)+15-7=33$</td></tr>
</tbody></table></div>
<p>The simplified payoff table is</p>
<div class="table-card"><table class="data-table" aria-label="Problem data or payoff calculations">
<thead><tr><th scope="col">Alternative</th><th scope="col">Clear network</th><th scope="col">Busy network</th><th scope="col">Disrupted network</th></tr></thead>
<tbody>
<tr><th scope="row">Express service</th><td>100</td><td>68.5</td><td>31</td></tr>
<tr><th scope="row">Flexible service</th><td>80</td><td>64</td><td>33</td></tr>
</tbody></table></div>
            `
          }
        ]
      }
    ]
  };

  window.practiceData = practiceData;
})();
