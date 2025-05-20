import streamlit as st
import re

# Custom styling
st.set_page_config(page_title="BotLang | Lexical Analyzer", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #111827;
        color: white;
    }
    .stApp {
        background-color: #111827;
        color: white;
    }
    .big-title {
        font-size: 3em;
        font-weight: bold;
    }
    .section-title {
        font-size: 1.5em;
        margin-top: 1em;
        font-weight: 600;
    }
    .token, .error, .suggestion {
        background-color: #1f2937;
        padding: 0.75em;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown("<div class='big-title'>🤖 BotLang</div>", unsafe_allow_html=True)
st.markdown("### LEXICAL ANALYZER")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

def lexical_analyze(text):
    tokens = []
    errors = []
    suggestions = []

    keywords = {"boot", "shutdown", "ping", "beep", "set", "check", "else", "repeat",
    "stop", "go", "function", "end", "true", "false", "send"}
    pattern = r'"[^"]*"|\b\w+\b|[{}();=+\-*/<>]|[^\w\s]+'

    for match in re.finditer(pattern, text):
        token = match.group()
        if token in keywords:
            tokens.append(f"Keyword: {token}")
        elif token.isdigit():
            tokens.append(f"Integer: {token}")
        elif re.match(r'^"[^\"]*"$',token):
            tokens.append(f"String: {token}")
        elif re.match(r'^[a-zA-Z_]\w*$', token):
            tokens.append(f"Identifier: {token}")
        elif token in "{}();=+-*/<>":
            tokens.append(f"Symbol: {token}")
        else:
            errors.append(f"Unrecognized token: {token}")
            suggestions.append(f"Check '{token}' – may be a typo or unsupported syntax.")

    return tokens, errors, suggestions


if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    
    if st.button("🔍 Analyze"):
        tokens, errors, suggestions = lexical_analyze(text)

        st.markdown("#### ✅ Tokens")
        for t in tokens:
            st.markdown(f"<div class='token'>{t}</div>", unsafe_allow_html=True)

        st.markdown("#### ❌ Errors")
        if errors:
            for e in errors:
                st.markdown(f"<div class='error'>{e}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='error'>No lexical errors found.</div>", unsafe_allow_html=True)

        st.markdown("#### 💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.markdown(f"<div class='suggestion'>{s}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='suggestion'>No suggestions. Code looks clean!</div>", unsafe_allow_html=True)

    if st.button("❌ Clear"):
        st.rerun()
