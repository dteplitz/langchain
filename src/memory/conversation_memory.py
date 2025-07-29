"""
Conversation memory management with SQLite persistence.

This module provides conversation memory functionality using SQLite
for persistent storage of chat history.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMemory
from src.config import get_settings


class SQLiteConversationMemory(BaseMemory):
    """
    SQLite-based conversation memory for persistent chat history.
    
    Stores conversation history in SQLite database with session management.
    """
    
    session_id: str
    db_path: str = "chat_memory.db"
    
    def __init__(self, session_id: str, db_path: str = "chat_memory.db"):
        """
        Initialize SQLite conversation memory.
        
        Args:
            session_id: Unique session identifier
            db_path: Path to SQLite database file
        """
        super().__init__(session_id=session_id, db_path=db_path)
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            conn.commit()
    
    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return ["chat_history"]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load memory variables from SQLite.
        
        Args:
            inputs: Input dictionary
            
        Returns:
            Dict[str, Any]: Memory variables including chat history
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT message, response, timestamp 
                FROM conversations 
                WHERE session_id = ? 
                ORDER BY timestamp ASC
            """, (self.session_id,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "message": row[0],
                    "response": row[1],
                    "timestamp": row[2]
                })
            
            return {"chat_history": history}
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """
        Save context to SQLite database.
        
        Args:
            inputs: Input dictionary containing user message
            outputs: Output dictionary containing agent response
        """
        message = inputs.get("message", "")
        response = outputs.get("response", "")
        metadata = json.dumps(inputs.get("metadata", {}))
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO conversations (session_id, message, response, metadata)
                VALUES (?, ?, ?, ?)
            """, (self.session_id, message, response, metadata))
            conn.commit()
    
    def clear(self) -> None:
        """Clear memory for current session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM conversations WHERE session_id = ?", (self.session_id,))
            conn.commit()


def create_memory(session_id: str) -> SQLiteConversationMemory:
    """
    Create a new conversation memory instance.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        SQLiteConversationMemory: Configured memory instance
    """
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
    memory = SQLiteConversationMemory(session_id, db_path)
    return memory


def get_conversation_history(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session identifier
        limit: Maximum number of messages to return
        
    Returns:
        List[Dict[str, Any]]: Conversation history
    """
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT message, response, timestamp 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (session_id, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "message": row[0],
                "response": row[1],
                "timestamp": row[2]
            })
        
        return list(reversed(history)) 