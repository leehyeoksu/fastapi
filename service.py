import json
import openai
from schemas import RefineResponse, AnalysisResult

# config.json에서 API KEY 로드
def load_api_keys():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return {
                "OPENAI_API_KEY": config.get("OPENAI_API_KEY"),
                "GROK_API_KEY": config.get("GROK_API_KEY")
            }
    except FileNotFoundError:
        return {}

def process_prompt_with_ai(prompt: str, style: str, manual_category: str = "Auto", model: str = "gpt-3.5-turbo") -> RefineResponse:
    # 매 요청마다 API Key 새로 로드 (config.json 수정 시 즉시 반영)
    api_keys = load_api_keys()
    
    client = None
    current_api_key = None
    
    if "grok" in model.lower():
        current_api_key = api_keys.get("GROK_API_KEY")
        client = openai.OpenAI(
            api_key=current_api_key,
            base_url="https://api.x.ai/v1"
        )
    else:
        current_api_key = api_keys.get("OPENAI_API_KEY")
        client = openai.OpenAI(
            api_key=current_api_key
        )

    # API Key 체크
    if not current_api_key or current_api_key.startswith("여기에") or current_api_key.startswith("your-"):
        print(f"DEBUG: API Key check failed for model {model}")
        return RefineResponse(
            original_prompt=prompt,
            refined_prompt=f"[{style} Style] {prompt} (Please set your API Key for {model} to get real AI refinement.)",
            analysis=AnalysisResult(
                category=manual_category if manual_category != "Auto" else "General",
                missing_context=True,
                missing_format=True,
                suggestions=[f"Please enter your API Key for {model} in config.json."]
            ),
            tips=["Check the config.json file."]
        )

    # 시스템 프롬프트 설계 (프롬프트 엔지니어링 강화)
    category_instruction = ""
    if manual_category and manual_category != "Auto":
        category_instruction = f"The user has explicitly specified the category as: '{manual_category}'. Focus on this domain."
    else:
        category_instruction = "Analyze the user's intent and Classify the category into one of: [Coding, Math, Writing, Background Knowledge, Image Generation, Data Analysis, General]."

    system_prompt = f"""
    You are an expert AI Prompt Engineer. Your goal is to rewrite the user's raw prompt into a highly optimized, professional prompt that yields the best results from LLMs (like ChatGPT).

    [Instructions]
    1. **Category**: {category_instruction}
    2. **Refine** the prompt by applying the following principles:
       - **Clarity**: Remove ambiguity.
       - **Context**: Add necessary background information (inferred or generic placeholders).
       - **Constraints**: Add specific constraints (length, format, exclusions).
       - **Output Format**: Explicitly define how the output should look (Markdown, JSON, List, etc.).
    3. **Tone**: Apply the requested style: "{style}".
    4. **Consistency**: Ensure the output is deterministic and robust.
    5. **Language**: **ALL Output (Refined Prompt, Analysis, Tips) MUST be in ENGLISH.** Even if the user input is in Korean, translate and refine it into high-quality English.

    [Output Format - JSON Only]
    The output must be a valid JSON object with the following structure:
    {{
        "refined_prompt": "The fully optimized, ready-to-use prompt text (in English).",
        "analysis": {{
            "category": "The classified or selected category",
            "missing_context": true/false,
            "missing_format": true/false,
            "suggestions": ["Specific advice 1 (English)", "Specific advice 2 (English)"]
        }},
        "tips": ["General tip 1 (English)", "General tip 2 (English)"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model=model, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # 랜덤성 최소화 (Deterministic)
            top_p=0.9,
            seed=1234 # 결과 일관성 보장
        )
        
        content = response.choices[0].message.content
        result_json = json.loads(content)
        
        return RefineResponse(
            original_prompt=prompt,
            refined_prompt=result_json["refined_prompt"],
            analysis=AnalysisResult(**result_json["analysis"]),
            tips=result_json["tips"]
        )
        
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        # 에러 발생 시 기본 응답
        return RefineResponse(
            original_prompt=prompt,
            refined_prompt=f"Error: {str(e)}",
            analysis=AnalysisResult(
                category="Error",
                missing_context=False, 
                missing_format=False, 
                suggestions=[]
            ),
            tips=["API 호출 중 오류가 발생했습니다."]
        )
