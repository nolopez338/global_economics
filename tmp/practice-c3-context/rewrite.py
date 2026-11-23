from pathlib import Path
import re

target = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex')
old = Path('tmp/practice-c3-context/original.tex').read_text(encoding='utf-8')
s = old
replacements = {
    'Introductory example 1: clothing inventory': 'Introductory example 1: campus art-print stall',
    "Observe one shop's demand over one weekend. Let $E$ be high demand and\n$E^c$ low demand.": "Observe a student's art-print stall over one weekend. High demand means campus-market\nattendance meets the organizer's fixed target; low demand means it falls below that target.\nThese states cover every outcome and apply to either hypothetical print-batch choice.\nLet $E$ be high demand and\n$E^c$ low demand.",
    'A small order gives': 'After printing and stall costs, a small print batch gives',
    'a large order gives': 'a large print batch gives',
    'Introductory example 2: coffee-shop disruption': 'Introductory example 2: freelance livestream work',
    'Observe one coffee shop over one day. Let $E$ be an equipment disruption\nand $E^c$ no disruption.': 'Observe a freelancer hosting paid livestream sessions over one day. Let $E$ be a home-internet disruption\nand $E^c$ no disruption that day. These are the only states. Compare hypothetical choices:\nuse home internet alone or buy mobile data as backup. All payoffs are net gains or losses\nafter platform fees, data charges and refunds.',
    'Without backup,': 'With home internet alone,',
    'With a limited backup contract,': 'With mobile-data backup,',
    'high demand over one weekend.': 'high campus-market attendance over one weekend.',
    'equipment disruption over one day;': 'home-internet disruption over one day;',
    'low weekend demand.': 'campus-market attendance below its target that weekend.',
    'small- or large-order net profit': 'small- or large-batch net gain or loss',
    'net profit with or without backup': 'net gain or loss with or without mobile-data backup',
    '(small and large orders)': '(small and large print batches)',
    '(without backup and limited backup)': '(home internet alone and mobile-data backup)',
    "either order's monetary rule": "either print batch's monetary rule",
    "either backup strategy's monetary rule": "either internet choice's monetary rule",
    'for the small order,': 'for the small print batch,',
    'Clothing inventory for one weekend': 'Campus sticker sales for one weekend',
    "one clothing shop's net profit over one weekend": "a student's campus sticker sales over one weekend",
    'Coffee-shop service strategy': 'Campus fair or online CV workshop',
    "one coffee shop's net profit over one day": "a graduate's paid sessions over one day",
    'a busy day': 'the fair goes ahead',
    'a quiet day': 'the fair is cancelled',
    'seated service': 'portrait sessions',
    'quiet-day workshops': 'online CV workshop',
    'Renewable-energy sales contract': 'Freelance digital projects for one month',
    "one small solar producer's net profit over one month": "a freelancer's digital projects over one month",
    'a sunny month': 'high inquiry volume',
    'a cloudy month': 'low inquiry volume',
    'market sales': 'social-media graphics',
    'delivery contract': 'short video edits',
    'Manufacturing capacity investment': 'Graduation photography for one quarter',
    "one manufacturer's net profit over one quarter": "a graduate's photography work over one quarter",
    'a large order arrives': 'the ceremony goes ahead',
    'no large order arrives': 'the ceremony is cancelled',
    'existing equipment': 'basic photo package',
    'capacity investment': 'edited photo package',
    'Restaurant capacity: three alternatives, two states': 'Campus concert: three venue choices, two states',
    "one restaurant's net profit over one evening": "a student group's ticketed concert over one evening",
    'small room': 'small hired room',
    'medium room': 'student-union room',
    'large room': 'large hired room',
    'Agricultural planting: three individual break-even thresholds': 'Student fitness sessions: three break-even thresholds',
    "one farm plot's net profit over one growing season": "a student's paid fitness sessions over one university term",
    'unfavorable weather': 'low enrollment',
    'favorable weather': 'high enrollment',
    'hardy crop': 'walking group',
    'high-yield crop': 'dance sessions',
    'specialty crop': 'circuit sessions',
}
for a, b in replacements.items():
    assert a in s, a
    s = s.replace(a, b)

