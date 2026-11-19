# MTG Limited Advisor - Project State V2

Last Updated:
2026-11-19

---

# Project Goal

Build a Limited Advisor for MTG Limited (starting with Star Trek / TRK).

Do NOT build a Draftsim clone.

Do NOT build an automatic Deck Builder.

Build a:

DECK AUDITOR

that explains:

- where the power is
- what packages exist
- what may have been overlooked
- tradeoffs between decisions

---

# Advisor Architecture

Two completely separate advisors.

## Advisor 1

Pool Analyzer

Input:

Pool Only

Output:

- Power Map
- Color Analysis
- Multicolor Rewards
- Candidate Color Pairs

No deck construction.

No trophy learning.

No curve analysis.

Purpose:

Identify where the strength of the pool lies.

---

## Advisor 2

Deck Reviewer

Input:

Pool
+
Candidate Deck

Output:

- Curve warnings
- Missing power
- Ignored packages
- Splash analysis
- Tradeoff analysis

Will eventually use:

- Trophy Decks
- Draftsim recommendations
- Results

---

# Current Database

Keep:

## card_metadata

Purpose:

What is the card?

Contains:

- mana_cost
- mana_value
- colors
- type_line
- oracle_text
- rarity
- is_creature
- is_artifact
- is_land
- is_legendary

Rows:

311

---

## trk_ratings

Purpose:

17Lands data

Contains:

- GIH WR
- GP WR
- GNS WR
- IIH
- Play Rate

Rows:

336

---

## pools

Purpose:

Store sealed pools

---

## pool_cards

Purpose:

Store cards belonging to pools

---

## deck_events

Purpose:

Future deck review events

Contains:

- pool_id
- result_wins
- result_losses
- draftsim_score
- notes

No deck list stored here.

---

# Pool Analyzer Logic

Analysis Order:

## Step 1

Power Distribution

By color.

Question:

Where is the power?

---

## Step 2

Multicolor Rewards

Question:

What rewards do I receive if I combine colors?

Examples:

BG
→ Vash
→ Cleveland Booker

BR
→ Gowron

UB
→ Seven of Nine

---

## Step 3

Candidate Color Pairs

Question:

Which color combinations deserve exploration?

Only use:

Two-color rewards

DO NOT use:

3+ color cards

---

# Current Visual Model

Columns:

⚪ White

🔵 Blue

⚫ Black

🔴 Red

🟢 Green

◇ Colorless

🏞 Lands

🌈 Multicolor

---

# Color Categories

## Monocolor

Contributes to color strength.

---

## Multicolor (2 colors)

Contributes to reward analysis.

Example:

BG Reward:

Vash
Booker

---

## Multicolor (3+ colors)

Visible only.

No scoring.

Example:

Sarek

---

## Colorless

Cards with:

colors = empty

and

is_land = false

Examples:

Warp Core
Tricorder
Automated Warfare System

Do NOT contribute to color strength.

---

## Lands

Cards with:

is_land = true

Examples:

Andoria
Risa
Temple Garden

Do NOT contribute to color strength.

---

# Major Discoveries

## Discovery 1

Card Strength != Deck Strength

---

## Discovery 2

Package Strength > Individual Card Strength

---

## Discovery 3

Splashability != Mana Cost

Examples:

The Traveler

Poor splash despite GU cost.

---

Borg Cube

Good splash despite expensive cost.

---

## Discovery 4

Cards have requirements.

Examples:

Seven of Nine

Requires:

Dilemmas

---

Captain Benjamin Sisko

Requires:

Dilemmas
Officers

---

Primary Unimatrix Adjunct

Requires:

Artifact Creatures

---

Ghost of Illyria

Requires:

Strong ETB targets

---

# Current Pool Analyzer Success Criteria

When opening a pool the user should immediately answer:

1. What is my strongest color?

2. What is my second strongest color?

3. What multicolor rewards exist?

4. Which color pairs deserve exploration?

Without looking at Draftsim.

---

# Current State of Code

Pool Analyzer exists.

Visual layout approved.

Need refactor.

Current issues:

- Candidate Color Pairs implementation unstable
- Colorless and Lands not yet separated
- Multicolor 3+ still pollutes pair logic

Need:

Clean V2 rewrite.

---

# Next Coding Session

Do NOT continue patching app.py.

Create clean:

app_v2.py

Goals:

- White
- Blue
- Black
- Red
- Green
- Colorless
- Lands
- Multicolor

- Candidate Color Pairs
- Multicolor Rewards

using correct classification.

No Deck Review work yet.

Pool Analyzer first.
