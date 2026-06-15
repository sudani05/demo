key="AIzaSyBVzYPGp-4HF5CaYq0yvR7jWN3g_i_Hhwg"
from openai import OpenAI
import gradio as gr


gemini_model = OpenAI(
    api_key="AIzaSyBVzYPGp-4HF5CaYq0yvR7jWN3g_i_Hhwg",  
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are a professional life coach and personality transformation expert. Your task is to guide a young man who has faced multiple rejections when trying to propose to girls. Help him improve his lifestyle, personality, communication skills, grooming, mindset, emotional intelligence, and overall confidence.

Be supportive, realistic, and actionable. Provide him with step-by-step advice on:
- How to rebuild his self-confidence
- How to improve his physical appearance and grooming
- How to develop an attractive personality
- How to talk to girls naturally and respectfully
- How to handle rejection positively
- How to improve social skills, body language, and eye contact
- How to upgrade his mindset, habits, and environment for long-term self-growth

Avoid toxic behavior, manipulation, or pick-up lines. Focus on genuine self-improvement and self-respect. Your goal is to help him become the best version of himself and live a confident, happy life—whether or not he gets a "yes."
"""

def get_advice(user_input):
    mymsg = [
        {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
    ]

    response = gemini_model.chat.completions.create(
        model="gemini-2.5-flash",
        messages=mymsg
    )

    return response.choices[0].message.content


with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 💬 Life Transformation AI
    Facing rejection doesn't mean the end — it's the beginning of becoming your best self.

    👉 Enter your current struggle or story, and get expert advice to improve your lifestyle, personality, mindset, and confidence.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(
                lines=5,
                label="🗣 Tell your story or ask for advice",
                
                placeholder="Type your situation, problem, or question..."
            )
            submit_btn = gr.Button("🚀 Get Advice")

        with gr.Column(scale=1):
            output = gr.Textbox(
                label="🎯 Coach's Response",
                lines=15,
                interactive=False
            )

    submit_btn.click(fn=get_advice, inputs=user_input, outputs=output)


app.launch()