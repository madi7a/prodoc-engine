import os
import json
import re
import ast
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

OUTPUT_DIR = "output"
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def repair_json(json_str):
    if not json_str: return None
    if "```" in json_str:
        if "```json" in json_str: json_str = json_str.split("```json")[-1].split("```")[0].strip()
        else: json_str = json_str.split("```")[-1].split("```")[0].strip()
    match = re.search(r"\{.*\}", json_str, re.DOTALL)
    if match: json_str = match.group(0)
    try: return json.loads(json_str)
    except: pass
    try: return ast.literal_eval(json_str)
    except: pass
    return None

def generate_report_content(user_input: str):
    print(f"--> Processing Input: {user_input[:50]}...")
    
    client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

    # UPDATED PROMPT: Added 'author' field to the JSON schema
    system_instruction = """
    You are a professional business document engine.
    Analyze the user's input and output VALID JSON.

    LOGIC ROUTING:
    1. IF INPUT IS A SHORT TOPIC (e.g., "Marketing Plan for Shoes"):
       - Role: Creative Consultant.
       - Action: GENERATE a full, realistic report from scratch. Invent professional data.
       
    2. IF INPUT IS ROUGH NOTES/CONTENT (e.g., "Q3 results..."):
       - Role: Editor.
       - Action: ORGANIZE the user's text.
       - CRITICAL RULE: If the user provides lists, comparisons, or metrics, YOU MUST FORMAT THEM AS A TABLE within the 'table_data' field. Do not just write a paragraph.

    STRICT JSON OUTPUT SCHEMA:
    {
        "meta": { 
            "title": "Create a professional title based on input", 
            "client": "Name of client or 'Internal Report'",
            "author": "Extract the author name from input. If none found, use 'AI Consultant'",
            "date": "2026-01-06" 
        },
        "sections": [
            { 
                "heading": "Professional Section Heading", 
                "content": "The main text...", 
                "table_data": null 
            },
            { 
                "heading": "Data/Analysis Section", 
                "content": "Intro to the data...", 
                "table_data": { 
                    "columns": ["Col1", "Col2"], 
                    "rows": [["Val1", "Val2"], ["Val3", "Val4"]] 
                } 
            }
        ]
    }
    RULES: Output ONLY valid JSON. Close all braces. No markdown formatting outside the JSON.
    """

    try:
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_input}
            ],
            max_tokens=2500, 
            temperature=0.1  
        )
        
        raw_content = response.choices[0].message.content
        data = repair_json(raw_content)
        
        if not data:
            print("Error: Failed to parse JSON.")
            print("Raw Output:", raw_content)
            return None

        file_path = os.path.join(OUTPUT_DIR, "content.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        print(f"--> Success! Content saved to {file_path}")
        return data

    except Exception as e:
        print(f"API Error: {e}")
        return None

if __name__ == "__main__":
    print("--- 🧪 TESTING DYNAMIC AUTHOR ---")
    
    # Test with a specific author name to see if it catches it
    test_input = """
    Strategic Overview by Madiha Saeid.
    We need to expand our coffee business to Alexandria.
    Projected costs are 50,000 EGP.
    Projected revenue is 120,000 EGP.
    """
    generate_report_content(test_input)