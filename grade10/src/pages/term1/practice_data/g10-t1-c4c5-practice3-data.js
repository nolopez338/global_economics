(() => {
  "use strict";

  const practiceData = {
    selectors: [
      { key: "problemType", label: "Problem type", type: "filter", multiple: true, options: ["General", "Applied"] },
      { key: "stateCount", label: "Number of states", type: "filter", multiple: true, options: ["2", "3", "4"] },
      { key: "alternativeCount", label: "Number of alternatives", type: "filter", multiple: true, options: ["2", "3", "4"] }
    ],
    problems: [
      {
        id: "general-problem-2x2",
        problemType: "General",
        stateCount: "2",
        alternativeCount: "2",
        labels: { name: "General 2 × 2 Problem", section: "Introduction" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A decision maker must choose between two alternatives, $A_1$ and $A_2$. Two states of nature, $S_1$ and $S_2$, may occur. The payoff associated with each alternative–state combination is represented by $P(A_i,S_j)$, where $i$ identifies the alternative and $j$ identifies the state of nature.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th></tr></thead><tbody><tr><th scope="row">Alternative $A_1$</th><td>$P(A_1,S_1)$</td><td>$P(A_1,S_2)$</td></tr><tr><th scope="row">Alternative $A_2$</th><td>$P(A_2,S_1)$</td><td>$P(A_2,S_2)$</td></tr></tbody></table></div>
<p>Use Maximax, Maximin, and Minimax Regret to determine the decision rules for this general payoff table. <strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`<p><strong>Step 1: Find the largest payoff for each alternative.</strong> For $A_1$, compare its payoffs under $S_1$ and $S_2$:</p>
$$
M_1=\max\{P(A_1,S_1),P(A_1,S_2)\}.
$$
<p>For $A_2$, compare its payoffs under $S_1$ and $S_2$:</p>
$$
M_2=\max\{P(A_2,S_1),P(A_2,S_2)\}.
$$
<p>Therefore,</p>
$$
\begin{aligned}
		M_1&=\max\{P(A_1,S_1),P(A_1,S_2)\},\\
		M_2&=\max\{P(A_2,S_1),P(A_2,S_2)\}.
	\end{aligned}
$$
<p><strong>Step 2: Apply the Maximax criterion.</strong> Compare the largest payoffs $M_1$ and $M_2$:</p>
$$
M^*=\max\{M_1,M_2\}.
$$
<p>Equivalently,</p>
$$
M^*
	=
	\max\left\{
	\max\{P(A_1,S_1),P(A_1,S_2)\},
	\max\{P(A_2,S_1),P(A_2,S_2)\}
	\right\}.
$$
<p>The Maximax decision is</p>
$$
A_{\text{Maximax}}
	=
	\operatorname*{arg\,max}_{i\in\{1,2\}}
	\left\{
	\max_{j\in\{1,2\}}P(A_i,S_j)
	\right\}.
$$
<p>Thus, choose $A_1$ if $M_1>M_2$, choose $A_2$ if $M_2>M_1$, and report a tie if $M_1=M_2$. <strong>Step 3: Find the smallest payoff for each alternative.</strong> For $A_1$,</p>
$$
m_1=\min\{P(A_1,S_1),P(A_1,S_2)\}.
$$
<p>For $A_2$,</p>
$$
m_2=\min\{P(A_2,S_1),P(A_2,S_2)\}.
$$
<p>Therefore,</p>
$$
\begin{aligned}
		m_1&=\min\{P(A_1,S_1),P(A_1,S_2)\},\\
		m_2&=\min\{P(A_2,S_1),P(A_2,S_2)\}.
	\end{aligned}
$$
<p><strong>Step 4: Apply the Maximin criterion.</strong> Compare the smallest payoffs $m_1$ and $m_2$:</p>
$$
m^*=\max\{m_1,m_2\}.
$$
<p>Equivalently,</p>
$$
m^*
	=
	\max\left\{
	\min\{P(A_1,S_1),P(A_1,S_2)\},
	\min\{P(A_2,S_1),P(A_2,S_2)\}
	\right\}.
$$
<p>The Maximin decision is</p>
$$
A_{\text{Maximin}}
	=
	\operatorname*{arg\,max}_{i\in\{1,2\}}
	\left\{
	\min_{j\in\{1,2\}}P(A_i,S_j)
	\right\}.
$$
<p>Thus, choose $A_1$ if $m_1>m_2$, choose $A_2$ if $m_2>m_1$, and report a tie if $m_1=m_2$.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p><strong>Step 1: Find the best payoff in each state of nature.</strong> Under $S_1$, compare the payoffs of $A_1$ and $A_2$:</p>
$$
b_1=\max\{P(A_1,S_1),P(A_2,S_1)\}.
$$
<p>Under $S_2$, compare the payoffs of $A_1$ and $A_2$:</p>
$$
b_2=\max\{P(A_1,S_2),P(A_2,S_2)\}.
$$
<p>Therefore,</p>
$$
\begin{aligned}
		b_1&=\max\{P(A_1,S_1),P(A_2,S_1)\},\\
		b_2&=\max\{P(A_1,S_2),P(A_2,S_2)\}.
	\end{aligned}
$$
<p><strong>Step 2: Calculate the regret for every alternative–state combination.</strong> The regret associated with alternative $A_i$ under state $S_j$ is</p>
$$
r_{ij}=b_j-P(A_i,S_j).
$$
<p>Consequently,</p>
$$
\begin{aligned}
		r_{11}&=b_1-P(A_1,S_1),&
		r_{12}&=b_2-P(A_1,S_2),\\
		r_{21}&=b_1-P(A_2,S_1),&
		r_{22}&=b_2-P(A_2,S_2).
	\end{aligned}
$$
<p>The general regret table is therefore</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th></tr></thead><tbody><tr><th scope="row">$A_1$</th><td>$b_1-P(A_1,S_1)$</td><td>$b_2-P(A_1,S_2)$</td></tr><tr><th scope="row">$A_2$</th><td>$b_1-P(A_2,S_1)$</td><td>$b_2-P(A_2,S_2)$</td></tr></tbody></table></div>
<p><strong>Step 3: Find the maximum regret for each alternative.</strong> For $A_1$,</p>
$$
R_1=
	\max\{
	b_1-P(A_1,S_1),
	b_2-P(A_1,S_2)
	\}.
$$
<p>For $A_2$,</p>
$$
R_2=
	\max\{
	b_1-P(A_2,S_1),
	b_2-P(A_2,S_2)
	\}.
$$
<p>Thus,</p>
$$
\begin{aligned}
		R_1&=\max\{r_{11},r_{12}\},\\
		R_2&=\max\{r_{21},r_{22}\}.
	\end{aligned}
$$
<p><strong>Step 4: Apply the Minimax Regret criterion.</strong> Compare the maximum regrets $R_1$ and $R_2$:</p>
$$
R^*=\min\{R_1,R_2\}.
$$
<p>The Minimax Regret decision is</p>
$$
A_{\text{Minimax Regret}}
	=
	\operatorname*{arg\,min}_{i\in\{1,2\}}
	\left\{
	\max_{j\in\{1,2\}}
	\left[b_j-P(A_i,S_j)\right]
	\right\}.
$$
<p>Thus, choose $A_1$ if $R_1<R_2$, choose $A_2$ if $R_2<R_1$, and report a tie if $R_1=R_2$. <strong>General decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">General decision rule</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>$
			\operatorname*{arg\,max}_{i\in\{1,2\}}
			\max_{j\in\{1,2\}}P(A_i,S_j)$</td></tr><tr><th scope="row">Maximin</th><td>$
			\operatorname*{arg\,max}_{i\in\{1,2\}}
			\min_{j\in\{1,2\}}P(A_i,S_j)$</td></tr><tr><th scope="row">Minimax Regret</th><td>$
			\operatorname*{arg\,min}_{i\in\{1,2\}}
			\max_{j\in\{1,2\}}
			\left[b_j-P(A_i,S_j)\right]$</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "general-problem-4x3",
        problemType: "General",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "General 4 × 3 Problem", section: "Introduction" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A decision maker must choose among three alternatives, $A_1$, $A_2$, and $A_3$. Four states of nature, $S_1$, $S_2$, $S_3$, and $S_4$, may occur. The payoff associated with each alternative–state combination is represented by $P(A_i,S_j)$.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Alternative $A_1$</th><td>$P(A_1,S_1)$</td><td>$P(A_1,S_2)$</td><td>$P(A_1,S_3)$</td><td>$P(A_1,S_4)$</td></tr><tr><th scope="row">Alternative $A_2$</th><td>$P(A_2,S_1)$</td><td>$P(A_2,S_2)$</td><td>$P(A_2,S_3)$</td><td>$P(A_2,S_4)$</td></tr><tr><th scope="row">Alternative $A_3$</th><td>$P(A_3,S_1)$</td><td>$P(A_3,S_2)$</td><td>$P(A_3,S_3)$</td><td>$P(A_3,S_4)$</td></tr></tbody></table></div>
<p>Use Maximax, Maximin, and Minimax Regret to determine the decision rules for this general payoff table. <strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`<p><strong>Step 1: Find the largest payoff for each alternative.</strong> For the three alternatives,</p>
$$
\begin{aligned}
		M_1&=\max\{
		P(A_1,S_1),P(A_1,S_2),P(A_1,S_3),P(A_1,S_4)
		\},\\
		M_2&=\max\{
		P(A_2,S_1),P(A_2,S_2),P(A_2,S_3),P(A_2,S_4)
		\},\\
		M_3&=\max\{
		P(A_3,S_1),P(A_3,S_2),P(A_3,S_3),P(A_3,S_4)
		\}.
	\end{aligned}
$$
<p><strong>Step 2: Apply the Maximax criterion.</strong> Compare the three largest payoffs:</p>
$$
M^*=\max\{M_1,M_2,M_3\}.
$$
<p>Equivalently,</p>
$$
\begin{aligned}
		M^*=\max\{&
		\max\{
		P(A_1,S_1),P(A_1,S_2),P(A_1,S_3),P(A_1,S_4)
		\},\\
		&
		\max\{
		P(A_2,S_1),P(A_2,S_2),P(A_2,S_3),P(A_2,S_4)
		\},\\
		&
		\max\{
		P(A_3,S_1),P(A_3,S_2),P(A_3,S_3),P(A_3,S_4)
		\}
		\}.
	\end{aligned}
$$
<p>The Maximax decision is</p>
$$
A_{\text{Maximax}}
	=
	\operatorname*{arg\,max}_{i\in\{1,2,3\}}
	\left\{
	\max_{j\in\{1,2,3,4\}}P(A_i,S_j)
	\right\}.
$$
<p>Choose the alternative whose value $M_i$ is the largest. If two or more alternatives have the same largest value, the Maximax criterion produces a tie. <strong>Step 3: Find the smallest payoff for each alternative.</strong> For the three alternatives,</p>
$$
\begin{aligned}
		m_1&=\min\{
		P(A_1,S_1),P(A_1,S_2),P(A_1,S_3),P(A_1,S_4)
		\},\\
		m_2&=\min\{
		P(A_2,S_1),P(A_2,S_2),P(A_2,S_3),P(A_2,S_4)
		\},\\
		m_3&=\min\{
		P(A_3,S_1),P(A_3,S_2),P(A_3,S_3),P(A_3,S_4)
		\}.
	\end{aligned}
$$
<p><strong>Step 4: Apply the Maximin criterion.</strong> Compare the three smallest payoffs:</p>
$$
m^*=\max\{m_1,m_2,m_3\}.
$$
<p>Equivalently,</p>
$$
\begin{aligned}
		m^*=\max\{&
		\min\{
		P(A_1,S_1),P(A_1,S_2),P(A_1,S_3),P(A_1,S_4)
		\},\\
		&
		\min\{
		P(A_2,S_1),P(A_2,S_2),P(A_2,S_3),P(A_2,S_4)
		\},\\
		&
		\min\{
		P(A_3,S_1),P(A_3,S_2),P(A_3,S_3),P(A_3,S_4)
		\}
		\}.
	\end{aligned}
$$
<p>The Maximin decision is</p>
$$
A_{\text{Maximin}}
	=
	\operatorname*{arg\,max}_{i\in\{1,2,3\}}
	\left\{
	\min_{j\in\{1,2,3,4\}}P(A_i,S_j)
	\right\}.
$$
<p>Choose the alternative whose value $m_i$ is the largest. If two or more alternatives have the same largest value, the Maximin criterion produces a tie.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p><strong>Step 1: Find the best payoff in each state of nature.</strong> For the four states,</p>
$$
\begin{aligned}
		b_1&=\max\{P(A_1,S_1),P(A_2,S_1),P(A_3,S_1)\},\\
		b_2&=\max\{P(A_1,S_2),P(A_2,S_2),P(A_3,S_2)\},\\
		b_3&=\max\{P(A_1,S_3),P(A_2,S_3),P(A_3,S_3)\},\\
		b_4&=\max\{P(A_1,S_4),P(A_2,S_4),P(A_3,S_4)\}.
	\end{aligned}
$$
<p><strong>Step 2: Calculate the regret for every alternative–state combination.</strong> For every alternative $A_i$ and state $S_j$, the regret is</p>
$$
r_{ij}=b_j-P(A_i,S_j).
$$
<p>The general regret table is therefore</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">$A_1$</th><td>$b_1-P(A_1,S_1)$</td><td>$b_2-P(A_1,S_2)$</td><td>$b_3-P(A_1,S_3)$</td><td>$b_4-P(A_1,S_4)$</td></tr><tr><th scope="row">$A_2$</th><td>$b_1-P(A_2,S_1)$</td><td>$b_2-P(A_2,S_2)$</td><td>$b_3-P(A_2,S_3)$</td><td>$b_4-P(A_2,S_4)$</td></tr><tr><th scope="row">$A_3$</th><td>$b_1-P(A_3,S_1)$</td><td>$b_2-P(A_3,S_2)$</td><td>$b_3-P(A_3,S_3)$</td><td>$b_4-P(A_3,S_4)$</td></tr></tbody></table></div>
<p><strong>Step 3: Find the maximum regret for each alternative.</strong> For $A_1$,</p>
$$
R_1
	=
	\max\{
	b_1-P(A_1,S_1),
	b_2-P(A_1,S_2),
	b_3-P(A_1,S_3),
	b_4-P(A_1,S_4)
	\}.
$$
<p>For $A_2$,</p>
$$
R_2
	=
	\max\{
	b_1-P(A_2,S_1),
	b_2-P(A_2,S_2),
	b_3-P(A_2,S_3),
	b_4-P(A_2,S_4)
	\}.
$$
<p>For $A_3$,</p>
$$
R_3
	=
	\max\{
	b_1-P(A_3,S_1),
	b_2-P(A_3,S_2),
	b_3-P(A_3,S_3),
	b_4-P(A_3,S_4)
	\}.
$$
<p>Equivalently,</p>
$$
\begin{aligned}
		R_1&=\max\{r_{11},r_{12},r_{13},r_{14}\},\\
		R_2&=\max\{r_{21},r_{22},r_{23},r_{24}\},\\
		R_3&=\max\{r_{31},r_{32},r_{33},r_{34}\}.
	\end{aligned}
$$
<p><strong>Step 4: Apply the Minimax Regret criterion.</strong> Compare the maximum regrets:</p>
$$
R^*=\min\{R_1,R_2,R_3\}.
$$
<p>The Minimax Regret decision is</p>
$$
A_{\text{Minimax Regret}}
	=
	\operatorname*{arg\,min}_{i\in\{1,2,3\}}
	\left\{
	\max_{j\in\{1,2,3,4\}}
	\left[b_j-P(A_i,S_j)\right]
	\right\}.
$$
<p>Choose the alternative whose value $R_i$ is the smallest. If two or more alternatives have the same smallest value, the Minimax Regret criterion produces a tie. <strong>General decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">General decision rule</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>$
			\operatorname*{arg\,max}_{i\in\{1,2,3\}}
			\max_{j\in\{1,2,3,4\}}P(A_i,S_j)$</td></tr><tr><th scope="row">Maximin</th><td>$
			\operatorname*{arg\,max}_{i\in\{1,2,3\}}
			\min_{j\in\{1,2,3,4\}}P(A_i,S_j)$</td></tr><tr><th scope="row">Minimax Regret</th><td>$
			\operatorname*{arg\,min}_{i\in\{1,2,3\}}
			\max_{j\in\{1,2,3,4\}}
			\left[b_j-P(A_i,S_j)\right]$</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "food-truck-location",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "2",
        labels: { name: "Food Truck Location", section: "Applied: 2 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A food truck operator must choose between Location A and Location B. Demand can be strong or weak. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a location.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Weak demand</th></tr></thead><tbody><tr><th scope="row">Location A</th><td>100</td><td>0</td></tr><tr><th scope="row">Location B</th><td>60</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Location A}) &= \max\{100,0\}=100,\\
		\max(\text{Location B}) &= \max\{60,50\}=60.
	\end{aligned}
$$
$$
\max\{\max(\text{Location A}),\max(\text{Location B})\}
	=\max\{100,60\}
	=100.
$$
<p>The Maximax choice is Location A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Location A}) &= \min\{100,0\}=0,\\
		\min(\text{Location B}) &= \min\{60,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Location A}),\min(\text{Location B})\}
	=\max\{0,50\}
	=50.
$$
<p>The Maximin choice is Location B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Strong demand: }&\max\{100,60\}=100,\\
		\text{Weak demand: }&\max\{0,50\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Weak demand</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Location A</th><td>$100-100=0$</td><td>$50-0=50$</td><td>50</td></tr><tr><th scope="row">Location B</th><td>$100-60=40$</td><td>$50-50=0$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Location B because it has the smallest maximum regret, $40$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Location A</td></tr><tr><th scope="row">Maximin</th><td>Location B</td></tr><tr><th scope="row">Minimax Regret</th><td>Location B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "promotional-campaign",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "2",
        labels: { name: "Promotional Campaign", section: "Applied: 2 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A business must choose between Campaign A and Campaign B. Customer response can be strong or weak. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a campaign.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong response</th><th scope="col">Weak response</th></tr></thead><tbody><tr><th scope="row">Campaign A</th><td>100</td><td>20</td></tr><tr><th scope="row">Campaign B</th><td>80</td><td>30</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Campaign A}) &= \max\{100,20\}=100,\\
		\max(\text{Campaign B}) &= \max\{80,30\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Campaign A}),\max(\text{Campaign B})\}
	=\max\{100,80\}
	=100.
$$
<p>The Maximax choice is Campaign A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Campaign A}) &= \min\{100,20\}=20,\\
		\min(\text{Campaign B}) &= \min\{80,30\}=30.
	\end{aligned}
