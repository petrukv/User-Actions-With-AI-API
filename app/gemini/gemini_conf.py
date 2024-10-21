from dotenv import load_dotenv
import os

from fastapi import HTTPException
import google.generativeai as genai


load_dotenv()

api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def check_profanity(content: str) -> bool:
    try:
        response = model.generate_content(f"Чи містить даний контент нецензурну лексику? '{content}'")
        
        if hasattr(response, 'text'):
            if "так" in response.text.lower():
                return True
        else:
            # Якщо finish_reason = 3, це означає, що контент вважається шкідливим
            if response.candidates and any(candidate.finish_reason == 3 for candidate in response.candidates):
                raise HTTPException(status_code=400, detail="Content deemed inappropriate by AI")
        
        return False
    except Exception as e:
        print(f"Error checking profanity: {e}")