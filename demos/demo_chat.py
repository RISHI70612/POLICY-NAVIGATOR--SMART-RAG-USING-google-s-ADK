#!/usr/bin/env python3
"""
Demo: Stateful Chat with Policy Navigator

This demo shows how to use the PolicyChatSession for multi-turn conversations
where the agent remembers context.

Run this after setup:
    python demos/demo_chat.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.config import Config
from policy_navigator.session import PolicyChatSession
from policy_navigator.utils import validate_api_key

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")

def main():
    """Run the chat demo."""
    print_section("Policy Navigator - Stateful Chat Demo")

    # Validate
    if not validate_api_key():
        print("[FAIL] GOOGLE_API_KEY not set")
        return False

    try:
        # Initialize session
        print("Initializing Chat Session...")
        session = PolicyChatSession()
        print(f"[OK] Session initialized with model: {session.model_name}\n")

        # Turn 1: Initial Query
        print_section("Turn 1: Initial Query")
        query1 = "What are the requirements for remote work?"
        print(f"User: {query1}")
        
        response1 = session.send_message(query1)
        print(f"\nAgent: {response1}\n")

        # Turn 2: Follow-up (Implicit Context)
        print_section("Turn 2: Follow-up (Implicit Context)")
        query2 = "Does this apply to contractors?"
        print(f"User: {query2}")
        print("(Note: 'this' refers to 'remote work' from the previous turn)\n")
        
        response2 = session.send_message(query2)
        print(f"\nAgent: {response2}\n")

        # Turn 3: Another Follow-up
        print_section("Turn 3: Another Follow-up")
        query3 = "Summarize the key points we just discussed."
        print(f"User: {query3}")
        
        response3 = session.send_message(query3)
        print(f"\nAgent: {response3}\n")

        print_section("Demo Complete")
        print("[OK] Multi-turn conversation demonstrated successfully.")
        return True

    except Exception as e:
        print(f"\n[FAIL] Chat demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
