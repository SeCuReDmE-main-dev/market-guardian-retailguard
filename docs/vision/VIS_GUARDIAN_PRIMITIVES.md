# V.I.S Guardian Primitives

V.I.S Guardian converts visual facts into metadata-only primitives. The primitives are intentionally small so they can be scored, tested, and rejected without storing raw frames by default.

## Contour

Contour marks the boundary of an object or region. It helps distinguish shelf, basket, hand, item, and checkout zone changes.

## Motion

Motion captures visual change over time. It is useful for hand-to-shelf movement, basket movement, and checkout movement.

## Saliency

Saliency marks what the visual system should inspect more carefully. It is not proof; it is attention pressure.

## Occlusion

Occlusion records when the system cannot see enough. It increases indeterminacy instead of forcing a confident interpretation.

## Track Continuity

Track continuity measures whether one temporary `track_id` remains coherent. If continuity fails, the agent freezes and requests review.

## Object Permanence

Object permanence preserves a bounded hypothesis that an object may still exist while temporarily hidden. It must stay evidence-bound.

## Scene Contradiction

Scene contradiction records conflicts between visual evidence and other channels such as POS, inventory, basket state, or cash closeout.
