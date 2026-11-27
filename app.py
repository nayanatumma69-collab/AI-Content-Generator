import base64
import random
import re
from pathlib import Path

import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Content Generator", page_icon="✨", layout="wide")

ASSETS = Path(__file__).parent / "assets"
IMAGES = {"Blog Post": "blog.svg", "Social Media Caption": "social.svg", "Email Newsletter": "email.svg"}

# Hardcoded backend configuration
MODEL_NAME = "openai/gpt-oss-20b"

FORMATS = {
    "Blog Post": ("📝", "Write a well-structured blog post with a title, engaging intro, clear section headings, and a conclusion with a CTA."),
    "Social Media Caption": ("📱", "Write an attention-grabbing social media caption with a strong hook, readable spacing, relevant emojis, and 3-5 hashtags."),
    "Email Newsletter": ("📧", "Write a compelling email newsletter featuring 2-3 subject line options, a greeting placeholder, clean narrative body, and a CTA."),
}
TONES = ["Professional", "Casual & Friendly", "Persuasive", "Enthusiastic"]
LENGTHS = {
    "Short": "Keep it brief and tight.",
    "Medium": "Use a moderate length that suits the format.",
    "Long": "Be detailed and thorough.",
}
EXAMPLES = {
    "🤖 AI for small business": "How AI automation agents transform small business workflows",
    "🌱 Eco-friendly launch": "Launching our new range of eco-friendly water bottles",
    "🎓 Learning to code": "Five habits that help beginners learn to code faster",
}
QUICK_REFINEMENTS = {
    "✂️ Shorter": "Make it noticeably shorter while keeping the key message.",
    "👔 More formal": "Make the tone more formal and polished.",
    "😄 Add emojis": "Add a few relevant emojis without overdoing it.",
    "📣 Stronger CTA": "Make the call to action stronger and clearer.",
}

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 90% 5%, #FFE4F1 0, transparent 35%),
                    radial-gradient(circle at 30% 95%, #FFEDD5 0, transparent 35%), #FFFBFE;
    }
    .hero { width: 100%; border-radius: 22px; box-shadow: 0 12px 30px #7C3AED40; }
    img { border-radius: 16px; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #F5EEFF, #FFEFF6);
        border-radius: 16px; padding: 12px 16px;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #7C3AED, #DB2777); border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
hero = base64.b64encode((ASSETS / "hero.svg").read_bytes()).decode()
st.markdown(
    f'<img class="hero" src="data:image/svg+xml;base64,{hero}" '
    'alt="AI Content Studio: one idea in, blogs, captions and emails out">',
    unsafe_allow_html=True,
)


@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def compute_metrics(text):
    words = len(re.findall(r"\b\w+\b", text))
    sentences = len([s for s in re.split(r"[.!?]+(?:\s+|$)|\n+", text) if re.search(r"\w", s)])
    read_time = max(1, round(words / 225))
    return words, len(text), sentences, read_time


def build_generation_prompt(topic, content_type, tone, audience, length, instructions):
    return f"""You are an expert AI content writer.
Task: Write {content_type}.
Topic: {topic}
Tone: {tone}
Target Audience: {audience}
Length: {LENGTHS[length]}

Format Rules:
{FORMATS[content_type][1]}

Additional Instructions (these override the length above):
{instructions or 'None.'}

Output only the generated content in clean Markdown without preambles.
"""


def build_refinement_prompt(current_text, instruction):
    return f"""You are an expert copy editor.
Current Draft:
\"\"\"
{current_text}
\"\"\"

Refinement Instruction:
{instruction}

Output only the rewritten content in clean Markdown without preambles.
"""


def run_model(system_message, prompt, temperature, label, placeholder):
    """Stream a reply into placeholder. A new version is saved only on success."""
    finish = {}

    def chunks():
        stream = get_groq_client().chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            model=MODEL_NAME,
            temperature=temperature,
            max_tokens=2048,
            stream=True,
        )
        for chunk in stream:
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            if choice.finish_reason:
                finish["reason"] = choice.finish_reason
            if choice.delta.content:
                yield choice.delta.content

    try:
        with placeholder.container(border=True), st.spinner(f"{label}..."):
            text = st.write_stream(chunks())
        text = text.strip() if isinstance(text, str) else ""
        if not text:
            raise ValueError("The model returned no text. Please try again.")
    except Exception as e:
        placeholder.empty()
        st.error(f"{label} failed. Your previous draft is unchanged.\n\n{e}")
        return

    st.session_state.history.append({"label": label, "text": text})
    st.session_state.truncated = finish.get("reason") == "length"
    st.rerun()


def use_example(text):
    st.session_state.topic = text


def surprise_me():
    others = [t for t in EXAMPLES.values() if t != st.session_state.get("topic")]
    st.session_state.topic = random.choice(others)


def undo():
    st.session_state.history.pop()
    st.session_state.truncated = False


def restore(index):
    version = st.session_state.history[index]
    st.session_state.history.append({"label": "Restored", "text": version["text"]})
    st.session_state.truncated = False


st.session_state.setdefault("history", [])
st.session_state.setdefault("truncated", False)

# Sidebar: content settings
with st.sidebar:
    st.header("🎨 Create")
    content_type = st.segmented_control(
        "Content format",
        list(FORMATS),
        default="Blog Post",
        format_func=lambda name: f"{FORMATS[name][0]} {name}",
    ) or "Blog Post"
    st.image(str(ASSETS / IMAGES[content_type]), width="stretch")
    tone = st.pills("Tone of voice", TONES, default="Professional") or "Professional"
    length = st.select_slider("Length", list(LENGTHS), value="Medium")
    topic = st.text_area(
        "Topic / key message",
        key="topic",
        placeholder="What do you want to write about?",
        height=130,
    )
    audience = st.text_input("Target audience", value="Tech Professionals & Entrepreneurs")
    notes = st.text_input("Extra constraints (optional)", placeholder="e.g., include bullet points")
    st.button("🎲 Surprise me with a topic", on_click=surprise_me, width="stretch")
    generate_clicked = st.button("🚀 Generate content", type="primary", width="stretch")

# Main area
st.caption("Need inspiration? Try one of these:")
for column, (name, example) in zip(st.columns(len(EXAMPLES)), EXAMPLES.items()):
    column.button(name, on_click=use_example, args=(example,), width="stretch")

history = st.session_state.history
action = None  # (system message, prompt, temperature, label)


def generation_action(label):
    if not topic.strip():
        st.error("Please enter a topic in the sidebar.")
        return None
    prompt = build_generation_prompt(topic, content_type, tone, audience, length, notes)
    return ("You are a professional copywriter.", prompt, 0.7, label)


def refinement_action(instruction, label):
    prompt = build_refinement_prompt(history[-1]["text"], instruction)
    return ("You are a professional copy editor.", prompt, 0.6, label)


if generate_clicked:
    action = generation_action("Generating")

output = st.empty()

if history:
    draft = history[-1]["text"]

    with output.container():
        if st.session_state.truncated:
            st.warning("This draft hit the length limit and may be cut off. Try a shorter length.")

        words, chars, sentences, read_time = compute_metrics(draft)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📖 Words", words)
        m2.metric("🔤 Characters", chars)
        m3.metric("💬 Sentences", sentences)
        m4.metric("⏱️ Read time", f"~{read_time} min")

        preview_tab, markdown_tab, history_tab = st.tabs(["👀 Preview", "📋 Markdown", "🕘 History"])
        with preview_tab:
            with st.container(border=True):
                st.markdown(draft)
        with markdown_tab:
            st.code(draft, language="markdown", wrap_lines=True)
        with history_tab:
            for index in range(len(history) - 1, -1, -1):
                current = " (current)" if index == len(history) - 1 else ""
                with st.expander(f"Version {index + 1}: {history[index]['label']}{current}"):
                    st.markdown(history[index]["text"])
                    if not current:
                        st.button("Restore this version", key=f"restore_{index}",
                                  on_click=restore, args=(index,))

        d1, d2, d3, d4 = st.columns(4)
        d1.download_button("⬇️ Markdown", draft, "content.md", "text/markdown",
                           on_click="ignore", width="stretch")
        d2.download_button("⬇️ Text", draft, "content.txt", "text/plain",
                           on_click="ignore", width="stretch")
        d3.button("↩️ Undo", on_click=undo, disabled=len(history) < 2, width="stretch")
        if d4.button("🔁 Regenerate", width="stretch"):
            action = generation_action("Regenerating")

        st.subheader("🪄 Polish it")
        for column, (name, instruction) in zip(st.columns(4), QUICK_REFINEMENTS.items()):
            if column.button(name, width="stretch"):
                action = refinement_action(instruction, name)

        with st.form("refine_form", clear_on_submit=False):
            custom = st.text_input("Or describe your own change",
                                   placeholder="e.g., add 3 bullet points")
            if st.form_submit_button("Apply refinement"):
                if custom.strip():
                    action = refinement_action(custom.strip(), "Refining")
                else:
                    st.warning("Please describe the change you want.")
elif not action:
    with output.container():
        st.subheader("What will you create today?")
        blurbs = [
            "Title, intro, clear sections and a closing call to action.",
            "A strong hook, emojis and 3-5 hashtags.",
            "Subject line options, greeting, body and call to action.",
        ]
        for column, (name, (icon, _)), blurb in zip(st.columns(3), FORMATS.items(), blurbs):
            with column.container(border=True):
                st.image(str(ASSETS / IMAGES[name]), width="stretch")
                st.markdown(f"### {icon} {name}\n{blurb}")
        st.info("Pick your settings in the sidebar, then click **Generate content**.")

if action:
    run_model(*action, placeholder=output)
