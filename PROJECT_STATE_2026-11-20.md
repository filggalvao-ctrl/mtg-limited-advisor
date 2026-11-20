# MTG Limited Advisor - Project State
Date: 2026-11-20

---

# Project Status

## Pool Analyzer

Status:

✅ FROZEN v1.0

The Pool Analyzer is considered feature-complete and stable.

Purpose:

```text
Answer one question only:

"Where is the power in this pool?"
```

The Pool Analyzer is intentionally statistical and not intelligent.

It must never:

- Recommend a deck
- Recommend colors
- Recommend splashes
- Evaluate curve
- Evaluate creature count
- Detect packages
- Detect synergies
- Critique deck construction

Those responsibilities belong exclusively to the Deck Advisor.

---

## Deck Advisor

Status:

⏳ Not Started

Purpose:

```text
Answer:

"Does this deck make sense?"
```

Input:

- Full Pool
- Deck List

Output:

- Curve analysis
- Creature count analysis
- Splash analysis
- Missed opportunities
- Package detection
- Synergy detection
- Tradeoff analysis
- Sideboard recommendations

---

# Architecture Rule

Critical design decision:

```text
Pool Analyzer
≠
Deck Advisor
```

They are separate tools.

The Pool Analyzer must never grow into a deck-building advisor.

The Deck Advisor must never replace the Pool Analyzer.

---

# Pool Analyzer Scope

Input:

```text
Raw sealed pool
```

Example:

1 Ghost of Illyria

3 Pet Sehlat

2 Shuttle Ace

1 The Duras Sisters

2 Kirk, Commanding Officer

...

---

Output Sections

## 1. Pool Power Overview

Displays:

- Color
- Premium Count
- Premium Strength
- Best Cards

Purpose:

```text
Show where the power is concentrated.
```

No interpretation.

No recommendations.

No deck suggestions.

---

## 2. Candidate Color Pairs

Displays:

- Pair
- Premiums
- Reward Strength
- Total Pair Score
- Key Cards

Purpose:

```text
Identify color pair rewards present in the pool.
```

Current Version:

Only pairs with actual multicolor rewards appear.

Examples:

```text
B,R
B,G
R,W
G,W
```

Potential future enhancement:

Show all ten pairs.

Not implemented.

---

## 3. Multicolor Rewards

Displays:

All multicolor cards found in pool.

Purpose:

```text
Show rewards for opening additional colors.
```

Examples:

```text
Daniels, Temporal Agent
The Duras Sisters
Sarek, Federation Ambassador
```

---

## 4. Detailed Color Breakdown

Display:

Top 4 cards per category.

Categories:

```text
White
Blue
Black
Red
Green
Colorless
Lands
Multicolor
```

Purpose:

```text
Quick visual inspection.
```

---

# Category Rules

## White

Monowhite cards only.

---

## Blue

Monoblue cards only.

---

## Black

Monoblack cards only.

---

## Red

Monored cards only.

---

## Green

Monogreen cards only.

---

## Colorless

Everything with no color identity that is not a land.

Examples:

```text
Tricorder
Cybernetic Specialist
U.S.S. Cerritos, Following Up
```

---

## Lands

All lands.

Examples:

```text
Andoria
Risa
Temple Garden
Unexplored Territory
```

---

## Multicolor

All cards with more than one color.

Examples:

```text
Daniels, Temporal Agent
The Duras Sisters
Kirk, Commanding Officer
Phlox, Unorthodox Doctor
Sarek, Federation Ambassador
```

---

# Multicolor Logic

## Two-color cards

Eligible for:

- Multicolor Rewards
- Candidate Color Pairs
- Pair Score

Examples:

```text
B,R
B,G
R,W
G,W
```

---

## Three-color cards

Visible only.

Not eligible for:

- Candidate Pair Score
- Reward Strength
- Candidate Pair Calculations

Example:

```text
Sarek, Federation Ambassador
G,U,W
```

Behavior:

```text
Appears in Multicolor

Does NOT affect Pair Scores
```

---

## Four-color cards

Visible only.

No Pair Score contribution.

---

## Five-color cards

Visible only.

No Pair Score contribution.

---

# Quantity Handling

17Lands export format:

Example:

```text
3 Pet Sehlat
2 Shuttle Ace
2 Kirk, Commanding Officer
```

The quantity value must be respected.

---

## Quantity affects

### Premium Count

Example:

```text
3 copies of premium card

Counts as:

3 Premiums
```

---

### Premium Strength

Example:

```text
60.9 GIH card

3 copies

Result:

60.9 × 3
```

---

### Reward Strength

Example:

```text
3x The Duras Sisters

Reward Strength:

60.9 × 3
```

---

### Pair Scores

Example:

```text
2 copies of a reward card

Contribute twice.
```

---

## Quantity Display

Detailed Breakdown shows:

```text
2x Shuttle Ace
3x Pet Sehlat
```

instead of duplicate rows.

---

# Premium Definition

Current thresholds:

## S

```text
>= 60
```

---

## A

```text
58 - 59.9
```

---

## B

```text
55 - 57.9
```

---

## C

```text
52 - 54.9
```

---

## D

```text
< 52
```

---

Only:

```text
S
A
B
```

count as Premium.

---

# Bugs Fixed During Freeze

## Lands vs Artifacts

Old behavior:

```text
All colorless cards mixed together.
```

New behavior:

```text
Colorless
+
Lands
```

Separate categories.

---

## Tricolor Pair Score Pollution

Old behavior:

```text
GUW
BRU
WUBRG

could affect Pair Scores.
```

New behavior:

```text
Only exact two-color cards
affect Pair Scores.
```

---

## Quantity Parsing

Old behavior:

```text
2 Kirk, Commanding Officer

counted as:

1 copy.
```

New behavior:

```text
Quantity fully supported.
```

---

## Breakdown Readability

Old behavior:

```text
Entire color pools displayed.
```

New behavior:

```text
Top 4 cards only.
```

---

# Known Future Ideas

These are NOT part of Pool Analyzer v1.0.

## Candidate Pair Expansion

Potential future version:

Always display:

```text
WU
WB
WR
WG
UB
UR
UG
BR
BG
RG
```

even if no reward exists.

Status:

Not implemented.

---

## Export Analysis

Potential:

```text
Export pool report.
```

Status:

Not implemented.

---

# Deck Advisor Requirements

Must be implemented separately.

Input:

```text
Pool
+
Deck
```

Future responsibilities:

## Curve Analysis

Examples:

```text
Too many 2-drops
Too few 4-drops
```

---

## Creature Analysis

Examples:

```text
14 creatures
18 creatures
```

compare to Limited targets.

---

## Splash Analysis

Examples:

```text
Splash worth it
Splash not worth it
```

---

## Package Detection

Examples:

```text
ETB Package

Dilemma Package

Officer Package

Artifact Package
```

---

## Missed Opportunities

Examples:

```text
You left Daniels in sideboard.

You ignored a strong BG reward.

You have ETB support available.
```

---

# Freeze Decision

Pool Analyzer is now considered:

```text
Frozen v1.0
```

Further work should focus on:

```text
Deck Advisor
```

without modifying Pool Analyzer behavior.
