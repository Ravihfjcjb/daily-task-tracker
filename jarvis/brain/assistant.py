"""
JARVIS Brain - Main AI Assistant Logic
Handles reasoning, decision making, and command execution.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ModeType(Enum):
    """Operating modes."""
    OFFLINE = "offline"
    ONLINE = "online"


class StatusType(Enum):
    """Status types."""
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    BUSY = "busy"


@dataclass
class ConversationMessage:
    """A single conversation message."""
    timestamp: datetime
    sender: str  # "user" or "jarvis"
    message: str
    mode: ModeType = ModeType.ONLINE
    confidence: float = 1.0


@dataclass
class JarvisContext:
    """Context for JARVIS operations."""
    user_name: str = "User"
    current_mode: ModeType = ModeType.ONLINE
    current_status: StatusType = StatusType.IDLE
    conversation_history: List[ConversationMessage] = field(default_factory=list)
    is_internet_available: bool = True
    properties: Dict[str, Any] = field(default_factory=dict)


class JarvisAssistant:
    """
    Main JARVIS Assistant class.
    Orchestrates all components and manages state.
    """
    
    def __init__(self, config):
        """
        Initialize JARVIS assistant.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.context = JarvisContext()
        self.llm_router = None
        self.memory = None
        self.speech = None
        self.automation = None
        self.skills = {}
        
        self._initialize_components()
    
    def _initialize_components(self) -> None:
        """Initialize all components."""
        try:
            # Import here to avoid circular dependencies
            from brain.llm_router import LLMRouter
            from brain.memory import Memory
            from speech.speak import Speaker
            from speech.listen import Listener
            
            self.llm_router = LLMRouter(self.config)
            self.memory = Memory(self.config)
            self.speech = {
                'speaker': Speaker(self.config),
                'listener': Listener(self.config)
            }
            
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    async def process_input(self, user_input: str) -> str:
        """
        Process user input and generate response.
        
        Args:
            user_input: User's spoken or typed input
            
        Returns:
            JARVIS's response
        """
        try:
            self.context.current_status = StatusType.THINKING
            
            # Check internet connectivity
            await self._check_internet()
            
            # Add to conversation history
            self.context.conversation_history.append(
                ConversationMessage(
                    timestamp=datetime.now(),
                    sender="user",
                    message=user_input,
                    mode=self.context.current_mode
                )
            )
            
            # Store in memory
            await self.memory.add_message(user_input, "user")
            
            # Get response from LLM
            response = await self.llm_router.get_response(
                user_input,
                self.context,
                self.skills
            )
            
            # Add to conversation history
            self.context.conversation_history.append(
                ConversationMessage(
                    timestamp=datetime.now(),
                    sender="jarvis",
                    message=response
                )
            )
            
            # Store response in memory
            await self.memory.add_message(response, "jarvis")
            
            self.context.current_status = StatusType.SPEAKING
            return response
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            error_response = "I encountered an error processing your request. Please try again."
            self.context.current_status = StatusType.IDLE
            return error_response
        finally:
            self.context.current_status = StatusType.IDLE
    
    async def _check_internet(self) -> None:
        """
        Check if internet is available and update mode.
        """
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.context.is_internet_available = True
            self.context.current_mode = ModeType.ONLINE
            logger.info("Internet available - Switched to ONLINE mode")
        except:
            self.context.is_internet_available = False
            self.context.current_mode = ModeType.OFFLINE
            logger.info("Internet unavailable - Switched to OFFLINE mode")
    
    def register_skill(self, skill_name: str, skill_instance: Any) -> None:
        """
        Register a skill plugin.
        
        Args:
            skill_name: Name of the skill
            skill_instance: Skill instance
        """
        self.skills[skill_name] = skill_instance
        logger.info(f"Skill registered: {skill_name}")
    
    def get_context(self) -> JarvisContext:
        """
        Get current context.
        
        Returns:
            Current context
        """
        return self.context
    
    def set_user_name(self, name: str) -> None:
        """
        Set user's name.
        
        Args:
            name: User's name
        """
        self.context.user_name = name
        logger.info(f"User name set to: {name}")
    
    async def shutdown(self) -> None:
        """
        Gracefully shutdown JARVIS.
        """
        try:
            logger.info("JARVIS shutting down...")
            # Add cleanup logic here
            logger.info("JARVIS shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
