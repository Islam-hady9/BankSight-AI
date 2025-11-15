"""
Main AI agent orchestrator.
"""
from typing import Dict, List, Optional
from .intent_classifier import classify_intent
from .query_router import route_query
from ..utils.logger import logger

# Try to import LangChain agent (optional dependency)
try:
    from .langchain_agent import get_langchain_response
    LANGCHAIN_AVAILABLE = True
    logger.info("✅ LangChain agent available")
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logger.warning(f"⚠️ LangChain not available: {e}")


class BankingAgent:
    """Main banking assistant agent."""

    def __init__(self, use_langchain: bool = True):
        """
        Initialize banking agent.

        Args:
            use_langchain: If True and available, use LangChain agent with memory
        """
        self.conversation_history = []
        self.use_langchain = use_langchain and LANGCHAIN_AVAILABLE

        if self.use_langchain:
            logger.info("🤖 Using LangChain agent with conversation memory")
        else:
            logger.info("🤖 Using classic intent-routing agent")

    async def process_query(
        self,
        query: str,
        session_id: str = "default",
        old_messages: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process user query end-to-end.

        Args:
            query: User query
            session_id: Session ID for conversation tracking
            old_messages: Optional previous conversation history for LangChain agent
                         Format: [{"user": "...", "assistant": "..."}]

        Returns:
            Dict with response and metadata
        """
        logger.info(f"Processing query [{session_id}]: {query[:100]}...")

        try:
            # Use LangChain agent if available and enabled
            if self.use_langchain:
                return await self._process_with_langchain(query, session_id, old_messages)
            else:
                return await self._process_classic(query, session_id)

        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return {
                "success": False,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "intent": "error",
                "sources": [],
                "metadata": {"error": str(e), "session_id": session_id}
            }

    async def _process_with_langchain(
        self,
        query: str,
        session_id: str,
        old_messages: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process query using LangChain agent with memory.

        Args:
            query: User query
            session_id: Session ID
            old_messages: Optional previous messages

        Returns:
            Response dict
        """
        result = await get_langchain_response(
            message=query,
            session_id=session_id,
            old_messages=old_messages
        )

        # Format response to match classic agent structure
        return {
            "success": result.get("success", True),
            "response": result.get("response", ""),
            "intent": "langchain_agent",
            "sources": [],
            "tools_used": result.get("tools_used", []),
            "metadata": {
                "session_id": session_id,
                "query": query,
                "agent_type": "langchain"
            }
        }

    async def _process_classic(self, query: str, session_id: str) -> Dict:
        """
        Process query using classic intent classification and routing.

        Args:
            query: User query
            session_id: Session ID

        Returns:
            Response dict
        """
        # 1. Classify intent
        intent = classify_intent(query)

        # 2. Route to appropriate handler
        result = await route_query(query, intent)

        # 3. Add to conversation history
        self.conversation_history.append({
            "query": query,
            "response": result["response"],
            "intent": result["intent"]
        })

        # 4. Return result
        return {
            "success": True,
            "response": result["response"],
            "intent": result["intent"],
            "sources": result.get("sources", []),
            "metadata": {
                "session_id": session_id,
                "query": query,
                "agent_type": "classic"
            }
        }


# Global agent instance (configuration from config.yaml)
from ..config import config as app_config
agent = BankingAgent(use_langchain=app_config.agent_use_langchain)
