# LangChain Agent with Conversation Memory

**BankSight AI** now features a powerful **LangChain-based agent** with conversation memory and intelligent tool calling!

---

## 🎯 Overview

The LangChain agent provides advanced capabilities beyond the classic intent-routing system:

### Key Features

✅ **Conversation Memory** - Remembers context across messages
✅ **Tool Calling** - Intelligently uses banking tools based on user intent
✅ **Multi-Turn Dialogues** - Natural conversations with context awareness
✅ **Session Management** - Separate memory for each user session
✅ **Groq Integration** - Ultra-fast inference via langchain-groq
✅ **Configurable** - Easily customize behavior via config.yaml

---

## 📦 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Query                        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              BankingAgent                           │
│  ┌──────────────────────────────────────────────┐  │
│  │  LangChain Mode?                             │  │
│  │  ├─ Yes → BankSightAgent (LangChain)         │  │
│  │  └─ No  → Classic Intent Router              │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          BankSightAgent (LangChain)                 │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  ChatGroq (Groq API)                         │  │
│  │  + ConversationBufferMemory                  │  │
│  │  + Tool-Calling Agent                        │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Banking Tools (Pydantic)                    │  │
│  │  ├─ GetAccountBalance                        │  │
│  │  ├─ GetTransactions                          │  │
│  │  ├─ TransferFunds                            │  │
│  │  └─ SearchTransactions                       │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Banking Actions                        │
│  (Execute operations on dummy data)                 │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Installation

The LangChain dependencies are included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Core LangChain framework
- `langchain-groq` - Groq integration for LangChain
- `langchain-community` - Community tools and integrations

### Configuration

Edit `config.yaml` to enable/configure the agent:

```yaml
# Agent Settings
agent:
  # Use LangChain agent with conversation memory and tool calling
  use_langchain: true  # Set to false for classic routing
  max_iterations: 5    # Maximum tool call iterations
  verbose: true        # Enable verbose logging
```

### Environment Setup

Ensure your `.env` file has the Groq API key:

```bash
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

## 💡 Usage Examples

### Example 1: Conversation Memory

**First message:**
```
User: What's my checking account balance?
Agent: Your checking account (****1234) has $5,430.50.
```

**Follow-up (agent remembers context):**
```
User: Transfer $100 from it to savings
Agent: ✅ Transfer completed!
       $100 transferred from checking to savings.
       New checking balance: $5,330.50
```

**Another follow-up:**
```
User: Show me the last 5 transactions
Agent: Here are your last 5 transactions:
       -$150.00 - Whole Foods (2025-01-14)
       -$45.00 - Starbucks (2025-01-13)
       ...
```

### Example 2: Multi-Step Workflow

```
User: I need to pay my rent. Can you check if I have enough in checking, and if so, tell me my balance after transferring $1200 to my landlord?

Agent:
[Tool 1: GetAccountBalance(account_type="checking")]
Result: $5,430.50 available

[Reasoning: User has sufficient funds ($5,430.50 > $1,200)]

Your checking account has $5,430.50, which is enough to cover the $1,200 rent payment.
After the transfer, your balance would be $4,230.50.

Would you like me to proceed with the transfer?
```

### Example 3: Complex Query

```
User: Find all my grocery transactions over $50 and tell me the total

Agent:
[Tool 1: SearchTransactions(keyword="grocery", min_amount=50)]
Result: 3 transactions found

I found 3 grocery transactions over $50:
- $75.00 - Whole Foods (2025-01-14)
- $62.50 - Trader Joe's (2025-01-10)
- $55.00 - Safeway (2025-01-07)

