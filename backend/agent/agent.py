"""
Main AI agent orchestrator.
"""
from typing import Dict
from .intent_classifier import classify_intent
from .query_router import route_query
from ..utils.logger import logger


class BankingAgent:
    """Main banking assistant agent."""

    def __init__(self):
        self.conversation_history = []

    async def process_query(self, query: str, session_id: str = "default") -> Dict:
        """
        Process user query end-to-end.

        Args:
            query: User query
            session_id: Session ID for conversation tracking

        Returns:
            Dict with response and metadata
        """
        logger.info(f"Processing query [{session_id}]: {query}")

        try:
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
                    "query": query
                }
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "intent": "error",
                "sources": [],
                "metadata": {"error": str(e)}
            }


# Global agent instance
agent = BankingAgent()
