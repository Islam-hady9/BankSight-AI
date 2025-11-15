"""
LangChain-based agent with conversation memory for BankSight AI.
"""
from typing import Optional, List, Dict
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_groq import ChatGroq
from .langchain_tools import create_banking_tools
from ..llm.prompts import BANKING_ASSISTANT_SYSTEM
from ..config import config
from ..utils.logger import logger
import os


class BankSightAgent:
    """
    LangChain-based banking agent with conversation memory.
    """

    def __init__(self, session_id: str = "default"):
        """
        Initialize the BankSight agent.

        Args:
            session_id: Unique session identifier for conversation memory
        """
        self.session_id = session_id
        self.memory = self._create_memory()
        self.llm = self._create_llm()
        self.tools = create_banking_tools()
        self.agent_executor = self._create_agent()

        logger.info(f"✅ LangChain agent initialized for session: {session_id}")

    def _create_memory(self) -> ConversationBufferMemory:
        """Create conversation memory for the agent."""
        memory = ConversationBufferMemory(
            memory_key=f"chat_history_{self.session_id}",
            input_key="input",
            output_key="output",
            return_messages=True
        )
        return memory

    def _create_llm(self) -> ChatGroq:
        """Create Groq LLM instance for LangChain."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=config.llm_groq_model_name,
            temperature=config.llm_groq_temperature,
            max_tokens=config.llm_groq_max_tokens,
        )

        logger.info(f"✅ ChatGroq LLM initialized: {config.llm_groq_model_name}")
        return llm

    def _create_agent(self) -> AgentExecutor:
        """Create the tool-calling agent with memory."""

        # Create prompt template with chat history
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(BANKING_ASSISTANT_SYSTEM),
            MessagesPlaceholder(variable_name=f"chat_history_{self.session_id}"),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create the tool-calling agent
        agent_chain = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        # Wrap in AgentExecutor with memory
        agent_executor = AgentExecutor(
            agent=agent_chain,
            memory=self.memory,
            tools=self.tools,
            verbose=config.agent_verbose,
            handle_parsing_errors=True,
            max_iterations=config.agent_max_iterations,
            return_intermediate_steps=True,
        )

        logger.info(f"✅ Agent executor created with {len(self.tools)} tools (max_iterations={config.agent_max_iterations})")
        return agent_executor

    def invoke(self, message: str, old_messages: Optional[List[Dict]] = None) -> Dict:
        """
        Invoke the agent with a user message.

        Args:
            message: User's input message
            old_messages: Optional list of previous messages to inject into memory
                         Format: [{"user": "...", "assistant": "..."}]

        Returns:
            Dict with agent response and metadata
        """
        try:
            # Inject old history into memory if provided
            if old_messages:
                logger.info(f"Injecting {len(old_messages)} old messages into memory")
                for item in old_messages:
                    if item.get("user"):
                        self.memory.chat_memory.add_user_message(item["user"])
                    if item.get("assistant"):
                        self.memory.chat_memory.add_ai_message(item["assistant"])

            # Invoke the agent
            logger.info(f"Invoking agent with message: {message[:100]}...")
            result = self.agent_executor.invoke({"input": message})

            # Extract response
            response = result.get("output", "No response generated")
            intermediate_steps = result.get("intermediate_steps", [])

            # Log tool usage
            tools_used = []
            for step in intermediate_steps:
                if len(step) >= 2:
                    action = step[0]
                    tools_used.append({
                        "tool": action.tool,
                        "input": action.tool_input
                    })

            logger.info(f"Agent response generated. Tools used: {len(tools_used)}")

            return {
                "success": True,
                "response": response,
                "tools_used": tools_used,
                "session_id": self.session_id
            }

        except Exception as e:
            logger.error(f"Agent invocation error: {e}", exc_info=True)
            return {
                "success": False,
                "response": f"I apologize, but I encountered an error: {str(e)}",
                "error": str(e),
                "session_id": self.session_id
            }

    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()
        logger.info(f"Memory cleared for session: {self.session_id}")

    def get_memory_history(self) -> List[Dict]:
        """
        Get conversation history from memory.

        Returns:
            List of message dictionaries
        """
        messages = []
        for msg in self.memory.chat_memory.messages:
            if hasattr(msg, 'type'):
                messages.append({
                    "type": msg.type,
                    "content": msg.content
                })
        return messages


# Global agent instances (one per session)
_agent_instances: Dict[str, BankSightAgent] = {}


def get_agent(session_id: str = "default") -> BankSightAgent:
    """
    Get or create an agent instance for a session.

    Args:
        session_id: Session identifier

    Returns:
        BankSightAgent instance
    """
    if session_id not in _agent_instances:
        _agent_instances[session_id] = BankSightAgent(session_id=session_id)
        logger.info(f"Created new agent instance for session: {session_id}")
    return _agent_instances[session_id]


def clear_agent_session(session_id: str):
    """
    Clear an agent session.

    Args:
        session_id: Session identifier
    """
    if session_id in _agent_instances:
        _agent_instances[session_id].clear_memory()
        del _agent_instances[session_id]
        logger.info(f"Cleared agent session: {session_id}")


async def get_langchain_response(
    message: str,
    session_id: str = "default",
    old_messages: Optional[List[Dict]] = None
) -> Dict:
    """
    Get response from LangChain agent.

    Args:
        message: User message
        session_id: Session ID for conversation memory
        old_messages: Optional previous conversation history

    Returns:
        Dict with response and metadata
    """
    agent = get_agent(session_id)
    result = agent.invoke(message, old_messages=old_messages)
    return result
