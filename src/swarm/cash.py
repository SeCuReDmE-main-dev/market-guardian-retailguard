# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""End-of-day cash/POS reconciliation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CashCloseResult:
    expected_cash: float
    counted_cash: float
    threshold: float = 100.0

    @property
    def mismatch(self) -> float:
        return round(self.counted_cash - self.expected_cash, 2)

    @property
    def requires_review(self) -> bool:
        return abs(self.mismatch) >= self.threshold


class CashCloseAgent:
    def reconcile(self, *, expected_cash: float, counted_cash: float, threshold: float = 100.0) -> CashCloseResult:
        if threshold < 0:
            raise ValueError("threshold must be >= 0")
        return CashCloseResult(
            expected_cash=round(float(expected_cash), 2),
            counted_cash=round(float(counted_cash), 2),
            threshold=round(float(threshold), 2),
        )
