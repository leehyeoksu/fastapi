import sys
import os
import json

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def verify_ultra_quality():
    print("\n=== Testing Ultra-High Quality Image Prompt ===")
    # Using a simpler prompt to see if the AI "hallucinates" the missing details as instructed
    img_prompt = "Polar bear skiing"
    
    try:
        response = process_prompt_with_ai(img_prompt, "Creative", "Image")
        print(f"Refined Image Prompt:\n{response.refined_prompt}\n")
        
        # Check for key cinematic terms
        keywords = ["Camera", "Lighting", "Physics", "8k", "Detail"]
        found = [k for k in keywords if k.lower() in response.refined_prompt.lower()]
        print(f"Found Cinematic Keywords: {found}")
        
    except Exception as e:
        print(f"Caught Error: {e}")

    print("\n=== Testing Ultra-High Quality Data Prompt ===")
    data_prompt = "Analyze this customer churn csv"
    try:
        response = process_prompt_with_ai(data_prompt, "Professional", "Data")
        print(f"Refined Data Prompt Preview:\n{response.refined_prompt[:200]}...")
    except Exception as e:
        print(f"Caught Error: {e}")

if __name__ == "__main__":
    verify_ultra_quality()