$$
$$
\max\{\min(\text{Campaign A}),\min(\text{Campaign B})\}
	=\max\{20,30\}
	=30.
$$
<p>The Maximin choice is Campaign B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Strong response: }&\max\{100,80\}=100,\\
		\text{Weak response: }&\max\{20,30\}=30.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong response</th><th scope="col">Weak response</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Campaign A</th><td>$100-100=0$</td><td>$30-20=10$</td><td>10</td></tr><tr><th scope="row">Campaign B</th><td>$100-80=20$</td><td>$30-30=0$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Campaign A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Campaign A</td></tr><tr><th scope="row">Maximin</th><td>Campaign B</td></tr><tr><th scope="row">Minimax Regret</th><td>Campaign A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "equipment-lease",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "2",
        labels: { name: "Equipment Lease", section: "Applied: 2 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose between Lease A and Lease B. Market conditions can be favourable or unfavourable. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a lease.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable market</th><th scope="col">Unfavourable market</th></tr></thead><tbody><tr><th scope="row">Lease A</th><td>70</td><td>40</td></tr><tr><th scope="row">Lease B</th><td>60</td><td>30</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Lease A}) &= \max\{70,40\}=70,\\
		\max(\text{Lease B}) &= \max\{60,30\}=60.
	\end{aligned}
$$
$$
\max\{\max(\text{Lease A}),\max(\text{Lease B})\}
	=\max\{70,60\}
	=70.
$$
<p>The Maximax choice is Lease A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Lease A}) &= \min\{70,40\}=40,\\
		\min(\text{Lease B}) &= \min\{60,30\}=30.
	\end{aligned}
$$
$$
\max\{\min(\text{Lease A}),\min(\text{Lease B})\}
	=\max\{40,30\}
	=40.
$$
<p>The Maximin choice is Lease A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable market: }&\max\{70,60\}=70,\\
		\text{Unfavourable market: }&\max\{40,30\}=40.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Unfavourable</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Lease A</th><td>$70-70=0$</td><td>$40-40=0$</td><td>0</td></tr><tr><th scope="row">Lease B</th><td>$70-60=10$</td><td>$40-30=10$</td><td>10</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Lease A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Lease A</td></tr><tr><th scope="row">Maximin</th><td>Lease A</td></tr><tr><th scope="row">Minimax Regret</th><td>Lease A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "production-plan",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "3",
        labels: { name: "Production Plan", section: "Applied: 2 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A manufacturer must choose Production Plan A, Plan B, or Plan C. Demand can be strong or weak. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a plan.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Weak demand</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>100</td><td>0</td></tr><tr><th scope="row">Plan B</th><td>70</td><td>60</td></tr><tr><th scope="row">Plan C</th><td>80</td><td>20</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Plan A}) &= \max\{100,0\}=100,\\
		\max(\text{Plan B}) &= \max\{70,60\}=70,\\
		\max(\text{Plan C}) &= \max\{80,20\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Plan A}),\max(\text{Plan B}),\max(\text{Plan C})\}
	=\max\{100,70,80\}
	=100.
