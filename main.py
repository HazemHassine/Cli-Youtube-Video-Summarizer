from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ')

def youtube_url_to_id(url):
    return url.replace('https://www.youtube.com/watch?v=', '')

def summarize_text(to_summarize_text: list, extra_instructions: str = "") -> str:
    Groq_client = Groq(api_key=GROQ_API_KEY)
    completion = Groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"in the first line without any markdown, Write the suitable name of the for this, without any other text, then in the next lines, in Structured Markdown and with clear sections, tell me (in detail) what this youtube video talk about while keeping all the important information, mention important details also! and good informations. When needed explain more where the text is lacking explanations.{extra_instructions}. text: {to_summarize_text}"
            }
        ],
        temperature=1.1,
        max_tokens=4640,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response