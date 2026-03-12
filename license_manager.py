#!/usr/bin/env python3
"""
License Manager
Validates software licenses for AutomatePortal installations.
"""

import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path


# License signing secret — MUST be set via environment variable.
_LICENSE_SECRET = os.environ.get('AUTOMATEPORTAL_LICENSE_SECRET')
if not _LICENSE_SECRET:
    raise RuntimeError(
        "AUTOMATEPORTAL_LICENSE_SECRET environment variable is not set. "
        "Set it before starting the application (e.g. in your .env file)."
    )

LICENSE_FILE = Path('data/license.json')


class LicenseTier:
    TRIAL = 'trial'
    STARTER = 'starter'
    PROFESSIONAL = 'professional'
    ENTERPRISE = 'enterprise'


TIER_LIMITS = {
    LicenseTier.TRIAL: {
        'max_tasks': 3,
        'max_credentials': 2,
        'max_users': 1,
        'max_executions_per_month': 50,
        'label': 'Trial (14 days)',
    },
    LicenseTier.STARTER: {
        'max_tasks': 5,
        'max_credentials': 3,
        'max_users': 1,
        'max_executions_per_month': 100,
        'label': 'Starter',
    },
    LicenseTier.PROFESSIONAL: {
        'max_tasks': 25,
        'max_credentials': 15,
        'max_users': 5,
        'max_executions_per_month': 1000,
        'label': 'Professional',
    },
    LicenseTier.ENTERPRISE: {
        'max_tasks': 999999,
        'max_credentials': 999999,
        'max_users': 25,
        'max_executions_per_month': 10000,
        'label': 'Enterprise',
    },
}


def _sign(data: str) -> str:
    """Create an HMAC-SHA256 signature for license validation."""
    return hmac.new(
        _LICENSE_SECRET.encode(), data.encode(), hashlib.sha256
    ).hexdigest()[:16]


def generate_license_key(company: str, tier: str, days: int = 365) -> str:
    """
    Generate a license key.  Run this on YOUR machine to create keys for customers.

    Format:  AP-<TIER_CODE>-<EXPIRY>-<COMPANY_HASH>-<SIGNATURE>
    Example: AP-PRO-20270309-A3F2-8B4C1D2E
    """
    tier_codes = {
        LicenseTier.TRIAL: 'TRI',
        LicenseTier.STARTER: 'STR',
        LicenseTier.PROFESSIONAL: 'PRO',
        LicenseTier.ENTERPRISE: 'ENT',
    }
    code = tier_codes.get(tier, 'TRI')
    expiry = (datetime.now() + timedelta(days=days)).strftime('%Y%m%d')
    company_hash = hashlib.md5(company.lower().encode()).hexdigest()[:4].upper()
    payload = f'{code}-{expiry}-{company_hash}'
    sig = _sign(payload).upper()[:8]
    return f'AP-{payload}-{sig}'


def validate_license_key(key: str) -> dict:
    """
    Validate a license key and return its details.

    Returns dict with:  valid, tier, expires, company_hash, message
    """
    result = {
        'valid': False,
        'tier': LicenseTier.TRIAL,
        'expires': None,
        'days_remaining': 0,
        'message': '',
    }

    if not key or not key.startswith('AP-'):
        result['message'] = 'Invalid key format'
        return result

    parts = key.split('-')
    # Expected: AP - TIER - EXPIRY - COMPANY - SIGNATURE
    if len(parts) != 5:
        result['message'] = 'Invalid key format'
        return result

    _, tier_code, expiry_str, company_hash, sig = parts

    # Verify signature
    payload = f'{tier_code}-{expiry_str}-{company_hash}'
    expected_sig = _sign(payload).upper()[:8]
    if not hmac.compare_digest(sig, expected_sig):
        result['message'] = 'Invalid license key'
        return result

    # Check expiry
    try:
        expiry = datetime.strptime(expiry_str, '%Y%m%d')
    except ValueError:
        result['message'] = 'Invalid expiry date in key'
        return result

    days_remaining = (expiry - datetime.now()).days
    if days_remaining < 0:
        result['message'] = f'License expired {abs(days_remaining)} days ago'
        result['expires'] = expiry.isoformat()
        return result

    # Map tier code
    tier_map = {
        'TRI': LicenseTier.TRIAL,
        'STR': LicenseTier.STARTER,
        'PRO': LicenseTier.PROFESSIONAL,
        'ENT': LicenseTier.ENTERPRISE,
    }
    tier = tier_map.get(tier_code, LicenseTier.TRIAL)

    result['valid'] = True
    result['tier'] = tier
    result['expires'] = expiry.isoformat()
    result['days_remaining'] = days_remaining
    result['message'] = f'{TIER_LIMITS[tier]["label"]} - {days_remaining} days remaining'

    return result


