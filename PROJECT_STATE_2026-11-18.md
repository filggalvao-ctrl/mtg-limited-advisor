# MTG Limited Advisor - Project State

Last Updated: 2026-11-18

---

# Project Goal

Build a Limited Advisor for MTG (initially Star Trek / TRK).

NOT a deck builder.

NOT a Draftsim clone.

The advisor should:

- Analyze a candidate deck built by the player.
- Identify missed opportunities.
- Identify strong packages not being used.
- Identify weak cards occupying slots.
- Analyze splash opportunities.
- Explain trade-offs.
- Learn from Trophy decks and Draftsim recommendations.

The advisor should ASK QUESTIONS and RAISE WARNINGS.

The advisor should NOT simply say:

"Play this deck."

---

# Most Important Design Principle

Card Strength != Deck Strength

Examples observed:

- The Traveler can have excellent GIH WR but still be incorrect.
- Seven of Nine may have a lower GIH WR but fit a strategy better.
- Borg Cube may justify a splash because of its role.
- A package can be stronger than a single bomb.

Always evaluate plans, not just ratings.

---

# Current Database Schema

## KEEP

### card_metadata

Purpose:

What the card is.

Columns:

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

Rows:

311

---

### trk_ratings

Purpose:

17Lands performance metrics.

Rows:

336

Contains:

- card_name
- color
- rarity
- games_played
- gp_percent
- gp_wr
- gih_wr
- gns_wr
- iih

---

### pools

Purpose:

One Limited pool.

---

### pool_cards

Purpose:

Cards available in a pool.

---

### deck_events

Purpose:

Construction event.

Current Columns:

- id
- pool_id
- result_wins
- result_losses
- draftsim_score
- notes
- created_at

No player_deck or draftsim_deck columns anymore.

---

# Deleted Tables

Deleted intentionally:

- cards
- card_stats
- trophy_decks
- card_tags
- card_rules

Reason:

Created too early.

Need real examples first.

---

# Major Lessons Learned

## Lesson 1

Do not evaluate colors.

Evaluate plans.

Wrong:

Green strongest color.

Correct:

Green package strongest plan.

---

## Lesson 2

Splashability is NOT based only on mana cost.

Example:

The Traveler

Cost:
{G}{U}

Appears splashable.

Actually poor splash because:

- wants to be cast early
- wants both colors immediately
- loses value if cast late

---

## Lesson 3

Removal is often better splash material than threats.

Example:

He's Dead, Jim

Works equally well on turn 4, 6 or 8.

---

## Lesson 4

Need to evaluate card roles.

Examples:

The Traveler
→ Early Threat

He's Dead, Jim
→ Hard Removal

Borg Cube
→ Late Game Finisher

Perils of the Past
→ Pseudo Removal

---

## Lesson 5

Packages matter more than individual cards.

Examples seen:

RG Landfall Package

BR Death Trigger Package

WR Artifact / Spacecraft Package

The Advisor must detect packages.

---

# Important Example

Pool:

Contained:

- The Traveler
- Spock
- Vash

Draftsim:

9.8 RG Landfall

9.7 BR Death Triggers

Player:

7-1 WR splash B

The player ignored:

- The Traveler
- Spock
- Vash

but still achieved 7-1.

Conclusion:

High GIH WR cards do not automatically belong in the deck.

Need context.

---

# Borg Cube Lesson

Critical Example.

Do NOT evaluate Borg Cube as:

7 mana WB card.

Instead evaluate:

Role:

- Late Game Finisher
- Removal
- Threat

Because:

When entering or attacking it assimilates creatures.

Player likely splashed black for Borg Cube first.

Not for He's Dead Jim.

---

# Current Advisor Capabilities

Works:

- Pool parsing
- Lookup in card_metadata
- Lookup in trk_ratings
- Card ranking by GIH WR
- Artifact count
- Creature count
- Legendary count
- Bomb detection
- Color quality analysis

Status:

Prototype only.

---

# What NOT To Build Next

Do NOT create more metadata tables.

Do NOT create tags.

Do NOT create rules.

Do NOT add machine learning.

Do NOT add more schema until more examples are collected.

---

# Immediate Next Goal

Create storage for real-world examples.

Need:

Deck lists linked to:

- Pool
- Draftsim recommendation
- Draftsim score
- Result

Design still pending.

Need discussion BEFORE creating table.

---

# Advisor Future Behaviour

Input:

Pool

Player Deck

Output:

Questions.

Examples:

- Are you intentionally ignoring this package?
- Have you considered this splash?
- Why are you playing this low-rated card while stronger options remain?
- This package appears fully supported.
- This package appears incomplete.

