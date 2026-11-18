# MTG Limited Advisor

## Vision

This project is NOT intended to replace Draftsim.

The objective is to build a Limited Advisor capable of:

- analysing a Sealed pool;
- analysing a player-built deck;
- comparing decisions against Draftsim recommendations;
- learning from trophy players;
- identifying recurring patterns;
- explaining WHY a card should or should not be played.

The emphasis is on explanation and decision support rather than automatic deck construction.

---

# Core Philosophy

The system should not answer:

> "Play these 23 cards."

The system should answer:

> "This card is usually only played when supported by X."

> "This card is frequently splashed by trophy players."

> "This card has a strong rating but historically fails without specific support."

---

# Example

Card:

Collation Trimatrix

Draftsim Rating:
3.8

Observed Usage:

- Available in 48 pools
- Played in 9 decks
- Usually appears with high artifact density

Advisor Output:

"Collation Trimatrix normally appears in successful decks containing at least 7-8 relevant artifacts. The current build contains only 4."

---

# Data Sources

## 1. Card Metadata

Source:
- Scryfall

Purpose:
- define card characteristics
- identify colors
- identify artifacts
- identify creatures
- identify lands
- identify legendary permanents

Fields:

- card_name
- mana_cost
- mana_value
- colors
- type_line
- power
- toughness
- oracle_text
- rarity

---

## 2. 17Lands Data

Source:
- card-ratings export

Purpose:
- individual card strength

Important metrics:

- GIH WR
- GP WR
- GNS WR
- GP %
- ALSA
- ATA
- IIH

This table will be updated multiple times during the life of a set.

Historical snapshots should be preserved.

---

## 3. Trophy Deck Data

Source:
- 17Lands Trophy Decks
- Untapped profiles
- Manual collection

Purpose:
- discover real player behavior

Stored data:

Pool
Deck
Result

---

## 4. Draftsim Recommendations

Purpose:
- compare human decisions against automated recommendations

Stored:

- Score
- Suggested deck
- Individual card ratings (when available)

---

# Architectural Layers

## Layer 1

Facts

Examples:

The Traveler

- color identity
- mana value
- card type

Seven of Nine

- legendary creature
- Borg

---

## Layer 2

Statistics

Examples:

The Traveler

GIH WR = 61.5%

Seven of Nine

GIH WR = 49.1%

---

## Layer 3

Patterns

Examples:

Collation Trimatrix

Artifact Density >= 7

Confidence = 0.87

---

## Layer 4

Rules

Example:

IF

Artifacts < 7

THEN

Warn Player

---

## Layer 5

Advisor

Uses:

- Metadata
- Statistics
- Patterns
- Rules

Produces explanations.

---

# Current Database Tables

## cards

General card information.

---

## card_metadata

Per-set metadata.

Fields:

- card_name
- mana_cost
- mana_value
- colors
- type_line
- rarity
- power
- toughness
- oracle_text

---

## card_stats

General statistics.

---

## trk_ratings

17Lands statistics for Star Trek.

Fields:

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

## pools

Stores individual pools.

---

## pool_cards

Stores cards available in a pool.

---

## trophy_decks

Stores actual decks played.

---

## card_rules

Manually defined or automatically learned rules.

Example:

Collation Trimatrix

minimum_artifacts = 7

---

# Future Tables

## deck_events

Purpose:

Store complete deck building events.

Fields:

- pool_id
- player_name
- draftsim_score
- wins
- losses
- event_date

---

## deck_decisions

Purpose:

Compare player and Draftsim decisions.

Example:

Pool 1

Card:

Collation Trimatrix

Draftsim:
YES

Player:
NO

Result:
7-0

---

## learned_patterns

Purpose:

Automatically discovered patterns.

Examples:

Collation Trimatrix

Condition:

artifacts >= 8

Confidence:

0.87

---

The Traveler

Condition:

splashable

Confidence:

0.91

---

Seven of Nine

Condition:

improved_with_artifacts

Confidence:

0.72

---

# MVP Roadmap

## Phase 1 ✅

Infrastructure

- GitHub
- Streamlit
- Supabase

Completed.

---

## Phase 2 ✅

17Lands CSV Reader

Completed.

Current status:

- Loads 336 cards
- Parses correctly
- Cleans columns

---

## Phase 3

Import ratings into Supabase.

Goals:

- Persistent storage
- Historical snapshots

---

## Phase 4

Pool Analysis

Input:

Raw pool text

Output:

- Best individual cards
- Best colors
- Top GIH WR cards

---

## Phase 5

Trophy Deck Analysis

Goals:

- Track card inclusion rate
- Track splash frequency
- Track sideboard frequency

---

## Phase 6

Pattern Discovery

Examples:

- Requires artifacts
- Requires Borg density
- Usually splashed
- Requires removal support

---

## Phase 7

Advisor

Input:

Pool

Deck under consideration

Output:

Strengths

Weaknesses

Potential mistakes

Possible splashes

Suspicious inclusions

Cards with insufficient support

---

# Fundamental Project Principle

The system should never simply say:

"Play this card."

The system should explain:

WHY.

The goal is to learn from the repeated decisions of successful players and combine those decisions with 17Lands statistics to create a transparent and explainable Limited Advisor.
