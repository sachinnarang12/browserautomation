#!/usr/bin/env python3

print("Starting Nova Act test...")

try:
    from nova_act import NovaAct
    print("Nova Act imported successfully")
    
    # Test basic initialization
    nova = NovaAct(
        starting_page="https://www.google.com",
        headless=True,
        tty=False,
        nova_act_api_key="3371a1a7-d4f9-4aac-a9c7-9ded0ba21463"
    )
    print("Nova Act initialized successfully")
    
    # Try to start
    print("Starting Nova Act session...")
    nova.start()
    print("Nova Act session started successfully")
    
    # Simple test action
    print("Performing test action...")
    result = nova.act("Take a screenshot of the current page")
    print(f"Test action result: {result}")
    
    # Stop the session
    print("Stopping Nova Act session...")
    nova.stop()
    print("Nova Act session stopped successfully")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")