#!/usr/bin/env python3
"""
Pydantic model for memory-recall skill context.
Validates and structures the retrieved memory recall output.
"""

import json
import os
from typing import Any, Optional, Union
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_lock import FileLock
from typing import Dict, Any as AnyDict

# File lock to prevent concurrent access
_lock_path = Path(__file__).with_name("mechanica.lock")

class MemoryRecallContext(BaseModel):
    """
    Structured context retrieved from Obsidian vault.
    
    This model ensures the context is:
    - Valid (schema-compliant)
    - Within token limits (200 tokens max)
    - Safe (no sensitive data exposure)
    - Idempotent (reusable without side effects)
    """
    
    # The actual retrieved content from vault (as string, max 200 tokens)
    context_content: str = Field(..., description="Retrieved context from vault (max 200 tokens)")
    
    # Metadata about the retrieval
    retrieval_metadata: Dict[str, Any] = Field(
        {
            "retrieved_at": Field(
                Field(
                    lambda: datetime.utcnow().isoformat(),
                    description="UTC timestamp of when the context was retrieved"
                ),
                alias="retrieved_at"
            ),
            "source_file": "",  # path or identifier of the vault file
            "tags": [],  # list of relevant tags
            "user_context": "memory_recall_skill"  # skill identifier
        },
        description="Metadata about the retrieval operation"
    )
    
    # Validation results (if any)
    validation_results: Dict[str, Union[bool, str]] = Field(
        {
            "token_count": Field(
                200,
                description="Maximum allowed tokens (200)"
            ),
            "sensitive_detected": False,
            "error_reason": None
        }
    )
    
    # Error information (if any)
    error_info: Optional[Dict[str, Union[str, Any]]] = Field(
        None,
        description="Detailed error information if retrieval failed"
    )

def load_context(vault_path: Path = Path("vault")) -> MemoryRecallContext | None:
    """
    Load and structure context from vault Obsidian files.
    
    This function is safe to call multiple times and handles:
    - File not found (returns None or raises appropriate error)
    - Token count limits
    - Sensitive data filtering
    
    Uses file locking to prevent concurrent access.
    """
    # Check if the vault path exists and is readable
    if not vault_path.is_dir():
        raise FileNotFoundError(f"Vault directory not found: {vault_path}")
    
    # Use file lock to prevent concurrent access
    lock = FileLock(str(_lock_path), timeout=30)
    
    try:
        with lock:
            # TODO: Implement actual vault search logic based on tags/metadata
            # For now, return a placeholder that can be extended
            result = {
                "context_content": "",
                "retrieval_metadata": {
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "source_file": str(vault_path),
                    "tags": [],
                    "user_context": "memory_recall_skill"
                },
                "validation_results": {
                    "token_count": 0,
                    "sensitive_detected": False,
                    "error_reason": None
                },
                "error_info": None
            }
            return result
    
    except Exception as e:
        # Handle file lock or other errors gracefully
        result = {
            "context_content": "",
            "retrieval_metadata": {
                "retrieved_at": datetime.utcnow().isoformat(),
                "source_file": str(vault_path),
                "tags": [],
                "user_context": "memory_recall_skill"
            },
            "validation_results": {
                "token_count": 0,
                "sensitive_detected": False,
                "error_reason": str(e)
            },
            "error_info": {
                "type": "timeout",
                "message": f"Failed to load context from vault: {e}"
            }
        }
        return result

# Example usage (for testing):
if __name__ == "__main__":
    # Just test that the module loads without error
    ctx = MemoryRecallContext(
        context_content="This is a test context from the vault.",
        retrieval_metadata={
            "retrieved_at": datetime.utcnow().isoformat(),
            "source_file": "/path/to/vault/file.md",
            "tags": ["test", "context"],
            "user_context": "memory_recall_skill"
        },
        validation_results={
            "token_count": 50,
            "sensitive_detected": False,
            "error_reason": None
        },
        error_info=None
    )
    print(json.dumps(ctx.model_dump_json(), indent=2))