The advisor must help review decisions.

The advisor must not build decks automatically.

---

# If You Resume This Project

First question:

"Before creating new tables, review PROJECT_STATE_2026-11-18.md and continue from there."

Second question:

"Design the storage model for Pool + Player Deck + Draftsim Deck + Result."

Do not start by creating more metadata.


---

# PROJECT STATE UPDATE - Limited Advisor Design

Date:
2026-11-19

---

# Critical Discovery

The project is NOT a deck builder.

The project is a Deck Auditor.

Input:

- Pool
- Candidate Deck

Output:

- Structural warnings
- Missing packages
- Alternative build paths
- Tradeoff analysis

The advisor should never replace the player.

It should challenge assumptions.

---

# Current Advisor Maturity

Already Working:

- card_metadata
- trk_ratings
- pool parsing
- card lookup
- GIH WR lookup
- color detection

Not Yet Working:

- package identification
- role identification
- structural deck analysis
- trophy knowledge

---

# Fundamental Construction Rules

These must become first-class rules inside the advisor.

## Rule 1

40 cards

Default:

23 spells
17 lands

Exceptions possible.

---

## Rule 2

Creature count

Typical range:

14-18 creatures

Alert outside range.

---

## Rule 3

Raw curve is misleading.

Need:

Functional Curve

Example:

De-evolve

Mana Cost:
2

Expected Play Turn:
4-6

Therefore:

Should not be counted as a true 2-drop.

---

## Rule 4

Evaluate:

Board Development Curve

Not:

Mana Curve

Example:

Tal Shiar Operative

TRUE 2-drop

De-evolve

FALSE 2-drop

---

## Rule 5

When replacing cards:

Role must be preserved.

Bad example:

Threat → Removal

Good example:

Removal → Removal

Threat → Threat

or

Threat lost compensated by large increase elsewhere.

---

# Major Discovery

Card Rating != Deck Rating

Card Strength != Deck Strength

Examples:

The Traveler
Borg Cube
Captain Benjamin Sisko
Seven of Nine
Tal Shiar Operative

---

# New Advisor Model

Before discussing cards:

Step 1

Validate Structure

- Lands
- Creatures
- Functional Curve

Step 2

Identify Main Color Packages

Example:

Green Value Package

Cards:

- Cleveland Booker
- Vash
- Species 8472
- Temporal Conqueror

Step 3

Identify Candidate Splashes

Example:

Blue Package:

- Marooned x3
- Constable Odo
- Humpback Whales

Red Package:

- Gowron
- Planetary Bombardment

White Package:

- Captain Benjamin Sisko
- Ghost of Illyria
- Primary Unimatrix Adjunct

---

# Package Evaluation Rule

Do NOT evaluate:

single cards.

Evaluate:

packages.

Question:

"This splash gives me what?"

Example:

Red

+ Gowron
+ Planetary Bombardment

Blue

+ Marooned x3
+ Constable Odo
+ Humpback Whales

White

+ Sisko
+ Ghost
+ Adjunct

---

# Requirements Concept

Cards do not only have strength.

Cards have requirements.

Examples:

Captain Benjamin Sisko

Requirements:

- dilemmas
- officers
- ideally WUBRG activation

---

Seven of Nine

Requirements:

- dilemma support

---

Primary Unimatrix Adjunct

Requirements:

- artifact creatures

---

Ghost of Illyria

Requirements:

- valuable ETB targets

---

Advisor must evaluate:

Requirements satisfied?

YES / NO

before recommending card.

---

# Splash Evaluation

Splashability is NOT mana cost.

Splashability is:

Mana Cost
+
Expected Play Turn
+
Role

Example:

The Traveler

Cost:
GU

Needs to be played early.

Poor splash candidate.

---

Borg Cube

Cost:
WB + 7 mana

Comes down very late.

Good splash candidate.

---

Removal

Single pip removal

Excellent splash candidate.

---

# Future Database Direction

Current Tables:

- card_metadata
- trk_ratings
- pools
- pool_cards
- deck_events

No additional schema should be created before reviewing real examples.

---

# Immediate Next Goal

Before creating new tables:

Design storage model for:

Pool
Player Deck
Draftsim Deck
Result

Need one model capable of:

- comparing paths
- identifying package inclusion
- tracking results

---

# Ultimate Advisor Question

Do not ask:

"What is the strongest card?"

Do not ask:

"What is the strongest color?"

Ask:

"What problem is the deck trying to solve?"

and

"What is the cost of this decision?"
Do not start by creating machine learning.
Do not start by creating tags.
