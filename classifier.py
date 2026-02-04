import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "openai/gpt-oss-120b"

def classify_po(po_description: str, supplier: str = "Not provided"):
    user_prompt = f"""
PO Description:
{po_description}

Supplier:
{supplier}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        # ✅ Safe return
        return response.choices[0].message.content.strip()

    except Exception as e:
        # ✅ Prevent app crash
        return None


