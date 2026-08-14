(() => {
  "use strict";

  const practiceData = {
    selectors: [
      { key: "section", label: "Section", type: "filter", multiple: true }
    ],
    problems: [
      {
        id: "problem-1",
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
