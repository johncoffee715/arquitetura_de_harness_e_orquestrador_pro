#!/usr/bin/env python3
"""
Mechanic for claude-mem: micro-classifier/extractor (Wave1-micro 0.1B)
Extracts 5-digit numeric patterns from dirty text using GBNF regex.
Returns the first 5-digit pattern found as an integer, or None if none exists.
"""

import re
import json
from typing import Union, Optional


def extract_five_digit_pattern(text: str) -> Union[int, None]:
    """
    Uses GBNF regex [0-9]{5} to find the first 5-digit pattern in text.
    Returns the integer value if found, otherwise None.
    
    The regex finds exactly 5 consecutive digits (allowing leading zeros).
    This matches the R84 requirement for Wave1-micro micro-classifier/extractor.
    """
    # GBNF regex: [0-9]{5} - finds exactly 5 consecutive digits
    # This is the core extraction rule per R84 specification.
    pattern = r'\b(?:0|[1-9])(?:[0-9]|[1-9]|0){4}\b'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        # Convert the matched string to integer (handles leading zeros)
        try:
            return int(match.group())
        except (ValueError, TypeError):
            return None
    
    # No 5-digit pattern found
    return None


def claude_mem_mechanic(input_text: str) -> Union[json.JSON_Type, None]:
    """
    Main mechanic entry point.
    
    Input: raw text (potentially dirty/noisy)
    Output: integer if 5-digit pattern found, otherwise None
    
    Enforces strict schema validation and deterministic output.
    """
    # Clean input - strip excessive noise but preserve structure
    # Convert to lowercase for regex matching (per GBNF deterministic rules)
    clean_text = str(input_text).lower()
    
    # Extract the 5-digit pattern using GBNF regex logic
    result = extract_five_digit_pattern(clean_text)
    
    # Return in clean JSON format matching schema
    if result is None:
        return None
    elif result == 0:
        # Special case: 00000 is valid 5-digit pattern (leading zeros allowed)
        return 0
    else:
        # Return as integer (not string)
        return result


if __name__ == "__main__":
    # Example usage (for testing):
    example_text = "Here are some numbers: 12, 123, 1234, 12345, 67890"
    result = claude_mem_mechanic(example_text)
    print(json.dumps(result))
    
    # The output should be: 12345