"""
Hybrid conversation memory combining buffer, summary, and metadata.

This module provides a hybrid conversation memory that combines:
- ConversationBufferMemory: For recent conversation history
- ConversationSummaryMemory: For long-term conversation summaries
- SQLite metadata: For custom session metadata and state
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import BaseMessage
from langchain.schema.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from src.config import get_settings


class HybridConversationMemory:
    """
    Hybrid conversation memory combining buffer, summary, and metadata.
    
    This memory system provides:
    - Recent conversation buffer (last N messages)
    - Long-term conversation summary (for context)
    - Custom metadata storage (user info, conversation state, etc.)
    - Automatic switching between buffer and summary based on conversation length
    """
    
    def __init__(
        self,
        session_id: str,
        db_path: str = "chat_memory.db",
        buffer_window: int = 10,
        summary_threshold: int = 15,
        llm_model: str = "llama3-8b-8192",
        verbose: bool = False
    ):
        """
        Initialize hybrid conversation memory.
        
        Args:
            session_id: Unique session identifier
            db_path: Path to SQLite database file
            buffer_window: Number of recent messages to keep in buffer
            summary_threshold: Number of messages before switching to summary mode
            llm_model: Groq model to use for summarization
            verbose: Enable verbose logging
        """
        self.session_id = session_id
        self.db_path = db_path
        self.buffer_window = buffer_window
        self.summary_threshold = summary_threshold
        self.verbose = verbose
        
        # Initialize LLM for summarization
        settings = get_settings()
        self.llm = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=llm_model,
            temperature=0.1
        )
        
        # Initialize memory components
        self._init_memory_components()
        self._init_database()
        
        # Track conversation length
        self._conversation_length = 0
    
    def _init_memory_components(self) -> None:
        """Initialize buffer and summary memory components."""
        
        # Buffer memory for recent conversations
        self.buffer_memory = ConversationBufferMemory(
            memory_key="recent_history",
            return_messages=True,
            max_token_limit=2000  # Limit buffer size
        )
        
        # Summary memory for long-term context
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="conversation_summary",
            return_messages=True,
            max_token_limit=1000  # Limit summary size
        )
    
    def _init_database(self) -> None:
        """Initialize the SQLite database for metadata."""
        with sqlite3.connect(self.db_path) as conn:
            # Create sessions table for metadata
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    metadata TEXT DEFAULT '{}',
                    conversation_length INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create conversations table for full history (optional)
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
    
    def _get_conversation_length(self) -> int:
        """Get current conversation length from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT conversation_length FROM sessions WHERE session_id = ?
            """, (self.session_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def _update_conversation_length(self, length: int) -> None:
        """Update conversation length in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sessions (session_id, conversation_length, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (self.session_id, length))
            conn.commit()
    
    def _should_use_summary(self) -> bool:
        """Determine if we should use summary mode."""
        return self._conversation_length >= self.summary_threshold
    
    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return ["recent_history", "conversation_summary", "session_metadata"]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load memory variables based on conversation length.
        
        Args:
            inputs: Input dictionary
            
        Returns:
            Dict[str, Any]: Memory variables
        """
        # Update conversation length
        self._conversation_length = self._get_conversation_length()
        
        # Load metadata
        session_metadata = self.get_session_metadata()
        
        if self._should_use_summary():
            # Use summary + recent buffer
            if self.verbose:
                print(f"📝 Using summary mode (length: {self._conversation_length})")
            
            # Load summary memory
            summary_vars = self.summary_memory.load_memory_variables(inputs)
            conversation_summary = summary_vars.get("conversation_summary", "")
            
            # Load recent buffer
            buffer_vars = self.buffer_memory.load_memory_variables(inputs)
            recent_history = buffer_vars.get("recent_history", [])
            
            return {
                "recent_history": recent_history,
                "conversation_summary": conversation_summary,
                "session_metadata": session_metadata
            }
        else:
            # Use only buffer
            if self.verbose:
                print(f"📋 Using buffer mode (length: {self._conversation_length})")
            
            buffer_vars = self.buffer_memory.load_memory_variables(inputs)
            recent_history = buffer_vars.get("recent_history", [])
            
            return {
                "recent_history": recent_history,
                "conversation_summary": "",
                "session_metadata": session_metadata
            }
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """
        Save context to both buffer and summary memory.
        
        Args:
            inputs: Input dictionary containing user message
            outputs: Output dictionary containing agent response
        """
        # Convert to messages format
        user_message = inputs.get("message", "")
        ai_message = outputs.get("response", "")
        
        messages = [
            HumanMessage(content=user_message),
            AIMessage(content=ai_message)
        ]
        
        # Save to buffer memory
        self.buffer_memory.save_context(inputs, outputs)
        
        # Save to summary memory if needed
        if self._should_use_summary():
            self.summary_memory.save_context(inputs, outputs)
        
        # Update conversation length
        self._conversation_length += 1
        self._update_conversation_length(self._conversation_length)
        
        # Save to full history (optional)
        self._save_to_full_history(inputs, outputs)
        
        if self.verbose:
            print(f"💾 Saved context (length: {self._conversation_length})")
    
    def _save_to_full_history(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save to full conversation history in SQLite."""
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
        """Clear all memory for current session."""
        self.buffer_memory.clear()
        self.summary_memory.clear()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM conversations WHERE session_id = ?", (self.session_id,))
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (self.session_id,))
            conn.commit()
        
        self._conversation_length = 0
    
    # Metadata management methods (compatible with existing system)
    def set_session_metadata(self, metadata: Dict[str, Any]) -> None:
        """Set or update session metadata."""
        with sqlite3.connect(self.db_path) as conn:
            existing_metadata = self.get_session_metadata()
            merged_metadata = {**existing_metadata, **metadata}
            
            conn.execute("""
                INSERT OR REPLACE INTO sessions (session_id, metadata, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (self.session_id, json.dumps(merged_metadata)))
            conn.commit()
    
    def get_session_metadata(self) -> Dict[str, Any]:
        """Get session metadata."""
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
        """Update a specific key in session metadata."""
        metadata = self.get_session_metadata()
        metadata[key] = value
        self.set_session_metadata(metadata)
    
    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """Get a specific value from session metadata using dot notation."""
        metadata = self.get_session_metadata()
        
        # Handle dot notation for nested access
        keys = key.split('.')
        current = metadata
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    # Extended metadata methods (compatible with existing system)
    def set_welcome_status(self, welcome_done: bool) -> None:
        """Set whether the welcome message has been shown."""
        self.update_session_metadata("welcome_done", welcome_done)
    
    def get_welcome_status(self) -> bool:
        """Get whether the welcome message has been shown."""
        return self.get_metadata_value("welcome_done", False)
    
    def set_reasons(self, reasons: list) -> None:
        """Set the list of reasons for the conversation."""
        self.update_session_metadata("reasons", reasons)
    
    def get_reasons(self) -> list:
        """Get the list of reasons for the conversation."""
        return self.get_metadata_value("reasons", [])
    
    def add_reason(self, reason: str) -> None:
        """Add a reason to the list of reasons."""
        reasons = self.get_reasons()
        if reason not in reasons:
            reasons.append(reason)
            self.set_reasons(reasons)
    
    def remove_reason(self, reason: str) -> None:
        """Remove a reason from the list of reasons."""
        reasons = self.get_reasons()
        if reason in reasons:
            reasons.remove(reason)
            self.set_reasons(reasons)
    
    def set_reasons_confirmed(self, confirmed: bool) -> None:
        """Set whether the reasons have been confirmed."""
        self.update_session_metadata("reasons_confirmed", confirmed)
    
    def get_reasons_confirmed(self) -> bool:
        """Get whether the reasons have been confirmed."""
        return self.get_metadata_value("reasons_confirmed", False)
    
    def set_vars_info_given(self, given: bool) -> None:
        """Set whether variables info has been given."""
        self.update_session_metadata("vars_info_given", given)
    
    def get_vars_info_given(self) -> bool:
        """Get whether variables info has been given."""
        return self.get_metadata_value("vars_info_given", False)
    
    def set_vars(self, vars_data: dict) -> None:
        """Set variables data."""
        self.update_session_metadata("vars", vars_data)
    
    def get_vars(self) -> dict:
        """Get variables data."""
        return self.get_metadata_value("vars", {"monthly": None, "duration": None, "rate": None})
    
    def update_var(self, var_name: str, value: any) -> None:
        """Update a specific variable."""
        vars_data = self.get_vars()
        vars_data[var_name] = value
        self.set_vars(vars_data)
    
    def get_var(self, var_name: str) -> any:
        """Get a specific variable value."""
        vars_data = self.get_vars()
        return vars_data.get(var_name)
    
    def set_loan_variables(self, monthly: float = None, duration: int = None, rate: float = None) -> None:
        """Set loan-related variables."""
        vars_data = self.get_vars()
        if monthly is not None:
            vars_data["monthly"] = monthly
        if duration is not None:
            vars_data["duration"] = duration
        if rate is not None:
            vars_data["rate"] = rate
        self.set_vars(vars_data)
    
    def get_loan_variables(self) -> dict:
        """Get all loan-related variables."""
        return self.get_vars()
    
    def is_loan_info_complete(self) -> bool:
        """Check if all loan variables have been provided."""
        vars_data = self.get_vars()
        return all(vars_data.get(key) is not None for key in ["monthly", "duration", "rate"])
    
    def reset_loan_variables(self) -> None:
        """Reset all loan variables to None."""
        self.set_vars({"monthly": None, "duration": None, "rate": None})
        self.set_vars_info_given(False)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics for debugging."""
        return {
            "session_id": self.session_id,
            "conversation_length": self._conversation_length,
            "using_summary": self._should_use_summary(),
            "buffer_window": self.buffer_window,
            "summary_threshold": self.summary_threshold,
            "session_metadata": self.get_session_metadata()
        }


def create_hybrid_memory(
    session_id: str,
    buffer_window: int = 5,
    summary_threshold: int = 3,
    verbose: bool = False
) -> HybridConversationMemory:
    """
    Create a new hybrid conversation memory instance.
    
    Args:
        session_id: Unique session identifier
        buffer_window: Number of recent messages to keep in buffer
        summary_threshold: Number of messages before switching to summary mode
        verbose: Enable verbose logging
        
    Returns:
        HybridConversationMemory: Configured memory instance
    """
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
     
    # TODO esto esta guardando todo en db, no esta usando lo embebido de LangChain, hay que cambiarlo

    return HybridConversationMemory(
        session_id=session_id,
        db_path=db_path,
        buffer_window=buffer_window,
        summary_threshold=summary_threshold,
        verbose=verbose
    )


def get_hybrid_conversation_history(
    session_id: str,
    limit: int = 10,
    include_summary: bool = True
) -> Dict[str, Any]:
    """
    Get conversation history from hybrid memory.
    
    Args:
        session_id: Session identifier
        limit: Maximum number of recent messages to return
        include_summary: Whether to include conversation summary
        
    Returns:
        Dict[str, Any]: Conversation history with summary and recent messages
    """
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
    
    # Get recent messages
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT message, response, timestamp 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (session_id, limit))
        
        recent_messages = []
        for row in cursor.fetchall():
            recent_messages.append({
                "message": row[0],
                "response": row[1],
                "timestamp": row[2]
            })
        
        recent_messages = list(reversed(recent_messages))
    
    # Get summary if requested
    summary = ""
    if include_summary:
        # Create temporary memory to get summary
        temp_memory = create_hybrid_memory(session_id)
        summary_vars = temp_memory.summary_memory.load_memory_variables({})
        summary_obj = summary_vars.get("conversation_summary", "")
        
        # Convert summary to string if it's a LangChain message object
        if hasattr(summary_obj, 'content'):
            summary = str(summary_obj.content)
        elif hasattr(summary_obj, 'text'):
            summary = str(summary_obj.text)
        else:
            summary = str(summary_obj)
    
    return {
        "recent_messages": recent_messages,
        "conversation_summary": summary,
        "total_messages": len(recent_messages)
    } 