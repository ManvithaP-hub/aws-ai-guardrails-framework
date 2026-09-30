# AWS AI Guardrails Framework

A dual-layer LLM security framework on AWS Bedrock that combines
Bedrock Guardrails (Layer 1) with semantic intent classification (Layer 2).

## Results (390 author-written inputs)

| System | Detection | Multi-turn | FP rate | F1 |
|---|---|---|---|---|
| Keyword rules (author-built) | 43/190 (22.6%) | 5/18 | 1/200 (0.5%) | 0.368 |
| Bedrock Guardrails, MEDIUM | 88/190 (46.3%) | 11/18 | 0/200 (0.0%) | 0.633 |
| Bedrock Guardrails, HIGH | 115/190 (60.5%) | 14/18 | 0/200 (0.0%) | 0.754 |
| **Layer 2 classifier** | **184/190 (96.8%)** | **18/18** | **0/200 (0.0%)** | **0.984** |
| **Dual (Bedrock HIGH OR Layer 2)** | **185/190 (97.4%)** | **18/18** | **0/200 (0.0%)** | **0.987** |

Bedrock Guardrails was measured live through the ApplyGuardrail API with the
prompt-attack filter, evaluated per user turn (September 2026). The classifier
caught 70 attacks the guardrail missed and missed one the guardrail caught
(exact McNemar p < 0.001). Bedrock is weakest on code injection (1/9),
reasoning manipulation (1/9) and gradual escalation (0/7), and strongest on
persona hijacking (21/22) and indirect injection (15/17).

An earlier version of this evaluation substituted author-written keyword rules
for Bedrock Guardrails, because API quota was unavailable, and understated the
service by 38 percentage points. Those rows are kept above for comparison and
labelled as author-built.

Not yet evaluated: whether conversational history is what gives the classifier
its advantage, and robustness to adaptive attacks.

## Architecture
- Layer 1: AWS Bedrock Guardrails (input + output filtering)
- Layer 2: Semantic classifier (conversational context analysis)
- Audit logging: DynamoDB

## Quick Start
```bash
pip install anthropic boto3
export ANTHROPIC_API_KEY="your-key"
python3 src/layer2_classifier.py
```

## Reproducing results

    python3 eval/bedrock_eval_standalone.py     # live Bedrock Guardrails, 390 inputs

## License
Apache 2.0
