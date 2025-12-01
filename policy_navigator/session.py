"""
Session management for stateful policy navigation.
"""
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from loguru import logger

from policy_navigator.config import Config
from policy_navigator.tools import (
    search_policies,
    check_compliance_risk,
    generate_policy_summary,
    create_audit_trail,
    compare_policies,
    extract_policy_requirements,
    filter_policies_by_metadata,
)

class PolicyChatSession:
    """
    Manages a stateful chat session with the Policy Navigator agent.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or Config.DEFAULT_MODEL
        self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
        
        # Define tools available to the chat session
        # We exclude upload_policy_documents as it's typically an admin task
        self.tools = [
            search_policies,
            check_compliance_risk,
            generate_policy_summary,
            create_audit_trail,
            compare_policies,
            extract_policy_requirements,
            filter_policies_by_metadata,
        ]
        
        logger.info(f"Initializing PolicyChatSession with model: {self.model_name}")
        
        # Initialize chat with tools
        # automatic_function_calling is enabled by default when tools are provided in some SDK versions,
        # but we can configure it explicitly if needed. For now, we rely on the default behavior.
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                tools=self.tools,
                temperature=0.0, # Keep it deterministic for policy queries
                system_instruction="""You are the Policy Navigator, an intelligent compliance assistant.
Your role is to help employees and compliance teams quickly find answers to policy questions.

IMPORTANT: You can search the following policy stores:
- "policy-navigator-hr" for HR policies (vacation, benefits, hiring, employee handbook, remote work)
- "policy-navigator-it" for IT policies (security, access control, data protection)
- "policy-navigator-legal" for legal policies (contracts, compliance, governance)
- "policy-navigator-safety" for safety policies (workplace safety, emergency procedures)

You have access to tools to search policies, assess risks, and generate summaries.
Always use the search_policies tool first to find information before answering.
If the user asks a follow-up question, use the context from the previous turn.

When answering:
1. Cite the policy sources provided by the tools.
2. Be concise and professional.
3. If you perform a search, you don't need to mention "I am searching...", just provide the answer.
"""
            )
        )

    def send_message(self, message: str) -> str:
        """
        Send a message to the chat session and get the response.
        
        Args:
            message: User's message
            
        Returns:
            str: The agent's response
        """
        try:
            logger.info(f"User: {message}")
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error: {str(e)}"

    def get_history(self) -> List[Dict[str, Any]]:
        """Get the chat history."""
        history = []
        for content in self.chat.history:
            role = content.role
            parts = []
            for part in content.parts:
                if part.text:
                    parts.append(part.text)
                # We could also capture function calls/responses here if needed
            
            history.append({
                "role": role,
                "content": " ".join(parts)
            })
        return history
