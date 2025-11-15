# BankSight AI - API Reference

Complete API documentation for BankSight AI with LangChain agent support.

---

## Base URL

```
http://localhost:8000
```

---

## Table of Contents

1. [Chat Endpoints](#chat-endpoints)
2. [Agent Management](#agent-management)
3. [Document Management](#document-management)
4. [System Endpoints](#system-endpoints)
5. [Request/Response Models](#requestresponse-models)
6. [Examples](#examples)

---

## Chat Endpoints

### POST /api/chat

Send a message to the AI agent with optional conversation history.

**Features:**
- Conversation memory (session-based)
- Old message injection for context restoration
- Tool calling with banking actions
- Bilingual support (English/Arabic)

**Request Body:**

```json
{
  "message": "What's my checking account balance?",
  "session_id": "user_123",
  "old_messages": [
    {
      "user": "Hello!",
      "assistant": "Hi! How can I help you today?"
    }
  ]
}
```

**Parameters:**
- `message` (string, required): User's message
- `session_id` (string, optional): Session identifier for memory. Default: `"default"`
- `old_messages` (array, optional): Previous conversation history for context restoration

**Response:**

```json
{
  "success": true,
  "response": "Your checking account (****1234) has $5,430.50",
  "intent": "langchain_agent",
  "sources": [],
  "tools_used": [
    {
      "tool": "GetAccountBalance",
      "input": {
        "account_type": "checking"
      }
    }
  ],
  "agent_type": "langchain"
}
```

**Response Fields:**
- `success` (boolean): Whether request succeeded
- `response` (string): Agent's text response
- `intent` (string): Detected intent or agent type
- `sources` (array): Source documents for RAG responses
- `tools_used` (array, optional): Tools called during processing
- `agent_type` (string, optional): Agent type used ("langchain" or "classic")

**Example cURL:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Transfer $100 from checking to savings",
    "session_id": "demo_user"
  }'
```

---

## Agent Management

### POST /api/agent/clear-session/{session_id}

Clear conversation memory for a specific session.

**Path Parameters:**
- `session_id` (string, required): Session to clear

**Response:**

```json
{
  "success": true,
  "message": "Session demo_user cleared",
  "agent_type": "langchain"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/agent/clear-session/demo_user
```

**Use Cases:**
- Reset conversation context
- Free memory for inactive sessions
- Start fresh conversations

---

### GET /api/agent/memory/{session_id}

Get full conversation history for a session.

**Path Parameters:**
- `session_id` (string, required): Session to query

**Response:**

```json
{
  "success": true,
  "session_id": "demo_user",
  "messages": [
    {
      "type": "human",
      "content": "What's my balance?"
    },
    {
      "type": "ai",
      "content": "Your checking account has $5,430.50"
    }
  ],
  "count": 2,
  "agent_type": "langchain"
}
```

**Response Fields:**
- `messages` (array): Full conversation history
  - `type` (string): "human" or "ai"
  - `content` (string): Message content
- `count` (integer): Number of messages
- `agent_type` (string): Agent type

**Example:**

```bash
curl http://localhost:8000/api/agent/memory/demo_user
```

---

### GET /api/agent/info

Get agent configuration and capabilities.

**Response:**

```json
{
  "agent_type": "langchain",
  "langchain_available": true,
  "features": {
    "conversation_memory": true,
    "tool_calling": true,
    "session_management": true,
    "rag": true,
    "bilingual": true
  },
  "config": {
    "max_iterations": 5,
    "verbose": true,
    "llm_model": "moonshotai/kimi-k2-instruct-0905",
    "llm_provider": "groq"
  },
  "tools": [
    {
      "name": "GetAccountBalance",
      "description": "Get the current balance of a bank account..."
    },
    {
      "name": "GetTransactions",
      "description": "Get recent transactions for an account..."
    },
    {
      "name": "TransferFunds",
      "description": "Transfer money between accounts..."
    },
    {
      "name": "SearchTransactions",
      "description": "Search for specific transactions..."
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/api/agent/info
```

---

## Document Management

### POST /api/documents/upload

Upload and process a document for RAG.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: File upload

**Supported Formats:**
- PDF (.pdf)
- Text (.txt)
- Word (.docx)
- CSV (.csv)

**Response:**

```json
{
  "success": true,
  "message": "Document 'banking_policy.pdf' uploaded and processed",
  "chunks": 42
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@banking_policy.pdf"
```

---

### GET /api/documents

List all uploaded documents.

**Response:**

```json
{
  "documents": [
    {
      "filename": "banking_policy.pdf",
      "size": 245678,
      "type": ".pdf"
    },
    {
      "filename": "faq.txt",
      "size": 12345,
      "type": ".txt"
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/api/documents
```

---

### POST /api/documents/process-all

Process all documents in the upload directory.

**Response:**

```json
{
  "success": true,
  "processed": 3,
  "total_chunks": 156
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/documents/process-all
```

---

## System Endpoints

### GET /

Root endpoint - API information.

**Response:**

```json
{
  "message": "BankSight AI API",
  "status": "running",
  "version": "1.0.0"
}
```

---

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "llm_loaded": true,
  "vector_store_count": 156
}
```

**Fields:**
- `status` (string): "healthy" or "unhealthy"
- `llm_loaded` (boolean): Whether LLM is loaded
- `vector_store_count` (integer): Number of document chunks in vector DB

**Example:**

```bash
curl http://localhost:8000/health
```

---

## Request/Response Models

### ChatRequest

```python
class ChatRequest(BaseModel):
    message: str                      # Required
    session_id: str = "default"       # Optional
    old_messages: List[OldMessage]    # Optional
```

### OldMessage

```python
class OldMessage(BaseModel):
    user: Optional[str] = None
    assistant: Optional[str] = None
```

### ChatResponse

```python
class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: str
    sources: List[dict] = []
    tools_used: Optional[List[ToolUsage]] = None
    agent_type: Optional[str] = None
```

### ToolUsage

```python
class ToolUsage(BaseModel):
    tool: str
    input: dict
```

---

## Examples

### Example 1: Basic Chat

**Request:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my checking account balance?",
    "session_id": "user_123"
  }'
```

**Response:**

```json
{
  "success": true,
  "response": "Your checking account (****1234) has $5,430.50",
  "intent": "langchain_agent",
  "sources": [],
  "tools_used": [
    {
      "tool": "GetAccountBalance",
      "input": {"account_type": "checking"}
    }
  ],
  "agent_type": "langchain"
}
```

---

### Example 2: Conversation with Memory

**First Message:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my balance?",
    "session_id": "user_123"
  }'
```

**Second Message (remembers context):**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Transfer $100 from it to savings",
    "session_id": "user_123"
  }'
```

The agent remembers "it" refers to the checking account from the previous message.

---

### Example 3: Restoring Context

**Request with Old Messages:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Transfer $200 to savings",
    "session_id": "new_session",
    "old_messages": [
      {
        "user": "What is my balance?",
        "assistant": "Your checking account has $5,430.50"
      }
    ]
  }'
```

The agent has context from the injected old messages.

---

### Example 4: Complex Query

**Request:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find all grocery transactions over $50 and tell me the total",
    "session_id": "user_123"
  }'
```

**Response:**

```json
{
  "success": true,
  "response": "I found 3 grocery transactions over $50:\n- $75.00 - Whole Foods (2025-01-14)\n- $62.50 - Trader Joe's (2025-01-10)\n- $55.00 - Safeway (2025-01-07)\n\nTotal: $192.50",
  "intent": "langchain_agent",
  "tools_used": [
    {
      "tool": "SearchTransactions",
      "input": {
        "keyword": "grocery",
        "min_amount": 50.0,
        "account_type": "checking"
      }
    }
  ],
  "agent_type": "langchain"
}
```

---

### Example 5: Bilingual (Arabic)

**Request:**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ما هو رصيد حسابي؟",
    "session_id": "user_123"
  }'
```

**Response (in Arabic):**

```json
{
  "success": true,
  "response": "رصيد حسابك الجاري (****1234) هو 5,430.50 دولار",
  "intent": "langchain_agent",
  "tools_used": [
    {
      "tool": "GetAccountBalance",
      "input": {"account_type": "checking"}
    }
  ]
}
```

---

### Example 6: Get Memory

**Request:**

```bash
curl http://localhost:8000/api/agent/memory/user_123
```

**Response:**

```json
{
  "success": true,
  "session_id": "user_123",
  "messages": [
    {"type": "human", "content": "What's my balance?"},
    {"type": "ai", "content": "Your checking account has $5,430.50"},
    {"type": "human", "content": "Transfer $100 to savings"},
    {"type": "ai", "content": "✅ Transfer completed!..."}
  ],
  "count": 4,
  "agent_type": "langchain"
}
```

---

### Example 7: Clear Session

**Request:**

```bash
curl -X POST http://localhost:8000/api/agent/clear-session/user_123
```

**Response:**

```json
{
  "success": true,
  "message": "Session user_123 cleared",
  "agent_type": "langchain"
}
```

---

## Python Client Example

```python
import requests

class BankSightClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = "my_session"

    def chat(self, message, old_messages=None):
        url = f"{self.base_url}/api/chat"
        data = {
            "message": message,
            "session_id": self.session_id,
            "old_messages": old_messages
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_memory(self):
        url = f"{self.base_url}/api/agent/memory/{self.session_id}"
        response = requests.get(url)
        return response.json()

    def clear_session(self):
        url = f"{self.base_url}/api/agent/clear-session/{self.session_id}"
        response = requests.post(url)
        return response.json()

# Usage
client = BankSightClient()

# Chat
response = client.chat("What's my balance?")
print(response['response'])

# Follow-up (remembers context)
response = client.chat("Transfer $100 to savings")
print(response['response'])

# Get history
memory = client.get_memory()
print(f"Messages: {memory['count']}")

# Clear
client.clear_session()
```

---

## Error Handling

All endpoints return errors in this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

**Example Error:**

```json
{
  "detail": "Unsupported file type. Supported: ['pdf', 'txt', 'docx', 'csv']"
}
```

---

## Rate Limiting

No built-in rate limiting. Groq API has its own rate limits:
- Free tier: ~30 requests/minute
- Check: https://console.groq.com/settings/limits

---

## Authentication

Currently no authentication required. In production:
- Add API key authentication
- Implement session-based auth
- Use JWT tokens
- Rate limiting per user

---

## Best Practices

1. **Session Management**
   - Use unique session IDs per user
   - Clear inactive sessions regularly
   - Don't use "default" for production

2. **Old Messages**
   - Only inject recent context (last 5-10 messages)
   - Too many old messages can slow down inference

3. **Error Handling**
   - Always check `success` field
   - Handle network errors gracefully
   - Retry failed requests with exponential backoff

4. **Performance**
   - Reuse session IDs for conversation continuity
   - Clear sessions when done
   - Monitor Groq API quotas

---

## Additional Resources

- **Full Documentation:** [docs/LANGCHAIN_AGENT.md](docs/LANGCHAIN_AGENT.md)
- **Examples:** [examples/](examples/)
  - `langchain_agent_demo.py` - Python examples
  - `api_examples.sh` - cURL examples
- **Migration Guide:** [MIGRATION_GROQ.md](MIGRATION_GROQ.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)

---

**API Version:** 1.0.0
**Last Updated:** November 15, 2025
**Base Technology:** FastAPI + Groq API + LangChain
