#!/usr/bin/env python3
"""
AutomatePortal – Standard Edition launcher
Sets the edition to 'standard' and starts a feature-limited instance.
"""

import os
import sys

# Force standard edition
os.environ["AUTOMATEPORTAL_EDITION"] = "standard"

# Ensure project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from agent_dashboard_v2 import app  # noqa: E402


def main():
    print("=" * 60)
    print("  AutomatePortal – Internal Edition")
    print("  Copyright (c) 2025-2026 Sachin Narang")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