$$
<p>The Maximax choice is Plan A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Plan A}) &= \min\{100,0\}=0,\\
		\min(\text{Plan B}) &= \min\{70,60\}=60,\\
		\min(\text{Plan C}) &= \min\{80,20\}=20.
	\end{aligned}
$$
$$
\max\{\min(\text{Plan A}),\min(\text{Plan B}),\min(\text{Plan C})\}
	=\max\{0,60,20\}
	=60.
$$
<p>The Maximin choice is Plan B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Strong demand: }&\max\{100,70,80\}=100,\\
		\text{Weak demand: }&\max\{0,60,20\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong demand</th><th scope="col">Weak demand</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>$100-100=0$</td><td>$60-0=60$</td><td>60</td></tr><tr><th scope="row">Plan B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>30</td></tr><tr><th scope="row">Plan C</th><td>$100-80=20$</td><td>$60-20=40$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Plan B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Plan A</td></tr><tr><th scope="row">Maximin</th><td>Plan B</td></tr><tr><th scope="row">Minimax Regret</th><td>Plan B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "marketing-strategy",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "3",
        labels: { name: "Marketing Strategy", section: "Applied: 2 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must select Strategy A, Strategy B, or Strategy C for a new marketing campaign. Customer response can be strong or weak. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a strategy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong response</th><th scope="col">Weak response</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>100</td><td>40</td></tr><tr><th scope="row">Strategy B</th><td>80</td><td>50</td></tr><tr><th scope="row">Strategy C</th><td>70</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Strategy A}) &= \max\{100,40\}=100,\\
		\max(\text{Strategy B}) &= \max\{80,50\}=80,\\
		\max(\text{Strategy C}) &= \max\{70,45\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Strategy A}),\max(\text{Strategy B}),
	\max(\text{Strategy C})\}
	=\max\{100,80,70\}
	=100.
$$
<p>The Maximax choice is Strategy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Strategy A}) &= \min\{100,40\}=40,\\
		\min(\text{Strategy B}) &= \min\{80,50\}=50,\\
		\min(\text{Strategy C}) &= \min\{70,45\}=45.
	\end{aligned}
$$
$$
\max\{\min(\text{Strategy A}),\min(\text{Strategy B}),
	\min(\text{Strategy C})\}
	=\max\{40,50,45\}
	=50.
$$
<p>The Maximin choice is Strategy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Strong response: }&\max\{100,80,70\}=100,\\
		\text{Weak response: }&\max\{40,50,45\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Strong response</th><th scope="col">Weak response</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>$100-100=0$</td><td>$50-40=10$</td><td>10</td></tr><tr><th scope="row">Strategy B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>20</td></tr><tr><th scope="row">Strategy C</th><td>$100-70=30$</td><td>$50-45=5$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Strategy A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Strategy A</td></tr><tr><th scope="row">Maximin</th><td>Strategy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Strategy A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "event-venue",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "3",
        labels: { name: "Event Venue", section: "Applied: 2 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>An event organiser must select Venue A, Venue B, or Venue C. Attendance can be high or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a venue.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High attendance</th><th scope="col">Low attendance</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>100</td><td>0</td></tr><tr><th scope="row">Venue B</th><td>70</td><td>60</td></tr><tr><th scope="row">Venue C</th><td>80</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Venue A}) &= \max\{100,0\}=100,\\
		\max(\text{Venue B}) &= \max\{70,60\}=70,\\
		\max(\text{Venue C}) &= \max\{80,50\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Venue A}),\max(\text{Venue B}),\max(\text{Venue C})\}
	=\max\{100,70,80\}
	=100.
$$
<p>The Maximax choice is Venue A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Venue A}) &= \min\{100,0\}=0,\\
		\min(\text{Venue B}) &= \min\{70,60\}=60,\\
		\min(\text{Venue C}) &= \min\{80,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Venue A}),\min(\text{Venue B}),\min(\text{Venue C})\}
	=\max\{0,60,50\}
	=60.
$$
<p>The Maximin choice is Venue B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High attendance: }&\max\{100,70,80\}=100,\\
		\text{Low attendance: }&\max\{0,60,50\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High attendance</th><th scope="col">Low attendance</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>$100-100=0$</td><td>$60-0=60$</td><td>60</td></tr><tr><th scope="row">Venue B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>30</td></tr><tr><th scope="row">Venue C</th><td>$100-80=20$</td><td>$60-50=10$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Venue C because it has the smallest maximum regret, $20$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Venue A</td></tr><tr><th scope="row">Maximin</th><td>Venue B</td></tr><tr><th scope="row">Minimax Regret</th><td>Venue C</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "distribution-plan",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "3",
        labels: { name: "Distribution Plan", section: "Applied: 2 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must select Distribution Plan A, Plan B, or Plan C. Market conditions can be favourable or unfavourable. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a distribution plan.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable market</th><th scope="col">Unfavourable market</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>90</td><td>60</td></tr><tr><th scope="row">Plan B</th><td>80</td><td>40</td></tr><tr><th scope="row">Plan C</th><td>70</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Plan A}) &= \max\{90,60\}=90,\\
		\max(\text{Plan B}) &= \max\{80,40\}=80,\\
		\max(\text{Plan C}) &= \max\{70,50\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Plan A}),\max(\text{Plan B}),\max(\text{Plan C})\}
	=\max\{90,80,70\}
	=90.
$$
<p>The Maximax choice is Plan A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Plan A}) &= \min\{90,60\}=60,\\
		\min(\text{Plan B}) &= \min\{80,40\}=40,\\
		\min(\text{Plan C}) &= \min\{70,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Plan A}),\min(\text{Plan B}),\min(\text{Plan C})\}
	=\max\{60,40,50\}
	=60.
$$
<p>The Maximin choice is Plan A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable market: }&\max\{90,80,70\}=90,\\
		\text{Unfavourable market: }&\max\{60,40,50\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Unfavourable</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>$90-90=0$</td><td>$60-60=0$</td><td>0</td></tr><tr><th scope="row">Plan B</th><td>$90-80=10$</td><td>$60-40=20$</td><td>20</td></tr><tr><th scope="row">Plan C</th><td>$90-70=20$</td><td>$60-50=10$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Plan A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Plan A</td></tr><tr><th scope="row">Maximin</th><td>Plan A</td></tr><tr><th scope="row">Minimax Regret</th><td>Plan A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "routing-system",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "2",
        labels: { name: "Routing System", section: "Applied: 3 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A shipping company must choose between System A and System B. Three states of nature represent different operating conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a routing system.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">System A</th><td>100</td><td>50</td><td>50</td></tr><tr><th scope="row">System B</th><td>70</td><td>49</td><td>90</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{System A}) &= \max\{100,50,50\}=100,\\
		\max(\text{System B}) &= \max\{70,49,90\}=90.
	\end{aligned}
$$
$$
\max\{\max(\text{System A}),\max(\text{System B})\}
	=\max\{100,90\}
	=100.
$$
<p>The Maximax choice is System A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{System A}) &= \min\{100,50,50\}=50,\\
		\min(\text{System B}) &= \min\{70,49,90\}=49.
	\end{aligned}
$$
$$
\max\{\min(\text{System A}),\min(\text{System B})\}
	=\max\{50,49\}
	=50.
$$
<p>The Maximin choice is System A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70\}=100,\\
		\text{State }S_2:\;&\max\{50,49\}=50,\\
		\text{State }S_3:\;&\max\{50,90\}=90.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">System A</th><td>$100-100=0$</td><td>$50-50=0$</td><td>$90-50=40$</td><td>40</td></tr><tr><th scope="row">System B</th><td>$100-70=30$</td><td>$50-49=1$</td><td>$90-90=0$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is System B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>System A</td></tr><tr><th scope="row">Maximin</th><td>System A</td></tr><tr><th scope="row">Minimax Regret</th><td>System B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "service-model-3x2",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "2",
        labels: { name: "Service Model", section: "Applied: 3 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A service company must choose between Service Model A and Service Model B. Demand can be high, moderate, or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a service model.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Moderate demand</th><th scope="col">Low demand</th></tr></thead><tbody><tr><th scope="row">Model A</th><td>100</td><td>45</td><td>40</td></tr><tr><th scope="row">Model B</th><td>80</td><td>50</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Model A}) &= \max\{100,45,40\}=100,\\
		\max(\text{Model B}) &= \max\{80,50,50\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Model A}),\max(\text{Model B})\}
	=\max\{100,80\}
	=100.
$$
<p>The Maximax choice is Model A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Model A}) &= \min\{100,45,40\}=40,\\
		\min(\text{Model B}) &= \min\{80,50,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Model A}),\min(\text{Model B})\}
	=\max\{40,50\}
	=50.
$$
<p>The Maximin choice is Model B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High demand: }&\max\{100,80\}=100,\\
		\text{Moderate demand: }&\max\{45,50\}=50,\\
		\text{Low demand: }&\max\{40,50\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High</th><th scope="col">Moderate</th><th scope="col">Low</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Model A</th><td>$100-100=0$</td><td>$50-45=5$</td><td>$50-40=10$</td><td>10</td></tr><tr><th scope="row">Model B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>$50-50=0$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Model A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Model A</td></tr><tr><th scope="row">Maximin</th><td>Model B</td></tr><tr><th scope="row">Minimax Regret</th><td>Model A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "inventory-policy-3x2",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "2",
        labels: { name: "Inventory Policy", section: "Applied: 3 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must choose between Inventory Policy A and Inventory Policy B. Demand can be high, moderate, or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an inventory policy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Moderate demand</th><th scope="col">Low demand</th></tr></thead><tbody><tr><th scope="row">Policy A</th><td>100</td><td>20</td><td>0</td></tr><tr><th scope="row">Policy B</th><td>70</td><td>60</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Policy A}) &= \max\{100,20,0\}=100,\\
		\max(\text{Policy B}) &= \max\{70,60,50\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Policy A}),\max(\text{Policy B})\}
	=\max\{100,70\}
	=100.
$$
<p>The Maximax choice is Policy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Policy A}) &= \min\{100,20,0\}=0,\\
		\min(\text{Policy B}) &= \min\{70,60,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Policy A}),\min(\text{Policy B})\}
	=\max\{0,50\}
	=50.