# Alternatives are choices under one common event, never additive income streams.
s = s.replace('All variables in a problem are functions of the same $X$;',
    'Each scenario compares hypothetical alternatives; choose one rather than running them together.\nAll monetary payoffs are net gains or losses after the relevant costs for the stated period.\nAll variables in a problem are functions of the same $X$;')


# Give each event an operational, exhaustive interpretation without changing any givens.
starts = {
    'Observe a student\'s campus sticker sales over one weekend.':
        " High demand means campus-market attendance meets the organizer's fixed target; low demand means it falls below that target. Compare a basic sticker pack with a premium pack printed more cheaply per sticker through a shared bulk order. These are alternative stall plans after printing and stall costs.",
    "Observe a graduate's paid sessions over one day.":
        ' A campus careers fair either goes ahead or is cancelled. Compare paid portraits at the fair with an online CV workshop. The fair brings portrait customers but draws students away from the workshop; cancellation reverses this effect. Payoffs include venue, platform, travel and refund costs.',
    "Observe a freelancer's digital projects over one month.":
        ' High inquiry volume means messages from potential clients meet a fixed monthly target; low inquiry volume means fewer messages. Compare offering social-media graphics with offering short video edits to the same client pool. Payoffs include software, platform and promotion costs.',
    "Observe a graduate's photography work over one quarter.":
        ' The university graduation ceremony either goes ahead or is cancelled during that quarter. Compare a basic photo package with a package including extra editing. Both involve the same advance preparation costs; the edited package earns more when the ceremony takes place. Payoffs include travel, software, preparation and refunds.',
    "Observe a student group's ticketed concert over one evening.":
        ' High demand means advance expressions of interest meet a fixed target; low demand means they fall below it. Compare hiring a small room, a discounted student-union room or a large room for the same concert. Payoffs include venue hire, performers, ticket fees and refunds.',
    "Observe a student's paid fitness sessions over one university term.":
        ' High enrollment means responses to a campus fitness-interest survey meet a fixed target; low enrollment means they fall below it. Compare a walking group, dance sessions or circuit sessions, using the same survey outcome for each hypothetical format. Payoffs include space hire, supplies, promotion and refunds.',
}
for a, extra in starts.items():
    assert s.count(a) == 1
    s = s.replace(a, a + extra)

# Make short state labels grammatical in the repeated problem and solution wording.
s = s.replace('probability of the fair goes ahead is', 'probability that the fair goes ahead is')
s = s.replace('Let $E$ be the fair goes ahead; $E^c$ is the fair is cancelled.',
              'Let $E$ be the fair going ahead; $E^c$ is its cancellation.')
s = s.replace('probability of the ceremony goes ahead is', 'probability that the ceremony goes ahead is')
s = s.replace('Let $E$ be the ceremony goes ahead; $E^c$ is the ceremony is cancelled.',
              'Let $E$ be the ceremony going ahead; $E^c$ is its cancellation.')

# Preserve the two weekend print scales in the introduction; rename only the
# sticker problem's alternatives, which have different original payoffs.
start = s.index(r'\subsection{Campus sticker sales for one weekend}')
end = s.index(r'\subsection{Campus fair or online CV workshop}')
block = s[start:end].replace('small order', 'basic sticker pack').replace('large order', 'premium sticker pack')
s = s[:start] + block + s[end:]

# Context-only edits must leave every literal number and every math fragment intact.
assert re.findall(r'\d+(?:\.\d+)?', old) == re.findall(r'\d+(?:\.\d+)?', s)
math = r'\$[^$]*\$|(?<!\\)\\\[.*?\\\]|\\begin\{(?:align\*?|equation\*?)\}.*?\\end\{(?:align\*?|equation\*?)\}'
assert re.findall(math, old, re.S) == re.findall(math, s, re.S)
target.write_text(s, encoding='utf-8', newline='\n')
print('Updated context; all literal numbers and math fragments match the original.')

