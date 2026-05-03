import boto3
import json
import time
from layer2_classifier import evaluate_conversation_risk
from logger import log_request

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def process_request(
    message: str,
    conversation_history: list,
    guardrail_id: str,
    guardrail_version: str = 'DRAFT'
) -> dict:

    start_total = time.time()
    result = {
        'message': message,
        'layer1_result': None,
        'layer2_result': None,
        'final_decision': None,
        'response': None,
        'total_latency_ms': None
    }

    # --- LAYER 1: Bedrock Guardrails ---
    print(f"\n[Layer 1] Evaluating: {message[:80]}...")
    try:
        layer1_response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 512
            })
        )
        layer1_body = json.loads(layer1_response['body'].read())
        stop_reason = layer1_body.get('stop_reason', '')

        if stop_reason == 'guardrail_intervened':
            result['layer1_result'] = 'BLOCKED'
            result['final_decision'] = 'BLOCKED_LAYER1'
            result['response'] = 'Request blocked by Layer 1 security policy.'
            print(f"[Layer 1] BLOCKED")
            log_request(message, 'BLOCKED', {}, 'BLOCKED_LAYER1')
            return result
        else:
            result['layer1_result'] = 'PASSED'
            print(f"[Layer 1] PASSED")

    except Exception as e:
        print(f"[Layer 1] Error: {e}")
        result['layer1_result'] = 'ERROR'

    # --- LAYER 2: Semantic Classifier ---
    print(f"[Layer 2] Running semantic analysis...")
    layer2_result = evaluate_conversation_risk(conversation_history, message)
    result['layer2_result'] = layer2_result
    print(f"[Layer 2] Risk: {layer2_result['risk_level']} | "
          f"Attack: {layer2_result['attack_type']} | "
          f"Confidence: {layer2_result['confidence']} | "
          f"Latency: {layer2_result['latency_ms']}ms")

    if layer2_result['risk_level'] == 'HIGH':
        result['final_decision'] = 'BLOCKED_LAYER2'
        result['response'] = 'Request blocked by Layer 2 semantic analysis.'
        print(f"[Layer 2] BLOCKED")
        log_request(message, result['layer1_result'], layer2_result, 'BLOCKED_LAYER2')
        return result

    # --- BOTH LAYERS PASSED: Generate response ---
    print(f"[Both layers passed] Generating response...")
    try:
        final_response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 512
            })
        )
        final_body = json.loads(final_response['body'].read())
        result['response'] = final_body['content'][0]['text']
        result['final_decision'] = 'ALLOWED'
        print(f"[Response generated]")

    except Exception as e:
        print(f"[Response error] {e}")
        result['response'] = 'Error generating response.'
        result['final_decision'] = 'ERROR'

    result['total_latency_ms'] = round((time.time() - start_total) * 1000, 2)
    log_request(message, result['layer1_result'], layer2_result, result['final_decision'])
    return result

if __name__ == '__main__':
    # Quick smoke test
    test_result = process_request(
        message="What is the capital of France?",
        conversation_history=[],
        guardrail_id="PLACEHOLDER"
    )
    print(f"\nDecision: {test_result['final_decision']}")
    print(f"Response: {test_result['response']}")
    print(f"Total latency: {test_result['total_latency_ms']}ms")
