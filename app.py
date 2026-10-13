import streamlit as st
import re
from groq import Groq


st.set_page_config(page_title="AI Content Generator", page_icon="✍️", layout="wide")

st.title("✍️ AI Content Generator")
st.write("Generate tailored marketing copy, blog posts, and social media captions with instant refinement.")

# Hardcoded backend configuration
MODEL_NAME = "openai/gpt-oss-20b"

@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_groq_client()

def compute_metrics(text):
    if not text or text.startswith("Groq API Error:"):
        return 0, 0, 0.0
    words = len(re.findall(r'\b\w+\b', text))
    chars = len(text)
    read_time = round(words / 225, 2)
    return words, chars, read_time

def generate_content(topic, content_type, tone, audience, instructions):
    format_guides = {
        "Blog Post": "Write a well-structured blog post with a title, engaging intro, clear section headings, and a conclusion with a CTA.",
        "Social Media Caption": "Write an attention-grabbing social media caption with a strong hook, readable spacing, relevant emojis, and 3-5 hashtags.",
        "Email Newsletter": "Write a compelling email newsletter featuring 2-3 subject line options, a greeting placeholder, clean narrative body, and a CTA."
    }
    prompt = f"""You are an expert AI content writer.
Task: Write {content_type}.
Topic: {topic}
Tone: {tone}
Target Audience: {audience}

Format Rules:
{format_guides.get(content_type, '')}

Additional Instructions:
{instructions if instructions else 'None.'}

Output only the generated content in clean Markdown without preambles.
"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional copywriter."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=2048
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Groq API Error: {str(e)}"

def refine_content(current_text, refinement_instruction):
    prompt = f"""You are an expert copy editor.
Current Draft:
\"\"\"
{current_text}
\"\"\"

Refinement Instruction:
{refinement_instruction}

Output only the rewritten content in clean Markdown without preambles.
"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional copy editor."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL_NAME,
            temperature=0.6,
            max_tokens=2048
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Groq API Error during refinement: {str(e)}"

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

# Two-column layout
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1. Content Settings")
    content_type = st.selectbox("Content Format", ["Blog Post", "Social Media Caption", "Email Newsletter"])
    tone = st.selectbox("Tone of Voice", ["Professional", "Casual & Friendly", "Persuasive", "Enthusiastic"])
    target_audience = st.text_input("Target Audience", value="Tech Professionals & Entrepreneurs")
    topic = st.text_area("Topic / Key Message", value="How AI automation agents transform small business workflows", height=130)
    custom_notes = st.text_input("Additional Constraints (Optional)", placeholder="e.g., under 150 words, include bullet points")

    generate_btn = st.button("🚀 Generate Content", type="primary")

with col_right:
    st.subheader("2. Generated Output & Analytics")
    if generate_btn:
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating content via Groq LPU..."):
                st.session_state.generated_text = generate_content(
                    topic, content_type, tone, target_audience, custom_notes
                )

    if st.session_state.generated_text:
        words, chars, read_time = compute_metrics(st.session_state.generated_text)

        m1, m2, m3 = st.columns(3)
        m1.metric("Words", words)
        m2.metric("Characters", chars)
        m3.metric("Est. Read Time", f"{read_time} min")

        st.markdown("---")
        st.markdown(st.session_state.generated_text)
        st.markdown("---")

        with st.expander("📋 View Raw Markdown (Copyable)"):
            st.code(st.session_state.generated_text, language="markdown")

        st.subheader("3. Refine or Modify")
        refine_instruction = st.text_input(
            "Refinement instruction:",
            placeholder="e.g., Make it shorter, add 3 bullet points, add emojis"
        )

        r1, r2 = st.columns([1, 1])
        with r1:
            if st.button("🔄 Apply Refinement"):
                if refine_instruction.strip():
                    with st.spinner("Refining text..."):
                        st.session_state.generated_text = refine_content(
                            st.session_state.generated_text, refine_instruction
                        )
                        st.rerun()
                else:
                    st.warning("Please provide a refinement command.")
        with r2:
            if st.button("🔁 Regenerate"):
                with st.spinner("Regenerating..."):
                    st.session_state.generated_text = generate_content(
                        topic, content_type, tone, target_audience, custom_notes
                    )
                    st.rerun()
    else:
        st.info("Set your content parameters on the left and click **Generate Content**.")
