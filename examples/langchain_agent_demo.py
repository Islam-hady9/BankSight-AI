"""
Example script demonstrating LangChain agent with conversation memory.

This script shows how to:
1. Use the chat API with conversation memory
2. Inject old messages for context restoration
3. Clear sessions
4. Get conversation history
5. Use banking tools via natural language
"""
import requests
import json
from typing import List, Dict


# API Configuration
BASE_URL = "http://localhost:8000"
SESSION_ID = "demo_user_123"


def chat(message: str, old_messages: List[Dict] = None) -> Dict:
    """
    Send a message to the agent.

    Args:
        message: User message
        old_messages: Optional previous conversation history

    Returns:
        Response dict
    """
    url = f"{BASE_URL}/api/chat"
    payload = {
        "message": message,
        "session_id": SESSION_ID,
        "old_messages": old_messages
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def get_agent_info() -> Dict:
    """Get agent configuration information."""
    url = f"{BASE_URL}/api/agent/info"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_memory(session_id: str = SESSION_ID) -> Dict:
    """Get conversation history for a session."""
    url = f"{BASE_URL}/api/agent/memory/{session_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def clear_session(session_id: str = SESSION_ID) -> Dict:
    """Clear conversation memory for a session."""
    url = f"{BASE_URL}/api/agent/clear-session/{session_id}"
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def print_response(response: Dict):
    """Pretty print agent response."""
    print("\n" + "=" * 60)
    print(f"Agent Type: {response.get('agent_type', 'N/A')}")
    print(f"Intent: {response.get('intent')}")
    print(f"\nResponse:")
    print(f"  {response['response']}")

    if response.get('tools_used'):
        print(f"\nTools Used:")
        for tool in response['tools_used']:
            print(f"  - {tool['tool']}")
            print(f"    Input: {tool['input']}")

    if response.get('sources'):
        print(f"\nSources: {len(response['sources'])} documents")

    print("=" * 60)


def example_1_basic_conversation():
    """Example 1: Basic conversation with memory."""
    print("\n📝 Example 1: Basic Conversation with Memory")
    print("-" * 60)

    # Message 1
    print("\n👤 User: What's my checking account balance?")
    response = chat("What's my checking account balance?")
    print_response(response)

    # Message 2 - Agent remembers context
    print("\n👤 User: Transfer $100 from it to savings")
    response = chat("Transfer $100 from it to savings")
    print_response(response)

    # Message 3 - Still remembers
    print("\n👤 User: Show me the last 5 transactions")
    response = chat("Show me the last 5 transactions")
    print_response(response)


def example_2_old_messages():
    """Example 2: Restoring conversation context."""
    print("\n📝 Example 2: Restoring Conversation Context")
    print("-" * 60)

    # Clear session first
    print("\n🗑️  Clearing session...")
    clear_session()

    # Simulate restored conversation
    old_messages = [
        {
            "user": "What's my checking account balance?",
            "assistant": "Your checking account (****1234) has $5,430.50"
        },
        {
            "user": "Thanks!",
            "assistant": "You're welcome! How else can I help you today?"
        }
    ]

    print("\n🔄 Injecting old conversation...")
    print(f"  - {old_messages[0]['user']}")
    print(f"  - {old_messages[1]['user']}")

    # New message with context
    print("\n👤 User: Can you transfer $200 to my savings?")
    response = chat(
        "Can you transfer $200 to my savings?",
        old_messages=old_messages
    )
    print_response(response)


def example_3_complex_query():
    """Example 3: Complex multi-tool workflow."""
    print("\n📝 Example 3: Complex Multi-Tool Query")
    print("-" * 60)

    # Clear session
    clear_session()

    print("\n👤 User: Find all my grocery transactions over $50")
    response = chat("Find all my grocery transactions over $50")
    print_response(response)


def example_4_bilingual():
    """Example 4: Bilingual support."""
    print("\n📝 Example 4: Bilingual Support (Arabic)")
    print("-" * 60)

    # Clear session
    clear_session()

    # Arabic greeting
    print("\n👤 User: مرحباً! من أنت؟ (Hello! Who are you?)")
    response = chat("مرحباً! من أنت؟")
    print_response(response)

    # Arabic query
    print("\n👤 User: ما هو رصيد حسابي؟ (What is my account balance?)")
    response = chat("ما هو رصيد حسابي؟")
    print_response(response)


def example_5_memory_inspection():
    """Example 5: Inspecting conversation memory."""
    print("\n📝 Example 5: Inspecting Conversation Memory")
    print("-" * 60)

    # Clear and start new conversation
    clear_session()

    # Exchange a few messages
    chat("Hi! What's my balance?")
    chat("Transfer $50 to savings")

    # Get memory
    print("\n🧠 Getting conversation memory...")
    memory = get_memory()

    print(f"\nSession ID: {memory['session_id']}")
    print(f"Agent Type: {memory['agent_type']}")
    print(f"Message Count: {memory['count']}")
    print(f"\nConversation History:")

    for i, msg in enumerate(memory['messages'], 1):
        msg_type = msg.get('type', 'unknown')
        content = msg.get('content', '')[:100]  # Truncate long messages
        print(f"  {i}. [{msg_type}]: {content}...")


def show_agent_info():
    """Show agent configuration."""
    print("\n🤖 Agent Information")
    print("-" * 60)

    info = get_agent_info()

    print(f"\nAgent Type: {info['agent_type']}")
    print(f"LangChain Available: {info['langchain_available']}")

    print(f"\nFeatures:")
    for feature, enabled in info['features'].items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature}")

    if info.get('config'):
        print(f"\nConfiguration:")
        for key, value in info['config'].items():
            print(f"  - {key}: {value}")

    if info.get('tools'):
        print(f"\nAvailable Tools ({len(info['tools'])}):")
        for tool in info['tools']:
            print(f"  - {tool['name']}")
            print(f"    {tool['description'][:80]}...")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  LangChain Agent Examples - BankSight AI")
    print("=" * 60)

    try:
        # Show agent info
        show_agent_info()

        # Run examples
        example_1_basic_conversation()
        example_2_old_messages()
        example_3_complex_query()
        example_4_bilingual()
        example_5_memory_inspection()

        print("\n✅ All examples completed successfully!")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend.")
        print("Make sure the backend is running:")
        print("  python -m uvicorn backend.main:app --reload")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
