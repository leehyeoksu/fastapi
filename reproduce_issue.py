import sys
import os

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def reproduce():
    # Test Image Category with "Auto"
    print("\n=== Testing Image Category with Auto ===")
    img_prompt = "Describe a panda in a bamboo forest"
    # Passing "Auto" instead of "Image"
    img_response = process_prompt_with_ai(img_prompt, "Creative", "Auto")
    print(f"Refined Image Prompt:\n{img_response.refined_prompt}\n")
    print(f"Detected Category: {img_response.analysis.category}")

if __name__ == "__main__":
    reproduce()
