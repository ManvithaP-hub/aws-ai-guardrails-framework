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

## License
Apache 2.0
