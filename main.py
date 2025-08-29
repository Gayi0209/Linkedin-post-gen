import streamlit as st
from groq import Groq


# --- App Configuration ---
st.set_page_config(
    page_title="AI Post Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh !important;
        padding: 0 !important;
    }
    
    .stApp {
        background: transparent !important;
    }
    
    .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        padding: 3rem !important;
        margin: 2rem auto !important;
        max-width: 1400px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 4rem;
        padding: 2rem 0;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .suggestion-label {
        font-size: 0.9rem;
        color: #667eea;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stSelectbox label {
        display: none !important;
    }
    
    .stTextInput > div > div > input {
        background: white !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput label {
        display: none !important;
    }
    
    .stTextArea > div > div > textarea {
        background: white !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        resize: vertical !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    .stTextArea label {
        display: none !important;
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .api-key-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .api-key-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .output-area {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        min-height: 400px;
        border: 2px dashed #cbd5e1;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .output-area.has-content {
        background: white;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .output-placeholder {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        padding: 4rem 2rem;
    }
    
    .output-placeholder .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .copy-button {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        cursor: pointer;
        opacity: 0.8;
        transition: opacity 0.3s ease;
    }
    
    .copy-button:hover {
        opacity: 1;
    }
    
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 3rem;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 3px solid #e2e8f0;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .info-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 2rem;
        text-align: center;
    }
    
    .info-card strong {
        font-weight: 600;
    }
    
    /* Hide default Streamlit elements and fix layout */
    .stDeployButton {display: none !important;}
    header[data-testid="stHeader"] {display: none !important;}
    .stMainBlockContainer {padding-top: 0 !important;}
    footer {display: none !important;}
    .stDecoration {display: none !important;}
    
    /* Fix margins and paddings */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin-top: 1rem !important;
    }
    
    /* Ensure proper spacing */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Fix container positioning */
    .main > .block-container {
        width: 100% !important;
        max-width: none !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def get_course_suggestions(post_type, api_key):
    """Generate course/topic suggestions based on post type"""
    if not api_key:
        return []
    
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Generate 5 specific course/topic suggestions for a "{post_type}" LinkedIn post for SkillSet, an IT and data science online learning platform.

        Return only the course names, one per line, without numbers or bullets. Examples:
        Advanced Python for Data Science
        Cloud Security Fundamentals
        Machine Learning with TensorFlow
        DevOps with Docker and Kubernetes
        Data Analytics with Power BI

        Post type: {post_type}
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        
        suggestions = [line.strip() for line in response.choices[0].message.content.strip().split('\n') if line.strip()]
        return suggestions[:5]  # Limit to 5 suggestions
        
    except Exception as e:
        return []

def get_customization_suggestions(post_type, api_key):
    """Generate customization suggestions based on post type"""
    if not api_key:
        return []
    
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Generate 5 specific customization/instruction suggestions for a "{post_type}" LinkedIn post for SkillSet.

        Return only the instructions, one per line, without numbers or bullets. Examples:
        Make it engaging for career changers
        Include industry statistics and trends
        Focus on practical benefits and outcomes
        Add a personal success story element
        Emphasize job market opportunities

        Post type: {post_type}
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        
        suggestions = [line.strip() for line in response.choices[0].message.content.strip().split('\n') if line.strip()]
        return suggestions[:5]  # Limit to 5 suggestions
        
    except Exception as e:
        return []

# --- Initialize Session State ---
if 'generated_post' not in st.session_state:
    st.session_state.generated_post = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'course_suggestions' not in st.session_state:
    st.session_state.course_suggestions = []
if 'customization_suggestions' not in st.session_state:
    st.session_state.customization_suggestions = []
if 'suggestions_generated_for' not in st.session_state:
    st.session_state.suggestions_generated_for = ""

# --- Hero Section ---
st.markdown("""
<div class="hero-section">
    <div class="feature-badge">✨ Powered by Advanced AI</div>
    <h1 class="hero-title">AI Post Generator</h1>
    <p class="hero-subtitle">Create compelling LinkedIn posts that engage your audience and grow your online presence</p>
</div>
""", unsafe_allow_html=True)

# --- API Key Section ---
st.markdown('<div class="api-key-section">', unsafe_allow_html=True)
st.markdown('<div class="api-key-title">🔑 API Configuration</div>', unsafe_allow_html=True)

groq_api_key = st.text_input(
    "Enter your Groq API Key", 
    type="password", 
    placeholder="gsk_...",
    help="Get your free API key from https://console.groq.com/keys",
    label_visibility="collapsed"
)

if groq_api_key:
    st.markdown('<div class="success-message">✅ API Key configured successfully!</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Main Content Grid ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Step 1
    st.markdown('<div class="section-title"><span class="step-number">1</span>Select Post Type</div>', unsafe_allow_html=True)
    post_type = st.selectbox(
        "Post Type",
        ("Course Highlight", "Company News", "Industry Trends", "Job Posting", "Success Story", "Tech Tutorial", "Career Advice"),
        label_visibility="collapsed",
        help="Choose the type of LinkedIn post you want to create"
    )
    
    # Generate suggestions when post type changes
    if st.session_state.suggestions_generated_for != post_type and groq_api_key:
        with st.spinner("Loading suggestions..."):
            st.session_state.course_suggestions = get_course_suggestions(post_type, groq_api_key)
            st.session_state.customization_suggestions = get_customization_suggestions(post_type, groq_api_key)
            st.session_state.suggestions_generated_for = post_type
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step 2
    st.markdown('<div class="section-title"><span class="step-number">2</span>Course/Topic Details</div>', unsafe_allow_html=True)
    
    # Course suggestions dropdown
    if st.session_state.course_suggestions and groq_api_key:
        st.markdown('<div class="suggestion-label">💡 Quick Suggestions:</div>', unsafe_allow_html=True)
        course_suggestion = st.selectbox(
            "Course Suggestions",
            ["Type your own..."] + st.session_state.course_suggestions,
            label_visibility="collapsed",
            key="course_suggestion_box",
            help="Select a suggestion or choose 'Type your own...' to write custom text"
        )
        
        # Set default value based on suggestion
        if course_suggestion != "Type your own...":
            default_course_value = course_suggestion
        else:
            default_course_value = ""
    else:
        default_course_value = ""
        course_suggestion = "Type your own..."
    
    course_topic_name = st.text_input(
        "Course/Topic Name",
        value=default_course_value,
        placeholder="e.g., Advanced Python for Data Science, Cloud Security Fundamentals",
        label_visibility="collapsed",
        help="Enter the main topic or course name for your post",
        key="course_input"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step 3
    st.markdown('<div class="section-title"><span class="step-number">3</span>Message Length</div>', unsafe_allow_html=True)
    
    length_options_with_details = {
        "Short": "Short (80-100 words)",
        "Medium": "Medium (120-200 words)",
        "Long": "Long (250-400 words)"
    }
    
    message_length = st.selectbox(
        "Message Length",
        options=list(length_options_with_details.keys()),
        format_func=lambda key: length_options_with_details[key],
        label_visibility="collapsed",
        help="Choose the desired length for your LinkedIn post"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step 4
    st.markdown('<div class="section-title"><span class="step-number">4</span>Customization (Optional)</div>', unsafe_allow_html=True)
    
    # Customization suggestions dropdown
    if st.session_state.customization_suggestions and groq_api_key:
        st.markdown('<div class="suggestion-label">💡 Customization Ideas:</div>', unsafe_allow_html=True)
        customization_suggestion = st.selectbox(
            "Customization Suggestions",
            ["Type your own..."] + st.session_state.customization_suggestions,
            label_visibility="collapsed",
            key="customization_suggestion_box",
            help="Select a suggestion or choose 'Type your own...' to write custom instructions"
        )
        
        # Set default value based on suggestion
        if customization_suggestion != "Type your own...":
            default_custom_value = customization_suggestion
        else:
            default_custom_value = ""
    else:
        default_custom_value = ""
        customization_suggestion = "Type your own..."
    
    specific_instructions = st.text_area(
        "Additional Instructions",
        value=default_custom_value,
        placeholder="e.g., Make it engaging for career changers, include statistics, focus on practical benefits",
        label_visibility="collapsed",
        height=100,
        help="Add any specific requirements or tone preferences",
        key="custom_input"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Generate Button
    if st.button("🚀 Generate LinkedIn Post", key="generate_btn"):
        if not groq_api_key:
            st.markdown('<div class="error-message">❌ Please enter your Groq API Key above</div>', unsafe_allow_html=True)
        elif not course_topic_name:
            st.markdown('<div class="error-message">❌ Please provide a course or topic name</div>', unsafe_allow_html=True)
        else:
            st.session_state.is_generating = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Generated LinkedIn Post</div>', unsafe_allow_html=True)

    # Output Logic
    if st.session_state.is_generating:
        st.markdown("""
        <div class="loading-animation">
            <div class="spinner"></div>
            <p style="color: #667eea; font-weight: 500;">Creating your perfect LinkedIn post...</p>
            <p style="color: #94a3b8; font-size: 0.9rem;">This may take a few seconds</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            client = Groq(api_key=groq_api_key)

            prompt = f"""
            Generate an exceptional LinkedIn post for SkillSet, a premium online learning platform specializing in IT and data science education.

            **Post Type:** {post_type}
            **Course/Topic:** {course_topic_name}
            **Message Length:** {message_length}
            **Special Instructions:** {specific_instructions}

            Create a post that:
            - Starts with an attention-grabbing hook or question
            - Uses storytelling elements when appropriate
            - Includes 2-3 relevant emojis (not excessive)
            - Has clear value proposition for the reader
            - Contains social proof or statistics when relevant
            - Ends with a strong call-to-action
            - Includes 3-5 strategic hashtags from: #elearning #ITskills #DataScience #Cybersecurity #AI #MachineLearning #CloudComputing #CareerDevelopment #TechEducation #OnlineLearning #SkillSet #SkillUp #FutureOfWork #DigitalTransformation #TechCareer

            Important:
            - Do NOT include any introduction text like "Here's a post" or "As requested".
            - The output should ONLY be the final LinkedIn post text.
            - Format the response exactly as a LinkedIn post that can be copied and pasted directly.
            """

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=1024
            )

            st.session_state.generated_post = chat_completion.choices[0].message.content
            st.session_state.is_generating = False
            st.rerun()

        except Exception as e:
            st.session_state.is_generating = False
            st.markdown(f'<div class="error-message">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

    elif st.session_state.generated_post:
        st.markdown(st.session_state.generated_post)

        if st.button("📋 Copy to Clipboard", key="copy_btn"):
            st.success("✅ Post copied! Ready to share on LinkedIn")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Generate Another", key="regenerate"):
                st.session_state.is_generating = True
                st.rerun()
        with col_b:
            if st.button("🗑️ Clear", key="clear"):
                st.session_state.generated_post = ""
                st.rerun()

    else:
        # ✅ Compact placeholder (no giant empty box anymore)
        st.markdown("""
        <div style="text-align:center; color:#94a3b8; font-size:1rem; padding:2rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">✨</div>
            <p><strong>Your generated post will appear here</strong></p>
            <p>Fill in the details and click "Generate LinkedIn Post" to create engaging content.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- Info Card ---
st.markdown("""
<div class="info-card">
    <strong>💡 Pro Tips:</strong> The best LinkedIn posts tell a story, provide value, and encourage engagement. 
    Use specific examples and include a clear call-to-action to maximize your post's impact!
</div>
""", unsafe_allow_html=True)
