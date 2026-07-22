"""
Speech Recognition - Listen Module
Handles voice input with offline and online options.
"""

import logging
import asyncio
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class Listener:
    """
    Handles speech recognition.
    Uses Faster Whisper for offline mode.
    """
    
    def __init__(self, config):
        """
        Initialize listener.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.is_listening = False
        self.wake_words = config.speech.wake_words
        
        self._init_speech_recognition()
    
    def _init_speech_recognition(self) -> None:
        """Initialize speech recognition."""
        try:
            from faster_whisper import WhisperModel
            
            # Load offline speech model
            self.whisper_model = WhisperModel(
                "base",
                device="cuda",
                compute_type="float16"
            )
            
            logger.info("Faster Whisper model loaded")
        except Exception as e:
            logger.warning(f"Faster Whisper initialization failed: {e}")
    
    async def listen_for_wakeword(self) -> bool:
        """
        Listen for wake word.
        
        Returns:
            True if wake word detected
        """
        try:
            logger.info(f"Listening for wake words: {self.wake_words}")
            # Implementation would go here
            return True
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")
            return False
    
    async def listen(self, timeout: int = 30) -> Optional[str]:
        """
        Listen for user speech.
        
        Args:
            timeout: Maximum listening time in seconds
            
        Returns:
            Transcribed text or None
        """
        try:
            self.is_listening = True
            logger.info("Listening for speech...")
            
            # Implementation would go here
            # This is a placeholder
            
            return None
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        finally:
            self.is_listening = False
    
    async def continuous_listen(self, callback: Callable[[str], None]) -> None:
        """
        Continuously listen and call callback on detected speech.
        
        Args:
            callback: Function to call with transcribed text
        """
        try:
            while True:
                # Check for wake word
                if await self.listen_for_wakeword():
                    # Listen for command
                    text = await self.listen()
                    if text:
                        await callback(text)
                
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Continuous listening error: {e}")
    
    async def stop_listening(self) -> None:
        """Stop listening."""
        self.is_listening = False
        logger.info("Stopped listening")
