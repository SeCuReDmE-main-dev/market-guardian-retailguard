# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Privacy and retention defaults."""

from .retention import ALLOWED_REVIEW_STATUSES, RetentionPolicy

__all__ = ["ALLOWED_REVIEW_STATUSES", "RetentionPolicy"]
