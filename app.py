import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="MailCraft",
    page_icon="✉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Montserrat:wght@400;500;600;700;800&display=swap');

    /* ==================================================
       COLOR PALETTE
       ================================================== */

    :root {
        --purple-dark: #462C7D;
        --purple: #831C91;
        --pink: #D552A3;
        --pink-light: #FF70BF;

        --background: #FCFAFD;
        --white: #FFFFFF;
        --text-dark: #241B35;
        --text: #463B50;
        --muted: #75697F;
        --border: #E5DDE9;
        --soft-purple: #F5F0F9;
        --soft-pink: #FFF1F8;
    }


    /* ==================================================
       GLOBAL
       ================================================== */

    .stApp {
        background: var(--background);
    }

    html,
    body,
    [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* ==================================================
       BRAND
       ================================================== */

    .brand-name {
        color: var(--purple-dark) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 0 !important;
    }

    .brand-tagline {
        color: var(--muted) !important;
        font-family: 'Lora', serif !important;
        font-size: 1.02rem !important;
        margin-top: -5px !important;
        margin-bottom: 1.5rem !important;
    }


    /* ==================================================
       HERO
       ================================================== */

    .hero-box {
        background: var(--purple-dark);
        border-radius: 18px;
        padding: 2.25rem 2.4rem;
        margin-bottom: 2.2rem;
        box-shadow: 0 12px 30px rgba(70, 44, 125, 0.15);
    }

    .hero-title {
        color: white !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2.15rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px !important;
        margin: 0 !important;
    }

    .hero-description {
        color: rgba(255, 255, 255, 0.88) !important;
        font-family: 'Lora', serif !important;
        font-size: 1.08rem !important;
        line-height: 1.7 !important;
        margin-top: 0.65rem !important;
        max-width: 720px;
    }


    /* ==================================================
       SECTION HEADINGS
       ================================================== */

    .section-title {
        color: var(--text-dark) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.25rem !important;
    }

    .section-description {
        color: var(--muted) !important;
        font-family: 'Lora', serif !important;
        font-size: 1rem !important;
        line-height: 1.65 !important;
        margin-bottom: 1.25rem !important;
    }


    /* ==================================================
       SIDEBAR
       ================================================== */

    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.8rem;
    }

    .sidebar-title {
        color: var(--purple-dark) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }

    .sidebar-description {
        color: var(--muted) !important;
        font-family: 'Lora', serif !important;
        font-size: 0.94rem !important;
        line-height: 1.6 !important;
        margin-bottom: 1.3rem !important;
    }


    /* ==================================================
       LABELS
       ================================================== */

    label {
        color: var(--text-dark) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
    }


    /* ==================================================
   SELECTBOX - MAILCRAFT PALETTE
   ================================================== */

/* Main selectbox container */
section[data-testid="stSidebar"] [data-baseweb="select"] {
    width: 100% !important;
    background: #FFFFFF !important;
}

/* The visible box */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;

    border: 1.5px solid #D8CBE1 !important;
    border-radius: 10px !important;

    box-shadow: none !important;
}

/* Force every inner element to white */
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="select"] > div > div,
section[data-testid="stSidebar"] [data-baseweb="select"] > div > div > div {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}

/* Selected text */
section[data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"] {
    background: #FFFFFF !important;
    color: #462C7D !important;
}

/* Text */
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #462C7D !important;
    background: transparent !important;

    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* Arrow */
section[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #831C91 !important;
    fill: #831C91 !important;
    background: transparent !important;
}

/* Hover */
section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    border-color: #D552A3 !important;
    background: #FFFFFF !important;
}

/* Focus */
section[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #D552A3 !important;

    box-shadow:
        0 0 0 3px rgba(213, 82, 163, 0.12) !important;
}


/* ==================================================
   DROPDOWN OPTIONS
   ================================================== */

div[data-baseweb="popover"] {
    background: #FFFFFF !important;
}

div[data-baseweb="popover"] > div {
    background: #FFFFFF !important;
}

div[data-baseweb="menu"] {
    background: #FFFFFF !important;

    border: 1px solid #E5DDE9 !important;

    border-radius: 10px !important;

    box-shadow:
        0 10px 25px rgba(70, 44, 125, 0.12) !important;
}

