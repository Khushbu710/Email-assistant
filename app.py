import streamlit as st
import time
from email_generator import EmailGenerator

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="wide"
)

# --- CUSTOM CSS FOR PROFESSIONAL STYLING (Aurora Modern Flexbox Theme) ---
st.markdown("""
<style>
    /* Main Background & Font */
    html, body, .reportview-container {
        background: radial-gradient(circle at 20% 40%, #e8eaf6 0%, #f0f4c3 100%);
        font-family: 'Inter', 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', sans-serif;
    }

    .main .block-container {
        padding: 2rem 2rem;
    }

    /* Custom Banner */
    .banner {
        background: linear-gradient(120deg, #00bcd4 10%, #8e24aa 90%);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 32px -8px rgba(0, 188, 212, 0.15), 0 1.5px 9px #8e24aa44;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .banner h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
        text-shadow: 0px 2px 8px #8e24aa66;
    }
    .banner p {
        color: #e0e7ff;
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 0;
        text-shadow: 0px 0.5px 8px #00bcd444;
    }

    /* Form Container */
    .form-container {
        background-color: rgba(255,255,255,0.96);
        border-radius: 22px;
        padding: 2.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
        border: 1px solid #ede7f6;
        margin-bottom: 2rem;
    }

    /* Generated Email & Suggestions Flex Card */
    .result-card {
        background-color: #fff;
        border-radius: 22px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.09);
        display: flex;
        flex-direction: column;
        align-items: stretch;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .result-card h3 {
        color: #512da8;
        border-bottom: 2px solid #00bcd4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        font-size: 1.28rem;
        font-weight: 700;
    }
    .email-flex {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        width: 100%;
        min-height: 200px;
        max-height: 60vh;
        overflow-y: auto;
        background: #f6f9ff;
        border-radius: 13px;
        font-size: 1.08rem;
        padding: 1.2rem 1rem;
        color: #333;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px #e3e3e3;
        word-break: break-word;
        white-space: pre-wrap;
    }

    /* Expander styling */
    .stExpander {
        border-radius: 16px !important;
        border: 1px solid #d1c4e9 !important;
        background-color: #f7f6fc;
    }
    .stExpander header {
        font-size: 1.09rem;
        font-weight: 600;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 14px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        color: white;
        background: linear-gradient(120deg, #00bcd4 0%, #8e24aa 100%);
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px -5px #00bcd488;
        font-size: 1.06rem;
        margin-bottom: 0.5rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 7px 24px -6px #8e24aa88;
        background: linear-gradient(120deg, #8e24aa 0%, #00bcd4 100%);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 4px 15px -5px #00bcd488;
    }

    /* Copy to Clipboard Button */
    .copy-btn {
        background: linear-gradient(90deg, #66bb6a 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.3rem;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        box-shadow: 0 2px 8px #66bb6a33;
        transition: all 0.17s ease;
    }
    .copy-btn:hover {
        background: linear-gradient(90deg, #43a047 0%, #66bb6a 100%);
        box-shadow: 0 4px 16px #43a04733;
        transform: scale(1.04);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.97rem;
        margin-top: 3rem;
        padding-bottom: 1.5rem;
        letter-spacing: 0.02em;
    }
</style>
""", unsafe_allow_html=True)

