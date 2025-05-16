import os
import streamlit as st
import requests
import geocoder
import base64
import time
from geopy.geocoders import Nominatim  # For address-to-coordinates conversion
import osf
API_BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# Function to encode images as base64
def get_base64_of_image(file_path):
    try:
        with open(file_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        st.error(f"Error encoding image: {e}")
        return None

# Streamlit page configuration
st.set_page_config(page_title="HerHealth", page_icon="assets/gynae_genius.png", layout="wide")

# Load background images
maternal_bg_base64 = get_base64_of_image("assets/maternal-bg.jpg")
hero_bg_base64 = get_base64_of_image("assets/hero-bg.jpg")

# CSS for styling with improvements
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

    /* General Styles */
    * {{
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    .stApp {{
        background-image: url("{maternal_bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
        z-index: 0;
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background: rgba(255, 245, 247, 0.75);
        z-index: -1;
    }}

    # /* Hide Streamlit Defaults */
    # [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"], 
    # [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
    #     display: none !important;
    # }}

    /* Remove White Boxes and Ensure Content Visibility */
    .stApp > div, .st-emotion-cache-1wmy9hl, .st-emotion-cache-1r4qj8v, 
    .st-emotion-cache-1v0mbdj, .st-emotion-cache-1c7zf2v, .st-emotion-cache-1gv3huu {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        z-index: 1;
        position: relative;
    }}

    /* Navigation Bar */
    .navbar {{
        background: linear-gradient(135deg, #F06292, #F8A1B1);
        backdrop-filter: blur(12px);
        padding: 20px 40px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        border-radius: 0 0 25px 25px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .navbar-brand {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .navbar-brand img {{
        height: 60px; /* Increased size of the image */
        border-radius: 50%;
        border: 2px solid #FFFFFF;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        margin-left: 20px; /* Adjusted position */
    }}
    .navbar-brand h1 {{
        color: #F06292; 
        font-size: 40px; /* Increased font size */
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }}
    .navbar-brand h1:hover {{
        transform: scale(1.05);
    }}
    .navbar-menu {{
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        align-items: center;
    }}
    .nav-item {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255, 255, 255, 0.2);
        color: #FFFFFF;
        padding: 10px 20px;
        border-radius: 30px;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        cursor: pointer;
        z-index: 2;
    }}
    .nav-item:hover, .nav-item.active {{
        background: #FFFFFF;
        color: #F06292;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }}
    .nav-icon {{
        color: #FFFFFF;
        font-size: 20px;
    }}
    .nav-item:hover .nav-icon, .nav-item.active .nav-icon {{
        color: #F06292;
    }}
    @media (max-width: 768px) {{
        .navbar {{
            padding: 15px 20px;
        }}
        .navbar-menu {{
            gap: 10px;
        }}
        .nav-item {{
            padding: 8px 15px;
            font-size: 14px;
        }}
        .navbar-brand h1 {{
            font-size: 28px;
        }}
        .navbar-brand img {{
            height: 40px;
            margin-left: 10px;
        }}
    }}

    /* Hero Section */
    .hero {{
        background-image: url("{hero_bg_base64}");
        background-size: cover;
        background-position: center;
        border-radius: 25px;
        padding: 60px;
        margin: 100px auto 30px auto;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 450px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        max-width: 1200px;
        position: relative;
        z-index: 1;
    }}
    .hero::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 25px;
        z-index: 0;
    }}
    .hero h1, .hero p, .hero button {{
        position: relative;
        z-index: 1;
    }}
    .hero h1 {{
        font-size: 60px;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6);
        background: linear-gradient(135deg, #FFFFFF, #F8A1B1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero p {{
        font-size: 24px;
        font-weight: 400;
        margin-bottom: 30px;
        max-width: 600px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    .hero-button {{
        background: linear-gradient(135deg, #F06292, #F8A1B1);
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 500;
        padding: 15px 35px;
        border: none;
        border-radius: 30px;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    .hero-button:hover {{
        background: linear-gradient(135deg, #F8A1B1, #F06292);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }}

    /* Section Title */
    .section-title {{
        color: #FFFFFF;
        font-size: 36px;
        font-weight: 600;
        text-align: center;
        margin: 40px 0;
        background: linear-gradient(135deg, #F06292, #F8A1B1);
        padding: 15px 30px;
        border-radius: 15px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        position: relative;
        z-index: 1;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }}

    /* Cards and Containers */
    .services-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }}
    .card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(252, 240, 243, 0.98));
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
        border: 1px solid #F8A1B1;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
    }}
    .card:hover {{
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        transform: translateY(-5px);
    }}
    .card img {{
        width: 60px;
        height: 60px;
        margin-bottom: 15px;
    }}
    .card h3 {{
        color: #F06292;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }}
    .card p {{
        color: #555;
        font-size: 16px;
        margin-bottom: 15px;
        flex-grow: 1;
    }}

    /* Containers */
    .weather-container, .sos-container, .monitoring-container, .janani-container {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(252, 240, 243, 0.98));
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid #F8A1B1;
        max-width: 1200px;
        margin: 20px auto;
        position: relative;
        z-index: 1;
    }}

    /* Highlight SOS Container */
    .sos-container {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 200, 200, 0.98));
        border: 4px solid #FF5252;
        box-shadow: 0 0 25px rgba(255, 82, 82, 0.7);
        animation: flash 1.5s infinite;
    }}
    @keyframes flash {{
        0% {{ border-color: #FF5252; box-shadow: 0 0 25px rgba(255, 82, 82, 0.7); }}
        50% {{ border-color: #FF8A8A; box-shadow: 0 0 35px rgba(255, 82, 82, 1); }}
        100% {{ border-color: #FF5252; box-shadow: 0 0 25px rgba(255, 82, 82, 0.7); }}
    }}
    .sos-warning {{
        background: linear-gradient(to right, #FF5252, #FF8A8A);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }}

    /* Buttons */
    .stButton>button, .sos-button {{
        background: linear-gradient(135deg, #F06292, #FBD1D5);
        color: #FFFFFF;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 10px;
        transition: all 0.3s ease;
        z-index: 2;
    }}
    .stButton>button:hover, .sos-button:hover {{
        background: linear-gradient(135deg, #FBD1D5, #F06292);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }}
    .sos-button {{
        background: linear-gradient(to right, #FF5252, #FF8A8A);
        font-size: 28px;
        font-weight: 600;
        padding: 25px 50px;
        border-radius: 50px;
        width: 90%;
        margin: 20px auto;
        display: block;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(255, 82, 82, 0.7);
        animation: pulse 1.5s infinite;
    }}
    .sos-button:hover {{
        background: linear-gradient(to right, #FF8A8A, #FF5252);
        box-shadow: 0 0 30px rgba(255, 82, 82, 1);
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}

    /* Inputs */
    .stTextInput, .stNumberInput, .stCheckbox {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}
    .stTextInput>div, .stNumberInput>div, .stCheckbox>div {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {{
        background: rgba(255, 255, 255, 1) !important;
        border: 2px solid #F06292 !important;
        border-radius: 10px;
        padding: 12px !important;
        font-size: 16px !important;
        color: #333 !important;
        width: 100% !important;
        box-sizing: border-box;
        font-weight: 500 !important;
        -webkit-text-fill-color: #333 !important;
        opacity: 1 !important;
        transition: all 0.3s ease;
    }}
    div[data-testid="stTextInput"] input:hover, div[data-testid="stNumberInput"] input:hover {{
        border-color: #F8A1B1 !important;
        box-shadow: 0 0 10px rgba(240, 98, 146, 0.3);
    }}
    div[data-testid="stTextInput"] input::placeholder, div[data-testid="stNumberInput"] input::placeholder {{
        color: #888 !important;
        opacity: 1 !important;
    }}
    .stTextInput label, .stNumberInput label, .stCheckbox label {{
        color: #F06292 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        background: transparent !important;
        padding: 0 !important;
        margin-bottom: 8px !important;
        display: block !important;
    }}
    div[data-testid="stTextInput"], div[data-testid="stNumberInput"], div[data-testid="stCheckbox"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}
    div[data-testid="stTextInput"]>div, div[data-testid="stNumberInput"]>div, div[data-testid="stCheckbox"]>div {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}
    .st-emotion-cache-1v0mbdj, .st-emotion-cache-1c7zf2v, .st-emotion-cache-1gv3huu {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }}

    /* Janani Bot */
    .janani-header {{
        background: linear-gradient(135deg, #F06292, #F8A1B1);
        color: white;
        padding: 20px;
        border-radius: 15px 15px 0 0;
        margin: -40px -40px 20px -40px;
        display: flex;
        align-items: center;
        position: relative;
        z-index: 1;
    }}
    .janani-header img {{
        width: 50px;
        height: 50px;
        margin-right: 15px;
        border-radius: 50%;
    }}
    .janani-header h2 {{
        margin: 0;
        font-size: 26px;
    }}
    .janani-messages-wrapper {{
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        position: relative;
        z-index: 1;
    }}
    .janani-message {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 12px 18px;
        border-radius: 18px;
        margin-bottom: 15px;
        max-width: 80%;
        font-size: 16px;
        animation: fadeIn 0.3s ease-in-out;
    }}
    .janani-message img {{
        width: 30px;
        height: 30px;
        border-radius: 50%;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .janani-message.assistant {{
        background-color: #F8A1B1;
        color: white;
        border-bottom-left-radius: 5px;
        margin-right: auto;
    }}
    .janani-message.human {{
        background-color: #E0E0E0;
        color: #333;
        border-bottom-right-radius: 5px;
        margin-left: auto;
    }}
    .janani-message-content {{
        display: flex;
        flex-direction: column;
        gap: 10px;
    }}
    .janani-message-content p {{
        margin: 0;
        line-height: 1.5;
    }}
    .janani-message-content ul {{
        list-style-type: none;
        padding: 0;
        margin: 10px 0;
    }}
    .janani-message-content li {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 15px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        transition: all 0.3s ease;
    }}
    .janani-message-content li:hover {{
        background: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
    }}
    .janani-message-content li i {{
        color: #F06292;
        font-size: 18px;
        margin-top: 3px;
    }}
    .janani-message-content li div {{
        flex: 1;
    }}
    .janani-message-content li strong {{
        color: #FFFFFF;
        font-weight: 600;
    }}
    .janani-message-content .signature {{
        font-style: italic;
        font-size: 14px;
        margin-top: 10px;
        text-align: right;
        color: #FFFFFF;
    }}
    .quick-replies {{
        display: flex;
        gap: 10px;
        margin-top: 10px;
        flex-wrap: wrap;
    }}
    .quick-reply {{
        background: #F06292;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
    }}
    .quick-reply:hover {{
        background: #F8A1B1;
        transform: scale(1.05);
    }}

    /* Health Monitor, Fetal Health, SOS, Weather */
    .monitoring-title, .sos-title, .weather-title {{
        color: #F06292;
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 20px;
        text-align: center;
    }}
    .predict-button, .weather-button {{
        background: linear-gradient(135deg, #F06292, #F8A1B1);
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 500;
        padding: 15px 40px;
        border: none;
        border-radius: 30px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: block;
        margin: 20px auto;
    }}
    .predict-button:hover, .weather-button:hover {{
        background: linear-gradient(135deg, #F8A1B1, #F06292);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }}
    .result-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(252, 240, 243, 0.98));
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        border: 2px solid #F8A1B1;
        display: flex;
        align-items: center;
        gap: 15px;
        position: relative;
        z-index: 1;
    }}
    .result-card img {{
        width: 40px;
        height: 40px;
    }}
    .result-card h4 {{
        color: #F06292;
        font-size: 20px;
        font-weight: 600;
        margin: 0;
    }}
    .result-card p {{
        color: #555;
        font-size: 16px;
        margin: 5px 0 0 0;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 30px;
        color: #555;
        font-size: 16px;
        background: rgba(255, 255, 255, 0.98);
        border-top: 3px solid #F8A1B1;
        margin-top: 50px;
        border-radius: 20px 20px 0 0;
        position: relative;
        z-index: 1;
    }}
    </style>
""", unsafe_allow_html=True)

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation with Font Awesome icons
nav_items = {
    "home": ("Home", "fas fa-home"),
    "services": ("Services", "fas fa-cogs"),
    "weather": ("Weather", "fas fa-sun"),
    "sos": ("SOS", "fas fa-siren"),
    "janani_bot": ("Janani Bot", "fas fa-comment"),
    "health_monitor": ("Health Monitor", "fas fa-heartbeat"),
    "fetal_health": ("Fetal Health", "fas fa-baby")
}

# Navigation Bar
st.markdown('<div class="navbar"><div class="navbar-brand">', unsafe_allow_html=True)
st.image("assets/gynae_genius.png", width=60)  # Adjusted width to match CSS
st.markdown('<h1>HerHealth</h1></div><div class="navbar-menu">', unsafe_allow_html=True)

# Use columns to layout the navbar items
cols = st.columns(len(nav_items))
for i, (page_id, (page_name, icon_class)) in enumerate(nav_items.items()):
    with cols[i]:
        nav_html = f'<div class="nav-item {"active" if st.session_state.page == page_id else ""}" id="nav-{page_id}"><i class="{icon_class} nav-icon"></i> {page_name}</div>'
        if st.session_state.page != page_id:
            if st.button(page_name, key=f"nav_{page_id}", help=f"Navigate to {page_name}", use_container_width=True):
                st.session_state.page = page_id
                st.rerun()
            st.markdown(
                f"""
                <style>
                #nav-{page_id} {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 3;
                }}
                </style>
                {nav_html}
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(nav_html, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Main Content
with st.container():
    if st.session_state.page == "home":
        st.markdown("""
            <div class="hero">
                <h1>Welcome to HerHealth</h1>
                <p>Your trusted companion for maternal care, offering advanced monitoring, 24/7 support, and emergency services.</p>
                <button class="hero-button">Get Started</button>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-title">Explore Our Features</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="card">
                    <img src="https://img.icons8.com/ios-filled/50/F06292/chat.png" alt="Chat Icon">
                    <h3>Chat with Janani</h3>
                    <p>Ask anything about maternal health with our AI assistant.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Chat Now", key="home_janani"):
                st.session_state.page = "janani_bot"
                st.rerun()
        with col2:
            st.markdown("""
                <div class="card">
                    <img src="https://img.icons8.com/ios-filled/50/F06292/heart-monitor.png" alt="Health Icon">
                    <h3>Health Monitoring</h3>
                    <p>Track your vital signs in real-time.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Monitor Health", key="home_health"):
                st.session_state.page = "health_monitor"
                st.rerun()
        with col3:
            st.markdown("""
                <div class="card">
                    <img src="https://img.icons8.com/ios-filled/50/F06292/baby.png" alt="Fetal Icon">
                    <h3>Fetal Health</h3>
                    <p>Ensure your baby's well-being with advanced predictions.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Check Fetal Health", key="home_fetal"):
                st.session_state.page = "fetal_health"
                st.rerun()

    elif st.session_state.page == "services":
        st.markdown('<div class="section-title">Our Services</div>', unsafe_allow_html=True)
        st.markdown('<div class="services-grid">', unsafe_allow_html=True)
        st.markdown("""
            <div class="card">
                <img src="https://img.icons8.com/ios-filled/50/F06292/heart-monitor.png" alt="Health Icon">
                <h3>Health Monitoring</h3>
                <p>Track vital signs in real-time to ensure your well-being during pregnancy.</p>
            </div>
            <div class="card">
                <img src="https://img.icons8.com/ios-filled/50/F06292/alarm.png" alt="Alert Icon">
                <h3>Emergency Alerts</h3>
                <p>Instant SOS notifications to get help when you need it most.</p>
            </div>
            <div class="card">
                <img src="https://img.icons8.com/ios-filled/50/F06292/headset.png" alt="Support Icon">
                <h3>24/7 Support</h3>
                <p>Expert help available anytime to answer your questions.</p>
            </div>
            <div class="card">
                <img src="https://img.icons8.com/ios-filled/50/F06292/baby.png" alt="Fetal Icon">
                <h3>Fetal Health</h3>
                <p>Advanced fetal monitoring to keep your baby safe and healthy.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "weather":
        st.markdown('<div class="section-title">Weather Update</div>', unsafe_allow_html=True)
        st.markdown('<div class="weather-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="weather-title">Check Weather Conditions</h3>', unsafe_allow_html=True)
        city = st.text_input("Enter your city", placeholder="e.g., Mumbai", key="weather_input")
        if st.button("Get Weather", key="weather_button"):
            if city:
                api_key = os.getenv("OPENWEATHER_API_KEY", "ec7375ca788a1ea63ea37b54733f4241")
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                try:
                    response = requests.get(weather_url)
                    response.raise_for_status()
                    data = response.json()
                    weather = data["weather"][0]["description"].title()
                    temp = data["main"]["temp"]
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/F06292/sun.png" alt="Weather Icon">
                            <div>
                                <h4>Weather in {city}</h4>
                                <p>{weather}, {temp}°C</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                            <div>
                                <h4>Error</h4>
                                <p>Unable to fetch weather data: {str(e)}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "sos":
        st.markdown('<div class="section-title">SOS Emergency</div>', unsafe_allow_html=True)
        st.markdown('<div class="sos-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="sos-title">Emergency Help</h3>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 18px; color: #555; margin-bottom: 15px;">Press the SOS button below to send your current location to emergency contacts.</p>', unsafe_allow_html=True)
        st.markdown('<div class="sos-warning"><i class="fas fa-exclamation-triangle"></i> This will send your location to emergency contacts immediately!</div>', unsafe_allow_html=True)

        # Add a toggle for manual location input
        use_manual_location = st.checkbox("Use manual location (if detected location is inaccurate)", value=False)

        if use_manual_location:
            manual_address = st.text_input("Enter your address (e.g., 123 Main St, City, Country):", key="manual_address_input")
            if manual_address:
                try:
                    geolocator = Nominatim(user_agent="herhealth_app")
                    location = geolocator.geocode(manual_address)
                    if location:
                        st.markdown(f"""
                            <div class="result-card">
                                <img src="https://img.icons8.com/ios-filled/50/F06292/location.png" alt="Location Icon">
                                <div>
                                    <h4>Manual Location Detected</h4>
                                    <p>Latitude: {location.latitude}, Longitude: {location.longitude}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        latitude = location.latitude
                        longitude = location.longitude
                    else:
                        st.markdown(f"""
                            <div class="result-card">
                                <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                                <div>
                                    <h4>Error</h4>
                                    <p>Could not find the address. Please try a different format.</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        latitude = None
                        longitude = None
                except Exception as e:
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                            <div>
                                <h4>Error</h4>
                                <p>Failed to geocode address: {str(e)}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    latitude = None
                    longitude = None
            else:
                latitude = None
                longitude = None
        else:
            # Use IP-based geolocation as a fallback (using ipinfo for better accuracy)
            g = geocoder.ipinfo('me')
            location = g.latlng
            if location:
                st.markdown(f"""
                    <div class="result-card">
                        <img src="https://img.icons8.com/ios-filled/50/F06292/location.png" alt="Location Icon">
                        <div>
                            <h4>IP-Based Location Detected</h4>
                            <p>Latitude: {location[0]}, Longitude: {location[1]}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                latitude = location[0]
                longitude = location[1]
            else:
                st.markdown(f"""
                    <div class="result-card">
                        <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                        <div>
                            <h4>Error</h4>
                            <p>Could not detect location.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                latitude = None
                longitude = None

        if st.button("SEND SOS ALERT", key="sos_button"):
            if latitude is not None and longitude is not None:
                try:
                    with st.spinner("Sending alert..."):
                        response = requests.post(f"{API_BASE_URL}/sos", json={
                            "latitude": latitude,
                            "longitude": longitude,
                            "emergency_contacts": ["+917075735181"]
                        })
                        response.raise_for_status()
                        result = response.json()
                        if result.get("simulated", False):
                            st.markdown(f"""
                                <div class="result-card">
                                    <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                                    <div>
                                        <h4>Simulation Mode</h4>
                                        <p>{result['message']}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        elif result.get("all_delivered", False):
                            st.markdown(f"""
                                <div class="result-card">
                                    <img src="https://img.icons8.com/ios-filled/50/F06292/siren.png" alt="SOS Icon">
                                    <div>
                                        <h4>SOS Alert Sent</h4>
                                        <p>Alert sent and delivered successfully!</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="result-card">
                                    <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                                    <div>
                                        <h4>Delivery Failed</h4>
                                        <p>Alert sent but not delivered to all contacts. Check logs for details.</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                            <div>
                                <h4>Error</h4>
                                <p>Failed to send SOS alert: {str(e)}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-card">
                        <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                        <div>
                            <h4>Error</h4>
                            <p>Please provide a valid location before sending the SOS alert.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "janani_bot":
        st.markdown('<div class="section-title">Janani Bot</div>', unsafe_allow_html=True)
        st.markdown('<div class="janani-container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="janani-header">
                <img src="https://img.icons8.com/color/48/000000/chatbot.png" alt="Janani Bot">
                <h2>Janani - Your Maternal Health Assistant</h2>
            </div>
            <div class="janani-messages-wrapper" id="chat-container">
        """, unsafe_allow_html=True)
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Janani, your maternal health assistant. How can I help you today?"}]
        
        for message in st.session_state.messages:
            message_class = "assistant" if message["role"] == "assistant" else "human"
            avatar = "https://img.icons8.com/color/48/000000/chatbot.png" if message["role"] == "assistant" else "https://img.icons8.com/ios-filled/50/000000/user.png"
            
            # Format the response for "What are common health problems?" specifically
            if message["content"].startswith("Dear patient, as a maternal health assistant"):
                formatted_content = """
                <div class="janani-message-content">
                    <p>Dear patient, as a maternal health assistant, I'm here to help you understand some of the common health problems that women might face during pregnancy and post-pregnancy. Here are some conditions:</p>
                    <ul>
                        <li>
                            <i class="fas fa-circle"></i>
                            <div>
                                <strong>Anemia:</strong> This condition occurs when the body does not have enough healthy red blood cells to carry adequate oxygen to parts of the body, which can lead to fatigue and weakness.
                            </div>
                        </li>
                        <li>
                            <i class="fas fa-circle"></i>
                            <div>
                                <strong>Gestational Diabetes:</strong> A type of diabetes that develops during pregnancy and usually disappears after giving birth. It can cause high blood sugar levels in pregnant women.
                            </div>
                        </li>
                        <li>
                            <i class="fas fa-circle"></i>
                            <div>
                                <strong>Preeclampsia:</strong> A condition that occurs after 20 weeks of pregnancy, characterized by high blood pressure and damage to organs such as the kidneys and liver.
                            </div>
                        </li>
                        <li>
                            <i class="fas fa-circle"></i>
                            <div>
                                <strong>Thyroid Disorders:</strong> Hypothyroidism (underactive thyroid) or hyperthyroidism (overactive thyroid) can affect pregnancy and postpartum health.
                            </div>
                        </li>
                    </ul>
                    <p>Please remember that every woman's experience is unique, and these conditions may not affect everyone. If you have any concerns about your health during pregnancy or post-pregnancy, it’s important to speak with a healthcare provider for guidance and support. Take care of yourself and your baby!</p>
                    <p class="signature">Sincerely,<br>Janani (Maternal Health Assistant)</p>
                </div>
                """
            else:
                formatted_content = f'<div class="janani-message-content"><p>{message["content"]}</p></div>'
            
            st.markdown(
                f'<div class="janani-message {message_class}"><img src="{avatar}" alt="Avatar">{formatted_content}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Quick replies
        st.markdown('<div class="quick-replies">', unsafe_allow_html=True)
        quick_replies = [
            "What are common pregnancy symptoms?",
            "What foods should I avoid during pregnancy?",
            "How can I manage stress during pregnancy?",
            "What are the signs of labor?"
        ]
        cols = st.columns(len(quick_replies))
        for i, reply in enumerate(quick_replies):
            with cols[i]:
                if st.button(reply, key=f"quick_reply_{i}"):
                    st.session_state.messages.append({"role": "human", "content": reply})
                    with st.spinner("Janani is thinking..."):
                        try:
                            response = requests.post(f"{API_BASE_URL}/chat", json={"question": reply})
                            response.raise_for_status()
                            answer = response.json().get("answer", "Sorry, I couldn’t process your request.")
                        except requests.exceptions.RequestException as e:
                            answer = f"Sorry, I couldn’t process your request: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Chat input and clear button
        col1, col2 = st.columns([3, 1])
        with col1:
            question = st.chat_input(
                "Ask Janani a question...",
                key="janani_input"
            )
            if question:
                st.session_state.messages.append({"role": "human", "content": question})
                with st.spinner("Janani is thinking..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/chat", json={"question": question})
                        response.raise_for_status()
                        answer = response.json().get("answer", "Sorry, I couldn’t process your request.")
                    except requests.exceptions.RequestException as e:
                        answer = f"Sorry, I couldn’t process your request: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
        with col2:
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Janani, your maternal health assistant. How can I help you today?"}]
                st.rerun()

        # Auto-scroll
        st.markdown('<script>document.getElementById("chat-container").scrollTop = document.getElementById("chat-container").scrollHeight;</script>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "health_monitor":
        st.markdown('<div class="section-title">Health Risk Predictor</div>', unsafe_allow_html=True)
        st.markdown('<div class="monitoring-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="monitoring-title">Enter Your Vital Signs</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, value=30, key="age_input")
            systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200, value=120, key="systolic_bp_input")
            diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=120, value=80, key="diastolic_bp_input")
        with col2:
            bs = st.number_input("Blood Sugar (mmol/L)", min_value=3.0, max_value=20.0, value=5.0, key="bs_input")
            body_temp = st.number_input("Body Temp (°F)", min_value=95.0, max_value=105.0, value=98.6, key="body_temp_input")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180, value=70, key="heart_rate_input")

        if st.button("Predict Health Risk", key="predict_health_button"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/predict_risk", json={
                        "age": age, "systolic_bp": systolic_bp, "diastolic_bp": diastolic_bp,
                        "bs": bs, "body_temp": body_temp, "heart_rate": heart_rate
                    })
                    response.raise_for_status()
                    result = response.json()
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/F06292/heart-monitor.png" alt="Result Icon">
                            <div>
                                <h4>Risk Level: {result['risk_level']}</h4>
                                <p><strong>Recommendations:</strong> {result['recommendations']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                            <div>
                                <h4>Error</h4>
                                <p>Failed to predict health risk: {str(e)}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "fetal_health":
        st.markdown('<div class="section-title">Fetal Health Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="monitoring-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="monitoring-title">Enter Fetal Health Parameters</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            baseline_value = st.number_input("Baseline Value (bpm)", min_value=100.0, max_value=200.0, value=120.0, key="baseline_value_input")
            accelerations = st.number_input("Accelerations", min_value=0.0, max_value=1.0, value=0.1, key="accelerations_input")
            fetal_movement = st.number_input("Fetal Movement", min_value=0.0, max_value=1.0, value=0.0, key="fetal_movement_input")
            uterine_contractions = st.number_input("Uterine Contractions", min_value=0.0, max_value=1.0, value=0.0, key="uterine_contractions_input")
            light_decelerations = st.number_input("Light Decelerations", min_value=0.0, max_value=1.0, value=0.0, key="light_decelerations_input")
            severe_decelerations = st.number_input("Severe Decelerations", min_value=0.0, max_value=1.0, value=0.0, key="severe_decelerations_input")
            prolonged_decelerations = st.number_input("Prolonged Decelerations", min_value=0.0, max_value=1.0, value=0.0, key="prolonged_decelerations_input")
        with col2:
            abnormal_short_term_variability = st.number_input("Abnormal Short-Term Variability (%)", min_value=0.0, max_value=100.0, value=0.0, key="abnormal_short_term_variability_input")
            mean_short_term = st.number_input("Mean Short-Term Variability", min_value=0.0, max_value=10.0, value=2.0, key="mean_short_term_input")
            percentage_of_time_with_abnormal_long_term_variability = st.number_input("Percentage of Time with Abnormal Long-Term Variability", min_value=0.0, max_value=100.0, value=0.0, key="percentage_of_time_with_abnormal_long_term_variability_input")
            mean_long_term = st.number_input("Mean Long-Term Variability", min_value=0.0, max_value=50.0, value=0.0, key="mean_long_term_input")
            histogram_width = st.number_input("Histogram Width", min_value=0.0, max_value=200.0, value=50.0, key="histogram_width_input")
            histogram_min = st.number_input("Histogram Min", min_value=0.0, max_value=200.0, value=50.0, key="histogram_min_input")
            histogram_max = st.number_input("Histogram Max", min_value=0.0, max_value=200.0, value=150.0, key="histogram_max_input")
            histogram_number_of_peaks = st.number_input("Histogram Number of Peaks", min_value=0.0, max_value=20.0, value=2.0, key="histogram_number_of_peaks_input")
            histogram_number_of_zeroes = st.number_input("Histogram Number of Zeroes", min_value=0.0, max_value=20.0, value=0.0, key="histogram_number_of_zeroes_input")
            histogram_mode = st.number_input("Histogram Mode", min_value=0.0, max_value=200.0, value=120.0, key="histogram_mode_input")
            histogram_mean = st.number_input("Histogram Mean", min_value=0.0, max_value=200.0, value=120.0, key="histogram_mean_input")
            histogram_median = st.number_input("Histogram Median", min_value=0.0, max_value=200.0, value=120.0, key="histogram_median_input")
            histogram_variance = st.number_input("Histogram Variance", min_value=0.0, max_value=1000.0, value=100.0, key="histogram_variance_input")
            histogram_tendency = st.number_input("Histogram Tendency", min_value=-1.0, max_value=1.0, value=0.0, key="histogram_tendency_input")

        if st.button("Predict Fetal Health", key="predict_fetal_button"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/predict_fetal_health", json={
                        "baseline_value": baseline_value,
                        "accelerations": accelerations,
                        "fetal_movement": fetal_movement,
                        "uterine_contractions": uterine_contractions,
                        "light_decelerations": light_decelerations,
                        "severe_decelerations": severe_decelerations,
                        "prolongued_decelerations": prolonged_decelerations,
                        "abnormal_short_term_variability": abnormal_short_term_variability,
                        "mean_value_of_short_term_variability": mean_short_term,
                        "percentage_of_time_with_abnormal_long_term_variability": percentage_of_time_with_abnormal_long_term_variability,
                        "mean_value_of_long_term_variability": mean_long_term,
                        "histogram_width": histogram_width,
                        "histogram_min": histogram_min,
                        "histogram_max": histogram_max,
                        "histogram_number_of_peaks": histogram_number_of_peaks,
                        "histogram_number_of_zeroes": histogram_number_of_zeroes,
                        "histogram_mode": histogram_mode,
                        "histogram_mean": histogram_mean,
                        "histogram_median": histogram_median,
                        "histogram_variance": histogram_variance,
                        "histogram_tendency": histogram_tendency
                    })
                    response.raise_for_status()
                    result = response.json()
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/F06292/baby.png" alt="Result Icon">
                            <div>
                                <h4>Fetal Health Status: {result['fetal_health']}</h4>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                        <div class="result-card">
                            <img src="https://img.icons8.com/ios-filled/50/FF5252/error.png" alt="Error Icon">
                            <div>
                                <h4>Error</h4>
                                <p>Failed to predict fetal health: {str(e)}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2025 HerHealth | Powered by GynaeGenius | All rights reserved</div>', unsafe_allow_html=True)