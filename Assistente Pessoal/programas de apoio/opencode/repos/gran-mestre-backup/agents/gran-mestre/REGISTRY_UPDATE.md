# Registry Update — Héstia e Atena

## Agent Factory Pattern (OmO)

Baseado em `packages/omo-opencode/src/agents/`, cada agent segue o padrão:

```typescript
// createHestiaAgent.ts
export function createHestiaAgent(config: HestiaConfig): Agent {
  return {
    name: 'hestia',
    description: 'Validation agent for Gran-Mestre pipeline',
    capabilities: ['validate', 'check-coverage', 'check-contracts'],
    permissions: ['read'],
    skills: ['fable-method', 'fable-judge'],
    mcp: ['context7'],
    config: {
      validationLevel: config.validationLevel || 'strict',
      reportFormat: config.reportFormat || 'structured',
    },
  };
}
```

```typescript
// createAthenaAgent.ts
export function createAthenaAgent(config: AthenaConfig): Agent {
  return {
    name: 'athena',
    description: 'Macro-review agent for Gran-Mestre pipeline',
    capabilities: ['review', 'check-coherence', 'check-coupling'],
    permissions: ['read'],
    skills: ['fable-judge', 'systematic-debugging'],
    mcp: ['context7', 'codegraph'],
    config: {
      reviewDepth: config.reviewDepth || 'holistic',
      architectureCheck: config.architectureCheck || true,
    },
  };
}
```

## Registry Entry

```json
{
  "agents": {
    "hestia": {
      "name": "hestia",
      "description": "Validation agent for Gran-Mestre pipeline",
      "version": "1.0.0",
      "author": "Gran-Mestre",
      "capabilities": [
        "validate-spec",
        "validate-coverage",
        "validate-contracts",
        "validate-verifiability",
        "final-validation"
      ],
      "permissions": ["read"],
      "skills": [
        "fable-method",
        "fable-judge"
      ],
      "mcp": [
        "context7"
      ],
      "config": {
        "validationLevel": "strict",
        "reportFormat": "structured"
      },
      "triggers": [
        "/hestia validate",
        "/hestia check-coverage",
        "/hestia check-contracts",
        "/hestia final-check"
      ]
    },
    "athena": {
      "name": "athena",
      "description": "Macro-review agent for Gran-Mestre pipeline",
      "version": "1.0.0",
      "author": "Gran-Mestre",
      "capabilities": [
        "holistic-review",
        "coherence-check",
        "coupling-analysis",
        "architecture-alignment",
        "quality-check"
      ],
      "permissions": ["read"],
      "skills": [
        "fable-judge",
        "systematic-debugging"
      ],
      "mcp": [
        "context7",
        "codegraph"
      ],
      "config": {
        "reviewDepth": "holistic",
        "architectureCheck": true
      },
      "triggers": [
        "/athena review",
        "/athena check-coherence",
        "/athena check-coupling",
        "/athena check-architecture"
      ]
    }
  }
}
```

## Installation Instructions

### For Oh-My-Openagents

1. Copy agent definitions to `packages/omo-opencode/src/agents/`
2. Add factory functions
3. Register in agent registry
4. Update configuration schema

### For Claude Code

1. Copy SKILL.md files to `~/.claude/skills/`
2. Add to CLAUDE.md:
   ```markdown
   - Before final delivery, run /hestia final-check
   - After macro changes, run /athena review
   ```

### For OpenCode

1. Copy SKILL.md files to `.opencode/skills/`
2. Add to opencode.json:
   ```json
   {
     "skills": {
       "hestia": { "path": ".opencode/skills/hestia/SKILL.md" },
       "athena": { "path": ".opencode/skills/athena/SKILL.md" }
     }
   }
   ```

## Security Considerations

### Héstia
- **Read-only**: Nunca modifica código
- **Validation-only**: Apenas valida e reporta
- **No network**: Não faz requests externos

### Atena
- **Read-only**: Nunca modifica código
- **Review-only**: Apenas revisa e reporta
- **No network**: Não faz requests externos

## Testing

### Unit Tests

```typescript
// hestia.test.ts
describe('Héstia Agent', () => {
  it('should validate spec against request', () => {
    const hestia = createHestiaAgent({});
    const result = hestia.validateSpec(spec, request);
    expect(result.status).toBe('approved');
  });

  it('should check coverage', () => {
    const hestia = createHestiaAgent({});
    const result = hestia.checkCoverage(spec, requirements);
    expect(result.coverage).toBe(100);
  });
});
```

```typescript
// athena.test.ts
describe('Atena Agent', () => {
  it('should review holistic diff', () => {
    const athena = createAthenaAgent({});
    const result = athena.reviewDiff(diff);
    expect(result.status).toBe('approved');
  });

  it('should check coherence', () => {
    const athena = createAthenaAgent({});
    const result = athena.checkCoherence(tasks);
    expect(result.coherent).toBe(true);
  });
});
```

## Integration with Gran-Mestre Pipeline

### Phase 2 (Contrato)
```
Spec Writer → Héstia (validate spec) → Fable Judge (audit)
```

### Phase 3 (Plano)
```
Plan Writer → Fable Loop → Héstia (validate coverage)
```

### Phase 5 (Revisão Macro)
```
Atena (holistic review) → Fable Judge (audit)
```

### Phase 6 (Entrega)
```
Verification → Héstia (final check) → Fable Judge (verdict)
```