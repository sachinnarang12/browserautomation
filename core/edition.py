"""
Edition Configuration
---------------------
Controls which features are available in each product edition.

Version A  (employer)   — limited, single-tenant, no licensing/billing
Version B  (commercial) — full SaaS product with licensing, multi-tenant, branding
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class Edition(Enum):
    EMPLOYER = "employer"       # Version A – provided to employer
    COMMERCIAL = "commercial"   # Version B – sold on the market


@dataclass(frozen=True)
class EditionConfig:
    """Feature flags and limits that vary per edition."""

    edition: Edition
    product_name: str
    product_tagline: str

    # Feature gates
    licensing_enabled: bool = False
    multi_tenant: bool = False
    user_management: bool = False
    api_access: bool = False
    custom_branding: bool = False
    template_marketplace: bool = False
    advanced_scheduling: bool = False
    notifications_enabled: bool = False
    export_import: bool = False
    cloud_deployment: bool = False
    audit_logging: bool = False

    # Hard limits
    max_tasks: int = 5
    max_credentials: int = 3
    max_users: int = 1

    # Branding
    primary_color: str = "#2563eb"
    logo_path: str = ""
    support_email: str = ""
    support_url: str = ""


# ── Edition definitions ──────────────────────────────────────────────

EDITIONS: Dict[Edition, EditionConfig] = {

    Edition.EMPLOYER: EditionConfig(
        edition=Edition.EMPLOYER,
        product_name="AutomatePortal – Internal",
        product_tagline="Internal browser automation tool",

        licensing_enabled=False,     # no license keys needed
        multi_tenant=False,
        user_management=False,       # single shared login
        api_access=False,
        custom_branding=False,
        template_marketplace=False,
        advanced_scheduling=False,   # basic daily schedule only
        notifications_enabled=False,
        export_import=False,
        cloud_deployment=False,
        audit_logging=False,

        max_tasks=10,
        max_credentials=5,
        max_users=1,

        primary_color="#2563eb",
        support_email="",
        support_url="",
    ),

    Edition.COMMERCIAL: EditionConfig(
        edition=Edition.COMMERCIAL,
        product_name="AutomatePortal",
        product_tagline="Automate any web portal – no code required",

        licensing_enabled=True,
        multi_tenant=True,
        user_management=True,
        api_access=True,
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
