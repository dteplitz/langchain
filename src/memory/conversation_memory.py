"""
Conversation memory management with SQLite persistence.

This module provides conversation memory functionality using SQLite
for persistent storage of chat history and session metadata.
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
    
    Stores conversation history in SQLite database with session management
    and session metadata in JSON format.
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
            # Create sessions table for session metadata
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    metadata TEXT DEFAULT '{}',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create conversations table for chat history
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            """)
            conn.commit()
    
    def set_session_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Set or update session metadata.
        
        Args:
            metadata: Dictionary containing session metadata
        """
        with sqlite3.connect(self.db_path) as conn:
            # Get existing metadata and merge with new metadata
            existing_metadata = self.get_session_metadata()
            merged_metadata = {**existing_metadata, **metadata}
            
            conn.execute("""
                INSERT OR REPLACE INTO sessions (session_id, metadata, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (self.session_id, json.dumps(merged_metadata)))
            conn.commit()
    
    def get_session_metadata(self) -> Dict[str, Any]:
        """
        Get session metadata.
        
        Returns:
            Dict[str, Any]: Session metadata dictionary
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT metadata FROM sessions WHERE session_id = ?
            """, (self.session_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                try:
                    return json.loads(result[0])
                except json.JSONDecodeError:
                    return {}
            return {}
    
    def update_session_metadata(self, key: str, value: Any) -> None:
        """
        Update a specific key in session metadata.
        
        Args:
            key: Metadata key to update
            value: New value for the key
        """
        metadata = self.get_session_metadata()
        metadata[key] = value
        self.set_session_metadata(metadata)
    
    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific value from session metadata.
        Supports nested key access using dot notation (e.g., "user.profile.name").
        
        Args:
            key: Metadata key to retrieve (supports dot notation for nested access)
            default: Default value if key doesn't exist
            
        Returns:
            Any: Value for the key or default
        """
        metadata = self.get_session_metadata()
        
        # Handle nested key access
        if "." in key:
            keys = key.split(".")
            current = metadata
            
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return default
            
            return current
        
        # Handle simple key access
        return metadata.get(key, default)
    
    def set_user_info(self, user_info: Dict[str, Any]) -> None:
        """
        Set user information in session metadata.
        
        Args:
            user_info: Dictionary containing user information
        """
        self.update_session_metadata("user_info", user_info)
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get user information from session metadata.
        
        Returns:
            Dict[str, Any]: User information dictionary
        """
        return self.get_metadata_value("user_info", {})
    
    def set_conversation_objective(self, objective: str) -> None:
        """
        Set or update the conversation objective in session metadata.
        
        Args:
            objective: The conversation objective/context
        """
        self.update_session_metadata("conversation_objective", objective)
    
    def get_conversation_objective(self) -> Optional[str]:
        """
        Get the conversation objective from session metadata.
        
        Returns:
            Optional[str]: The conversation objective or None if not set
        """
        return self.get_metadata_value("conversation_objective")
    
    def update_conversation_objective(self, objective: str) -> None:
        """
        Update the conversation objective in session metadata.
        
        Args:
            objective: The updated conversation objective
        """
        self.set_conversation_objective(objective)
    
    def clear_objective(self) -> None:
        """Clear the conversation objective from session metadata."""
        metadata = self.get_session_metadata()
        if "conversation_objective" in metadata:
            del metadata["conversation_objective"]
            self.set_session_metadata(metadata)
    
    def set_conversation_state(self, state: Dict[str, Any]) -> None:
        """
        Set conversation state in session metadata.
        
        Args:
            state: Dictionary containing conversation state
        """
        self.update_session_metadata("conversation_state", state)
    
    def get_conversation_state(self) -> Dict[str, Any]:
        """
        Get conversation state from session metadata.
        
        Returns:
            Dict[str, Any]: Conversation state dictionary
        """
        return self.get_metadata_value("conversation_state", {})
    
    def update_conversation_state(self, key: str, value: Any) -> None:
        """
        Update a specific key in conversation state.
        
        Args:
            key: State key to update
            value: New value for the key
        """
        state = self.get_conversation_state()
        state[key] = value
        self.set_conversation_state(state)
    
    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return ["chat_history", "conversation_objective", "session_metadata"]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load memory variables from SQLite.
        
        Args:
            inputs: Input dictionary
            
        Returns:
            Dict[str, Any]: Memory variables including chat history, objective, and metadata
        """
        with sqlite3.connect(self.db_path) as conn:
            # Get chat history
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
            
            # Get session metadata
            session_metadata = self.get_session_metadata()
            conversation_objective = session_metadata.get("conversation_objective")
            
            return {
                "chat_history": history,
                "conversation_objective": conversation_objective,
                "session_metadata": session_metadata
            }
    
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
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (self.session_id,))
            conn.commit()

    def set_welcome_status(self, welcome_done: bool) -> None:
        """
        Set whether the welcome message has been shown.
        
        Args:
            welcome_done: Whether welcome message has been shown
        """
        self.update_session_metadata("welcome_done", welcome_done)
    
    def get_welcome_status(self) -> bool:
        """
        Get whether the welcome message has been shown.
        
        Returns:
            bool: Whether welcome message has been shown
        """
        return self.get_metadata_value("welcome_done", False)
    
    def set_reasons(self, reasons: list) -> None:
        """
        Set the list of reasons for the conversation.
        
        Args:
            reasons: List of reason strings
        """
        self.update_session_metadata("reasons", reasons)
    
    def get_reasons(self) -> list:
        """
        Get the list of reasons for the conversation.
        
        Returns:
            list: List of reason strings
        """
        return self.get_metadata_value("reasons", [])
    
    def add_reason(self, reason: str) -> None:
        """
        Add a reason to the list of reasons.
        
        Args:
            reason: Reason string to add
        """
        reasons = self.get_reasons()
        if reason not in reasons:
            reasons.append(reason)
            self.set_reasons(reasons)
    
    def remove_reason(self, reason: str) -> None:
        """
        Remove a reason from the list of reasons.
        
        Args:
            reason: Reason string to remove
        """
        reasons = self.get_reasons()
        if reason in reasons:
            reasons.remove(reason)
            self.set_reasons(reasons)
    
    def set_reasons_confirmed(self, confirmed: bool) -> None:
        """
        Set whether the reasons have been confirmed.
        
        Args:
            confirmed: Whether reasons have been confirmed
        """
        self.update_session_metadata("reasons_confirmed", confirmed)
    
    def get_reasons_confirmed(self) -> bool:
        """
        Get whether the reasons have been confirmed.
        
        Returns:
            bool: Whether reasons have been confirmed
        """
        return self.get_metadata_value("reasons_confirmed", False)
    
    def set_vars_info_given(self, given: bool) -> None:
        """
        Set whether variable information has been provided.
        
        Args:
            given: Whether variable information has been given
        """
        self.update_session_metadata("vars_info_given", given)
    
    def get_vars_info_given(self) -> bool:
        """
        Get whether variable information has been provided.
        
        Returns:
            bool: Whether variable information has been given
        """
        return self.get_metadata_value("vars_info_given", False)
    
    def set_vars(self, vars_data: dict) -> None:
        """
        Set the variables information.
        
        Args:
            vars_data: Dictionary containing variables (monthly, duration, rate)
        """
        self.update_session_metadata("vars", vars_data)
    
    def get_vars(self) -> dict:
        """
        Get the variables information.
        
        Returns:
            dict: Dictionary containing variables
        """
        return self.get_metadata_value("vars", {"monthly": None, "duration": None, "rate": None})
    
    def update_var(self, var_name: str, value: any) -> None:
        """
        Update a specific variable.
        
        Args:
            var_name: Name of the variable (monthly, duration, rate)
            value: Value to set
        """
        vars_data = self.get_vars()
        vars_data[var_name] = value
        self.set_vars(vars_data)
    
    def get_var(self, var_name: str) -> any:
        """
        Get a specific variable value.
        
        Args:
            var_name: Name of the variable (monthly, duration, rate)
            
        Returns:
            any: Value of the variable or None if not set
        """
        vars_data = self.get_vars()
        return vars_data.get(var_name)
    
    def set_loan_variables(self, monthly: float = None, duration: int = None, rate: float = None) -> None:
        """
        Set loan-related variables.
        
        Args:
            monthly: Monthly payment amount
            duration: Duration in months
            rate: Interest rate
        """
        vars_data = self.get_vars()
        if monthly is not None:
            vars_data["monthly"] = monthly
        if duration is not None:
            vars_data["duration"] = duration
        if rate is not None:
            vars_data["rate"] = rate
        self.set_vars(vars_data)
    
    def get_loan_variables(self) -> dict:
        """
        Get all loan-related variables.
        
        Returns:
            dict: Dictionary with monthly, duration, and rate values
        """
        return self.get_vars()
    
    def is_loan_info_complete(self) -> bool:
        """
        Check if all loan variables have been provided.
        
        Returns:
            bool: True if all variables are set, False otherwise
        """
        vars_data = self.get_vars()
        return all(vars_data.get(key) is not None for key in ["monthly", "duration", "rate"])
    
    def reset_loan_variables(self) -> None:
        """Reset all loan variables to None."""
        self.set_vars({"monthly": None, "duration": None, "rate": None})
        self.set_vars_info_given(False)


def create_memory(session_id: str):
    """
    DEPRECATED: Use create_hybrid_memory from hybrid_conversation_memory instead.
    """
    raise NotImplementedError("create_memory is deprecated. Use create_hybrid_memory from hybrid_conversation_memory instead.")


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