from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex')
s=p.read_text()
s=s.replace('All data are hypothetical. Each', 'All data are hypothetical. All monetary payoffs are net gains or losses after the stated costs. Each')
a=s.index('\\problemtitle{1}')
b=s.index('\\task{Task 1',a)
s=s[:a]+r'''\problemtitle{1}{Campus concert food stand or indoor games}{Complete}
A student club compares two hypothetical fundraising choices for one weekend: a food
stand at a campus outdoor concert or an indoor games afternoon. The concert either goes
ahead or is cancelled; initially, it goes ahead on three out of every eight weekends.
After food, room, equipment, and publicity costs as applicable, the food stand has a net
gain of USD 105 if the concert goes ahead and a net loss of USD 45 if it is cancelled.
The games afternoon has a net loss of USD 30 if the concert goes ahead, because it draws
potential players away, and a net gain of USD 90 if it is cancelled, because students
seek an indoor alternative. Only one option would be chosen; both use the same concert outcome.

'''+s[b:]
s=s.replace("One observation is the business's outcome over one weekend.", "One observation is the club's net outcome over one weekend for the chosen option.")
s=s.replace('Let $E$ be high demand and $E^c$ low demand; exactly one occurs.', 'Let $E$ be the concert going ahead and $E^c$ its cancellation; exactly one occurs.',1)
s=s.replace('festival stall net profit','food stand net profit').replace('studio net profit','games afternoon net profit')
s=s.replace('a stall loss','a food stand loss').replace('a studio loss','a games afternoon loss')
s=s.replace('The stall has','The food stand has').replace('The studio has','The games afternoon has')
a=s.index('\\problemtitle{2}')
b=s.index('\\task{Task 1',a)
s=s[:a]+r'''\problemtitle{2}{Graduation photo booth options}{Scaffolded}
A student photographer compares two hypothetical photo booth options for one graduation
weekend: a simple backdrop or a decorated set. Advance bookings either meet the advertised
target or fall short; initially, the target is met on two out of every seven weekends.
After equipment hire, decorations, printing, and travel costs as applicable, the simple
backdrop has a net gain of USD 72 if the target is met and a net loss of USD 24 otherwise.
The decorated set has a net gain of USD 126 if the target is met and a net loss of USD 54
otherwise: it attracts higher-priced bookings but costs more to prepare. Only one option
would be chosen; both are modelled using the same booking-target outcome.

'''+s[b:]
s=s.replace("One observation is the bookstall's outcome over one weekend.", "One observation is the photographer's net outcome over one graduation weekend.")
s=s.replace('Let $E$ be high demand and $E^c$ low demand; exactly one occurs.', 'Let $E$ be meeting the booking target and $E^c$ falling short; exactly one occurs.')
s=s.replace('both policies use the same $X$', 'both options use the same $X$')
s=s.replace('compact-stock','simple-backdrop').replace('expanded-stock','decorated-set')
s=s.replace('Compact stock has','The simple backdrop has').replace('Expanded stock has','The decorated set has')
a=s.index('\\problemtitle{3}')
s=s[:a]+r'''\problemtitle{3}{Campus portraits or an online CV workshop}{Core: service}
A recent graduate compares two hypothetical freelance activities for one day: campus
portrait sessions or an online CV workshop. The university's orientation day either goes
ahead or is cancelled; initially, it goes ahead on three out of every five days considered.
After equipment, software, and advertising costs as applicable, portraits have a net gain
of USD 84 if orientation goes ahead and a net loss of USD 36 if it is cancelled. The CV
workshop has a net loss of USD 48 if orientation goes ahead, since potential participants
are busy on campus, and a net gain of USD 72 if it is cancelled, since they are free to
attend online. Only one activity would be chosen; both use the same orientation outcome.

\problemtitle{4}{Meal preparation in a shared kitchen}{Core: sales}
Housemates compare two hypothetical plans for a small meal-preparation side business over
one month: disposable food boxes or reusable containers. Monthly subscriptions either
meet their advertised target or fall short; initially, the target is met in two out of
every five months. After ingredients, packaging, kitchen use, and cleaning costs as
applicable, the disposable-box plan has a net gain of USD 98 if the target is met and a
net loss of USD 42 otherwise. The reusable-container plan has a net gain of USD 70 if the
target is met and a net loss of USD 70 otherwise, reflecting its container and cleaning
costs. Only one plan would be chosen; both use the same subscription-target outcome.

\problemtitle{5}{Freelance video editing equipment}{Core: capacity}
A freelance video editor compares two hypothetical equipment choices over one quarter:
a personal laptop or a workstation rented only when a large project is confirmed.
A large project either arrives or does not arrive; initially, one arrives in four out
of every nine quarters. After software, promotion, and any equipment rental costs, the
laptop option has a net gain of USD 150 with the project and a net loss of USD 75 without
it. The workstation option has a net gain of USD 375 with the project, because faster
editing allows more paid deliverables, and a net loss of USD 75 without it, when no
workstation is rented. Only one option would be chosen; both use the same project outcome.

\problemtitle{6}{First-job event shifts}{Extension: precision}
A young adult compares two hypothetical job offers for one paid shift during a week:
catering work or ticket-desk work at the same event. The event either is cancelled or
goes ahead; initially, cancellation occurs in five out of every twelve weeks. After
transport bookings and required preparation costs, the catering offer has a net loss of
USD 27.50 if the event is cancelled and a net gain of USD 82.50 if it goes ahead. The
ticket-desk offer has a net loss of USD 45 if it is cancelled and a net gain of USD 67.50
if it goes ahead. Cancellation means no shift pay, but preparation and booked transport
still cost money. Only one offer would be accepted; both use the same weekly event outcome.
The decimal amounts are exact.

\problemtitle{7}{Online tutoring or an offline study workshop}{Extension: relabelling}
A student tutor compares two hypothetical choices for a scheduled revision weekend within
one month: online tutoring from a shared apartment or an offline study workshop at a
nearby library. The apartment building's internet either is interrupted during that
weekend or remains uninterrupted; initially, an interruption occurs in seven out of every
twenty months. After preparation, advertising, internet, and room-booking costs as
applicable, online tutoring has a net loss of USD 64 with interruption and a net gain of
USD 96 with uninterrupted service. The offline workshop has a net gain of USD 112 with
interruption, as affected students seek help at the library, and a net loss of USD 28
with uninterrupted service, when too few attend. Only one option would be chosen; both
use the same monthly internet outcome. For each option, also express net profit as a
constant plus a coefficient times an indicator that equals one for uninterrupted service
and zero for interruption. Express its expected net profit in terms of the probability of
uninterrupted service, which is one minus the interruption probability; find the exact
break-even probability of uninterrupted service and calculate its initial expected net profit
under this relabelling. Use the interruption probability on the horizontal axis of both
expected-value graphs.

\end{document}
'''
p.write_text(s)