Total: $192.50 spent on groceries over $50
```

---

## 🛠️ Banking Tools

The agent has access to 4 banking tools:

### 1. GetAccountBalance

**Purpose:** Check account balance

**Parameters:**
- `account_type` (str): "checking", "savings", or "credit_card"
- `user_id` (optional str): User ID

**Example:**
```python
{
    "account_type": "checking"
}
```

**Returns:**
```json
{
    "success": true,
    "account_type": "checking",
    "balance": 5430.50,
    "account_number": "****1234",
    "status": "active"
}
```

### 2. GetTransactions

**Purpose:** Retrieve recent transactions

**Parameters:**
- `account_type` (str): Account type
- `limit` (int): Number of transactions (1-20)
- `user_id` (optional str): User ID

**Example:**
```python
{
    "account_type": "checking",
    "limit": 5
}
```

**Returns:**
```json
{
    "success": true,
    "transactions": [
        {
            "date": "2025-01-14",
            "amount": -150.00,
            "merchant": "Whole Foods",
            "category": "groceries"
        },
        ...
    ],
    "count": 5
}
```

### 3. TransferFunds

**Purpose:** Transfer money between accounts

**Parameters:**
- `from_account` (str): Source account type
- `to_account` (str): Destination account type
- `amount` (float): Transfer amount
- `user_id` (optional str): User ID

**Example:**
```python
{
    "from_account": "checking",
    "to_account": "savings",
    "amount": 100.0
}
```

**Returns:**
```json
{
    "success": true,
    "from_account": "checking",
    "to_account": "savings",
    "amount": 100.0,
    "new_balance": 5330.50,
    "transaction_id": "txn_abc123"
}
```

### 4. SearchTransactions

**Purpose:** Search transactions by criteria

**Parameters:**
- `keyword` (optional str): Search in merchant/description
- `category` (optional str): Transaction category
- `min_amount` (optional float): Minimum amount
- `account_type` (str): Account to search
- `user_id` (optional str): User ID

**Example:**
```python
{
    "keyword": "grocery",
    "min_amount": 50.0,
    "account_type": "checking"
}
```

**Returns:**
```json
{
    "success": true,
    "transactions": [...],
    "count": 3,
    "filters": {
        "keyword": "grocery",
        "min_amount": 50.0
    }
}
```

---

## 🧠 How It Works

### 1. Conversation Memory

Each session has its own `ConversationBufferMemory`:

```python
memory = ConversationBufferMemory(
    memory_key=f"chat_history_{session_id}",
    input_key="input",
    output_key="output",
    return_messages=True
)
```

**Memory stores:**
- User messages
- Assistant responses
- Tool calls and results
- Full conversation context

### 2. Tool Calling

The agent uses `create_tool_calling_agent` from LangChain:

```python
agent = create_tool_calling_agent(
    llm=ChatGroq(...),
    tools=banking_tools,
    prompt=prompt_template
)
```

**Process:**
1. User sends message
2. Agent analyzes intent and available tools
3. Decides which tool(s) to call
4. Executes tool(s) and receives results
5. Formulates natural language response
6. Stores in conversation memory

### 3. System Prompt

The agent uses `BANKING_ASSISTANT_SYSTEM` prompt:

```python
"""You are BankSight AI, an intelligent bilingual banking assistant.

Identity:
- Name: BankSight AI (بنك سايت إيه آي)
- Purpose: Help users with banking questions, transactions, and account management
- Languages: English and Arabic (fully bilingual)

Core Guidelines:
- ALWAYS respond in the SAME language the user uses
- Be concise, clear, and professional
- For questions, use only the provided context
- For actions, extract relevant parameters accurately
- Use tools when needed to accomplish user requests
"""
```

---

## 🔧 Advanced Features

### Session Management

```python
from backend.agent.langchain_agent import get_agent, clear_agent_session

# Get agent for specific session
agent = get_agent(session_id="user_123")

# Use the agent
result = agent.invoke("What's my balance?")

# Clear session when done
clear_agent_session("user_123")
```

### Injecting Old Messages

Restore conversation context from previous sessions:

```python
old_messages = [
    {"user": "What's my balance?", "assistant": "Your balance is $5,430.50"},
    {"user": "Thanks!", "assistant": "You're welcome! How else can I help?"}
]

result = agent.invoke(
    message="Transfer $100 to savings",
    old_messages=old_messages
)
```

### Accessing Memory History

```python
agent = get_agent(session_id="user_123")
history = agent.get_memory_history()

for msg in history:
    print(f"{msg['type']}: {msg['content']}")
```

---

## 📊 Comparison: LangChain vs Classic Agent

| Feature | LangChain Agent | Classic Agent |
|---------|----------------|---------------|
| **Conversation Memory** | ✅ Yes (per session) | ❌ No |
| **Multi-Turn Context** | ✅ Yes | ❌ Limited |
| **Tool Calling** | ✅ Intelligent | ⚠️ Manual |
| **Intent Detection** | ✅ Automatic (LLM) | ⚠️ Keyword-based |
| **Complex Workflows** | ✅ Yes | ❌ Limited |
| **Bilingual Support** | ✅ Yes | ✅ Yes |
| **RAG Integration** | ⚠️ Planned | ✅ Yes |
| **Response Speed** | ⚡ Fast | ⚡ Very Fast |
| **Setup Complexity** | ⚠️ Medium | ✅ Simple |

**Recommendation:**
- **Use LangChain** for: Multi-turn conversations, complex banking workflows, tool orchestration
- **Use Classic** for: Simple queries, RAG-only applications, minimal dependencies

---

## 🎯 Configuration Options

### Agent Settings (config.yaml)

```yaml
agent:
  # Enable/disable LangChain agent
  use_langchain: true

  # Maximum number of tool calling iterations
  # Higher = more complex workflows, but slower
  max_iterations: 5

  # Enable verbose logging (shows agent reasoning)
  verbose: true
```

### LLM Settings (config.yaml)

```yaml
llm:
  provider: "groq"

  groq:
    model_name: "moonshotai/kimi-k2-instruct-0905"
    temperature: 0.6
    max_tokens: 4096
