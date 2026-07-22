"""
Text-to-Speech - Speak Module
Handles voice output with offline and online options.
"""

import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)


class Speaker:
    """
    Handles text-to-speech.
    Uses pyttsx3 for offline, ElevenLabs for online.
    """
    
    def __init__(self, config):
        """
        Initialize speaker.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.is_speaking = False
        
        self._init_offline_tts()
        self._init_online_tts()
    
    def _init_offline_tts(self) -> None:
        """Initialize offline TTS (pyttsx3)."""
        try:
            import pyttsx3
            
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.config.speech.speech_rate)
            
            logger.info("pyttsx3 TTS initialized")
        except Exception as e:
            logger.warning(f"pyttsx3 initialization failed: {e}")
            self.engine = None
    
    def _init_online_tts(self) -> None:
        """Initialize online TTS (ElevenLabs)."""
        try:
            from elevenlabs import client as elevenlabs_client
            
            self.elevenlabs_client = elevenlabs_client(
                api_key=self.config.speech.elevenlabs_api_key
            )
            
            logger.info("ElevenLabs TTS initialized")
        except Exception as e:
            logger.warning(f"ElevenLabs initialization failed: {e}")
            self.elevenlabs_client = None
    
    async def speak(self, text: str, online: bool = False) -> None:
        """
        Speak text.
        
        Args:
            text: Text to speak
            online: Use online TTS if available
        """
        try:
            self.is_speaking = True
            
            if online and self.elevenlabs_client:
                await self._speak_online(text)
            elif self.engine:
                await self._speak_offline(text)
            else:
                logger.warning("No TTS engine available")
        except Exception as e:
            logger.error(f"Speech error: {e}")
        finally:
            self.is_speaking = False
    
    async def _speak_offline(self, text: str) -> None:
        """
        Speak using offline TTS.
        
        Args:
            text: Text to speak
        """
        try:
            logger.info(f"Speaking (offline): {text}")
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._speak_with_engine,
                text
            )
        except Exception as e:
            logger.error(f"Offline TTS error: {e}")
    
    def _speak_with_engine(self, text: str) -> None:
        """Helper method for pyttsx3."""
        self.engine.say(text)
        self.engine.runAndWait()
    
    async def _speak_online(self, text: str) -> None:
        """
        Speak using online TTS.
        
        Args:
            text: Text to speak
        """
        try:
            logger.info(f"Speaking (online): {text}")
            
            # Implementation would go here
            # This is a placeholder
        except Exception as e:
            logger.error(f"Online TTS error: {e}")
    
    async def stop_speaking(self) -> None:
        """Stop speaking."""
        self.is_speaking = False
        if self.engine:
            self.engine.stop()
        logger.info("Stopped speaking")
