import streamlit as st
import time
from email_generator import EmailGenerator

# Set page configuration
st.set_page_config(
    page_title="Email Assistant",
    page_icon="📧",
    layout="wide"
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
        with st.spinner("Testing Hugging Face API connection..."):
            connection_ok, message = st.session_state.generator.test_connection()
            st.session_state.connection_tested = True
            st.session_state.connection_ok = connection_ok
            st.session_state.connection_message = message
else:
    st.session_state.connection_tested = False
    st.session_state.connection_ok = False

# Page title and description
st.title("📧 Email Assistant")
st.markdown("Generate professional emails with the perfect tone, formatting, and content.")

# Show connection status
if "connection_tested" in st.session_state:
    if st.session_state.connection_ok:
        st.success(f"✅ {st.session_state.connection_message}")
    else:
        st.warning(f"⚠️ {st.session_state.connection_message}")
        
        if st.button("Retry Connection"):
            with st.spinner("Testing connection..."):
                connection_ok, message = st.session_state.generator.test_connection()
                st.session_state.connection_ok = connection_ok
                st.session_state.connection_message = message
                st.rerun()

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
                
                # Display the generated email
                st.subheader("Generated Email")
                
                with st.container():
                    st.code(email_content, language="")
                
                # Options for the email
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Copy to Clipboard"):
                        st.code(email_content)  # This makes it easier to copy
                        st.success("Select the text above and press Ctrl+C/Cmd+C to copy")
                
                with col2:
                    if st.button("Improve This Email"):
                        with st.spinner("Analyzing and improving email..."):
                            suggestions = st.session_state.generator.improve_email(email_text)
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

# Debugging tool
with st.expander("Troubleshoot API Connection"):
    st.markdown("""
    ### Hugging Face API Troubleshooting
    
    If you're experiencing connection issues:
    
    1. **Check if your token is valid** - Go to [Hugging Face Settings](https://huggingface.co/settings/tokens) and verify
    2. **Verify model availability** - The app tries multiple models until it finds one that works
    3. **Check interface permissions** - Your Hugging Face account needs correct permissions
    
    Common errors:
    - **404 Error**: Model not found - try a different model
    - **403 Error**: Authentication issue - check your token
    - **429 Error**: Rate limit - wait and try again later
    """)
    
    st.write("Currently using model:", st.session_state.generator.model if hasattr(st.session_state.generator, "model") else "Unknown")
    
    if st.button("Test Different Models"):
        model_status = {}
        test_models = ["gpt2", "distilgpt2", "facebook/opt-125m", "EleutherAI/gpt-neo-125M"]
        
        for model in test_models:
            with st.spinner(f"Testing {model}..."):
                success, message = st.session_state.generator._test_model(model)
                model_status[model] = "✅ Working" if success else f"❌ Failed ({message})"
        
        st.write("### Model Status")
        for model, status in model_status.items():
            st.write(f"**{model}**: {status}")

# Add information about the tool
with st.expander("Email Writing Tips"):
    st.markdown("""
    ## Tips for Effective Emails
    
    ### 1. Clear Subject Line
    - Make it specific and relevant
    - Keep it under 50 characters
    
    ### 2. Professional Greeting
    - Use the recipient's name when possible
    - When unsure, use "Dear [Role/Team]"
    
    ### 3. Concise Content
    - Start with the main point or request
    - Use bullet points for multiple items
    - Keep paragraphs short (3-4 lines max)
    
    ### 4. Professional Closing
    - Include a call to action if appropriate
    - Use standard closings like "Best regards," "Sincerely," etc.
    - Include your signature with relevant contact information
    """)

# Add footer
st.markdown("---")
st.caption("Email Assistant - Your personal email writing tool")
