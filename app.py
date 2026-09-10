import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered"
)

# Title
st.title("📧 AI Email Generator")
st.write("Generate professional emails using AI in seconds.")

# Sidebar
st.sidebar.header("Email Settings")

email_type = st.sidebar.selectbox(
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

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Formal",
        "Professional",
        "Friendly"
    ]
)

length = st.sidebar.selectbox(
    "Email Length",
    [
        "Short",
        "Medium",
        "Detailed"
    ]
)

# Main inputs
recipient = st.text_input(
    "Recipient",
    placeholder="e.g., HR Manager"
)

key_points = st.text_area(
    "What should the email contain?",
    placeholder="Enter the important points you want to include..."
)

# Generate button
if st.button("✨ Generate Email", use_container_width=True):

    if not recipient or not key_points:
        st.warning("Please enter the recipient and key points.")

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

            st.success("Email generated successfully!")

            st.subheader("📨 Generated Email")

            st.text_area(
                "Result",
                value=result,
                height=400
            )

        except Exception as e:

            st.error(f"Something went wrong: {e}")