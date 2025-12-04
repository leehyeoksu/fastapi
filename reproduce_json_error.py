import sys
import os
import json

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def reproduce_json_error():
    print("\n=== Testing Image Category for JSON Error ===")
    img_prompt = "Describe a panda in a bamboo forest"
    
    # This should trigger the error if the output is not JSON
    try:
        img_response = process_prompt_with_ai(img_prompt, "Creative", "Auto")
        print(f"Success! Refined Image Prompt:\n{img_response.refined_prompt}\n")
    except Exception as e:
        print(f"Caught Expected Error: {e}")

if __name__ == "__main__":
    reproduce_json_error()
