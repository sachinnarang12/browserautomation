# AutomatePortal – Dual-Version Strategy

## Overview

AutomatePortal is the **sole intellectual property of Sachin Narang**, created
on personal time using personal resources.  Two editions exist:

| Aspect           | Standard Edition                     | Commercial Edition                       |
|------------------|--------------------------------------|------------------------------------------|
| Purpose          | Internal operations                  | SaaS product sold on the market          |
| License          | `LICENSE` (MIT)                      | Proprietary / commercial                 |
| Source code      | Shared (for customisation)           | Full source (your private repo)          |
| Features today   | Everything EXCEPT licensing/billing  | Everything including licensing/billing   |
| Future features  | Frozen at what exists today          | Gets all new features (multi-tenant, marketplace, etc.) |
| Branding         | "AutomatePortal – Internal"          | "AutomatePortal"                         |
| Updates          | At your discretion                   | Continuous, paid tiers                   |

---

## Directory Structure

```
browserautomation/
├── core/                          # Shared engine (YOUR IP)
│   ├── __init__.py                # Version & copyright
│   └── edition.py                 # Feature flags per edition
│
├── editions/
│   ├── standard/                  # Standard edition config & launcher
│   │   ├── __init__.py
│   │   ├── config.py              # Standard branding
│   │   ├── run.py                 # Standard launcher
│   │   └── package_edition.py     # Builds distributable package
│   │
│   └── commercial/                # Commercial edition config & launcher
│       ├── __init__.py
│       ├── config.py              # Commercial branding
│       └── run.py                 # Commercial launcher
│
├── LICENSE                        # MIT license
├── DUAL_VERSION_STRATEGY.md       # This document (KEEP PRIVATE)
│
├── agent_dashboard_v2.py          # Dashboard (reads edition at runtime)
├── portal_automation_agent.py     # Core automation engine
├── credential_manager.py          # Credential vault
├── auth_manager.py                # Authentication
├── database.py                    # SQLite backend
├── license_manager.py             # License key system (commercial only)
└── ...
```

---

## How It Works

### Edition Detection
Set `AUTOMATEPORTAL_EDITION` environment variable:
- `standard`   → Standard edition (limited features)
- `commercial` → Commercial edition (full features)  ← default

### Feature Gating
`core/edition.py` defines an `EditionConfig` dataclass with boolean flags:

```python
from core.edition import get_config, require_feature

cfg = get_config()
if cfg.licensing_enabled:
    # show license page
    ...

# Or raise an error if feature isn't available:
require_feature('multi_tenant')
```

### Running Each Edition

```bash
# Standard Edition
AUTOMATEPORTAL_EDITION=standard python editions/standard/run.py

# Commercial Edition (default)
python editions/commercial/run.py
```

---

## Packaging the Standard Edition

```bash
python editions/standard/package_edition.py --output-dir ./dist
```

This produces:
- `dist/AutomatePortal-Standard/` — source code package
- `dist/AutomatePortal-Standard.zip` — ready to hand over

The package includes:
- Python source files (`.py`) for customisation
- HTML templates (UI)
- `LICENSE` (MIT)
- `start.py` launcher
- `requirements.txt`

The package does NOT include:
- Commercial edition files
- Your roadmap, SaaS guides, or strategy docs
- License key generator
- Product documentation
- Your private strategy docs

---

## IP Protection Checklist

### Before Sharing the Standard Edition
- [ ] Document (in writing/email) that this is your personal project
- [ ] Check your employment agreement for IP clauses
- [ ] Keep records of your personal development (git history, timestamps)

### Ongoing Protection
- [ ] Your private repo has full source + git history (proof of authorship)
- [ ] Every source file has copyright header
- [ ] Keep `DUAL_VERSION_STRATEGY.md` out of standard packages
- [ ] Commercial features are never included in standard packages

### Evidence of Independent Creation
Your git history serves as evidence. Maintain:
- Commits from your personal machine/account
- Timestamps outside work hours
- This strategy document

---

## Revenue Model (Commercial Edition)

| Tier          | Tasks | Credentials | Users | Price Target |
|---------------|-------|-------------|-------|--------------|
| Trial         | 3     | 2           | 1     | Free (14d)   |
| Starter       | 5     | 3           | 1     | $29/mo       |
| Professional  | 25    | 15          | 5     | $99/mo       |
| Enterprise    | ∞     | ∞           | 25    | $299/mo      |