```

**Model recommendations:**
- `moonshotai/kimi-k2-instruct-0905` - Best for reasoning and tool calling
- `llama-3.3-70b-versatile` - Most powerful, slower
- `llama-3.1-8b-instant` - Fastest, good for simple tasks

---

## 🐛 Troubleshooting

### LangChain Not Loading

**Error:** `⚠️ LangChain not available`

**Solution:**
```bash
pip install langchain langchain-groq langchain-community
```

### Agent Not Using Tools

**Check:**
1. Tools are properly defined in `langchain_tools.py`
2. `agent.verbose = true` in config to see agent reasoning
3. Check logs for tool execution errors

**Debug:**
```python
# Set verbose mode
agent.use_langchain = True
config.agent_verbose = True
```

### Memory Not Persisting

**Issue:** Agent forgets previous messages

**Solution:**
- Ensure same `session_id` across messages
- Check if agent was recreated (clears memory)
- Use `old_messages` parameter to inject history

### Tool Errors

**Check backend logs:**
```bash
# Terminal with backend running
# Look for:
INFO - Agent executor created with 4 tools
INFO - Tool call: GetAccountBalance
ERROR - Tool execution failed: ...
```

---

## 📚 API Reference

### BankSightAgent

Main LangChain agent class.

**Methods:**

#### `__init__(session_id: str)`
Initialize agent with session ID.

```python
agent = BankSightAgent(session_id="user_123")
```

#### `invoke(message: str, old_messages: List[Dict] = None) -> Dict`
Process a user message.

```python
result = agent.invoke(
    message="What's my balance?",
    old_messages=[...]  # Optional
)
```

**Returns:**
```python
{
    "success": True,
    "response": "Your checking account has $5,430.50",
    "tools_used": [
        {"tool": "GetAccountBalance", "input": {...}}
    ],
    "session_id": "user_123"
}
```

#### `clear_memory()`
Clear conversation history.

```python
agent.clear_memory()
```

#### `get_memory_history() -> List[Dict]`
Get conversation history.

```python
history = agent.get_memory_history()
```

### Helper Functions

#### `get_agent(session_id: str) -> BankSightAgent`
Get or create agent for session.

```python
from backend.agent.langchain_agent import get_agent

agent = get_agent("user_123")
```

#### `clear_agent_session(session_id: str)`
Clear a session.

```python
from backend.agent.langchain_agent import clear_agent_session

clear_agent_session("user_123")
```

#### `async get_langchain_response(message: str, session_id: str, old_messages: List[Dict] = None) -> Dict`
High-level API for getting responses.

```python
from backend.agent.langchain_agent import get_langchain_response

result = await get_langchain_response(
    message="Transfer $100 to savings",
    session_id="user_123"
)
```

---

## 🎓 Best Practices

### 1. Session Management

✅ **DO:**
- Use unique session IDs per user
- Clear sessions when user logs out
- Store session IDs in frontend state

❌ **DON'T:**
- Use global default session for all users
- Forget to clear old sessions (memory leak)

### 2. Tool Design

✅ **DO:**
- Use clear, descriptive tool names
- Provide detailed descriptions
- Define Pydantic schemas for parameters
- Handle errors gracefully

❌ **DON'T:**
- Create too many similar tools (confuses agent)
- Use vague descriptions
- Return raw error messages to users

### 3. Prompts

✅ **DO:**
- Use system prompts to define agent personality
- Include examples in tool descriptions
- Be specific about expected behavior

❌ **DON'T:**
- Make prompts too long (reduces context window)
- Contradict yourself in prompts

### 4. Performance

✅ **DO:**
- Set appropriate `max_iterations`
- Use faster models for simple tasks
- Cache frequent queries if possible

❌ **DON'T:**
- Set max_iterations too high (slow)
- Use large models for all requests

---

## 🚀 Future Enhancements

Planned features:

1. **RAG Integration** - Add document Q&A as a tool
2. **Response Streaming** - Stream agent responses in real-time
3. **Tool Chaining** - More complex multi-tool workflows
4. **Memory Persistence** - Save/load conversation history
5. **Analytics** - Track tool usage and performance
6. **Custom Tools** - Easy plugin system for new tools
7. **Multi-Agent** - Collaborate between specialized agents

---

## 📞 Support

**Issues:**
- Check logs in terminal running backend
- Enable `verbose: true` in config
- Review this documentation

**Common Questions:**
- Q: How many sessions can I have?
  - A: Unlimited, but each uses memory

- Q: Does memory persist after restart?
  - A: No, memory is in-process only

- Q: Can I use other LLM providers?
  - A: Yes, but requires implementing langchain-compatible client

---

## 📝 License

MIT License - Same as BankSight-AI project

---

**Built with ❤️ using LangChain + Groq + FastAPI**

**Documentation Version:** 1.0.0
**Last Updated:** November 15, 2025
