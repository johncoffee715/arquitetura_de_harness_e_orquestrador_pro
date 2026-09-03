# Mecânica do Fable-Judge Feature
- Role: Fable Judge (evaluator)
- Purpose: Evaluate generated text for factual accuracy, coherence, and adherence to instructions; provide structured feedback.
- Persona: A specialized evaluator that checks content against ground truth, identifies hallucinations, and provides clear, actionable feedback.
- Constraints:
  - Context window: 4096 tokens (max)
  - Output format: Valid JSON with verdict, reasoning, suggestions, and metrics
  - Never hallucinate facts not present in the source
  - Provide clear, actionable feedback with evidence
  - Use deterministic tool-calling (Pydantic + GBNF) to avoid randomness
- Input format:
  {
    "text": "The generated text...",
    "ground_truth": "The ground truth source...",
    "instructions": "Instructions for evaluation..."
  }
- Output format:
  {
    "verdict": "PASS" | "FAIL" | "PARTIAL",
    "reasoning": "structured explanation with evidence",
    "suggestions": [
      "Improvement 1 suggestion",
      "Improvement 2 suggestion"
    ],
    "metrics": {
      "accuracy": 0.95,
      "coherence": 0.98,
      "staleness": 0.02
    }
  }
- Validation:
  - System prompt must be immutable and immutable in format.
  - Use Pydantic model_validate_json for strict schema enforcement.
  - Use GBNF to enforce token boundaries and prevent out-of-schema generation.
  - Deterministic tool-calling prevents randomness.
  - Max tokens: 1024
  - Context size: 4096 tokens
- Anti-loop prevention:
  - Retry limit: 3 attempts with increasing max tokens.
  - Fallback default output if all attempts fail.
- Anti-hallucination:
  - Use GBNF to restrict generation to known vocabulary.
  - Use Pydantic model_validate_json to reject out-of-schema responses.
  - Stop tokens to prevent continuation beyond valid context.
- Anti-stall:
  - If task takes >300 seconds, abort and report progress.
  - Use health-watchdog to detect backend stall.
- Idempotency:
  - Feature should work independently without side effects.
  - No modification of persistent state except returning evaluation result.
- Performance:
  - Batch size: 256
  - UBATCH: 512
  - KV cache type: q4_0/q4_0 (quantized)
  - Attention: Flash Attention on GPU, otherwise standard attention on CPU.
- Error handling:
  - If input is malformed or missing required fields, return structured error.
  - If evaluation fails due to context overflow, return PARTIAL verdict with appropriate metrics.
  - If text is too long (>4096 tokens), truncate and evaluate with warning.
- Logging:
  - Log evaluation steps, decisions, and metrics for auditability.
  - Record decisions in decision-log with evidence.
  - Record benchmark metrics for reproducibility.
