import streamlit as st
import time
from email_generator import EmailGenerator

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="wide"
)

# --- CUSTOM CSS FOR PROFESSIONAL STYLING (AURORA THEME) ---
st.markdown("""
<style>
    /* Main Background & Font */
    body {
        background: linear-gradient(to right, #f0f2f6, #e6e9f0);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main content area */
    .main .block-container {
        padding: 2rem 2rem;
    }

    /* Custom Banner */
    .banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(102, 126, 234, 0.5);
    }
    .banner h1 {
        color: white;
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .banner p {
        color: #e0e7ff;
        font-size: 1.4rem;
    }

    /* Form Container */
    .form-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.08);
    }

    /* Generated Email & Suggestions Card */
    .result-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    }
    .result-card h3 {
        color: #333;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Expander styling */
    .stExpander {
        border-radius: 15px !important;
        border: 1px solid #ddd !important;
        background-color: #fafafa;
    }
    .stExpander header {
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        color: white;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px -5px rgba(102, 126, 234, 0.6);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px -5px rgba(102, 126, 234, 0.8);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 4px 15px -5px rgba(102, 126, 234, 0.6);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
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
                email_content = st.session_state.generator.generate_email(
                    key_points=key_points, recipient=recipient, sender=sender,
                    purpose=purpose, tone=tone, length=length
                )
                
                # Using session state to persist results
                st.session_state.email_content = email_content
                st.session_state.suggestions = None # Reset suggestions
                
            except Exception as e:
                st.error(f"Error during email generation: {str(e)}")

# --- DISPLAY RESULTS ---
if "email_content" in st.session_state and st.session_state.email_content:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("Generated Email")
    st.code(st.session_state.email_content, language="")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Copy to Clipboard"):
            st.code(st.session_state.email_content)
            st.success("Select the text above and press Ctrl+C/Cmd+C to copy.")
    with col2:
        if st.button("Improve This Email"):
            with st.spinner("Analyzing and suggesting improvements..."):
                suggestions = st.session_state.generator.improve_email(st.session_state.email_content)
                st.session_state.suggestions = suggestions
    st.markdown('</div>', unsafe_allow_html=True)

if "suggestions" in st.session_state and st.session_state.suggestions:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("Suggested Improvements")
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
