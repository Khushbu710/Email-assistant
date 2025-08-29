import streamlit as st
import time
from email_generator import EmailGenerator

# Set page configuration
st.set_page_config(
    page_title="Email Assistant",
    page_icon="📧",
    layout="wide"
)

# Custom Banner/Header
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #2196F3 0%, #21CBF3 100%);
                padding: 2rem 1rem;
                border-radius: 18px;
                margin-bottom: 1.5rem;">
        <h1 style="color: white; margin-bottom: 0.25rem; font-size: 2.6rem;">
            📧 Email Assistant
        </h1>
        <p style="color: #f2f2f2; font-size: 1.25rem; margin-top:0;">
            Generate professional emails with the perfect tone, formatting, and content, powered by AI.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Initialize the email generator
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
    # Test connection at startup
    if "connection_tested" not in st.session_state:
        with st.spinner("Testing GROQ API connection..."):
            connection_ok, message = st.session_state.generator.test_connection()
            st.session_state.connection_tested = True
            st.session_state.connection_ok = connection_ok
            st.session_state.connection_message = message
else:
    st.session_state.connection_tested = False
    st.session_state.connection_ok = False

# Connection Status Card
if "connection_tested" in st.session_state:
    if st.session_state.connection_ok:
        st.markdown(
            f"""
            <div style="background-color:#e8f5e9; border-left:5px solid #43a047; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <span style="font-size:1.1rem;">✅ <b>Connection Status:</b> {st.session_state.connection_message}</span>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color:#fff3e0; border-left:5px solid #fb8c00; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <span style="font-size:1.1rem;">⚠️ <b>Connection Status:</b> {st.session_state.connection_message}</span>
            </div>
            """, unsafe_allow_html=True
        )
        
        if st.button("Retry Connection"):
            with st.spinner("Testing connection..."):
                connection_ok, message = st.session_state.generator.test_connection()
                st.session_state.connection_ok = connection_ok
                st.session_state.connection_message = message
                st.rerun()

