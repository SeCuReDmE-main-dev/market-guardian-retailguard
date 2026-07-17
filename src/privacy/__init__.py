# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Privacy and retention defaults."""

from .retention import ALLOWED_REVIEW_STATUSES, RetentionPolicy

__all__ = ["ALLOWED_REVIEW_STATUSES", "RetentionPolicy"]
