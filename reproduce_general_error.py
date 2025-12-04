import sys
import os
import json

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def reproduce_general_error():
    print("\n=== Testing General Prompt for JSON Error ===")
    prompt = "Hello"
    
    try:
        response = process_prompt_with_ai(prompt, "Friendly", "Auto")
        print(f"Success! Refined Prompt:\n{response.refined_prompt[:100]}...")
    except Exception as e:
        print(f"Caught Error: {e}")

if __name__ == "__main__":
    reproduce_general_error()
