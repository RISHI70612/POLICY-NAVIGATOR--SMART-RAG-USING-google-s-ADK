
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from policy_navigator.config import Config
from policy_navigator.stores import StoreManager
import traceback

def debug_store_creation():
    print("DEBUG: Starting store creation test")
    try:
        manager = StoreManager()
        print(f"DEBUG: API Key present: {bool(manager.api_key)}")
        
        # List existing
        print("DEBUG: Listing existing stores...")
        stores = manager.list_stores()
        print(f"DEBUG: Found {len(stores)} stores")
        expected_stores = ["policy-navigator-hr", "policy-navigator-it", "policy-navigator-legal", "policy-navigator-safety"]
        for s in stores:
            display_name = s.get('display_name')
            print(f"DEBUG: Store: {display_name} ({s.get('name')})")
            if display_name in expected_stores:
                print(f"DEBUG: FOUND EXPECTED STORE: {display_name}")

        # Create missing stores
        print("DEBUG: Checking and creating required stores...")
        required_stores = ["policy-navigator-hr", "policy-navigator-it", "policy-navigator-legal", "policy-navigator-safety"]
        
        existing_names = [s.get('display_name') for s in stores]
        
        for name in required_stores:
            if name not in existing_names:
                print(f"DEBUG: Creating missing store: {name}")
                try:
                    new_store = manager.create_policy_store(name)
                    print(f"DEBUG: Created {name}: {new_store}")
                except Exception as e:
                    print(f"DEBUG: Failed to create {name}: {e}")
            else:
                print(f"DEBUG: Store {name} already exists")
        
    except Exception as e:
        print(f"DEBUG: ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_store_creation()