$$
<p>The Maximin choice is Policy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High demand: }&\max\{100,70\}=100,\\
		\text{Moderate demand: }&\max\{20,60\}=60,\\
		\text{Low demand: }&\max\{0,50\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High</th><th scope="col">Moderate</th><th scope="col">Low</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Policy A</th><td>$100-100=0$</td><td>$60-20=40$</td><td>$50-0=50$</td><td>50</td></tr><tr><th scope="row">Policy B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$50-50=0$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Policy B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Policy A</td></tr><tr><th scope="row">Maximin</th><td>Policy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Policy B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "logistics-contract-3x2",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "2",
        labels: { name: "Logistics Contract", section: "Applied: 3 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose between Logistics Contract A and Logistics Contract B. Market conditions can be favourable, stable, or unfavourable. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a logistics contract.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable market</th><th scope="col">Stable market</th><th scope="col">Unfavourable market</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>90</td><td>70</td><td>60</td></tr><tr><th scope="row">Contract B</th><td>80</td><td>50</td><td>40</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Contract A}) &= \max\{90,70,60\}=90,\\
		\max(\text{Contract B}) &= \max\{80,50,40\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Contract A}),\max(\text{Contract B})\}
	=\max\{90,80\}
	=90.
$$
<p>The Maximax choice is Contract A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Contract A}) &= \min\{90,70,60\}=60,\\
		\min(\text{Contract B}) &= \min\{80,50,40\}=40.
	\end{aligned}
$$
$$
\max\{\min(\text{Contract A}),\min(\text{Contract B})\}
	=\max\{60,40\}
	=60.
$$
<p>The Maximin choice is Contract A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable market: }&\max\{90,80\}=90,\\
		\text{Stable market: }&\max\{70,50\}=70,\\
		\text{Unfavourable market: }&\max\{60,40\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Stable</th><th scope="col">Unfavourable</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>$90-90=0$</td><td>$70-70=0$</td><td>$60-60=0$</td><td>0</td></tr><tr><th scope="row">Contract B</th><td>$90-80=10$</td><td>$70-50=20$</td><td>$60-40=20$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Contract A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Contract A</td></tr><tr><th scope="row">Maximin</th><td>Contract A</td></tr><tr><th scope="row">Minimax Regret</th><td>Contract A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "technology-platform-3x3",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "3",
        labels: { name: "Technology Platform", section: "Applied: 3 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose Technology Platform A, Platform B, or Platform C. Operating conditions can be favourable, stable, or disrupted. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a technology platform.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable conditions</th><th scope="col">Stable conditions</th><th scope="col">Disrupted conditions</th></tr></thead><tbody><tr><th scope="row">Platform A</th><td>100</td><td>50</td><td>50</td></tr><tr><th scope="row">Platform B</th><td>70</td><td>49</td><td>90</td></tr><tr><th scope="row">Platform C</th><td>60</td><td>40</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Platform A}) &= \max\{100,50,50\}=100,\\
		\max(\text{Platform B}) &= \max\{70,49,90\}=90,\\
		\max(\text{Platform C}) &= \max\{60,40,45\}=60.
	\end{aligned}
$$
$$
\max\{\max(\text{Platform A}),\max(\text{Platform B}),
	\max(\text{Platform C})\}
	=\max\{100,90,60\}
	=100.
$$
<p>The Maximax choice is Platform A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Platform A}) &= \min\{100,50,50\}=50,\\
		\min(\text{Platform B}) &= \min\{70,49,90\}=49,\\
		\min(\text{Platform C}) &= \min\{60,40,45\}=40.
	\end{aligned}
$$
$$
\max\{\min(\text{Platform A}),\min(\text{Platform B}),
	\min(\text{Platform C})\}
	=\max\{50,49,40\}
	=50.
$$
<p>The Maximin choice is Platform A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable conditions: }&\max\{100,70,60\}=100,\\
		\text{Stable conditions: }&\max\{50,49,40\}=50,\\
		\text{Disrupted conditions: }&\max\{50,90,45\}=90.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Stable</th><th scope="col">Disrupted</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Platform A</th><td>$100-100=0$</td><td>$50-50=0$</td><td>$90-50=40$</td><td>40</td></tr><tr><th scope="row">Platform B</th><td>$100-70=30$</td><td>$50-49=1$</td><td>$90-90=0$</td><td>30</td></tr><tr><th scope="row">Platform C</th><td>$100-60=40$</td><td>$50-40=10$</td><td>$90-45=45$</td><td>45</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Platform B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Platform A</td></tr><tr><th scope="row">Maximin</th><td>Platform A</td></tr><tr><th scope="row">Minimax Regret</th><td>Platform B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "service-model-3x3",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "3",
        labels: { name: "Service Model", section: "Applied: 3 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A service company must choose Service Model A, Model B, or Model C. Demand can be high, moderate, or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a service model.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Moderate demand</th><th scope="col">Low demand</th></tr></thead><tbody><tr><th scope="row">Model A</th><td>100</td><td>45</td><td>40</td></tr><tr><th scope="row">Model B</th><td>80</td><td>50</td><td>50</td></tr><tr><th scope="row">Model C</th><td>70</td><td>35</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Model A}) &= \max\{100,45,40\}=100,\\
		\max(\text{Model B}) &= \max\{80,50,50\}=80,\\
		\max(\text{Model C}) &= \max\{70,35,45\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Model A}),\max(\text{Model B}),
	\max(\text{Model C})\}
	=\max\{100,80,70\}
	=100.
$$
<p>The Maximax choice is Model A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Model A}) &= \min\{100,45,40\}=40,\\
		\min(\text{Model B}) &= \min\{80,50,50\}=50,\\
		\min(\text{Model C}) &= \min\{70,35,45\}=35.
	\end{aligned}
$$
$$
\max\{\min(\text{Model A}),\min(\text{Model B}),
	\min(\text{Model C})\}
	=\max\{40,50,35\}
	=50.
$$
<p>The Maximin choice is Model B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High demand: }&\max\{100,80,70\}=100,\\
		\text{Moderate demand: }&\max\{45,50,35\}=50,\\
		\text{Low demand: }&\max\{40,50,45\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High</th><th scope="col">Moderate</th><th scope="col">Low</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Model A</th><td>$100-100=0$</td><td>$50-45=5$</td><td>$50-40=10$</td><td>10</td></tr><tr><th scope="row">Model B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>$50-50=0$</td><td>20</td></tr><tr><th scope="row">Model C</th><td>$100-70=30$</td><td>$50-35=15$</td><td>$50-45=5$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Model A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Model A</td></tr><tr><th scope="row">Maximin</th><td>Model B</td></tr><tr><th scope="row">Minimax Regret</th><td>Model A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "inventory-policy-3x3",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "3",
        labels: { name: "Inventory Policy", section: "Applied: 3 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must choose Inventory Policy A, Policy B, or Policy C. Demand can be high, moderate, or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an inventory policy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Moderate demand</th><th scope="col">Low demand</th></tr></thead><tbody><tr><th scope="row">Policy A</th><td>100</td><td>20</td><td>0</td></tr><tr><th scope="row">Policy B</th><td>70</td><td>60</td><td>50</td></tr><tr><th scope="row">Policy C</th><td>60</td><td>40</td><td>30</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Policy A}) &= \max\{100,20,0\}=100,\\
		\max(\text{Policy B}) &= \max\{70,60,50\}=70,\\
		\max(\text{Policy C}) &= \max\{60,40,30\}=60.
	\end{aligned}
$$
$$
\max\{\max(\text{Policy A}),\max(\text{Policy B}),
	\max(\text{Policy C})\}
	=\max\{100,70,60\}
	=100.
$$
<p>The Maximax choice is Policy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Policy A}) &= \min\{100,20,0\}=0,\\
		\min(\text{Policy B}) &= \min\{70,60,50\}=50,\\
		\min(\text{Policy C}) &= \min\{60,40,30\}=30.
	\end{aligned}
$$
$$
\max\{\min(\text{Policy A}),\min(\text{Policy B}),
	\min(\text{Policy C})\}
	=\max\{0,50,30\}
	=50.
$$
<p>The Maximin choice is Policy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High demand: }&\max\{100,70,60\}=100,\\
		\text{Moderate demand: }&\max\{20,60,40\}=60,\\
		\text{Low demand: }&\max\{0,50,30\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High</th><th scope="col">Moderate</th><th scope="col">Low</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Policy A</th><td>$100-100=0$</td><td>$60-20=40$</td><td>$50-0=50$</td><td>50</td></tr><tr><th scope="row">Policy B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$50-50=0$</td><td>30</td></tr><tr><th scope="row">Policy C</th><td>$100-60=40$</td><td>$60-40=20$</td><td>$50-30=20$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Policy B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Policy A</td></tr><tr><th scope="row">Maximin</th><td>Policy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Policy B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "event-venue-3x3",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "3",
        labels: { name: "Event Venue", section: "Applied: 3 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>An event organiser must choose Venue A, Venue B, or Venue C. Attendance can be high, moderate, or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an event venue.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High attendance</th><th scope="col">Moderate attendance</th><th scope="col">Low attendance</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>100</td><td>0</td><td>20</td></tr><tr><th scope="row">Venue B</th><td>70</td><td>60</td><td>55</td></tr><tr><th scope="row">Venue C</th><td>80</td><td>50</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Venue A}) &= \max\{100,0,20\}=100,\\
		\max(\text{Venue B}) &= \max\{70,60,55\}=70,\\
		\max(\text{Venue C}) &= \max\{80,50,50\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Venue A}),\max(\text{Venue B}),\max(\text{Venue C})\}
	=\max\{100,70,80\}
	=100.
$$
<p>The Maximax choice is Venue A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Venue A}) &= \min\{100,0,20\}=0,\\
		\min(\text{Venue B}) &= \min\{70,60,55\}=55,\\
		\min(\text{Venue C}) &= \min\{80,50,50\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Venue A}),\min(\text{Venue B}),\min(\text{Venue C})\}
	=\max\{0,55,50\}
	=55.
$$
<p>The Maximin choice is Venue B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High attendance: }&\max\{100,70,80\}=100,\\
		\text{Moderate attendance: }&\max\{0,60,50\}=60,\\
		\text{Low attendance: }&\max\{20,55,50\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High</th><th scope="col">Moderate</th><th scope="col">Low</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>$100-100=0$</td><td>$60-0=60$</td><td>$55-20=35$</td><td>60</td></tr><tr><th scope="row">Venue B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$55-55=0$</td><td>30</td></tr><tr><th scope="row">Venue C</th><td>$100-80=20$</td><td>$60-50=10$</td><td>$55-50=5$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Venue C because it has the smallest maximum regret, $20$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Venue A</td></tr><tr><th scope="row">Maximin</th><td>Venue B</td></tr><tr><th scope="row">Minimax Regret</th><td>Venue C</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "distribution-plan-3x3",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "3",
        labels: { name: "Distribution Plan", section: "Applied: 3 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose Distribution Plan A, Plan B, or Plan C. Market conditions can be favourable, stable, or unfavourable. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a distribution plan.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable market</th><th scope="col">Stable market</th><th scope="col">Unfavourable market</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>90</td><td>70</td><td>60</td></tr><tr><th scope="row">Plan B</th><td>80</td><td>50</td><td>40</td></tr><tr><th scope="row">Plan C</th><td>70</td><td>60</td><td>30</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Plan A}) &= \max\{90,70,60\}=90,\\
		\max(\text{Plan B}) &= \max\{80,50,40\}=80,\\
		\max(\text{Plan C}) &= \max\{70,60,30\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Plan A}),\max(\text{Plan B}),\max(\text{Plan C})\}
	=\max\{90,80,70\}
	=90.
