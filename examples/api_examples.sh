#!/bin/bash

# API Examples for BankSight AI with LangChain Agent
# These examples show how to use the REST API directly with cURL

BASE_URL="http://localhost:8000"
SESSION_ID="test_session_$(date +%s)"

echo "=================================="
echo "BankSight AI - API Examples"
echo "=================================="
echo ""

# Check if backend is running
echo "Checking backend health..."
curl -s "${BASE_URL}/health" | jq '.'
echo ""

# Example 1: Get agent information
echo "=================================="
echo "Example 1: Get Agent Information"
echo "=================================="
curl -s "${BASE_URL}/api/agent/info" | jq '.'
echo ""

# Example 2: Simple chat query
echo "=================================="
echo "Example 2: Simple Chat Query"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"What's my checking account balance?\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.'
echo ""

# Example 3: Chat with conversation memory
echo "=================================="
echo "Example 3: Follow-up Query (Memory)"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Transfer \$100 from it to savings\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.'
echo ""

# Example 4: Chat with old messages injection
echo "=================================="
echo "Example 4: Chat with Old Messages"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Transfer \$200 to savings\",
    \"session_id\": \"new_session\",
    \"old_messages\": [
      {
        \"user\": \"What's my balance?\",
        \"assistant\": \"Your checking account has \$5,430.50\"
      },
      {
        \"user\": \"Thanks!\",
        \"assistant\": \"You're welcome!\"
      }
    ]
  }" | jq '.'
echo ""

# Example 5: Complex query (search transactions)
echo "=================================="
echo "Example 5: Complex Query (Search)"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Find all grocery transactions over \$50\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.'
echo ""

# Example 6: Bilingual - Arabic query
echo "=================================="
echo "Example 6: Bilingual (Arabic)"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"مرحباً! ما هو رصيد حسابي؟\",
    \"session_id\": \"${SESSION_ID}\"
  }" | jq '.'
echo ""

# Example 7: Get conversation memory
echo "=================================="
echo "Example 7: Get Conversation Memory"
echo "=================================="
curl -s "${BASE_URL}/api/agent/memory/${SESSION_ID}" | jq '.'
echo ""

# Example 8: Clear session
echo "=================================="
echo "Example 8: Clear Session"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/agent/clear-session/${SESSION_ID}" | jq '.'
echo ""

# Example 9: Multiple tool calls
echo "=================================="
echo "Example 9: Multi-Tool Workflow"
echo "=================================="
curl -s -X POST "${BASE_URL}/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Check my balance, then if I have more than \$1000, transfer \$500 to savings\",
    \"session_id\": \"multi_tool_session\"
  }" | jq '.'
echo ""

echo "=================================="
echo "Examples completed!"
echo "=================================="
