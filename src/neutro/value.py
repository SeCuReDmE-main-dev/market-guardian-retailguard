# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Bounded Neutro value primitives."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _bounded(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    normalized = float(value)
    if not isfinite(normalized):
        raise ValueError(f"{name} must be finite")
    if not 0.0 <= normalized <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return normalized


@dataclass(frozen=True)
class NeutroValue:
    """Bounded system truth, indeterminacy, and falsity."""

    T_system: float
    I_system: float
    F_system: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "T_system", _bounded(self.T_system, "T_system"))
        object.__setattr__(self, "I_system", _bounded(self.I_system, "I_system"))
        object.__setattr__(self, "F_system", _bounded(self.F_system, "F_system"))

    @property
    def contradiction(self) -> float:
        """Local surface where support and conflict coexist."""

        return min(self.T_system, self.F_system)

    def to_dict(self) -> dict[str, float]:
        return {
            "T_system": self.T_system,
            "I_system": self.I_system,
            "F_system": self.F_system,
            "contradiction": self.contradiction,
        }


@dataclass(frozen=True)
class LocalTension:
    """A bounded dF contribution from one conflicting relation."""

    relation: str
    dF: float

    def __post_init__(self) -> None:
        if not self.relation:
            raise ValueError("relation is required")
        object.__setattr__(self, "dF", _bounded(self.dF, "dF"))

    def to_dict(self) -> dict[str, float | str]:
        return {"relation": self.relation, "dF": self.dF}


@dataclass(frozen=True)
class FractalComplexity:
    """Normalized D_f_hat complexity for an event or agent graph."""

    D_f_hat: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "D_f_hat", _bounded(self.D_f_hat, "D_f_hat"))

    def to_dict(self) -> dict[str, float]:
        return {"D_f_hat": self.D_f_hat}
