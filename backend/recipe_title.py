from llm import call_google_llm 

class RecipeTitleGenerator:
    def to_title(self, user_text: str) -> str:
        prompt = (
            "# 🎯 Task From the user's input, generate a single Japanese **recipe title** that reflects their food preference.\n\n"
            "# 📌 Output Format Only return:\n`<Japanese Recipe Title>`\n\n"
            "⚠️ Do NOT include any code, functions, or explanations.\n\n"
            "# ✅ Example Input: \"spicy pork\"  \nOutput: `ピリ辛豚こまのスタミナ炒め`\n\n"
            "---\n\n"
            "# 🧠 Instructions\n"
            "- Use the user input to infer the protein, flavor, and cooking method.\n"
            "- Balance:\n"
            "  - **Exploit**: stay relevant (same meat, flavor).\n"
            "  - **Explore**: small twist (different veggie, sauce, or fusion style).\n"
            "- Avoid copying exact input words.\n\n"
            "---\n\n"
            f"# 🧪 User Input\n\"{user_text}\""
        )
        response = call_google_llm(prompt=prompt)  
        return response.strip()