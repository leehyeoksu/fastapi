import sys
import os

# Add the current directory to sys.path so we can import service
sys.path.append(os.getcwd())

from service import process_prompt_with_ai

def test_prompt():
    # Test Image Category
    print("\n=== Testing Image Category ===")
    img_prompt = "Describe a panda in a bamboo forest"
    img_response = process_prompt_with_ai(img_prompt, "Creative", "Image")
    print(f"Refined Image Prompt:\n{img_response.refined_prompt}\n")

    # Test Data Category
    # print("\n=== Testing Data Category ===")
    # data_prompt = "Analyze this sales data csv"
    # data_response = process_prompt_with_ai(data_prompt, "Professional", "Data")
    # print(f"Refined Data Prompt:\n{data_response.refined_prompt}\n")

if __name__ == "__main__":
    test_prompt()
