# Grade 11 — Term 1 — C1 Practice Activity 1 with Solutions

## Context Descriptions

1. A currency-management app monitors one scheduled dollar payment for a Colombian importer buying production inputs. By the deadline, the payment will either have executed or remain unexecuted; those are the only operational outcomes used by the app. The variable \(X_1\) records which occurs because a missed deadline could interrupt the shipment and require costly short-term finance.

2. An international e-commerce platform adjusts Colombian sellers' peso receipts for exchange-rate movements. For the adjustment \(X_2\), treasury policy limits the change to between negative 1.5 percent and positive 1.5 percent, and historical transactions provide no reason to expect one part of that range more often than another. Sellers use this information to test margins and choose an adequate currency-risk buffer.

3. A Colombian tourism platform presents the same local-experience package to exactly 60 eligible travellers. For every traveller it records whether the package is purchased, and previous groups recruited through the same channel have responded comparably. The variable \(X_3\) counts the buyers so the platform can reserve enough Bogotá guides without making unnecessary advance payments.

4. A Bogotá bicycle-share operator monitors breakdown reports on a fixed 20-kilometre network segment for one week. Each report concerns a separate incident, and operational records for ordinary weeks show incidents scattered through the segment and week without a recurring timetable. The variable \(X_4\) counts the reports in that period so the operator can position mechanics and spare parts without excess inventory.

5. A circular-economy venture in Kennedy bids for used appliances while preserving margin for parts, labour, and warranties. The resale price \(X_5\) has a practical minimum of COP 400,000 and maximum of COP 900,000, with COP 650,000 most common in the venture's records; prices occur less often nearer either extreme. This experience helps the buyer set a prudent inventory bid.

6. A digital lender reviews Colombian microbusiness applications until it approves the first loan for a pilot product. Analysts apply the same lending rule to successive applicants from one eligibility list and stop after the first approval; earlier lists assembled in this way have shown comparable approval experience. The variable \(X_6\) records how many applications are reviewed through that approval so the lender can budget underwriting time and acquisition cost.

7. A Bogotá cloud startup must reserve infrastructure for a client whose storage use can range from zero to 20 terabytes. Contract records show that the observed demand \(X_7\) becomes steadily more common as use rises across that range, without turning downward before the contractual cap. The startup uses this behavior to buy enough capacity while limiting the cost of unused resources.

8. A Colombian online retailer sends the same promotional offer to exactly 100 customers selected from a comparable group. For each customer, the retailer records whether a purchase is made, and previous campaigns using the same offer and customer-selection procedure have produced comparable purchase behavior. The variable \(X_8\) counts how many of the 100 customers make a purchase so the retailer can estimate the inventory required for the campaign.

9. A Colombian coffee exporter monitors moisture percentage \(X_9\) because unsuitable storage can reduce inventory value before shipment. Readings from bags handled under the usual process gather around 11 percent, show similar behavior below and above that typical level, and become increasingly scarce farther away. The exporter uses the pattern to prioritise inspections and protect export quality.

10. A Colombian food-delivery platform monitors order cancellations during a fixed two-hour dinner period in one delivery zone. Each cancellation concerns a separate order, and records from comparable evenings show cancellations occurring independently throughout the period without a recurring timetable. The variable \(X_{10}\) counts the cancellations during those two hours so the platform can estimate the number of additional couriers and customer-service staff required.

## Solutions: Characterization

| Context | Type | Distribution | Characterization |
|---:|---|---|---|
| 1 | Discrete | Bernoulli | There is one situation with exactly two possible outcomes: the payment executes or remains unexecuted. |
| 2 | Continuous | Uniform | The variable is bounded between negative 1.5 percent and positive 1.5 percent, with no part of the range expected more often than another. |
| 3 | Discrete | Binomial | The variable counts how many purchases occur across a fixed number of 60 comparable travellers. |
| 4 | Discrete | Poisson | The variable counts how many separate breakdown reports occur during a fixed period and exposure. |
| 5 | Continuous | Triangular | The variable has a practical minimum, a practical maximum, and one most common value between them. |
| 6 | Discrete | Geometric | The variable counts how many applications are required until the first approval occurs. |
| 7 | Continuous | Linear | The variable is bounded and becomes steadily more common as its value increases across the range. |
| 8 | Discrete | Binomial | The variable counts how many purchases occur across a fixed number of 100 comparable customers. |
| 9 | Continuous | Normal | Values gather around a typical level and become increasingly uncommon farther from that level on either side. |
| 10 | Discrete | Poisson | The variable counts how many separate cancellations occur during a fixed two-hour period. |