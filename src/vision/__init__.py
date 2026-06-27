# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""V.I.S Guardian visual integrity primitives."""

from .continuity import TRACK_PURITY_FREEZE_THRESHOLD, TrackContinuityScore
from .events import VisualIntegrityEvent
from .neutro_bridge import visual_contradictions_to_divergence, visual_primitives_to_agent_evidence
from .primitives import VisualPrimitive, VisualPrimitiveKind

__all__ = [
    "TRACK_PURITY_FREEZE_THRESHOLD",
    "TrackContinuityScore",
    "VisualIntegrityEvent",
    "VisualPrimitive",
    "VisualPrimitiveKind",
    "visual_contradictions_to_divergence",
    "visual_primitives_to_agent_evidence",
]