$$
<p>The Maximax choice is Plan A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Plan A}) &= \min\{90,70,60\}=60,\\
		\min(\text{Plan B}) &= \min\{80,50,40\}=40,\\
		\min(\text{Plan C}) &= \min\{70,60,30\}=30.
	\end{aligned}
$$
$$
\max\{\min(\text{Plan A}),\min(\text{Plan B}),\min(\text{Plan C})\}
	=\max\{60,40,30\}
	=60.
$$
<p>The Maximin choice is Plan A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable market: }&\max\{90,80,70\}=90,\\
		\text{Stable market: }&\max\{70,50,60\}=70,\\
		\text{Unfavourable market: }&\max\{60,40,30\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Stable</th><th scope="col">Unfavourable</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>$90-90=0$</td><td>$70-70=0$</td><td>$60-60=0$</td><td>0</td></tr><tr><th scope="row">Plan B</th><td>$90-80=10$</td><td>$70-50=20$</td><td>$60-40=20$</td><td>20</td></tr><tr><th scope="row">Plan C</th><td>$90-70=20$</td><td>$70-60=10$</td><td>$60-30=30$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Plan A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Plan A</td></tr><tr><th scope="row">Maximin</th><td>Plan A</td></tr><tr><th scope="row">Minimax Regret</th><td>Plan A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "production-system-4x2",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "2",
        labels: { name: "Production System", section: "Applied: 4 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A manufacturing company must choose between Production System A and Production System B. Four states of nature represent different operating conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a production system.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">System A</th><td>100</td><td>50</td><td>50</td><td>55</td></tr><tr><th scope="row">System B</th><td>70</td><td>49</td><td>90</td><td>52</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{System A}) &= \max\{100,50,50,55\}=100,\\
		\max(\text{System B}) &= \max\{70,49,90,52\}=90.
	\end{aligned}
$$
$$
\max\{\max(\text{System A}),\max(\text{System B})\}
	=\max\{100,90\}
	=100.
$$
<p>The Maximax choice is System A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{System A}) &= \min\{100,50,50,55\}=50,\\
		\min(\text{System B}) &= \min\{70,49,90,52\}=49.
	\end{aligned}
$$
$$
\max\{\min(\text{System A}),\min(\text{System B})\}
	=\max\{50,49\}
	=50.
$$
<p>The Maximin choice is System A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70\}=100,\\
		\text{State }S_2:\;&\max\{50,49\}=50,\\
		\text{State }S_3:\;&\max\{50,90\}=90,\\
		\text{State }S_4:\;&\max\{55,52\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">System A</th><td>$100-100=0$</td><td>$50-50=0$</td><td>$90-50=40$</td><td>$55-55=0$</td><td>40</td></tr><tr><th scope="row">System B</th><td>$100-70=30$</td><td>$50-49=1$</td><td>$90-90=0$</td><td>$55-52=3$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is System B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>System A</td></tr><tr><th scope="row">Maximin</th><td>System A</td></tr><tr><th scope="row">Minimax Regret</th><td>System B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "service-network-4x2",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "2",
        labels: { name: "Service Network", section: "Applied: 4 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A service company must choose between Service Network A and Service Network B. Four states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a service network.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>100</td><td>45</td><td>40</td><td>48</td></tr><tr><th scope="row">Network B</th><td>80</td><td>50</td><td>50</td><td>52</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Network A}) &= \max\{100,45,40,48\}=100,\\
		\max(\text{Network B}) &= \max\{80,50,50,52\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Network A}),\max(\text{Network B})\}
	=\max\{100,80\}
	=100.
$$
<p>The Maximax choice is Network A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Network A}) &= \min\{100,45,40,48\}=40,\\
		\min(\text{Network B}) &= \min\{80,50,50,52\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Network A}),\min(\text{Network B})\}
	=\max\{40,50\}
	=50.
$$
<p>The Maximin choice is Network B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,80\}=100,\\
		\text{State }S_2:\;&\max\{45,50\}=50,\\
		\text{State }S_3:\;&\max\{40,50\}=50,\\
		\text{State }S_4:\;&\max\{48,52\}=52.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>$100-100=0$</td><td>$50-45=5$</td><td>$50-40=10$</td><td>$52-48=4$</td><td>10</td></tr><tr><th scope="row">Network B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>$50-50=0$</td><td>$52-52=0$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Network A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Network A</td></tr><tr><th scope="row">Maximin</th><td>Network B</td></tr><tr><th scope="row">Minimax Regret</th><td>Network A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "inventory-strategy-4x2",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "2",
        labels: { name: "Inventory Strategy", section: "Applied: 4 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must choose between Inventory Strategy A and Inventory Strategy B. Four states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an inventory strategy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>100</td><td>20</td><td>0</td><td>25</td></tr><tr><th scope="row">Strategy B</th><td>70</td><td>60</td><td>50</td><td>55</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Strategy A}) &= \max\{100,20,0,25\}=100,\\
		\max(\text{Strategy B}) &= \max\{70,60,50,55\}=70.
	\end{aligned}
$$
$$
\max\{\max(\text{Strategy A}),\max(\text{Strategy B})\}
	=\max\{100,70\}
	=100.
$$
<p>The Maximax choice is Strategy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Strategy A}) &= \min\{100,20,0,25\}=0,\\
		\min(\text{Strategy B}) &= \min\{70,60,50,55\}=50.
	\end{aligned}
$$
$$
\max\{\min(\text{Strategy A}),\min(\text{Strategy B})\}
	=\max\{0,50\}
	=50.
$$
<p>The Maximin choice is Strategy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70\}=100,\\
		\text{State }S_2:\;&\max\{20,60\}=60,\\
		\text{State }S_3:\;&\max\{0,50\}=50,\\
		\text{State }S_4:\;&\max\{25,55\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>$100-100=0$</td><td>$60-20=40$</td><td>$50-0=50$</td><td>$55-25=30$</td><td>50</td></tr><tr><th scope="row">Strategy B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$50-50=0$</td><td>$55-55=0$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Strategy B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Strategy A</td></tr><tr><th scope="row">Maximin</th><td>Strategy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Strategy B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "supply-contract-4x2",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "2",
        labels: { name: "Supply Contract", section: "Applied: 4 × 2" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose between Supply Contract A and Supply Contract B. Four states of nature represent different market and supply conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a supply contract.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>90</td><td>70</td><td>60</td><td>65</td></tr><tr><th scope="row">Contract B</th><td>80</td><td>50</td><td>40</td><td>55</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Contract A}) &= \max\{90,70,60,65\}=90,\\
		\max(\text{Contract B}) &= \max\{80,50,40,55\}=80.
	\end{aligned}
$$
$$
\max\{\max(\text{Contract A}),\max(\text{Contract B})\}
	=\max\{90,80\}
	=90.
$$
<p>The Maximax choice is Contract A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Contract A}) &= \min\{90,70,60,65\}=60,\\
		\min(\text{Contract B}) &= \min\{80,50,40,55\}=40.
	\end{aligned}
$$
$$
\max\{\min(\text{Contract A}),\min(\text{Contract B})\}
	=\max\{60,40\}
	=60.
$$
<p>The Maximin choice is Contract A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{90,80\}=90,\\
		\text{State }S_2:\;&\max\{70,50\}=70,\\
		\text{State }S_3:\;&\max\{60,40\}=60,\\
		\text{State }S_4:\;&\max\{65,55\}=65.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>$90-90=0$</td><td>$70-70=0$</td><td>$60-60=0$</td><td>$65-65=0$</td><td>0</td></tr><tr><th scope="row">Contract B</th><td>$90-80=10$</td><td>$70-50=20$</td><td>$60-40=20$</td><td>$65-55=10$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Contract A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Contract A</td></tr><tr><th scope="row">Maximin</th><td>Contract A</td></tr><tr><th scope="row">Minimax Regret</th><td>Contract A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "market-entry-strategy-2x4",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "4",
        labels: { name: "Market Entry Strategy", section: "Applied: 2 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose among Market Entry Strategy A, Strategy B, Strategy C, and Strategy D. Market conditions can be favourable or unfavourable. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a market entry strategy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable market</th><th scope="col">Unfavourable market</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>30</td><td>100</td></tr><tr><th scope="row">Strategy B</th><td>60</td><td>40</td></tr><tr><th scope="row">Strategy C</th><td>50</td><td>10</td></tr><tr><th scope="row">Strategy D</th><td>0</td><td>30</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Strategy A}) &= \max\{30,100\}=100,\\
		\max(\text{Strategy B}) &= \max\{60,40\}=60,\\
		\max(\text{Strategy C}) &= \max\{50,10\}=50,\\
		\max(\text{Strategy D}) &= \max\{0,30\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Strategy A}),\max(\text{Strategy B}),
		\max(\text{Strategy C}),\max(\text{Strategy D})\}\\
		&\qquad=\max\{100,60,50,30\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Strategy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Strategy A}) &= \min\{30,100\}=30,\\
		\min(\text{Strategy B}) &= \min\{60,40\}=40,\\
		\min(\text{Strategy C}) &= \min\{50,10\}=10,\\
		\min(\text{Strategy D}) &= \min\{0,30\}=0.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Strategy A}),\min(\text{Strategy B}),
		\min(\text{Strategy C}),\min(\text{Strategy D})\}\\
		&\qquad=\max\{30,40,10,0\}
		=40.
	\end{aligned}
