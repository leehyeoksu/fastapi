import json
import openai
from schemas import RefineResponse, AnalysisResult

# config.json에서 API KEY 로드
# config.json에서 API KEY 로드
def load_api_keys():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return {
                "OPENAI_API_KEY": config.get("OPENAI_API_KEY")
            }
    except FileNotFoundError:
        return {}

def process_prompt_with_ai(prompt: str, style: str, manual_category: str = "Auto") -> RefineResponse:
    # 매 요청마다 API Key 새로 로드 (config.json 수정 시 즉시 반영)
    api_keys = load_api_keys()
    
    current_api_key = api_keys.get("OPENAI_API_KEY")
    client = openai.OpenAI(
        api_key=current_api_key
    )
    
    # 사용할 모델 강제 지정
    model = "gpt-4o"

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
        if manual_category == "Image":
            category_instruction += " IMPORTANT: You are a CINEMATIC VISUAL DIRECTOR. The 'refined_prompt' MUST be a dense, ultra-detailed paragraph (or structured list of keywords) suitable for high-end video generation (Sora/Runway). You MUST invent specific details if missing: 1. **Camera Work** (e.g., 'Low-angle tracking shot', 'Drone flyover', 'Rack focus'), 2. **Lighting/Atmosphere** (e.g., 'Volumetric fog', 'Bioluminescent glow', 'HDR'), 3. **Physics/Movement** (e.g., 'Fur reacting to wind', 'Water splashing with high viscosity'), 4. **Micro-Details** (e.g., 'Dust particles', 'Scratches on metal'), 5. **Tech Specs** (e.g., '8k', '60fps', 'Unreal Engine 5 render'). Output raw prompt string only."
        elif manual_category == "Data":
            category_instruction += " IMPORTANT: You are a CHIEF DATA SCIENTIST. You MUST provide a SOPHISTICATED Python script. You MUST include: 1. **Hypothesis Generation** (What are we looking for?), 2. **Advanced Preprocessing** (Outlier detection, Imputation), 3. **Deep EDA** (Correlation matrices, Pairplots, Geospatial if applicable), 4. **Statistical Testing** (ANOVA, T-tests, Chi-square where relevant), 5. **Predictive Modeling** (Scikit-Learn snippets for Regression/Classification), 6. **Business Insights** (Actionable recommendations). Ensure code is professional and runnable."
    else:
        category_instruction = "Analyze the user's intent and Classify the category into one of: [Coding, Math, Writing, Background Knowledge, Image Generation, Data Analysis, General]."

    system_prompt = f"""
    ### Role
    You are a **World-Class Prompt Engineer & Creative Director**. Your goal is to transform simple requests into **Masterpiece-Level** prompts. You do not just "refine"; you **elevate**, **expand**, and **perfect**.

    ### Context
    The user wants a prompt that produces professional-grade results (e.g., a National Geographic documentary video, a Fortune 500 data analysis report). You must fill in ALL missing details (lighting, camera angles, statistical methods) to achieve this high standard.

    ### Task
    1. **Analyze** the user's intent deeply.
    2. **Classify** the category: {category_instruction}
    3. **Refine** the prompt. **HALLUCINATE DETAILS** if necessary to make it high-quality. (e.g., if user says "car", you add "vintage 1960s Mustang, gleaming chrome, sunset reflection").
    4. **Translate** to English if needed.

    ### Constraints & Guidelines
    - **Specificity**: Be extremely specific. Never use generic terms.
    - **Structure**: Use markdown headers.
    - **Variables**: Use `{{VARIABLE_NAME}}` for placeholders.
    - **Tone**: Apply the requested style: "{style}".
    - **Determinism**: Robust logic.
    - **Language**: **ALL Output MUST be in ENGLISH.**
    - **IMAGE GENERATION RULE**: If intent is Image/Video, classify as 'Image'. The 'refined_prompt' field MUST be the RAW PROMPT STRING. Include Camera, Lighting, Physics, Micro-Details. DO NOT output plain text outside JSON.

    ### Output Format (JSON Only)
    You must return a valid JSON object. Do not include any text outside the JSON block.
    {{
        "refined_prompt": "The fully optimized, structured prompt text (in English). Use \\n for line breaks.",
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
            seed=1234, # 결과 일관성 보장
            response_format={"type": "json_object"} # JSON 출력 강제
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
        if 'content' in locals():
            print(f"Failed Content: {content}")
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
