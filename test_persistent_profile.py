#!/usr/bin/env python3
"""
Test script to verify persistent browser profile works.

Usage:
  Step 1 - Create profile (opens browser, you log in manually):
    python test_persistent_profile.py --setup

  Step 2 - Verify profile reuses session (should skip login):
    python test_persistent_profile.py --verify
"""

import os
import sys
from pathlib import Path

TEST_URL = "https://the-internet.herokuapp.com/login"
PROFILE_DIR = str(Path(__file__).parent / "test_browser_profile")


def setup_profile():
    """Open browser for manual login and save the profile."""
    from nova_act import NovaAct

    Path(PROFILE_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Opening browser to: {TEST_URL}")
    print(f"Profile will be saved to: {PROFILE_DIR}")
    print()
    print("Instructions:")
    print("  1. Log in with: tomsmith / SuperSecretPassword!")
    print("  2. You should see 'You logged into a secure area!'")
    print("  3. Come back here and press Enter to save the session.")
    print()

    nova = NovaAct(
        starting_page=TEST_URL,
        headless=False,
        user_data_dir=PROFILE_DIR,
        clone_user_data_dir=False,
        nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", ""),
    )
    nova.start()

    # Let Nova Act do the login automatically
    print("Attempting automated login...")
    result = nova.act(
        "Type 'tomsmith' into the username field, type 'SuperSecretPassword!' "
        "into the password field, then click the Login button."
    )
    print(f"Login result: {result}")

    input("\nPress Enter to save the profile and close the browser...")
    nova.stop()
    print(f"Profile saved to: {PROFILE_DIR}")
    print("Now run: python test_persistent_profile.py --verify")


def verify_profile():
    """Open browser with saved profile - should still have cookies."""
    from nova_act import NovaAct

    if not Path(PROFILE_DIR).exists():
        print("ERROR: No profile found. Run --setup first.")
        sys.exit(1)

    # Navigate directly to the secure page (skipping login)
    secure_url = "https://the-internet.herokuapp.com/secure"
    print(f"Opening browser with saved profile to: {secure_url}")
    print(f"Using profile from: {PROFILE_DIR}")
    print()
    print("If the profile works, you should see the secure area WITHOUT logging in again.")
    print()

    nova = NovaAct(
        starting_page=secure_url,
        headless=False,
        user_data_dir=PROFILE_DIR,
        clone_user_data_dir=False,
        nova_act_api_key=os.environ.get("NOVA_ACT_API_KEY", ""),
    )
    nova.start()

    # Check if we're on the secure page or redirected to login
    result = nova.act(
        "Look at the current page. Tell me: does it say 'Secure Area' or "
        "'You logged into a secure area', or does it show a login form?"
    )
    print(f"Page check result: {result}")

    input("\nPress Enter to close the browser...")
    nova.stop()


def cleanup():
    """Remove the test profile directory."""
    import shutil
    if Path(PROFILE_DIR).exists():
        shutil.rmtree(PROFILE_DIR)
        print(f"Removed: {PROFILE_DIR}")
    else:
        print("Nothing to clean up.")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("--setup", "--verify", "--cleanup"):
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--setup":
        setup_profile()
    elif sys.argv[1] == "--verify":
        verify_profile()
    elif sys.argv[1] == "--cleanup":
        cleanup()