$$
<p>The Maximin choice is Strategy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Favourable market: }&
		\max\{30,60,50,0\}=60,\\
		\text{Unfavourable market: }&
		\max\{100,40,10,30\}=100.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Favourable</th><th scope="col">Unfavourable</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>$60-30=30$</td><td>$100-100=0$</td><td>30</td></tr><tr><th scope="row">Strategy B</th><td>$60-60=0$</td><td>$100-40=60$</td><td>60</td></tr><tr><th scope="row">Strategy C</th><td>$60-50=10$</td><td>$100-10=90$</td><td>90</td></tr><tr><th scope="row">Strategy D</th><td>$60-0=60$</td><td>$100-30=70$</td><td>70</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Strategy A because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Strategy A</td></tr><tr><th scope="row">Maximin</th><td>Strategy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Strategy A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "production-plan-2x4",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "4",
        labels: { name: "Production Plan", section: "Applied: 2 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A manufacturing company must choose among Production Plan A, Plan B, Plan C, and Plan D. Demand can be high or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a production plan.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>100</td><td>70</td></tr><tr><th scope="row">Plan B</th><td>90</td><td>90</td></tr><tr><th scope="row">Plan C</th><td>40</td><td>80</td></tr><tr><th scope="row">Plan D</th><td>30</td><td>40</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Plan A}) &= \max\{100,70\}=100,\\
		\max(\text{Plan B}) &= \max\{90,90\}=90,\\
		\max(\text{Plan C}) &= \max\{40,80\}=80,\\
		\max(\text{Plan D}) &= \max\{30,40\}=40.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Plan A}),\max(\text{Plan B}),
		\max(\text{Plan C}),\max(\text{Plan D})\}\\
		&\qquad=\max\{100,90,80,40\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Plan A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Plan A}) &= \min\{100,70\}=70,\\
		\min(\text{Plan B}) &= \min\{90,90\}=90,\\
		\min(\text{Plan C}) &= \min\{40,80\}=40,\\
		\min(\text{Plan D}) &= \min\{30,40\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Plan A}),\min(\text{Plan B}),
		\min(\text{Plan C}),\min(\text{Plan D})\}\\
		&\qquad=\max\{70,90,40,30\}
		=90.
	\end{aligned}
$$
<p>The Maximin choice is Plan B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High demand: }&\max\{100,90,40,30\}=100,\\
		\text{Low demand: }&\max\{70,90,80,40\}=90.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Plan A</th><td>$100-100=0$</td><td>$90-70=20$</td><td>20</td></tr><tr><th scope="row">Plan B</th><td>$100-90=10$</td><td>$90-90=0$</td><td>10</td></tr><tr><th scope="row">Plan C</th><td>$100-40=60$</td><td>$90-80=10$</td><td>60</td></tr><tr><th scope="row">Plan D</th><td>$100-30=70$</td><td>$90-40=50$</td><td>70</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Plan B because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Plan A</td></tr><tr><th scope="row">Maximin</th><td>Plan B</td></tr><tr><th scope="row">Minimax Regret</th><td>Plan B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "facility-location-2x4",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "4",
        labels: { name: "Facility Location", section: "Applied: 2 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose among Facility Location A, Location B, Location C, and Location D. Regional demand can be high or low. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a facility location.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High regional demand</th><th scope="col">Low regional demand</th></tr></thead><tbody><tr><th scope="row">Location A</th><td>10</td><td>100</td></tr><tr><th scope="row">Location B</th><td>60</td><td>70</td></tr><tr><th scope="row">Location C</th><td>50</td><td>80</td></tr><tr><th scope="row">Location D</th><td>20</td><td>40</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Location A}) &= \max\{10,100\}=100,\\
		\max(\text{Location B}) &= \max\{60,70\}=70,\\
		\max(\text{Location C}) &= \max\{50,80\}=80,\\
		\max(\text{Location D}) &= \max\{20,40\}=40.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Location A}),\max(\text{Location B}),
		\max(\text{Location C}),\max(\text{Location D})\}\\
		&\qquad=\max\{100,70,80,40\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Location A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Location A}) &= \min\{10,100\}=10,\\
		\min(\text{Location B}) &= \min\{60,70\}=60,\\
		\min(\text{Location C}) &= \min\{50,80\}=50,\\
		\min(\text{Location D}) &= \min\{20,40\}=20.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Location A}),\min(\text{Location B}),
		\min(\text{Location C}),\min(\text{Location D})\}\\
		&\qquad=\max\{10,60,50,20\}
		=60.
	\end{aligned}
$$
<p>The Maximin choice is Location B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{High regional demand: }&
		\max\{10,60,50,20\}=60,\\
		\text{Low regional demand: }&
		\max\{100,70,80,40\}=100.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">High demand</th><th scope="col">Low demand</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Location A</th><td>$60-10=50$</td><td>$100-100=0$</td><td>50</td></tr><tr><th scope="row">Location B</th><td>$60-60=0$</td><td>$100-70=30$</td><td>30</td></tr><tr><th scope="row">Location C</th><td>$60-50=10$</td><td>$100-80=20$</td><td>20</td></tr><tr><th scope="row">Location D</th><td>$60-20=40$</td><td>$100-40=60$</td><td>60</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Location C because it has the smallest maximum regret, $20$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Location A</td></tr><tr><th scope="row">Maximin</th><td>Location B</td></tr><tr><th scope="row">Minimax Regret</th><td>Location C</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "supply-agreement-2x4",
        problemType: "Applied",
        stateCount: "2",
        alternativeCount: "4",
        labels: { name: "Supply Agreement", section: "Applied: 2 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose among Supply Agreement A, Agreement B, Agreement C, and Agreement D. Supply conditions can be stable or disrupted. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a supply agreement.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Stable supply</th><th scope="col">Disrupted supply</th></tr></thead><tbody><tr><th scope="row">Agreement A</th><td>90</td><td>100</td></tr><tr><th scope="row">Agreement B</th><td>70</td><td>80</td></tr><tr><th scope="row">Agreement C</th><td>60</td><td>50</td></tr><tr><th scope="row">Agreement D</th><td>30</td><td>70</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Agreement A}) &= \max\{90,100\}=100,\\
		\max(\text{Agreement B}) &= \max\{70,80\}=80,\\
		\max(\text{Agreement C}) &= \max\{60,50\}=60,\\
		\max(\text{Agreement D}) &= \max\{30,70\}=70.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Agreement A}),\max(\text{Agreement B}),
		\max(\text{Agreement C}),\max(\text{Agreement D})\}\\
		&\qquad=\max\{100,80,60,70\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Agreement A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Agreement A}) &= \min\{90,100\}=90,\\
		\min(\text{Agreement B}) &= \min\{70,80\}=70,\\
		\min(\text{Agreement C}) &= \min\{60,50\}=50,\\
		\min(\text{Agreement D}) &= \min\{30,70\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Agreement A}),\min(\text{Agreement B}),
		\min(\text{Agreement C}),\min(\text{Agreement D})\}\\
		&\qquad=\max\{90,70,50,30\}
		=90.
	\end{aligned}
$$
<p>The Maximin choice is Agreement A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{Stable supply: }&
		\max\{90,70,60,30\}=90,\\
		\text{Disrupted supply: }&
		\max\{100,80,50,70\}=100.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">Stable supply</th><th scope="col">Disrupted supply</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Agreement A</th><td>$90-90=0$</td><td>$100-100=0$</td><td>0</td></tr><tr><th scope="row">Agreement B</th><td>$90-70=20$</td><td>$100-80=20$</td><td>20</td></tr><tr><th scope="row">Agreement C</th><td>$90-60=30$</td><td>$100-50=50$</td><td>50</td></tr><tr><th scope="row">Agreement D</th><td>$90-30=60$</td><td>$100-70=30$</td><td>60</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Agreement A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Agreement A</td></tr><tr><th scope="row">Maximin</th><td>Agreement A</td></tr><tr><th scope="row">Minimax Regret</th><td>Agreement A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "production-system-4x3",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "Production System", section: "Applied: 4 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A manufacturing company must choose among Production System A, System B, and System C. Four states of nature represent different operating conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a production system.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">System A</th><td>100</td><td>50</td><td>50</td><td>55</td></tr><tr><th scope="row">System B</th><td>70</td><td>49</td><td>90</td><td>52</td></tr><tr><th scope="row">System C</th><td>60</td><td>30</td><td>40</td><td>35</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{System A}) &= \max\{100,50,50,55\}=100,\\
		\max(\text{System B}) &= \max\{70,49,90,52\}=90,\\
		\max(\text{System C}) &= \max\{60,30,40,35\}=60.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{System A}),\max(\text{System B}),
		\max(\text{System C})\}\\
		&\qquad=\max\{100,90,60\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is System A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{System A}) &= \min\{100,50,50,55\}=50,\\
		\min(\text{System B}) &= \min\{70,49,90,52\}=49,\\
		\min(\text{System C}) &= \min\{60,30,40,35\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{System A}),\min(\text{System B}),
		\min(\text{System C})\}\\
		&\qquad=\max\{50,49,30\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is System A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,60\}=100,\\
		\text{State }S_2:\;&\max\{50,49,30\}=50,\\
		\text{State }S_3:\;&\max\{50,90,40\}=90,\\
		\text{State }S_4:\;&\max\{55,52,35\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">System A</th><td>$100-100=0$</td><td>$50-50=0$</td><td>$90-50=40$</td><td>$55-55=0$</td><td>40</td></tr><tr><th scope="row">System B</th><td>$100-70=30$</td><td>$50-49=1$</td><td>$90-90=0$</td><td>$55-52=3$</td><td>30</td></tr><tr><th scope="row">System C</th><td>$100-60=40$</td><td>$50-30=20$</td><td>$90-40=50$</td><td>$55-35=20$</td><td>50</td></tr></tbody></table></div>
<p>The Minimax Regret choice is System B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>System A</td></tr><tr><th scope="row">Maximin</th><td>System A</td></tr><tr><th scope="row">Minimax Regret</th><td>System B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "service-network-4x3",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "Service Network", section: "Applied: 4 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A service company must choose among Service Network A, Network B, and Network C. Four states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a service network.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>100</td><td>45</td><td>40</td><td>48</td></tr><tr><th scope="row">Network B</th><td>80</td><td>50</td><td>50</td><td>52</td></tr><tr><th scope="row">Network C</th><td>60</td><td>30</td><td>35</td><td>40</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Network A}) &= \max\{100,45,40,48\}=100,\\
		\max(\text{Network B}) &= \max\{80,50,50,52\}=80,\\
		\max(\text{Network C}) &= \max\{60,30,35,40\}=60.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Network A}),\max(\text{Network B}),
		\max(\text{Network C})\}\\
		&\qquad=\max\{100,80,60\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Network A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Network A}) &= \min\{100,45,40,48\}=40,\\
		\min(\text{Network B}) &= \min\{80,50,50,52\}=50,\\
		\min(\text{Network C}) &= \min\{60,30,35,40\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Network A}),\min(\text{Network B}),
		\min(\text{Network C})\}\\
		&\qquad=\max\{40,50,30\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is Network B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,80,60\}=100,\\
		\text{State }S_2:\;&\max\{45,50,30\}=50,\\
		\text{State }S_3:\;&\max\{40,50,35\}=50,\\
		\text{State }S_4:\;&\max\{48,52,40\}=52.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>$100-100=0$</td><td>$50-45=5$</td><td>$50-40=10$</td><td>$52-48=4$</td><td>10</td></tr><tr><th scope="row">Network B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>$50-50=0$</td><td>$52-52=0$</td><td>20</td></tr><tr><th scope="row">Network C</th><td>$100-60=40$</td><td>$50-30=20$</td><td>$50-35=15$</td><td>$52-40=12$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Network A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Network A</td></tr><tr><th scope="row">Maximin</th><td>Network B</td></tr><tr><th scope="row">Minimax Regret</th><td>Network A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "inventory-strategy-4x3",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "Inventory Strategy", section: "Applied: 4 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must choose among Inventory Strategy A, Strategy B, and Strategy C. Four states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an inventory strategy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>100</td><td>20</td><td>0</td><td>25</td></tr><tr><th scope="row">Strategy B</th><td>70</td><td>60</td><td>50</td><td>55</td></tr><tr><th scope="row">Strategy C</th><td>50</td><td>40</td><td>30</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Strategy A}) &= \max\{100,20,0,25\}=100,\\
		\max(\text{Strategy B}) &= \max\{70,60,50,55\}=70,\\
		\max(\text{Strategy C}) &= \max\{50,40,30,45\}=50.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Strategy A}),\max(\text{Strategy B}),
		\max(\text{Strategy C})\}\\
		&\qquad=\max\{100,70,50\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Strategy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Strategy A}) &= \min\{100,20,0,25\}=0,\\
		\min(\text{Strategy B}) &= \min\{70,60,50,55\}=50,\\
		\min(\text{Strategy C}) &= \min\{50,40,30,45\}=30.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Strategy A}),\min(\text{Strategy B}),
		\min(\text{Strategy C})\}\\
		&\qquad=\max\{0,50,30\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is Strategy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,50\}=100,\\
		\text{State }S_2:\;&\max\{20,60,40\}=60,\\
		\text{State }S_3:\;&\max\{0,50,30\}=50,\\
		\text{State }S_4:\;&\max\{25,55,45\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>$100-100=0$</td><td>$60-20=40$</td><td>$50-0=50$</td><td>$55-25=30$</td><td>50</td></tr><tr><th scope="row">Strategy B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$50-50=0$</td><td>$55-55=0$</td><td>30</td></tr><tr><th scope="row">Strategy C</th><td>$100-50=50$</td><td>$60-40=20$</td><td>$50-30=20$</td><td>$55-45=10$</td><td>50</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Strategy B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Strategy A</td></tr><tr><th scope="row">Maximin</th><td>Strategy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Strategy B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "event-venue-4x3",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "Event Venue", section: "Applied: 4 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>An event company must choose among Venue A, Venue B, and Venue C. Four states of nature represent different attendance levels. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an event venue.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>100</td><td>0</td><td>20</td><td>40</td></tr><tr><th scope="row">Venue B</th><td>70</td><td>60</td><td>55</td><td>58</td></tr><tr><th scope="row">Venue C</th><td>80</td><td>50</td><td>50</td><td>52</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Venue A}) &= \max\{100,0,20,40\}=100,\\
		\max(\text{Venue B}) &= \max\{70,60,55,58\}=70,\\
		\max(\text{Venue C}) &= \max\{80,50,50,52\}=80.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Venue A}),\max(\text{Venue B}),
		\max(\text{Venue C})\}\\
		&\qquad=\max\{100,70,80\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Venue A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Venue A}) &= \min\{100,0,20,40\}=0,\\
		\min(\text{Venue B}) &= \min\{70,60,55,58\}=55,\\
		\min(\text{Venue C}) &= \min\{80,50,50,52\}=50.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Venue A}),\min(\text{Venue B}),
		\min(\text{Venue C})\}\\
		&\qquad=\max\{0,55,50\}
		=55.
	\end{aligned}
