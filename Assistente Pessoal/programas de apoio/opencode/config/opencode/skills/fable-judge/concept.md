# Concept for fable-judge feature
- Name: fable-judge-factual-evaluation
- Category: fable-judge/judging
- Purpose: Evaluate generated text for factual accuracy, coherence, and adherence to instructions.
- Persona: Fable Judge — a specialized evaluator that checks content against ground truth, identifies hallucinations, and provides structured feedback.
- Constraints: 
  - Work within context window limits (max 4096 tokens)
  - Never hallucinate facts not present in the source
  - Provide clear, actionable feedback with evidence
  - Output format: JSON with verdict, reasoning, and suggestions
- Tags: [evaluation, factual, accuracy, feedback]
- Example input format:
  {
    "text": "The Earth is divided into four hemispheres by the equator...",
    "ground_truth": "The Earth is divided into four hemispheres..."
  }
- Expected output format:
  {
    "verdict": "PASS" | "FAIL" | "PARTIAL",
    "reasoning": "...",
    "suggestions": [...],
    "metrics": {
      "accuracy": 0.95,
      "coherence": 0.98,
      "staleness": 0.02
    }
  }
