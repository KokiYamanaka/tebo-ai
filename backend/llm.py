from config import GEMINI_API_KEY
from google import genai

def call_google_llm(
    prompt: str,
    model: str = "gemini-2.0-flash",  # update to latest model
    api_key: str = GEMINI_API_KEY,
    temperature: float = 0.4
) -> str:
    """
    Sends prompt to Gemini API (cloud) using genai.Client and returns the response text.
    """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error calling Google LLM API: {str(e)}"


# if __name__ == "__main__":
#     user_prompt = "Give three tips for staying focused while studying"
    
#     response = call_google_llm(prompt=user_prompt)
    
#     print("Gemini says:")
#     print(response)
