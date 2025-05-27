import streamlit as st
import re
import pandas as pd

from levenshtein_distance import suggest_keywords
from lexical import analyze_code
from error_handler import detect_errors

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

uploaded_file = st.file_uploader("Upload a .bot file", type=["bot"])

# Define keywords globally (all lowercase)
keywords = {
    "boot", "shutdown", "ping", "beep", "set", "check", "else", "repeat",
    "stop", "go", "function", "end", "true", "false", "send"
}

def clean_token(token):
    token = token.strip('"').strip("'")
    token = ''.join(ch for ch in token if ch.isalnum() or ch == '_')
    return token

def is_valid_identifier(token):
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token))

def error_help_message(error_msg, token):
    token_clean = clean_token(token)
    msg_lower = error_msg.lower()

    if "starts with a digit" in msg_lower or "identifier should not start with a digit" in msg_lower:
        return f"Error: Identifier '{token_clean}' should not start with a number."
    if "starts with an underscore" in msg_lower or "identifier should not start with an underscore" in msg_lower:
        return f"Error: Identifier '{token_clean}' should not start with an underscore."
    if "invalid character" in msg_lower or "contains invalid characters" in msg_lower:
        return f"Error: Identifier '{token_clean}' contains invalid characters. Use only letters, digits, or underscores."
    if "unclosed" in msg_lower or "unterminated" in msg_lower:
        return f"Error: Token '{token}' appears to be unclosed or incomplete."
    if "unrecognized symbol" in msg_lower:
        return f"Error: Token '{token_clean}' contains unrecognized symbol(s). Please remove invalid characters."
    if "invalid identifier" in msg_lower:
        return f"Error: Identifier '{token_clean}' is invalid. Identifiers must start with a letter or underscore and contain only letters, digits, or underscores."

    return f"Error: {error_msg} (token: '{token_clean}')"

def group_tokens_by_type(token_stream):
    grouped = {
        "KEYWORD": set(),
        "IDENTIFIER": set(),
        "NUMBER": set(),
        "STRING": set(),
        "OPERATOR": set(),
        "DELIMITER": set(),
        "UNKNOWN": set()
    }
    for token, token_type, _ in token_stream:
        if token_type in grouped:
            grouped[token_type].add(token)
        else:
            grouped["UNKNOWN"].add(token)
    for key in grouped:
        grouped[key] = sorted(grouped[key])
    return grouped

def check_identifier_errors(token_stream):
    errors = []
    for token, token_type, line in token_stream:
        if token_type == "IDENTIFIER":
            if not token:
                errors.append({"line": line, "error": "Empty identifier", "token": token})
                continue
            if token[0].isdigit():
                errors.append({"line": line, "error": "Identifier should not start with a digit", "token": token})
            elif token[0] == '_':
                errors.append({"line": line, "error": "Identifier should not start with an underscore", "token": token})
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token):
                errors.append({"line": line, "error": "Identifier contains invalid characters", "token": token})
    return errors

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    if st.button("🔍 Analyze"):
        display_tokens, token_stream, suggestions = analyze_code(text)
        lexical_errors = detect_errors(token_stream)
        identifier_errors = check_identifier_errors(token_stream)

        errors = lexical_errors + identifier_errors
        grouped_tokens = group_tokens_by_type(token_stream)

        st.markdown("#### ✅ Tokens Grouped by Type")

        max_len = max(len(toks) for toks in grouped_tokens.values()) if grouped_tokens else 0
        formatted_data = {
            cat: toks + [""] * (max_len - len(toks))
            for cat, toks in grouped_tokens.items()
        }

        df_grouped = pd.DataFrame(formatted_data)

        # Remove columns that are all empty strings
        df_grouped = df_grouped.loc[:, (df_grouped != "").any(axis=0)]

        # Display the table with custom styling for dark theme
        styled_df = (
            df_grouped.style
            .hide(axis="index")
            .set_table_styles([
                {'selector': 'thead th', 'props': [
                    ('background-color', "#0d265c"),  # blue header background
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('font-size', '1.1em'),
                    ('border-bottom', '2px solid #1e40af'),
                    ('padding', '8px'),
                    ('text-align', 'center')
                ]},
                {'selector': 'tbody td', 'props': [
                    ('background-color', '#1f2937'),  # dark background for cells
                    ('color', 'white'),
                    ('border', '1px solid #374151'),
                    ('padding', '8px'),
                    ('text-align', 'center'),
                    ('font-family', 'monospace'),
                    ('font-size', '1em'),
                    ('vertical-align', 'middle')
                ]},
                {'selector': 'tbody tr:hover', 'props': [
                    ('background-color', '#4b5563'),  # highlight row on hover
                    ('cursor', 'pointer')
                ]},
                {'selector': 'table', 'props': [
                    ('border-collapse', 'collapse'),
                    ('width', '100%'),
                    ('margin-top', '1em'),
                    ('margin-bottom', '1em'),
                    ('border-radius', '8px'),
                    ('overflow', 'hidden'),
                    ('box-shadow', '0 0 15px rgba(0,0,0,0.3)')
                ]}
            ])
        )
        st.table(styled_df)

        st.markdown("#### ❌ Errors")
        if errors:
            for e in errors:
                error_token = e["token"]
                error_token_str = error_token if isinstance(error_token, str) else str(error_token)
                st.markdown(
                    f"<div class='error'>Line {e['line']}: {e['error']} → <code>{error_token_str}</code></div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<div class='error'>No lexical errors found.</div>", unsafe_allow_html=True)

        st.markdown("#### 💡 Suggestions")
        if errors:
            for error in errors:
                raw_token = error["token"]
                token_str = raw_token if isinstance(raw_token, str) else str(raw_token)
                cleaned_token = clean_token(token_str)
                msg = error_help_message(error["error"], token_str)

                extra_info = ""
                if token_str != cleaned_token:
                    extra_info = f"<br><span style='font-size: 0.9em;'><b>Error token:</b> Raw = <code>{token_str}</code>, Clean = <code>{cleaned_token}</code></span>"

                st.markdown(
                    f"<div class='suggestion'>{msg}{extra_info}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("#### 🔎 Additional suggestions for identifiers not marked as errors")
            for tok in token_stream:
                tok_str = tok if isinstance(tok, str) else (tok[0] if isinstance(tok, tuple) else str(tok))
                lower_tok = tok_str.lower()
                if (tok_str and is_valid_identifier(tok_str) and lower_tok not in keywords
                    and not any(e['token'] == tok_str for e in errors)):
                    suggestion = suggest_keywords(lower_tok, keywords)
                    if suggestion:
                        st.markdown(
                            f"<div class='suggestion'>Did you mean: <b>{suggestion}</b>? "
                            f"(from token '<code>{tok_str}</code>')</div>",
                            unsafe_allow_html=True
                        )

        if not errors and not any(
            (clean_token(tok[0] if isinstance(tok, tuple) else tok).lower() not in keywords and
             is_valid_identifier(clean_token(tok[0] if isinstance(tok, tuple) else tok)) and
             not any(e['token'] == (tok[0] if isinstance(e['token'], tuple) else e['token']) for e in errors))
            for tok in token_stream
        ):
            st.markdown("<div class='suggestion'>No suggestions needed.</div>")
        if st.button("🧹 Clear"):
           st.session_state.uploaded_file = None
    # Clear file uploader widget by resetting its key
           st.experimental_rerun()