div[data-baseweb="menu"] li {
    background: #FFFFFF !important;

    color: #462C7D !important;

    font-family: 'Montserrat', sans-serif !important;
}

div[data-baseweb="menu"] li:hover {
    background: #FFF1F8 !important;

    color: #831C91 !important;
}

    /* ==================================================
       TEXT INPUTS
       ================================================== */

    .stTextInput input,
    .stTextArea textarea {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: var(--text-dark) !important;

        border: 1px solid #D8CBE1 !important;
        border-radius: 10px !important;

        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;

        box-shadow: none !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #A99CAF !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--pink) !important;

        box-shadow:
            0 0 0 3px rgba(213, 82, 163, 0.10) !important;
    }


    /* ==================================================
       GENERATE BUTTON
       ================================================== */

    .stButton > button {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 11px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: var(--purple-dark) !important;
        color: #FFFFFF !important;

        border: 1px solid var(--purple-dark) !important;

        min-height: 54px !important;

        font-size: 0.95rem !important;
        font-weight: 700 !important;

        box-shadow:
            0 8px 20px rgba(70, 44, 125, 0.17) !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: var(--purple) !important;
        border-color: var(--purple) !important;

        transform: translateY(-1px);

        box-shadow:
            0 10px 24px rgba(131, 28, 145, 0.20) !important;
    }


    /* ==================================================
       NORMAL BUTTONS
       ================================================== */

    .stButton > button:not([kind="primary"]) {
        background: #FFFFFF !important;
        color: var(--purple-dark) !important;

        border: 1px solid #D8CBE1 !important;

        min-height: 44px !important;

        font-size: 0.84rem !important;
    }

    .stButton > button:not([kind="primary"]):hover {
        border-color: var(--pink) !important;
        color: var(--purple) !important;
    }


    /* ==================================================
       GENERATED EMAIL
       ================================================== */

    .preview-label {
        color: var(--purple) !important;

        font-family: 'Montserrat', sans-serif !important;

        font-size: 0.75rem !important;
        font-weight: 800 !important;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-top: 0.4rem;
        margin-bottom: 0.45rem;
    }

    .subject-display {
        background: var(--soft-purple);

        border-left: 4px solid var(--pink);

        border-radius: 0 9px 9px 0;

        padding: 0.8rem 1rem;

        color: var(--text-dark);

        font-family: 'Montserrat', sans-serif;

        font-size: 0.95rem;

        font-weight: 700;

        line-height: 1.5;

        margin-bottom: 1.1rem;
    }


    /* ==================================================
       FOOTER
       ================================================== */

    .app-footer {
        text-align: center;

        color: #9B8FA3;

        font-family: 'Montserrat', sans-serif;

        font-size: 0.76rem;

        margin-top: 2.5rem;

        padding-top: 1.2rem;

        border-top: 1px solid var(--border);
    }


    /* ==================================================
       MOBILE
       ================================================== */

    @media (max-width: 768px) {

        .brand-name {
            font-size: 1.9rem !important;
        }

        .hero-title {
            font-size: 1.75rem !important;
        }

        .hero-description {
            font-size: 0.95rem !important;
        }

        .section-title {
            font-size: 1.15rem !important;
        }

        .section-description {
            font-size: 0.92rem !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

api_key = None

try:
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "Groq API key is missing. Add GROQ_API_KEY to your .env file "
        "or Streamlit Cloud Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# ==================================================
# BRAND
# ==================================================

st.markdown(
    '<div class="brand-name">✉ MailCraft</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand-tagline">'
    'Thoughtful emails, crafted in seconds.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# HERO
# ==================================================

st.markdown(
    '<div class="hero-box">'
    '<div class="hero-title">'
    'Write emails that sound like you.'
    '</div>'
    '<div class="hero-description">'
    'Create clear, polished and personalized emails with the help of AI '
    '— without starting from a blank page.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Email settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Shape your email by choosing its purpose, tone and length.'
        '</div>',
        unsafe_allow_html=True
    )

    email_type = st.selectbox(
        "Email type",
        [
            "Job Application",
            "Internship Request",
            "Leave Request",
            "Follow-up",
            "General Request",
            "Complaint"
        ]
    )

    tone = st.selectbox(
        "Tone",
        [
            "Formal",
            "Professional",
            "Friendly"
        ]
    )

    length = st.selectbox(
        "Email length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )


# ==================================================
# MAIN LAYOUT
# ==================================================

input_column, output_column = st.columns(
    [1, 1],
    gap="large"
)


# ==================================================
# INPUT SECTION
# ==================================================

with input_column:

    st.markdown(
        '<div class="section-title">Email details</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Give MailCraft a little context. '
        'It will take care of the wording.'
        '</div>',
        unsafe_allow_html=True
    )

    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. Hiring Manager, Professor, HR Manager"
    )

    key_points = st.text_area(
        "What should the email contain?",
        placeholder=(
            "Mention the important points you want included "
            "in the email..."
        ),
        height=220
    )

    st.markdown(
        "<div style='height: 0.25rem;'></div>",
        unsafe_allow_html=True
    )

    generate_button = st.button(
        "Generate email",
        type="primary",
        use_container_width=True
    )


# ==================================================
# OUTPUT SECTION
# ==================================================

with output_column:

    st.markdown(
        '<div class="section-title">Your email</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Your subject and polished email will appear here.'
        '</div>',
        unsafe_allow_html=True
    )


    # ==================================================
    # GENERATE EMAIL
    # ==================================================

    if generate_button:

        if not recipient.strip() or not key_points.strip():

            st.warning(
                "Please enter both the recipient and key points."
            )

        else:

            prompt = f"""
You are a professional email writing assistant.

Write a high-quality email based on the following information:

Email Type: {email_type}
Recipient: {recipient}
Tone: {tone}
Length: {length}

Important points:
{key_points}

Requirements:
1. Generate a suitable subject line.
2. Write a professional email.
3. Keep the email clear and grammatically correct.
4. Do not add unnecessary information.
5. Include an appropriate greeting and closing.
6. Return the subject and email separately.

Format:

SUBJECT:
<subject>

EMAIL:
<email>
"""

            try:

                with st.spinner("Crafting your email..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7
                    )

                    result = response.choices[0].message.content


                # ==================================================
                # EXTRACT SUBJECT
                # ==================================================

                subject_match = re.search(
                    r"SUBJECT:\s*(.*?)(?=\n\s*EMAIL:)",
                    result,
                    re.IGNORECASE | re.DOTALL
                )


                # ==================================================
                # EXTRACT EMAIL BODY
                # ==================================================

                email_match = re.search(
                    r"EMAIL:\s*(.*)",
                    result,
                    re.IGNORECASE | re.DOTALL
                )


                if subject_match:
                    subject = subject_match.group(1).strip()
                else:
                    subject = "Generated Email"


                if email_match:
                    email_body = email_match.group(1).strip()
                else:
                    email_body = result.strip()


                # Save only ONE copy
                st.session_state["subject"] = subject
                st.session_state["email_body"] = email_body

                st.success("Email generated successfully!")


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


    # ==================================================
    # DISPLAY GENERATED EMAIL
    # ==================================================

    if (
        "subject" in st.session_state
        and "email_body" in st.session_state
    ):

        st.markdown(
            '<div class="preview-label">Subject</div>',
            unsafe_allow_html=True
        )


        # Safely display subject

        safe_subject = (
            st.session_state["subject"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )


        st.markdown(
            f'<div class="subject-display">'
            f'{safe_subject}'
            f'</div>',
            unsafe_allow_html=True
        )


        # ==================================================
        # EMAIL BODY
        # ==================================================

        st.markdown(
            '<div class="preview-label">Email body</div>',
            unsafe_allow_html=True
        )


        # ONLY ONE EMAIL BOX

        st.text_area(
            "Generated email",
            value=st.session_state["email_body"],
            height=330,
            label_visibility="collapsed"
        )


        # ==================================================
        # CLEAR EMAIL
        # ==================================================

        st.markdown(
            "<div style='height: 0.6rem;'></div>",
            unsafe_allow_html=True
        )

        if st.button(
            "Clear email",
            use_container_width=True
        ):

            del st.session_state["subject"]
            del st.session_state["email_body"]

            st.rerun()


    # ==================================================
    # EMPTY STATE
    # ==================================================

    else:

        st.info(
            "Your generated email will appear here after "
            "you click Generate email."
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="app-footer">'
    'MailCraft · Built with Python, Streamlit &amp; Groq AI'
    '</div>',
    unsafe_allow_html=True
)

