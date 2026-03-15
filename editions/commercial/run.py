#!/usr/bin/env python3
"""
AutomatePortal – Commercial Edition launcher (Version B)
Sets the edition to 'commercial' and starts the full-featured product.
"""

import os
import sys

# Force commercial edition
os.environ["AUTOMATEPORTAL_EDITION"] = "commercial"

# Ensure project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from agent_dashboard_v2 import app  # noqa: E402


def main():
    print("=" * 60)
    print("  AutomatePortal – Commercial Edition")
    print("  Copyright (c) 2025-2026 Sachin Narang")
    print("  All rights reserved.")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