# --- BANNER ---
st.markdown(
    """
    <div class="banner">
        <h1>📧 AI Email Assistant</h1>
        <p>Generate professional emails with the perfect tone, formatting, and content.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- INITIALIZATION LOGIC (No changes) ---
@st.cache_resource
def load_generator():
    try:
        generator = EmailGenerator()
        return generator
    except Exception as e:
        st.error(f"Failed to initialize Email Generator: {str(e)}")
        return None

if "generator" not in st.session_state:
    st.session_state.generator = load_generator()
    
if st.session_state.generator:
    if "connection_tested" not in st.session_state:
        with st.spinner("Testing GROQ API connection..."):
            connection_ok, message = st.session_state.generator.test_connection()
            st.session_state.connection_tested = True
            st.session_state.connection_ok = connection_ok
            st.session_state.connection_message = message
else:
    st.session_state.connection_tested = False
    st.session_state.connection_ok = False

# --- CONNECTION STATUS (No changes) ---
if "connection_tested" in st.session_state:
    if st.session_state.connection_ok:
        st.success(f"✅ Connection Status: {st.session_state.connection_message}")
    else:
        st.warning(f"⚠️ Connection Status: {st.session_state.connection_message}")
        if st.button("Retry Connection"):
            with st.spinner("Testing connection..."):
                connection_ok, message = st.session_state.generator.test_connection()
                st.session_state.connection_ok = connection_ok
                st.session_state.connection_message = message
                st.rerun()

# --- FORM SECTION ---
st.markdown('<div class="form-container">', unsafe_allow_html=True)
with st.form("email_form"):
    st.header("Craft Your Email")
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("Recipient", placeholder="e.g., John Doe, HR Manager")
        sender = st.text_input("Your Name/Role", placeholder="e.g., Jane Smith, Developer")
    with col2:
        purpose_options = ["Request Information", "Job Application", "Follow-up", "Thank You", "Proposal", "Apology", "Introduction", "Meeting Request", "Feedback", "Other"]
        purpose = st.selectbox("Email Purpose", purpose_options)
        tone_options = ["Professional", "Friendly", "Formal", "Casual", "Urgent", "Persuasive", "Apologetic"]
        tone = st.selectbox("Tone", tone_options)
        length_options = ["Short", "Medium", "Long"]
        length = st.selectbox("Length", length_options)
    
    key_points = st.text_area("Key Points to Include", height=150, placeholder="Enter the main points, requests, or questions for your email...")
    
    generate_button = st.form_submit_button("Generate Email")
st.markdown('</div>', unsafe_allow_html=True)

# --- FORM SUBMISSION LOGIC (No changes) ---
if generate_button:
    if not recipient or not sender or not key_points:
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Generating your email..."):
            try:
                email_text = st.session_state.generator.generate_email(
                    key_points=key_points, recipient=recipient, sender=sender,
                    purpose=purpose, tone=tone, length=length
                )
                st.session_state.email_text = email_text
                st.session_state.suggestions = None # Reset suggestions
            except Exception as e:
                st.error(f"Error during email generation: {str(e)}")

# --- DISPLAY RESULTS ---
if "email_text" in st.session_state and st.session_state.email_text:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<h3>Generated Email</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="email-flex" id="emailToCopy">{st.session_state.email_text}</div>', unsafe_allow_html=True)
    # Copy to Clipboard Button (uses JS directly)
    col1, col2 = st.columns(2)
    with col1:
        st.code(st.session_state.email_text, language="", line_numbers=False)  # Has native copy button
    with col2:
        if st.button("Improve This Email"):
            with st.spinner("Analyzing and suggesting improvements..."):
                suggestions = st.session_state.generator.improve_email(st.session_state.email_text)
                st.session_state.suggestions = suggestions
    st.markdown('</div>', unsafe_allow_html=True)

if "suggestions" in st.session_state and st.session_state.suggestions:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<h3>Suggested Improvements</h3>', unsafe_allow_html=True)
    st.write(st.session_state.suggestions)
    st.markdown('</div>', unsafe_allow_html=True)

# --- EXPANDABLE SECTIONS (No changes in logic) ---
with st.expander("Need inspiration? Try a template"):
    templates = {
        "Job Application": "I am writing to apply for the [Position] role advertised on [Platform]. With my experience in [Relevant Skills], I believe I am well-suited for this position. I have attached my resume and portfolio. I am particularly interested in this role because [Reason]. I would appreciate the opportunity to discuss my application further.",
        "Meeting Request": "I would like to schedule a meeting to discuss [Topic]. This is important because [Reason]. I am available on [Dates/Times]. The meeting should take approximately [Duration]. Please let me know what works best for your schedule.",
        "Thank You": "I wanted to express my sincere gratitude for [What They Did]. Your help with [Specific Action] was invaluable and [Positive Impact]. I truly appreciate your time and support. If there's ever anything I can do to return the favor, please don't hesitate to let me know.",
        "Follow-up": "I am writing to follow up on [Previous Communication/Meeting]. As discussed, [Reminder of Key Points]. I wanted to check in on [Next Steps/Decision]. Please let me know if you need any additional information from me to move forward."
    }
    template_selection = st.selectbox("Select a template", list(templates.keys()))
    template_text = st.text_area(f"{template_selection} Template", value=templates[template_selection], height=150)
    if st.button("Use This Template"):
        st.session_state["key_points_template"] = template_text
        st.rerun()

with st.expander("Email Writing Tips"):
    st.markdown("""
        <h3 style="color: #1565c0;">💡 Tips for Writing Effective Emails</h3>
        <ul style="line-height:1.7; font-size: 16px;">
            <li>✍️ <b>Be specific</b> about your purpose and desired outcome.</li>
            <li>📌 <b>List key points</b> or details for inclusion.</li>
            <li>🎭 <b>Define the tone</b> (formal, friendly, persuasive, etc.).</li>
            <li>👤 <b>Mention the recipient</b> and their role.</li>
            <li>📖 <b>Provide context</b> or background if helpful.</li>
            <li>📏 <b>Choose the right length</b> for your message.</li>
            <li>🔍 <b>Review & personalize</b> the draft before sending.</li>
            <li>🔒 <b>Avoid sensitive information</b> like passwords.</li>
        </ul>
    """, unsafe_allow_html=True)

with st.expander("Contact the Owner | Feedback & Suggestions"):
    st.markdown("""
        <h4 style="margin-top:0;">👤 App Owner</h4>
        <p><b>Name:</b> Khushbu Sharma<br>
           <b>Email:</b> <a href="mailto:khushbu.sharma7105@gmail.com">khushbu.sharma7105@gmail.com</a></p>
        <p>We welcome your feedback and suggestions! Please feel free to reach out with any issues, feature requests, or ideas.</p>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    <hr>
    <p><b>AI Email Assistant</b> &mdash; Your personal email writing tool &copy; {time.strftime('%Y')}</p>
</div>
""", unsafe_allow_html=True)
