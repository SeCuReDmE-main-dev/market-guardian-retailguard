# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Tamper-evident metadata ledger."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .events import EvidenceEvent, canonical_json


@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    event: EvidenceEvent
    previous_hash: str
    entry_hash: str

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "event": self.event.to_dict(),
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }


class EvidenceLedger:
    def __init__(self) -> None:
        self._entries: list[LedgerEntry] = []

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def append(self, event: EvidenceEvent) -> LedgerEntry:
        previous_hash = self._entries[-1].entry_hash if self._entries else "0" * 64
        sequence = len(self._entries) + 1
        entry_hash = _hash_entry(sequence, event, previous_hash)
        entry = LedgerEntry(sequence, event, previous_hash, entry_hash)
        self._entries.append(entry)
        return entry

    def verify(self) -> bool:
        previous_hash = "0" * 64
        for expected_sequence, entry in enumerate(self._entries, start=1):
            if entry.sequence != expected_sequence:
                return False
            if entry.previous_hash != previous_hash:
                return False
            if entry.entry_hash != _hash_entry(entry.sequence, entry.event, entry.previous_hash):
                return False
            previous_hash = entry.entry_hash
        return True


def _hash_entry(sequence: int, event: EvidenceEvent, previous_hash: str) -> str:
    payload = canonical_json(
        {
            "sequence": sequence,
            "event": event.to_dict(),
            "previous_hash": previous_hash,
        }
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
