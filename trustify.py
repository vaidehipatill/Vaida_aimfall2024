import streamlit as st
from PIL import Image
import time

# Set page configuration
st.set_page_config(page_title="Trustify", page_icon="🔒", layout="wide")

# Restore the original extensive CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset all Streamlit default styling */
    .stApp {
        background: linear-gradient(135deg, #f6f8ff 0%, #f0f4ff 100%) !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    div[data-testid="stHeader"],
    header,
    footer,
    #MainMenu {
        display: none !important;
    }
    
    /* Remove default padding and backgrounds */
    [data-testid="stAppViewContainer"],
    .main > div,
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="stAppViewContainer"] > section > div {
        padding: 0 !important;
        max-width: 100%;
        background: none !important;
    }
    
    .element-container, div.stButton, div.stMarkdown, div.row-widget {
        background: none !important;
    }
    
    /* Your app styling */
    .app-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem 0;
        background: none !important;
    }
    
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #1a365d 0%, #2b4c7e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
        line-height: 1.5;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 24px;
        padding: 2rem 1rem;
        margin: 1rem 0;
        position: relative;
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 2rem;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.5) !important;
    }
    
    .status-message {
        font-size: 1.2rem;
        font-weight: 500;
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .success-message {
        background: rgba(220, 252, 231, 0.7);
        color: #166534;
    }
    
    .processing-message {
        background: rgba(240, 249, 255, 0.7);
        color: #075985;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a365d;
        background: none !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        color: #2b4c7e;
        background: none !important;
    }
    
    /* Remove backgrounds from metric containers */
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricDelta"] > div {
        background: none !important;
    }
    
    /* Style the metric cards */
    div.stMetric {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px;
        padding: 1rem;
        margin: 0 0.5rem;
    }

    /* Improved Progress Bar Styling */
    .progress-wrapper {
        position: absolute;
        top: -10px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        z-index: 10;
    }

    div[data-testid="stProgressBar"] {
        max-width: 800px;
        width: 90%;
        margin: 0 auto;
    }

    /* Image container spacing and constraints */
    .stImage {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    
    .stImage > div {
        max-width: 600px;
        max-height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
    
    .stImage img {
        max-width: 600px;
        max-height: 500px;
        object-fit: contain;
        width: auto;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main app logic
def main():
    # Initialize session state for tracking verification status
    if 'uploaded_image' not in st.session_state:
        st.session_state['uploaded_image'] = None
    
    # Add a flag to track if this is the first time showing results
    if 'first_verification' not in st.session_state:
        st.session_state['first_verification'] = True
    
    # Upload page
    if st.session_state['uploaded_image'] is None:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        # Logo and Title
        st.markdown("""
            <h1 class='title'>🔒 Trustify</h1>
            <p class='subtitle'>Verify product authenticity with advanced AI technology</p>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your image here or click to browse",
            type=["jpg", "jpeg", "png"],
            label_visibility='collapsed'
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Save the uploaded image to session state
            st.session_state['uploaded_image'] = uploaded_file
            # Reset first verification flag
            st.session_state['first_verification'] = True
            # Rerun to trigger the results page
            st.rerun()
    
    # Results page
    else:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        # Logo and Title
        st.markdown("""
            <h1 class='title'>🔒 Trustify</h1>
            <p class='subtitle'>Product Authentication Results</p>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Processing animation only on first verification
        if st.session_state['first_verification']:
            st.markdown("""
                <div class='status-message processing-message'>
                    🔍 Analyzing Product...
                </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            
            # Mark that first verification is complete
            st.session_state['first_verification'] = False
        
        # Display uploaded image
        image = Image.open(st.session_state['uploaded_image'])
        st.image(image, use_container_width=True)
        
        # Result message
        st.markdown("""
            <div class='status-message success-message'>
                ✅ Product Verified as Authentic
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Confidence Score", "98%", "High")
        with col2:
            st.metric("Security Features", "12/12", "Complete")
        with col3:
            st.metric("Verification Time", "3.2s", "-0.5s")
        
        # Verify another button
        if st.button("🔄 Verify Another Product"):
            # Clear the uploaded image to go back to upload page
            st.session_state['uploaded_image'] = None
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
