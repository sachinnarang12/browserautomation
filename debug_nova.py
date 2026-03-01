#!/usr/bin/env python3

import sys
import traceback

print("Python version:", sys.version)
print("Starting debug...")

try:
    print("Step 1: Importing nova_act...")
    import nova_act
    print("✓ nova_act module imported successfully")
    print("Nova Act version:", getattr(nova_act, '__version__', 'Unknown'))
    
    print("Step 2: Importing NovaAct class...")
    from nova_act import NovaAct
    print("✓ NovaAct class imported successfully")
    
    print("Step 3: Creating NovaAct instance...")
    nova = NovaAct(
        starting_page="https://www.google.com",
        headless=True,
        tty=False,
        nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
    )
    print("✓ NovaAct instance created successfully")
    
    print("Step 4: Checking available methods...")
    methods = [method for method in dir(nova) if not method.startswith('_')]
    print("Available methods:", methods)
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()

print("Debug completed.")