def activate_license(key: str, company: str = '') -> dict:
    """Save license activation to disk."""
    validation = validate_license_key(key)
    if not validation['valid']:
        return validation

    license_data = {
        'key': key,
        'company': company,
        'tier': validation['tier'],
        'expires': validation['expires'],
        'activated_at': datetime.now().isoformat(),
    }

    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LICENSE_FILE, 'w') as f:
        json.dump(license_data, f, indent=2)

    validation['message'] = f'License activated! {validation["message"]}'
    return validation


def get_current_license() -> dict:
    """Load and validate the currently activated license."""
    if not LICENSE_FILE.exists():
        # No license = trial mode
        return {
            'valid': True,
            'tier': LicenseTier.TRIAL,
            'expires': (datetime.now() + timedelta(days=14)).isoformat(),
            'days_remaining': 14,
            'message': 'Trial mode - 14 days',
            'limits': TIER_LIMITS[LicenseTier.TRIAL],
        }

    with open(LICENSE_FILE, 'r') as f:
        data = json.load(f)

    validation = validate_license_key(data.get('key', ''))
    validation['company'] = data.get('company', '')
    validation['limits'] = TIER_LIMITS.get(validation['tier'], TIER_LIMITS[LicenseTier.TRIAL])
    return validation


def check_limit(resource: str, current_count: int) -> tuple:
    """
    Check if a resource limit has been reached.

    Args:
        resource: One of 'max_tasks', 'max_credentials', 'max_users', 'max_executions_per_month'
        current_count: Current count of the resource

    Returns:
        (allowed: bool, message: str)
    """
    license_info = get_current_license()
    limits = license_info.get('limits', TIER_LIMITS[LicenseTier.TRIAL])
    limit_value = limits.get(resource, 0)

    if current_count >= limit_value:
        tier_label = limits.get('label', 'current plan')
        return False, f'Limit reached ({current_count}/{limit_value}). Upgrade from {tier_label} for more.'

    return True, f'{current_count}/{limit_value}'


# ----- CLI for generating license keys -----
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('AutomatePortal License Manager')
        print('=' * 50)
        print()
        print('Usage:')
        print('  python license_manager.py generate <company> <tier> [days]')
        print('  python license_manager.py validate <key>')
        print('  python license_manager.py activate <key> [company]')
        print('  python license_manager.py status')
        print()
        print('Tiers: trial, starter, professional, enterprise')
        print()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'generate':
        company = sys.argv[2] if len(sys.argv) > 2 else 'TestCompany'
        tier = sys.argv[3] if len(sys.argv) > 3 else 'professional'
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 365
        key = generate_license_key(company, tier, days)
        print(f'License Key: {key}')
        print(f'Company:     {company}')
        print(f'Tier:        {tier}')
        print(f'Valid for:   {days} days')

    elif cmd == 'validate':
        key = sys.argv[2] if len(sys.argv) > 2 else ''
        result = validate_license_key(key)
        print(json.dumps(result, indent=2))

    elif cmd == 'activate':
        key = sys.argv[2] if len(sys.argv) > 2 else ''
        company = sys.argv[3] if len(sys.argv) > 3 else ''
        result = activate_license(key, company)
        print(result['message'])

    elif cmd == 'status':
        info = get_current_license()
        print(f'Tier:      {info.get("tier", "unknown")}')
        print(f'Expires:   {info.get("expires", "N/A")}')
        print(f'Remaining: {info.get("days_remaining", 0)} days')
        print(f'Status:    {info.get("message", "")}')
        if info.get('limits'):
            print(f'Limits:    Tasks={info["limits"]["max_tasks"]}, '
                  f'Creds={info["limits"]["max_credentials"]}, '
                  f'Users={info["limits"]["max_users"]}')
