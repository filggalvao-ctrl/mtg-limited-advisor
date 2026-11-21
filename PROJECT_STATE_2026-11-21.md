# MTG Limited Advisor - Project State
Date: 2026-11-21

---

# Current Status

## Pool Analyzer

Status:

✅ Frozen v1.0

Purpose:

Answer:

"Where is the power in this pool?"

The Pool Analyzer is statistical only.

No deckbuilding advice.
No synergy analysis.
No package analysis.

Current Outputs:

- Pool Power Overview
- Candidate Color Pairs
- Multicolor Rewards
- Detailed Color Breakdown

---

# Pool Analyzer Rules

## Color Categories

- White
- Blue
- Black
- Red
- Green
- Colorless
- Lands
- Multicolor

---

## Quantities

Supported.

Example:

2 Kirk, Commanding Officer

counts as:

Qty = 2

Quantities affect:

- Premium Count
- Premium Strength
- Reward Strength
- Pair Scores

---

## Candidate Color Pairs

Current Logic:

Generate all 10 possible color pairs:

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

Pair Score:

Mono Strength Color A
+
Mono Strength Color B
+
Reward Strength

3+ color cards do not contribute.

Example:

Sarek, Federation Ambassador

Visible in Multicolor.

Does not affect Pair Score.

---

## Multicolor Rules

2-color cards:

Contribute to:

- Rewards
- Pair Score

3+ color cards:

Visible only.

No Pair Score contribution.

---

# Ratings Infrastructure

Status:

✅ Operational

Table:

trk_ratings

Source:

17Lands card-ratings export

Import Method:

UPSERT

Behavior:

If card exists:

UPDATE

If card does not exist:

INSERT

Unique Key:

card_name

Current Snapshot:

Updated from latest export.

Verified using:

Captain Jonathan Archer

Old:
66.9

Updated:
65.0

---

# Database Status

## card_metadata

Status:

✅ Loaded

Rows:

311

Contains:

- card_name
- mana_cost
- mana_value
- colors
- type_line
- rarity
- power
- toughness
- oracle_text
- is_creature
- is_artifact
- is_land
- is_legendary

---

## trk_ratings

Status:

✅ Loaded

Rows:

336

Current source:

Latest 17Lands export

---

# Deck Capture System

Status:

✅ MVP Operational

File:

app_deck_capture.py

Purpose:

Store historical deckbuilding decisions.

Data Collected Per Event:

- Pool
- Draftsim Recommendation
- Player Final Deck
- Draftsim Score
- Event Result
- Notes

---

# Tables

## pools

Fields:

- id
- pool_name
- source
- pool_text
- pool_power
- created_at

---

## pool_cards

Fields:

- id
- pool_id
- card_name
- quantity

---

## deck_events

Fields:

- id
- pool_id
- event_name
- draftsim_deck_text
- player_deck_text
- draftsim_score
- draftsim_deck_power
- player_deck_power
- result_wins
- result_losses
- notes
- created_at

---

## deck_lists

Fields:

- id
- deck_event_id
- deck_type
- card_name
- quantity

deck_type values:

- draftsim
- player

---

# Event Naming

Generated automatically.

Example:

Star Trek Sealed #001

Star Trek Sealed #002

Star Trek Sealed #003

---

# Data Retention Philosophy

Store:

- Pool
- Draftsim Deck
- Player Deck
- Result

Do NOT store:

- Sideboards

Reason:

Sideboards can always be reconstructed:

Pool
minus
Deck

---

# Power Metrics

## Draftsim Deck Power

Formula:

SUM(
GIH_WR × Quantity
)

All cards count.

Not only Premium cards.

---

## Player Deck Power

Formula:

SUM(
GIH_WR × Quantity
)

All cards count.

Not only Premium cards.

---

# First Real Event

Event:

Star Trek Sealed #001

Draftsim Score:

10.0

Draftsim Power:

1763.4

Player Power:

1485.9

Result:

7-1

Observation:

Player deck power significantly lower than Draftsim deck power.

Future objective:

Determine whether lower theoretical power is compensated by stronger deck construction.

---

# Current Priority

Collect real deckbuilding events.

Target:

20+
events

before building the first real Deck Advisor.

---

# Deck Advisor Vision

Not a deck builder.

Not intended to answer:

"Play these cards."

Intended to answer:

"Why is this card being played?"

Examples:

- Card requires dilemmas.
- Card requires artifact density.
- Card usually appears in specific archetypes.
- Draftsim recommendation differs from player choice.
- Historical evidence supports or contradicts inclusion.

---

# Future Dataset

Desired relationship:

Pool
↓
Draftsim Recommendation
↓
Player Deck
↓
Result

Repeated over many events.

Historical decisions become training data for:

- rule discovery
- package analysis
- splash analysis
- card support analysis
- future advisor explanations

---

# Freeze Decisions

Pool Analyzer:

✅ Frozen

Ratings Importer:

✅ Operational

Deck Capture:

✅ MVP Operational

Deck Advisor:

⏳ Not Started

Current focus:

Collect high-quality event data.
