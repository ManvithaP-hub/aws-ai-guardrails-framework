# AWS AI Guardrails Framework

A dual-layer LLM security framework on AWS Bedrock that combines 
Bedrock Guardrails (Layer 1) with semantic intent classification (Layer 2).

## Test Results
- Single-turn attack detection: 100% (10/10)
- Multi-turn attack detection: 100% (5/5)  
- False positive rate: 7% (1/15)
- Average Layer 2 latency: 1,501ms

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
## Baseline Comparison

| System | Detection | Multi-turn | FP rate | F1 |
|---|---|---|---|---|
| Layer 1 (keyword) | 22.6% | 5/18 (27.8%) | 0.5% | 0.368 |
| NeMo-style | 21.6% | 8/18 (44.4%) | 0.5% | 0.353 |
| Perplexity-proxy | 10.0% | 3/18 (16.7%) | 0.5% | 0.181 |
| **Layer 2 (ours)** | **96.8%** | **18/18 (100%)** | **0.0%** | **0.984** |
| Dual (L1+L2) | 96.8% | 18/18 (100%) | 0.5% | 0.981 |

Evaluation: 390 prompts (190 attacks across 15 categories, 200 legitimate prompts).
Full results: `tests/cacm_results.json`

## License
Apache 2.0

## Draft is published here for reference
https://dev.to/manvitha_potluri_edbd8b9b/why-single-layer-llm-guardrails-fail-a-dual-detection-pattern-on-aws-bedrock-4okj
