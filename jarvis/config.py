"""
Configuration management for JARVIS.
Handles all settings, API keys, and environment variables.
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """LLM configuration."""
    offline_model: str = "ollama"
    online_provider: str = "openai"  # or "gemini"
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    temperature: float = 0.7
    max_tokens: int = 2048


@dataclass
class SpeechConfig:
    """Speech configuration."""
    offline_tts: str = "pyttsx3"
    online_tts: str = "elevenlabs"
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    speech_rate: int = 150
    wake_words: list = None
    noise_suppression: bool = True
    
    def __post_init__(self):
        if self.wake_words is None:
            self.wake_words = ["hey jarvis", "jarvis"]


@dataclass
class MemoryConfig:
    """Memory configuration."""
    sqlite_db: str = "data/jarvis.db"
    faiss_index_path: str = "data/faiss_index"
    memory_max_items: int = 10000
    embedding_model: str = "all-MiniLM-L6-v2"


@dataclass
class UIConfig:
    """UI configuration."""
    theme: str = "dark"
    primary_color: str = "#0066CC"
    accent_color: str = "#00FF00"
    window_width: int = 900
    window_height: int = 1000
    animation_speed: int = 200


class Config:
    """Main configuration class."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self.base_path = Path(__file__).parent
        
        # Initialize sub-configs
        self.llm = LLMConfig()
        self.speech = SpeechConfig()
        self.memory = MemoryConfig()
        self.ui = UIConfig()
        
        # Create data directories
        self._create_directories()
        
        # Load from file if exists
        if self.config_file.exists():
            self._load_from_file()
        else:
            self._load_from_env()
    
    def _create_directories(self) -> None:
        """Create necessary directories."""
        directories = [
            self.base_path / "data",
            self.base_path / "gui" / "assets",
            self.base_path / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # LLM
        self.llm.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.llm.online_provider = os.getenv("LLM_PROVIDER", "openai")
        
        # Speech
        self.speech.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
        logger.info("Configuration loaded from environment variables")
    
    def _load_from_file(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            if "llm" in config_data:
                self.llm = LLMConfig(**config_data["llm"])
            if "speech" in config_data:
                self.speech = SpeechConfig(**config_data["speech"])
            if "memory" in config_data:
                self.memory = MemoryConfig(**config_data["memory"])
            if "ui" in config_data:
                self.ui = UIConfig(**config_data["ui"])
            
            logger.info(f"Configuration loaded from {self.config_file}")
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}. Using defaults.")
            self._load_from_env()
    
    def save_to_file(self) -> None:
        """Save configuration to JSON file."""
        try:
            config_data = {
                "llm": asdict(self.llm),
                "speech": asdict(self.speech),
                "memory": asdict(self.memory),
                "ui": asdict(self.ui)
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get_dict(self) -> dict:
        """Get configuration as dictionary."""
        return {
            "llm": asdict(self.llm),
            "speech": asdict(self.speech),
            "memory": asdict(self.memory),
            "ui": asdict(self.ui)
        }
