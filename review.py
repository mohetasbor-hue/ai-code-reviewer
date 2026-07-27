# Testing Gemini review 
import os
import requests

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY secret is missing in GitHub settings!")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "You are an expert AI code reviewer. Please provide a short, helpful review summary for this code."}]
        }]
    }

    response = requests.post(url, json=payload)
    result = response.json()

    try:
        review_text = result['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        review_text = f"Gemini API Error: {result}"

    with open("review_comment.md", "w", encoding="utf-8") as f:
        f.write(review_text)

if __name__ == "__main__":
    main()
 
