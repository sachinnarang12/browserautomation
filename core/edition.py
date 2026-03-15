"""
Edition Configuration
---------------------
Controls which features are available in each product edition.

Standard    — core features, no licensing/billing
Commercial  — full product with licensing + future SaaS features

NOTE: Feature flags marked "future" are NOT yet implemented.  They exist as
placeholders so that when you build them, they are automatically gated to
the commercial edition.  Only `licensing_enabled` is actively enforced today.
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class Edition(Enum):
    STANDARD = "standard"       # Core feature set
    COMMERCIAL = "commercial"   # Full product


@dataclass(frozen=True)
class EditionConfig:
    """Feature flags and limits that vary per edition."""

    edition: Edition
    product_name: str
    product_tagline: str

    # ── Currently enforced ──────────────────────────────────────────
    licensing_enabled: bool = False       # license key system & tier limits

    # ── Currently implemented, same in both editions ────────────────
    user_management: bool = True          # /users page (exists today)
    api_access: bool = True               # /api/* endpoints (exist today)

    # ── Future – not yet built (gate when you implement them) ───────
    multi_tenant: bool = False
    custom_branding: bool = False
    template_marketplace: bool = False
    advanced_scheduling: bool = False     # cron-style (today is daily only)
    notifications_enabled: bool = False
    export_import: bool = False
    cloud_deployment: bool = False
    audit_logging: bool = False

    # Hard limits (only meaningful when licensing_enabled=True)
    max_tasks: int = 999999
    max_credentials: int = 999999
    max_users: int = 25

    # Branding
    primary_color: str = "#2563eb"
    logo_path: str = ""
    support_email: str = ""
    support_url: str = ""


# ── Edition definitions ──────────────────────────────────────────────

EDITIONS: Dict[Edition, EditionConfig] = {

    Edition.STANDARD: EditionConfig(
        edition=Edition.STANDARD,
        product_name="AutomatePortal – Internal",
        product_tagline="Internal browser automation tool",

        # Only real difference today: no licensing system
        licensing_enabled=False,

        # Everything that exists today stays enabled
        user_management=True,
        api_access=True,

        # Future features — will be commercial-only when built
        multi_tenant=False,
        custom_branding=False,
        template_marketplace=False,
        advanced_scheduling=False,
        notifications_enabled=False,
        export_import=False,
        cloud_deployment=False,
        audit_logging=False,

        primary_color="#2563eb",
        support_email="",
        support_url="",
    ),

    Edition.COMMERCIAL: EditionConfig(
        edition=Edition.COMMERCIAL,
        product_name="AutomatePortal",
        product_tagline="Automate any web portal – no code required",

        licensing_enabled=True,

        user_management=True,
        api_access=True,

        # Future features — commercial gets them when built
        multi_tenant=True,
        custom_branding=True,
        template_marketplace=True,
        advanced_scheduling=True,
        notifications_enabled=True,
        export_import=True,
        cloud_deployment=True,
        audit_logging=True,

        max_tasks=999999,     # governed by license tier
        max_credentials=999999,
        max_users=25,

        primary_color="#7c3aed",
        support_email="support@automateportal.com",
        support_url="https://automateportal.com/support",
    ),
}


def get_edition() -> Edition:
    """Determine the active edition from the AUTOMATEPORTAL_EDITION env var."""
    raw = os.environ.get("AUTOMATEPORTAL_EDITION", "commercial").lower().strip()
    try:
        return Edition(raw)
    except ValueError:
        return Edition.COMMERCIAL


def get_config() -> EditionConfig:
    """Return the feature configuration for the active edition."""
    return EDITIONS[get_edition()]


def require_feature(feature_name: str) -> bool:
    """
    Check whether a feature is enabled in the current edition.
    Raises RuntimeError if not.
    """
    cfg = get_config()
    if not getattr(cfg, feature_name, False):
        raise RuntimeError(
            f"Feature '{feature_name}' is not available in the "
            f"{cfg.product_name} edition."
        )
    return True
