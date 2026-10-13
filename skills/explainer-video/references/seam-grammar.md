# Seam Grammar

The motion rules that separate "designed" from "animated slides". Adapted from the film-grammar practices of the code-rendered video community.

## The seam law (vector law)
How scene A exits determines how scene B enters:
- **Same axis, same direction, matched speed.** X stays X, Y stays Y, Z stays Z. Never mirror direction across a cut.
- **Cut mid-motion on both sides.** A exits accelerating (fastest at the cut); B enters already in flight (≥50% along its entry path). Settling to rest before a cut, or starting from rest after it, is a dead beat.
- **Cross-dissolves between scenes are banned.** A crossfade hands nothing to the eye; use a carrier instead.

## The current (one dominant direction)
Pick ONE vector for all ordinary seams (e.g. push-through Z for "going deeper", or LEFT for "next beat"). Reserve other vectors for meaning: upward = elevation/reveal, Z-backward = arrival, scale-burst = leaving a world. A direction change needs a visible cause (a click, an impact) or a chapter boundary. Never ping-pong.

## Carriers
The eye follows objects, not abstractions. Hand a concrete carrier across every cut at matched position AND velocity: a cursor mid-flight, a card that docks into the next layout, a keyword that flies into its slot.

## Causal chains
Chain motion so each move is visibly launched by the last: click → squash → spring release → flight → impact → recoil → reveal. Effects start ON the causing frame, never "shortly after". Reactions scale with implied mass (big elements rebound slower).

## The oversized cursor
A deliberately oversized pointer (~7% of frame width) is the cheapest high-yield motion source: it enters **from off-screen** (never fades in), walks the eye to the next point of interest, and its click ignites the next beat.

## Waterfall text entry
Keyword typography cascades word-by-word with matched-velocity handoffs — never fades in as a block. Pre-roll entries ~0.15s so text is mid-cascade exactly at cuts.

## Banned list (template smell)
No bouncy easing, no particle bursts, no glows/neon, no RGB split, no lens flares, no gradients on UI chrome, no flashing backgrounds, no idle wobble (motion must perform, not breathe). Stillness is allowed only right before a climax beat.

## Motion physics
Closed-form spring step responses with slight overshoot for all element motion. Linear and CSS-style eases are banned for moving elements.