$$
<p>The Maximin choice is Venue B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,80\}=100,\\
		\text{State }S_2:\;&\max\{0,60,50\}=60,\\
		\text{State }S_3:\;&\max\{20,55,50\}=55,\\
		\text{State }S_4:\;&\max\{40,58,52\}=58.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>$100-100=0$</td><td>$60-0=60$</td><td>$55-20=35$</td><td>$58-40=18$</td><td>60</td></tr><tr><th scope="row">Venue B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$55-55=0$</td><td>$58-58=0$</td><td>30</td></tr><tr><th scope="row">Venue C</th><td>$100-80=20$</td><td>$60-50=10$</td><td>$55-50=5$</td><td>$58-52=6$</td><td>20</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Venue C because it has the smallest maximum regret, $20$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Venue A</td></tr><tr><th scope="row">Maximin</th><td>Venue B</td></tr><tr><th scope="row">Minimax Regret</th><td>Venue C</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "supply-contract-4x3",
        problemType: "Applied",
        stateCount: "4",
        alternativeCount: "3",
        labels: { name: "Supply Contract", section: "Applied: 4 × 3" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose among Supply Contract A, Contract B, and Contract C. Four states of nature represent different market and supply conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a supply contract.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th><th scope="col">State $S_4$</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>90</td><td>70</td><td>60</td><td>65</td></tr><tr><th scope="row">Contract B</th><td>80</td><td>50</td><td>40</td><td>55</td></tr><tr><th scope="row">Contract C</th><td>70</td><td>45</td><td>35</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Contract A}) &= \max\{90,70,60,65\}=90,\\
		\max(\text{Contract B}) &= \max\{80,50,40,55\}=80,\\
		\max(\text{Contract C}) &= \max\{70,45,35,50\}=70.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Contract A}),\max(\text{Contract B}),
		\max(\text{Contract C})\}\\
		&\qquad=\max\{90,80,70\}
		=90.
	\end{aligned}
$$
<p>The Maximax choice is Contract A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Contract A}) &= \min\{90,70,60,65\}=60,\\
		\min(\text{Contract B}) &= \min\{80,50,40,55\}=40,\\
		\min(\text{Contract C}) &= \min\{70,45,35,50\}=35.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Contract A}),\min(\text{Contract B}),
		\min(\text{Contract C})\}\\
		&\qquad=\max\{60,40,35\}
		=60.
	\end{aligned}
$$
<p>The Maximin choice is Contract A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{90,80,70\}=90,\\
		\text{State }S_2:\;&\max\{70,50,45\}=70,\\
		\text{State }S_3:\;&\max\{60,40,35\}=60,\\
		\text{State }S_4:\;&\max\{65,55,50\}=65.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">$S_4$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>$90-90=0$</td><td>$70-70=0$</td><td>$60-60=0$</td><td>$65-65=0$</td><td>0</td></tr><tr><th scope="row">Contract B</th><td>$90-80=10$</td><td>$70-50=20$</td><td>$60-40=20$</td><td>$65-55=10$</td><td>20</td></tr><tr><th scope="row">Contract C</th><td>$90-70=20$</td><td>$70-45=25$</td><td>$60-35=25$</td><td>$65-50=15$</td><td>25</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Contract A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Contract A</td></tr><tr><th scope="row">Maximin</th><td>Contract A</td></tr><tr><th scope="row">Minimax Regret</th><td>Contract A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "production-system-3x4",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "4",
        labels: { name: "Production System", section: "Applied: 3 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A manufacturing company must choose among Production System A, System B, System C, and System D. Three states of nature represent different operating conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a production system.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">System A</th><td>100</td><td>50</td><td>50</td></tr><tr><th scope="row">System B</th><td>70</td><td>49</td><td>90</td></tr><tr><th scope="row">System C</th><td>60</td><td>30</td><td>40</td></tr><tr><th scope="row">System D</th><td>55</td><td>35</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{System A}) &= \max\{100,50,50\}=100,\\
		\max(\text{System B}) &= \max\{70,49,90\}=90,\\
		\max(\text{System C}) &= \max\{60,30,40\}=60,\\
		\max(\text{System D}) &= \max\{55,35,45\}=55.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{System A}),\max(\text{System B}),
		\max(\text{System C}),\max(\text{System D})\}\\
		&\qquad=\max\{100,90,60,55\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is System A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{System A}) &= \min\{100,50,50\}=50,\\
		\min(\text{System B}) &= \min\{70,49,90\}=49,\\
		\min(\text{System C}) &= \min\{60,30,40\}=30,\\
		\min(\text{System D}) &= \min\{55,35,45\}=35.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{System A}),\min(\text{System B}),
		\min(\text{System C}),\min(\text{System D})\}\\
		&\qquad=\max\{50,49,30,35\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is System A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,60,55\}=100,\\
		\text{State }S_2:\;&\max\{50,49,30,35\}=50,\\
		\text{State }S_3:\;&\max\{50,90,40,45\}=90.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">System A</th><td>$100-100=0$</td><td>$50-50=0$</td><td>$90-50=40$</td><td>40</td></tr><tr><th scope="row">System B</th><td>$100-70=30$</td><td>$50-49=1$</td><td>$90-90=0$</td><td>30</td></tr><tr><th scope="row">System C</th><td>$100-60=40$</td><td>$50-30=20$</td><td>$90-40=50$</td><td>50</td></tr><tr><th scope="row">System D</th><td>$100-55=45$</td><td>$50-35=15$</td><td>$90-45=45$</td><td>45</td></tr></tbody></table></div>
