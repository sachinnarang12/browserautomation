# AutomatePortal – Dual-Version Strategy

## Overview

AutomatePortal is the **sole intellectual property of Sachin Narang**, created
on personal time using personal resources.  Two editions exist:

| Aspect           | Version A (Employer)                 | Version B (Commercial)                   |
|------------------|--------------------------------------|------------------------------------------|
| Purpose          | Help employer's operations           | SaaS product sold on the market          |
| License          | `LICENSE-EMPLOYER` (limited-use)     | `LICENSE` (proprietary / commercial)     |
| Source code      | Shared (for employer customisation)  | Full source (your private repo)          |
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
│   ├── employer/                  # Version A config & launcher
│   │   ├── __init__.py
│   │   ├── config.py              # Employer branding
│   │   ├── run.py                 # Employer launcher
│   │   └── package_employer_edition.py  # Builds bytecode-only package
│   │
│   └── commercial/                # Version B config & launcher
│       ├── __init__.py
│       ├── config.py              # Commercial branding
│       └── run.py                 # Commercial launcher
│
├── LICENSE                        # Master proprietary license (KEEP PRIVATE)
├── LICENSE-EMPLOYER               # What the employer receives
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
- `employer`   → Version A (limited features)
- `commercial` → Version B (full features)  ← default

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
# Version A – Employer
AUTOMATEPORTAL_EDITION=employer python editions/employer/run.py

# Version B – Commercial (default)
python editions/commercial/run.py
```

---

## Packaging Version A for Your Employer

```bash
python editions/employer/package_employer_edition.py --output-dir ./dist
```

This produces:
- `dist/AutomatePortal-Employer/` — source code package
- `dist/AutomatePortal-Employer.zip` — ready to hand over

The package includes:
- Python source files (`.py`) so employer can refine per their needs
- HTML templates (UI)
- `LICENSE-EMPLOYER` (the limited-use license)
- `start.py` launcher
- `requirements.txt`

The package does NOT include:
- Commercial edition files
- Your roadmap, SaaS guides, or strategy docs
- License key generator
- Product documentation
- Your private licenses or strategy docs

---

## IP Protection Checklist

### Before Offering Version A to Employer
- [ ] Have employer sign `LICENSE-EMPLOYER` or equivalent agreement
- [ ] Document (in writing/email) that this is your personal project
- [ ] Check your employment agreement for IP clauses
- [ ] Consider having a lawyer review the license
- [ ] Keep records of your personal development (git history, timestamps)

### Ongoing Protection
- [ ] Employer receives source under `LICENSE-EMPLOYER` (limited-use, no resale)
- [ ] Your private repo has full source + git history (proof of authorship)
- [ ] Every source file has copyright header
- [ ] Keep the `LICENSE` and `DUAL_VERSION_STRATEGY.md` out of employer packages
- [ ] Commercial features are never compiled into employer packages

### Evidence of Independent Creation
Your git history serves as evidence. Maintain:
- Commits from your personal machine/account
- Timestamps outside work hours
- No employer resources referenced in commits
- This strategy document

---

## Revenue Model (Version B)

| Tier          | Tasks | Credentials | Users | Price Target |
|---------------|-------|-------------|-------|--------------|
| Trial         | 3     | 2           | 1     | Free (14d)   |
| Starter       | 5     | 3           | 1     | $29/mo       |
| Professional  | 25    | 15          | 5     | $99/mo       |
| Enterprise    | ∞     | ∞           | 25    | $299/mo      |

---

## What to Tell Your Employer

> "I've built a browser automation tool on my own time that can help with
> [specific operations problem]. I'm happy to provide a version for internal
> use under a license agreement. The software remains my intellectual property,
> and I retain all rights to develop and sell it commercially."

Key points:
1. You're offering help, not giving away your work
2. The license is clear about ownership
3. They get a useful tool; you keep your IP
4. Professional, transparent, and fair to both sides
