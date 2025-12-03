import service
import sys

print("Testing service.py...")

try:
    # 1. API Key 로드 확인
    print(f"Loaded API Key: {service.api_key[:10]}..." if service.api_key else "API Key is None")

    # 2. 서비스 함수 호출 테스트
    prompt = "python code for hello world"
    style = "Professional"
    print(f"\nSending prompt: '{prompt}' with style: '{style}'")
    
    result = service.process_prompt_with_ai(prompt, style)
    
    print("\n[Success] Result received:")
    print(f"Refined: {result.refined_prompt}")
    print(f"Category: {result.analysis.category}")

except Exception as e:
    print(f"\n[Error] {e}")
    import traceback
    traceback.print_exc()
