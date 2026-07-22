"""
Memory Management System
Handles short-term and long-term memory with SQLite and FAISS.
"""

import logging
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class Memory:
    """
    Manages JARVIS memory system.
    Combines SQLite for structured data and FAISS for semantic search.
    """
    
    def __init__(self, config):
        """
        Initialize memory system.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.db_path = config.memory.sqlite_db
        self.faiss_path = config.memory.faiss_index_path
        
        # Create database
        self._init_database()
        
        # Initialize embeddings
        self._init_embeddings()
    
    def _init_database(self) -> None:
        """Initialize SQLite database."""
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    mode TEXT DEFAULT 'online'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    reminder_time DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _init_embeddings(self) -> None:
        """Initialize FAISS embeddings."""
        try:
            import faiss
            import numpy as np
            from sentence_transformers import SentenceTransformer
            
            self.embedding_model = SentenceTransformer(
                self.config.memory.embedding_model
            )
            
            Path(self.faiss_path).parent.mkdir(parents=True, exist_ok=True)
            
            logger.info("Embeddings initialized")
        except Exception as e:
            logger.warning(f"FAISS initialization skipped: {e}")
    
    async def add_message(self, message: str, sender: str, mode: str = "online") -> None:
        """
        Add message to memory.
        
        Args:
            message: Message content
            sender: Message sender ("user" or "jarvis")
            mode: Operating mode
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO messages (sender, message, mode) VALUES (?, ?, ?)",
                (sender, message, mode)
            )
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Message stored from {sender}")
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
    
    async def get_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent conversation history.
        
        Args:
            limit: Number of messages to retrieve
            
        Returns:
            List of messages
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT timestamp, sender, message FROM messages ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {"timestamp": row[0], "sender": row[1], "message": row[2]}
                for row in reversed(rows)
            ]
        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return []
    
    async def set_user_data(self, key: str, value: Any) -> None:
        """
        Store user data.
        
        Args:
            key: Data key
            value: Data value
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            value_json = json.dumps(value) if not isinstance(value, str) else value
            
            cursor.execute(
                "INSERT OR REPLACE INTO user_data (key, value) VALUES (?, ?)",
                (key, value_json)
            )
            
            conn.commit()
            conn.close()
            
            logger.debug(f"User data stored: {key}")
        except Exception as e:
            logger.error(f"Failed to set user data: {e}")
    
    async def get_user_data(self, key: str) -> Optional[Any]:
        """
        Retrieve user data.
        
        Args:
            key: Data key
            
        Returns:
            Data value or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT value FROM user_data WHERE key = ?", (key,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                try:
                    return json.loads(row[0])
                except:
                    return row[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get user data: {e}")
            return None
