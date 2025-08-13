import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Set page config for full width
st.set_page_config(
    page_title="AI Proposal Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Assistant configurations
ASSISTANTS = {
    "RFP Assessment": {
        "url": "https://hub.nexalab.ai/w/chat/rfpassessment-192",  
        "icon": "📋",
        "description": "Analyze and evaluate RFP requirements"
    },
    "Generate Proposal": {
        "url": "https://hub.nexalab.ai/w/chat/proposalgenerator-193",
        "icon": "📄",
        "description": "Create comprehensive proposals"
    },
    "Vendor Proposal Analysis": {
        "url": "https://hub.nexalab.ai/w/chat/vendorproposalevaluator-194",  
        "icon": "🔍",
        "description": "Compare and analyze vendor proposals"
    },
    "SOW Analysis": {
        "url": "https://hub.nexalab.ai/w/chat/sowanalysis-191",  
        "icon": "📊",
        "description": "Review and analyze statements of work"
    }
}

def main():
    # Initialize session state for selected assistant
    if "selected_assistant" not in st.session_state:
        st.session_state.selected_assistant = "RFP Assessment"
    
    # Initialize session state for iframe containers (to prevent recreation)
    if "iframes_created" not in st.session_state:
        st.session_state.iframes_created = False
    
    # Inject CSS to hide Streamlit elements and create your original layout
    st.markdown("""
    <style>
        /* Global Styles */
        html, body, .stApp {
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Sidebar Styles */
        .css-1d391kg {
            background: #1a1a2e !important;
            border-right: 2px solid #333 !important;
            width: 280px !important;
            box-shadow: 4px 0px 10px rgba(0, 0, 0, 0.2) !important;
            padding: 20px 15px;
        }
        
        /* Main Content Styling */
        .main {
            margin-left: 0 !important;
            padding: 20px 15px !important;
        }
        
        /* Sidebar Button Styles */
        div[data-testid="stButton"] > button {
            width: 100% !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px !important;
            margin: 6px 0 !important;
            font-weight: 600 !important;
            text-align: left;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Active Button */
        .active-button button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        }

        /* Iframe container styles */
        .iframe-container {
            width: 100%;
            height: 100vh;
            display: none;
            position: relative;
        }
        
        .iframe-container.active {
            display: block;
        }
        
        iframe {
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        /* Text and Header Styling */
        h2, h3 {
            color: #fff !important;
            font-size: 24px !important;
        }
        
        .active-assistant {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            border-radius: 8px;
            color: #fff;
            font-weight: 600;
        }

        .features {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            color: #ccc;
        }

    </style>
    """, unsafe_allow_html=True)
    
    # Create two-column layout
    col1, col2 = st.columns([1, 4])  # 1:4 ratio for sidebar:main
    
    with col1:
        st.markdown("""
        <div style='text-align: center; color: white; padding: 20px 0;'>
            <h2>🤖 AI Proposal Suite</h2>
            <p style='color: #888; font-size: 16px;'>Your Professional AI Assistants</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        for assistant_name, config in ASSISTANTS.items():
            if assistant_name == st.session_state.selected_assistant:
                st.markdown('<div class="active-button">', unsafe_allow_html=True)
            
            if st.button(f"{config['icon']} {assistant_name}", key=f"nav_{assistant_name}", help=config['description']):
                st.session_state.selected_assistant = assistant_name
            
            if assistant_name == st.session_state.selected_assistant:
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Active Assistant Display
        st.markdown(f"""
        <div class="active-assistant">
            Active Assistant: {ASSISTANTS[st.session_state.selected_assistant]['icon']} {st.session_state.selected_assistant}
        </div>
        """, unsafe_allow_html=True)

        # Features Section
        st.markdown("""
        <div class="features">
            <strong>Features:</strong><br>
            ✅ Chat history preserved<br>
            📁 Document uploads<br>
            🔄 Instant switching<br>
            🎯 Specialized models<br>
            💾 Persistent sessions
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create all iframe containers at once and manage their visibility
        iframe_containers_html = ""
        
        for i, (assistant_name, config) in enumerate(ASSISTANTS.items()):
            visibility_class = "active" if assistant_name == st.session_state.selected_assistant else ""
            iframe_containers_html += f"""
            <div class="iframe-container {visibility_class}" id="iframe-{i}">
                <iframe src="{config['url']}" width="100%" height="100%" frameborder="0" scrolling="yes"></iframe>
            </div>
            """
        
        st.markdown(iframe_containers_html, unsafe_allow_html=True)
        
        # Add JavaScript to handle switching between iframes
        assistant_names = list(ASSISTANTS.keys())
        selected_index = assistant_names.index(st.session_state.selected_assistant)
        
        st.markdown(f"""
        <script>
        // Function to switch iframe visibility
        function switchIframe(activeIndex) {{
            const allIframes = document.querySelectorAll('.iframe-container');
            allIframes.forEach((container, index) => {{
                if (index === activeIndex) {{
                    container.classList.add('active');
                }} else {{
                    container.classList.remove('active');
                }}
            }});
        }}
        switchIframe({selected_index});
        </script>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
