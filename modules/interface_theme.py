import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        .main {
            background: radial-gradient(circle at top right, #1a1c2c, #0d0e14);
            color: #ffffff;
        }
        
        /* Contenedores Glassmorphism */
        div[data-testid="stVerticalBlock"] > div.element-container:has(div.upload-container) {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        }
        
        /* Botones Premium con Neón */
        .stButton>button {
            background: linear-gradient(135deg, #7b2ff7 0%, #2196f3 100%);
            border: none;
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 4px 15px rgba(123, 47, 247, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(123, 47, 247, 0.6), 0 0 10px rgba(33, 150, 243, 0.4);
        }
        
        /* Títulos y Subtítulos */
        h1 {
            background: -webkit-linear-gradient(#fff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 3rem !important;
            text-align: center;
            margin-bottom: 0.5rem !important;
        }
        
        h3 {
            color: #7b2ff7 !important;
            font-weight: 600 !important;
            border-left: 4px solid #2196f3;
            padding-left: 15px;
            margin-top: 20px !important;
        }
        
        /* Inputs Estilizados */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #7b2ff7 !important;
            box-shadow: 0 0 10px rgba(123, 47, 247, 0.2) !important;
        }
        
        /* Estilo para las zonas de carga */
        .upload-text {
            color: #888;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
