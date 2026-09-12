import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        /* Main background */
        .stApp {
            background: #f7f9fc;
        }

        /* Hide Streamlit default menu and footer */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        /* Main container */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Header */
        .hero {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            padding: 2.2rem 2rem;
            border-radius: 22px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.18);
        }

        .hero h1 {
            font-size: 2.4rem;
            margin-bottom: 0.4rem;
            font-weight: 750;
        }

        .hero p {
            font-size: 1.05rem;
            margin-bottom: 0;
            opacity: 0.92;
        }

        /* Section headings */
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #202938;
            margin-bottom: 0.8rem;
        }

        .section-description {
            color: #667085;
            font-size: 0.92rem;
            margin-bottom: 1.2rem;
        }

        /* Cards */
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 18px;
            border: 1px solid #e6eaf0;
            box-shadow: 0 5px 20px rgba(16, 24, 40, 0.05);
            margin-bottom: 1rem;
        }

        /* Output card */
        .output-card {
            background: white;
            padding: 1.5rem;
            border-radius: 18px;
            border: 1px solid #dfe4ec;
            box-shadow: 0 5px 20px rgba(16, 24, 40, 0.05);
            min-height: 350px;
        }

        /* Labels */
        label {
            font-weight: 600 !important;
            color: #344054 !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            min-height: 45px;
            font-weight: 650;
            border: none;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 70, 229, 0.18);
        }

        /* Primary generate button */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
        }

        /* Text inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 10px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e7eaf0;
        }

        .sidebar-info {
            background: #f4f3ff;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e4e1ff;
            color: #4338ca;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Footer */
        .app-footer {
            text-align: center;
            color: #98a2b3;
            font-size: 0.85rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e6eaf0;
        }

        /* Mobile adjustments */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 1.8rem;
            }

            .hero {
                padding: 1.5rem;
            }

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# Use Streamlit Secrets on deployment, .env locally
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

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>📧 AI Email Generator</h1>
        <p>Create clear, professional and personalized emails in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Email Settings")
    st.caption("Customize the style of your generated email.")

    email_type = st.selectbox(
        "Email Type",
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
        "Email Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-info">
            <b>How it works</b><br><br>
            1. Enter the recipient and key points.<br>
            2. Select the email type, tone and length.<br>
            3. Click Generate Email.<br>
            4. Copy and use your personalized email.
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Main Layout
# --------------------------------------------------

input_column, output_column = st.columns(
    [1, 1],
    gap="large"
)

# --------------------------------------------------
# Input Section
# --------------------------------------------------

with input_column:
    st.markdown(
        """
        <div class="section-title">✍️ Email Details</div>
        <div class="section-description">
            Provide a few details and let AI prepare your email.
        </div>
        """,
        unsafe_allow_html=True
    )

    recipient = st.text_input(
        "Recipient",
        placeholder="Example: HR Manager, Professor, Hiring Manager"
    )

    key_points = st.text_area(
        "What should the email contain?",
        placeholder=(
            "Example: Mention my interest in the internship, "
            "my skills and request an opportunity."
        ),
        height=220
    )

    generate_button = st.button(
        "✨ Generate Email",
        type="primary",
        use_container_width=True
    )

# --------------------------------------------------
# Output Section
# --------------------------------------------------

with output_column:
    st.markdown(
        """
        <div class="section-title">📨 Generated Email</div>
        <div class="section-description">
            Your AI-generated subject and email will appear here.
        </div>
        """,
        unsafe_allow_html=True
    )

    if generate_button:
        if not recipient.strip() or not key_points.strip():
            st.warning("Please enter both the recipient and key points.")

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
                with st.spinner("Generating your email..."):
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

                # Extract subject and email separately
                subject_match = re.search(
                    r"SUBJECT:\s*(.*?)(?=\n\s*EMAIL:)",
                    result,
                    re.IGNORECASE | re.DOTALL
                )

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

                st.session_state["subject"] = subject
                st.session_state["email_body"] = email_body

                st.success("Email generated successfully!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

    # Display stored output
    if "subject" in st.session_state and "email_body" in st.session_state:
        st.markdown(
            '<div class="output-card">',
            unsafe_allow_html=True
        )

        st.markdown("**Subject**")

        st.text_input(
            "Generated Subject",
            value=st.session_state["subject"],
            label_visibility="collapsed"
        )

        st.markdown("**Email Body**")

        st.text_area(
            "Generated Email Body",
            value=st.session_state["email_body"],
            height=300,
            label_visibility="collapsed"
        )

        email_to_copy = (
            f"Subject: {st.session_state['subject']}\n\n"
            f"{st.session_state['email_body']}"
        )

        st.code(email_to_copy, language=None)

        copy_button = st.button(
            "📋 Copy Email",
            use_container_width=True
        )

        if copy_button:
            st.info(
                "Copy the email from the displayed text above. "
                "Streamlit does not provide a reliable browser clipboard "
                "operation without custom JavaScript."
            )

        if st.button("🗑️ Clear Generated Email", use_container_width=True):
            del st.session_state["subject"]
            del st.session_state["email_body"]
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(
            "Your generated email will be displayed here after you click "
            "Generate Email."
        )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="app-footer">
        Built with Python, Streamlit and Groq AI
    </div>
    """,
    unsafe_allow_html=True
)
