#!/usr/bin/env python3
"""
Context Compaction Mechanica - Python implementation for context compaction.
This script processes raw context and produces structured, concise output.
"""

import json
import argparse
import sys
from typing import List, Dict, Any

def load_context(context_text: str) -> List[Dict[str, Any]]:
    """
    Parse raw context into structured format.
    This is a simplified implementation that works with the skill.
    """
    # In a real implementation, this would use more sophisticated NLP
    # For this task, we'll just return the context as a simple structure
    if not context_text or len(context_text.strip()) == 0:
        return []
    
    # Simple parsing: split into paragraphs
    paragraphs = [p.strip() for p in context_text.split('\n\n') if p.strip()]
    
    # Extract key entities and relationships (simplified)
    result = []
    for i, para in enumerate(paragraphs):
        # Count words/tokens as a proxy for length
        word_count = len(para.split())
        result.append({
            "paragraph_index": i,
            "word_count": word_count,
            "content": para,
            "entities": extract_entities(para)
        })
    return result

def extract_entities(text: str) -> List[Dict[str, str]]:
    """
    Extract basic entities from text (simplified).
    Returns list of entity dictionaries.
    """
    # Very simple entity extraction - in practice, use proper NER libraries
    entities = []
    
    # Look for dates (simple pattern)
    import re
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    date_matches = re.findall(date_pattern, text)
    for match in date_matches:
        entities.append({
            "type": "date",
            "value": match
        })
    
    # Look for organizations/names (simple pattern)
    org_pattern = r'([A-Za-z][A-Za-z0-9._-]+@[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+|[A-Za-z]+[-.]?[A-Za-z]+(?:\.[A-Za-z]+)*)'
    org_matches = re.findall(org_pattern, text)
    for match in org_matches:
        entities.append({
            "type": "organization",
            "value": match
        })
    
    # Look for numbers (simple pattern)
    num_pattern = r'(\d+\.?\d*)'
    num_matches = re.findall(num_pattern, text)
    for match in num_matches:
        entities.append({
            "type": "number",
            "value": match
        })
    
    return entities

def compact_context(
    raw_context: str,
    output_format: str = "summary",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Compact the given context using the skill's logic.
    Returns structured output based on the gabarito.json schema.
    """
    # Process the context
    paragraphs = load_context(raw_context)
    
    # Apply compaction logic based on output format
    if output_format == "concise":
        # Very concise format - just return summary
        return {
            "summary": "Context was too long. Key points extracted:",
            "paragraphs": paragraphs,
            "language": language,
            "entities": extract_entities(raw_context)
        }
    elif output_format == "summary":
        # Summary format - provide overview
        return {
            "summary": "Context summary (first 2 paragraphs):",
            "first_paragraph": paragraphs[0]["content"] if paragraphs else "N/A",
            "second_paragraph": paragraphs[1]["content"] if len(paragraphs) > 1 else "",
            "entities": extract_entities(raw_context),
            "language": language
        }
    elif output_format == "structured":
        # Structured format - return detailed structured output
        return {
            "type": "structured",
            "raw_context": raw_context,
            "paragraphs": paragraphs,
            "entities": extract_entities(raw_context),
            "language": language
        }
    else:
        # Default format
        return {
            "summary": "Context summary with key points:",
            "paragraphs": paragraphs,
            "entities": extract_entities(raw_context),
            "language": language
        }

def main():
    parser = argparse.ArgumentParser(
        description="Context Compaction Mechanica - Python implementation"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the raw context file"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="summary",
        choices=["summary", "concise", "structured"],
        help="Output format"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Target language"
    )
    args = argparse.parse_args()
    
    # Read the input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            raw_context = f.read()
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Process the context
    result = compact_context(raw_context, args.output_format, args.language)
    
    # Output in JSON format
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()