# Form Section Styling (wrap form in a card)
with st.container():
    st.markdown(
        """
        <div style="background-color:#f5faff; border-radius:18px; padding:2rem; box-shadow: 0 2px 8px #e3e3e3;">
        """, unsafe_allow_html=True
    )
    # Create a form to collect email details
    with st.form("email_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            recipient = st.text_input("Recipient", placeholder="John Doe, HR Manager, etc.")
            sender = st.text_input("Your Name/Role", placeholder="Your name or role")
        
        with col2:
            purpose_options = [
                "Request Information", 
                "Job Application", 
                "Follow-up", 
                "Thank You", 
                "Proposal", 
                "Apology",
                "Introduction",
                "Meeting Request",
                "Feedback",
                "Other"
            ]
            purpose = st.selectbox("Email Purpose", purpose_options)
            
            tone_options = [
                "Professional", 
                "Friendly", 
                "Formal", 
                "Casual", 
                "Urgent", 
                "Persuasive", 
                "Apologetic"
            ]
            tone = st.selectbox("Tone", tone_options)
            
            length_options = ["Short", "Medium", "Long"]
            length = st.selectbox("Length", length_options)
        
        key_points = st.text_area(
            "Key Points to Include",
            height=150,
            placeholder="Enter the main points you want to include in your email..."
        )
        
        # Generate button
        generate_button = st.form_submit_button("Generate Email")
    st.markdown("</div>", unsafe_allow_html=True)

# Process the form submission
if generate_button:
    if not recipient or not sender or not key_points:
        st.error("Please fill in all required fields.")
    else:
        # Show progress
        progress_container = st.container()
        with progress_container:
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            progress_text.text("Generating your email...")
            progress_bar.progress(50)
            
            try:
                # Generate email
                email_content = st.session_state.generator.generate_email(
                    key_points=key_points,
                    recipient=recipient,
                    sender=sender,
                    purpose=purpose,
                    tone=tone,
                    length=length
                )
                
                progress_bar.progress(100)
                progress_text.text("Email generated successfully!")
                
                # Display the generated email in a card
                st.markdown(
                    """
                    <div style="background-color:#fffde7; border-radius:14px; padding:1.5rem; margin-top:1rem; box-shadow:0 2px 6px #f0e68c;">
                        <h3 style="margin-top:0;">Generated Email</h3>
                    """, unsafe_allow_html=True
                )
                st.code(email_content, language="")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Options for the email
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Copy to Clipboard"):
                        st.code(email_content)
                        st.success("Select the text above and press Ctrl+C/Cmd+C to copy")
                
                with col2:
                    if st.button("Improve This Email"):
                        with st.spinner("Analyzing and improving email..."):
                            suggestions = st.session_state.generator.improve_email(email_content)
                            st.subheader("Suggested Improvements")
                            st.write(suggestions)
                
            except Exception as e:
                progress_bar.progress(100)
                progress_text.empty()
                st.error(f"Error during email generation: {str(e)}")

# Sample templates
with st.expander("Need inspiration? Try a template"):
    templates = {
        "Job Application": "I am writing to apply for the [Position] role advertised on [Platform]. With my experience in [Relevant Skills], I believe I am well-suited for this position. I have attached my resume and portfolio. I am particularly interested in this role because [Reason]. I would appreciate the opportunity to discuss my application further.",
        
        "Meeting Request": "I would like to schedule a meeting to discuss [Topic]. This is important because [Reason]. I am available on [Dates/Times]. The meeting should take approximately [Duration]. Please let me know what works best for your schedule.",
        
        "Thank You": "I wanted to express my sincere gratitude for [What They Did]. Your help with [Specific Action] was invaluable and [Positive Impact]. I truly appreciate your time and support. If there's ever anything I can do to return the favor, please don't hesitate to let me know.",
        
        "Follow-up": "I am writing to follow up on [Previous Communication/Meeting]. As discussed, [Reminder of Key Points]. I wanted to check in on [Next Steps/Decision]. Please let me know if you need any additional information from me to move forward."
    }
    
    template_selection = st.selectbox("Select a template", list(templates.keys()))
    
    template_text = st.text_area(
        f"{template_selection} Template",
        value=templates[template_selection],
        height=150
    )
    
    if st.button("Use This Template"):
        st.session_state["key_points_template"] = template_text
        st.rerun()

# # Debugging tool
# with st.expander("Troubleshoot API Connection"):
#     st.markdown("""
#     ### Hugging Face API Troubleshooting
#    
#     If you're experiencing connection issues:
#    
#     1. **Check if your token is valid** - Go to [Hugging Face Settings](https://huggingface.co/settings/tokens) and verify
#     2. **Verify model availability** - The app tries multiple models until it finds one that works
#     3. **Check interface permissions** - Your Hugging Face account needs correct permissions
#    
#     Common errors:
#     - **404 Error**: Model not found - try a different model
#     - **403 Error**: Authentication issue - check your token
#     - **429 Error**: Rate limit - wait and try again later
#     """)
#    
#     st.write("Currently using model:", st.session_state.generator.model if hasattr(st.session_state.generator, "model") else "Unknown")
#    
#     if st.button("Test Different Models"):
#         model_status = {}
#         test_models = ["gpt2", "distilgpt2", "facebook/opt-125m", "EleutherAI/gpt-neo-125M"]
#        
#         for model in test_models:
#             with st.spinner(f"Testing {model}..."):
#                 success, message = st.session_state.generator._test_model(model)
#                 model_status[model] = "✅ Working" if success else f"❌ Failed ({message})"
#        
#         st.write("### Model Status")
#         for model, status in model_status.items():
#             st.write(f"**{model}**: {status}")

# Add information about the tool
with st.expander("Email Writing Tips"):
    st.markdown("""
    <div style="padding: 1rem; border-radius: 14px; background: linear-gradient(90deg, #e3f2fd 0%, #fce4ec 100%);
    box-shadow: 0 2px 10px #e0e0e0; border: 1px solid #ddd;">
        <h3 style="margin-top:0; color: #1565c0;">💡 Tips for Writing Effective Emails</h3>
        <ul style="line-height:1.7; font-size: 16px;">
            <li>✍️ <b>Be specific</b> about your purpose and desired outcome.</li>
            <li>📌 <b>List key points</b> or details for inclusion.</li>
            <li>🎭 <b>Define the tone</b> (formal, friendly, persuasive, etc.).</li>
            <li>👤 <b>Mention the recipient</b> and their role.</li>
            <li>📖 <b>Provide context</b> or background if helpful.</li>
            <li>📏 <b>Choose the right length</b> for your message.</li>
            <li>📝 <b>Ask for a subject line</b> to make it clear.</li>
            <li>🔍 <b>Review & personalize</b> the draft before sending.</li>
            <li>🔒 <b>Avoid sensitive information</b> unless necessary.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Contact the Owner Section
with st.expander("Contact the Owner | Feedback & Suggestions"):
    st.markdown("""
    <div style="background-color:#f5f5f5; border-radius:12px; border:1px solid #ccc; padding:1.25rem; box-shadow: 0 2px 6px #eee;">
        <h4 style="margin-top:0;">👤 App Owner</h4>
        <p style="font-size:1.1rem; margin-bottom:0.5rem;">
            <b>Name:</b> Khushbu Sharma<br>
            <b>Email:</b> <a href="mailto:khushbu.sharma7105@gmail.com">khushbu.sharma7105@gmail.com</a>
        </p>
        <hr>
        <p style="font-size:1.05rem;">
            We welcome your feedback and suggestions for improving this app.<br>
            Please feel free to contact the owner for any issues, feature requests, or ideas!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Add footer
st.markdown("""
<hr style="margin-top:2rem;">
<div style="text-align:center; color:#aaa; font-size: 1rem; margin-top:1rem; padding-bottom:1rem;">
    <b>Email Assistant</b> &mdash; Your personal email writing tool &copy; {year}
</div>
""".format(year=time.strftime('%Y')), unsafe_allow_html=True)
