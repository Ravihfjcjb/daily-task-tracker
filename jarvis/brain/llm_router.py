"""
LLM Router - Routes requests between online and offline LLMs.
Automatically switches based on connectivity and configuration.
"""

import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Available LLM providers."""
    OPENAI = "openai"
    GEMINI = "gemini"
    OLLAMA = "ollama"


class LLMRouter:
    """
    Routes LLM requests to appropriate provider.
    """
    
    def __init__(self, config):
        """
        Initialize LLM router.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.online_provider = None
        self.offline_provider = None
        
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """Initialize online and offline LLM providers."""
        try:
            # Initialize offline provider (Ollama)
            if self.config.llm.offline_model == "ollama":
                self.offline_provider = OllamaProvider(self.config)
                logger.info("Ollama provider initialized")
            
            # Initialize online provider
            if self.config.llm.online_provider == "openai":
                self.online_provider = OpenAIProvider(self.config)
                logger.info("OpenAI provider initialized")
            elif self.config.llm.online_provider == "gemini":
                self.online_provider = GeminiProvider(self.config)
                logger.info("Gemini provider initialized")
        
        except Exception as e:
            logger.error(f"Failed to initialize LLM providers: {e}")
    
    async def get_response(self, prompt: str, context, skills: dict) -> str:
        """
        Get response from appropriate LLM.
        
        Args:
            prompt: User's prompt
            context: Current context
            skills: Available skills
            
        Returns:
            LLM response
        """
        try:
            if context.is_internet_available and self.online_provider:
                logger.info("Using ONLINE LLM provider")
                response = await self.online_provider.generate(
                    prompt, context, skills
                )
            else:
                logger.info("Using OFFLINE LLM provider")
                response = await self.offline_provider.generate(
                    prompt, context, skills
                )
            
            return response
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return "I apologize, but I encountered an error processing your request."


class OpenAIProvider:
    """OpenAI GPT provider."""
    
    def __init__(self, config):
        self.config = config
        try:
            import openai
            openai.api_key = config.llm.openai_api_key
            self.client = openai.AsyncOpenAI(api_key=config.llm.openai_api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
    
    async def generate(self, prompt: str, context, skills: dict) -> str:
        """
        Generate response using OpenAI GPT.
        
        Args:
            prompt: User's prompt
            context: Current context
            skills: Available skills
            
        Returns:
            Generated response
        """
        try:
            messages = [
                {"role": "system", "content": self._get_system_prompt(context, skills)},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=self.config.llm.temperature,
                max_tokens=self.config.llm.max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise
    
    def _get_system_prompt(self, context, skills: dict) -> str:
        """Generate system prompt."""
        skills_list = ", ".join(skills.keys()) if skills else "None"
        return f"""
        You are JARVIS, an advanced AI assistant inspired by Iron Man's AI.
        You are helpful, friendly, funny, and confident.
        
        User: {context.user_name}
        Current Mode: {context.current_mode.value}
        Available Skills: {skills_list}
        
        Respond naturally and conversationally. If asked to perform an action,
        use the available skills. Be concise but thorough.
        """


class GeminiProvider:
    """Google Gemini provider."""
    
    def __init__(self, config):
        self.config = config
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.llm.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
    
    async def generate(self, prompt: str, context, skills: dict) -> str:
        """
        Generate response using Gemini.
        
        Args:
            prompt: User's prompt
            context: Current context
            skills: Available skills
            
        Returns:
            Generated response
        """
        try:
            system_prompt = self._get_system_prompt(context, skills)
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise
    
    def _get_system_prompt(self, context, skills: dict) -> str:
        """Generate system prompt."""
        skills_list = ", ".join(skills.keys()) if skills else "None"
        return f"""
        You are JARVIS, an advanced AI assistant inspired by Iron Man's AI.
        You are helpful, friendly, funny, and confident.
        
        User: {context.user_name}
        Current Mode: {context.current_mode.value}
        Available Skills: {skills_list}
        
        Respond naturally and conversationally. If asked to perform an action,
        use the available skills. Be concise but thorough.
        """


class OllamaProvider:
    """Ollama (Offline) provider."""
    
    def __init__(self, config):
        self.config = config
        try:
            import ollama
            self.client = ollama
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
    
    async def generate(self, prompt: str, context, skills: dict) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: User's prompt
            context: Current context
            skills: Available skills
            
        Returns:
            Generated response
        """
        try:
            system_prompt = self._get_system_prompt(context, skills)
            
            # Ollama doesn't have async, so we run in thread pool
            import asyncio
            loop = asyncio.get_event_loop()
            
            response = await loop.run_in_executor(
                None,
                self.client.generate,
                self.config.llm.ollama_model,
                f"{system_prompt}\n\nUser: {prompt}",
                False
            )
            
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
    
    def _get_system_prompt(self, context, skills: dict) -> str:
        """Generate system prompt."""
        skills_list = ", ".join(skills.keys()) if skills else "None"
        return f"""
        You are JARVIS, an advanced AI assistant inspired by Iron Man's AI.
        You are helpful, friendly, funny, and confident.
        
        User: {context.user_name}
        Current Mode: {context.current_mode.value}
        Available Skills: {skills_list}
        
        Respond naturally and conversationally. If asked to perform an action,
        use the available skills. Be concise but thorough.
        """
