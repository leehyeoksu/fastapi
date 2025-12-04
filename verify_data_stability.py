import sys
import os
import json

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def verify_data_category():
    print("\n=== Testing Data Category for JSON Stability ===")
    data_prompt = "Analyze this sales data csv and give me python code"
    
    try:
        # Testing with "Auto" to ensure detection works too
        response = process_prompt_with_ai(data_prompt, "Professional", "Auto")
        print(f"Success! Detected Category: {response.analysis.category}")
        print(f"Refined Data Prompt Preview:\n{response.refined_prompt[:100]}...")
    except Exception as e:
        print(f"Caught Error: {e}")
        raise e

if __name__ == "__main__":
    verify_data_category()