<p>The Minimax Regret choice is System B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>System A</td></tr><tr><th scope="row">Maximin</th><td>System A</td></tr><tr><th scope="row">Minimax Regret</th><td>System B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "service-network-3x4",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "4",
        labels: { name: "Service Network", section: "Applied: 3 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A service company must choose among Service Network A, Network B, Network C, and Network D. Three states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a service network.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>100</td><td>45</td><td>40</td></tr><tr><th scope="row">Network B</th><td>80</td><td>50</td><td>50</td></tr><tr><th scope="row">Network C</th><td>60</td><td>30</td><td>35</td></tr><tr><th scope="row">Network D</th><td>70</td><td>40</td><td>45</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Network A}) &= \max\{100,45,40\}=100,\\
		\max(\text{Network B}) &= \max\{80,50,50\}=80,\\
		\max(\text{Network C}) &= \max\{60,30,35\}=60,\\
		\max(\text{Network D}) &= \max\{70,40,45\}=70.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Network A}),\max(\text{Network B}),
		\max(\text{Network C}),\max(\text{Network D})\}\\
		&\qquad=\max\{100,80,60,70\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Network A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Network A}) &= \min\{100,45,40\}=40,\\
		\min(\text{Network B}) &= \min\{80,50,50\}=50,\\
		\min(\text{Network C}) &= \min\{60,30,35\}=30,\\
		\min(\text{Network D}) &= \min\{70,40,45\}=40.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Network A}),\min(\text{Network B}),
		\min(\text{Network C}),\min(\text{Network D})\}\\
		&\qquad=\max\{40,50,30,40\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is Network B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,80,60,70\}=100,\\
		\text{State }S_2:\;&\max\{45,50,30,40\}=50,\\
		\text{State }S_3:\;&\max\{40,50,35,45\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Network A</th><td>$100-100=0$</td><td>$50-45=5$</td><td>$50-40=10$</td><td>10</td></tr><tr><th scope="row">Network B</th><td>$100-80=20$</td><td>$50-50=0$</td><td>$50-50=0$</td><td>20</td></tr><tr><th scope="row">Network C</th><td>$100-60=40$</td><td>$50-30=20$</td><td>$50-35=15$</td><td>40</td></tr><tr><th scope="row">Network D</th><td>$100-70=30$</td><td>$50-40=10$</td><td>$50-45=5$</td><td>30</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Network A because it has the smallest maximum regret, $10$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Network A</td></tr><tr><th scope="row">Maximin</th><td>Network B</td></tr><tr><th scope="row">Minimax Regret</th><td>Network A</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "inventory-strategy-3x4",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "4",
        labels: { name: "Inventory Strategy", section: "Applied: 3 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A retailer must choose among Inventory Strategy A, Strategy B, Strategy C, and Strategy D. Three states of nature represent different demand conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an inventory strategy.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>100</td><td>20</td><td>0</td></tr><tr><th scope="row">Strategy B</th><td>70</td><td>60</td><td>50</td></tr><tr><th scope="row">Strategy C</th><td>50</td><td>40</td><td>30</td></tr><tr><th scope="row">Strategy D</th><td>60</td><td>45</td><td>35</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Strategy A}) &= \max\{100,20,0\}=100,\\
		\max(\text{Strategy B}) &= \max\{70,60,50\}=70,\\
		\max(\text{Strategy C}) &= \max\{50,40,30\}=50,\\
		\max(\text{Strategy D}) &= \max\{60,45,35\}=60.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Strategy A}),\max(\text{Strategy B}),
		\max(\text{Strategy C}),\max(\text{Strategy D})\}\\
		&\qquad=\max\{100,70,50,60\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Strategy A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Strategy A}) &= \min\{100,20,0\}=0,\\
		\min(\text{Strategy B}) &= \min\{70,60,50\}=50,\\
		\min(\text{Strategy C}) &= \min\{50,40,30\}=30,\\
		\min(\text{Strategy D}) &= \min\{60,45,35\}=35.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Strategy A}),\min(\text{Strategy B}),
		\min(\text{Strategy C}),\min(\text{Strategy D})\}\\
		&\qquad=\max\{0,50,30,35\}
		=50.
	\end{aligned}
$$
<p>The Maximin choice is Strategy B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,50,60\}=100,\\
		\text{State }S_2:\;&\max\{20,60,40,45\}=60,\\
		\text{State }S_3:\;&\max\{0,50,30,35\}=50.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Strategy A</th><td>$100-100=0$</td><td>$60-20=40$</td><td>$50-0=50$</td><td>50</td></tr><tr><th scope="row">Strategy B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$50-50=0$</td><td>30</td></tr><tr><th scope="row">Strategy C</th><td>$100-50=50$</td><td>$60-40=20$</td><td>$50-30=20$</td><td>50</td></tr><tr><th scope="row">Strategy D</th><td>$100-60=40$</td><td>$60-45=15$</td><td>$50-35=15$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Strategy B because it has the smallest maximum regret, $30$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Strategy A</td></tr><tr><th scope="row">Maximin</th><td>Strategy B</td></tr><tr><th scope="row">Minimax Regret</th><td>Strategy B</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "event-venue-3x4",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "4",
        labels: { name: "Event Venue", section: "Applied: 3 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>An event company must choose among Venue A, Venue B, Venue C, and Venue D. Three states of nature represent different attendance levels. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select an event venue.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>100</td><td>0</td><td>20</td></tr><tr><th scope="row">Venue B</th><td>70</td><td>60</td><td>55</td></tr><tr><th scope="row">Venue C</th><td>80</td><td>50</td><td>50</td></tr><tr><th scope="row">Venue D</th><td>60</td><td>45</td><td>40</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Venue A}) &= \max\{100,0,20\}=100,\\
		\max(\text{Venue B}) &= \max\{70,60,55\}=70,\\
		\max(\text{Venue C}) &= \max\{80,50,50\}=80,\\
		\max(\text{Venue D}) &= \max\{60,45,40\}=60.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Venue A}),\max(\text{Venue B}),
		\max(\text{Venue C}),\max(\text{Venue D})\}\\
		&\qquad=\max\{100,70,80,60\}
		=100.
	\end{aligned}
$$
<p>The Maximax choice is Venue A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Venue A}) &= \min\{100,0,20\}=0,\\
		\min(\text{Venue B}) &= \min\{70,60,55\}=55,\\
		\min(\text{Venue C}) &= \min\{80,50,50\}=50,\\
		\min(\text{Venue D}) &= \min\{60,45,40\}=40.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Venue A}),\min(\text{Venue B}),
		\min(\text{Venue C}),\min(\text{Venue D})\}\\
		&\qquad=\max\{0,55,50,40\}
		=55.
	\end{aligned}
$$
<p>The Maximin choice is Venue B because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{100,70,80,60\}=100,\\
		\text{State }S_2:\;&\max\{0,60,50,45\}=60,\\
		\text{State }S_3:\;&\max\{20,55,50,40\}=55.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Venue A</th><td>$100-100=0$</td><td>$60-0=60$</td><td>$55-20=35$</td><td>60</td></tr><tr><th scope="row">Venue B</th><td>$100-70=30$</td><td>$60-60=0$</td><td>$55-55=0$</td><td>30</td></tr><tr><th scope="row">Venue C</th><td>$100-80=20$</td><td>$60-50=10$</td><td>$55-50=5$</td><td>20</td></tr><tr><th scope="row">Venue D</th><td>$100-60=40$</td><td>$60-45=15$</td><td>$55-40=15$</td><td>40</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Venue C because it has the smallest maximum regret, $20$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Venue A</td></tr><tr><th scope="row">Maximin</th><td>Venue B</td></tr><tr><th scope="row">Minimax Regret</th><td>Venue C</td></tr></tbody></table></div>`
          }
        ]
      },
      {
        id: "supply-contract-3x4",
        problemType: "Applied",
        stateCount: "3",
        alternativeCount: "4",
        labels: { name: "Supply Contract", section: "Applied: 3 × 4" },
        descriptionHtml: String.raw`<p><em>All payoffs are in thousands of dollars. Regret = best payoff in the state − payoff.</em></p>
<p>A company must choose among Supply Contract A, Contract B, Contract C, and Contract D. Three states of nature represent different market and supply conditions. The final payoff table, in thousands of dollars, is given below. Use Maximax, Maximin, and Minimax Regret to select a supply contract.</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">State $S_1$</th><th scope="col">State $S_2$</th><th scope="col">State $S_3$</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>90</td><td>70</td><td>60</td></tr><tr><th scope="row">Contract B</th><td>80</td><td>50</td><td>40</td></tr><tr><th scope="row">Contract C</th><td>70</td><td>45</td><td>35</td></tr><tr><th scope="row">Contract D</th><td>75</td><td>55</td><td>50</td></tr></tbody></table></div>
<p><strong>Questions/Tasks.</strong></p>
<h4>Questions/Tasks</h4><ol><li><strong>C4:</strong> Apply the Maximin and Maximax criteria.</li><li><strong>C5:</strong> Construct an opportunity-loss table and apply the Minimax Regret criterion.</li></ol>`,
        solutionSections: [
          {
            title: "C4: Applying the Maximax and Maximin criteria",
            contentHtml: String.raw`$$
\begin{aligned}
		\max(\text{Contract A}) &= \max\{90,70,60\}=90,\\
		\max(\text{Contract B}) &= \max\{80,50,40\}=80,\\
		\max(\text{Contract C}) &= \max\{70,45,35\}=70,\\
		\max(\text{Contract D}) &= \max\{75,55,50\}=75.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\max(\text{Contract A}),\max(\text{Contract B}),
		\max(\text{Contract C}),\max(\text{Contract D})\}\\
		&\qquad=\max\{90,80,70,75\}
		=90.
	\end{aligned}
$$
<p>The Maximax choice is Contract A because it has the highest possible payoff.</p>
$$
\begin{aligned}
		\min(\text{Contract A}) &= \min\{90,70,60\}=60,\\
		\min(\text{Contract B}) &= \min\{80,50,40\}=40,\\
		\min(\text{Contract C}) &= \min\{70,45,35\}=35,\\
		\min(\text{Contract D}) &= \min\{75,55,50\}=50.
	\end{aligned}
$$
$$
\begin{aligned}
		&\max\{\min(\text{Contract A}),\min(\text{Contract B}),
		\min(\text{Contract C}),\min(\text{Contract D})\}\\
		&\qquad=\max\{60,40,35,50\}
		=60.
	\end{aligned}
$$
<p>The Maximin choice is Contract A because it has the largest worst-case payoff.</p>`
          },
          {
            title: "C5: Constructing the opportunity-loss table and applying Minimax Regret",
            contentHtml: String.raw`<p>Best payoff in each state:</p>
$$
\begin{aligned}
		\text{State }S_1:\;&\max\{90,80,70,75\}=90,\\
		\text{State }S_2:\;&\max\{70,50,45,55\}=70,\\
		\text{State }S_3:\;&\max\{60,40,35,50\}=60.
	\end{aligned}
$$
<p>Regret table (best payoff $ - $ payoff):</p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Alternative</th><th scope="col">$S_1$</th><th scope="col">$S_2$</th><th scope="col">$S_3$</th><th scope="col">Maximum regret</th></tr></thead><tbody><tr><th scope="row">Contract A</th><td>$90-90=0$</td><td>$70-70=0$</td><td>$60-60=0$</td><td>0</td></tr><tr><th scope="row">Contract B</th><td>$90-80=10$</td><td>$70-50=20$</td><td>$60-40=20$</td><td>20</td></tr><tr><th scope="row">Contract C</th><td>$90-70=20$</td><td>$70-45=25$</td><td>$60-35=25$</td><td>25</td></tr><tr><th scope="row">Contract D</th><td>$90-75=15$</td><td>$70-55=15$</td><td>$60-50=10$</td><td>15</td></tr></tbody></table></div>
<p>The Minimax Regret choice is Contract A because it has the smallest maximum regret, $0$. <strong>Decisions summary</strong></p>
<div class="table-card"><table class="data-table"><caption>Payoff, regret, or decision-analysis table</caption><thead><tr><th scope="col">Criterion</th><th scope="col">Final decision</th></tr></thead><tbody><tr><th scope="row">Maximax</th><td>Contract A</td></tr><tr><th scope="row">Maximin</th><td>Contract A</td></tr><tr><th scope="row">Minimax Regret</th><td>Contract A</td></tr></tbody></table></div>`
          }
        ]
      }
    ]
  };

  window.practiceData = practiceData;
})();
