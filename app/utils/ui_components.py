"""
UI Components for the HydroAI Streamlit Application

This module contains reusable UI components and theme settings for the HydroAI application.
"""
import streamlit as st

def apply_theme():
    """Applies the custom theme and styles to the Streamlit app."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #60a5fa;
            --accent-hover: #3b82f6;
            --border: #334155;
            --card-bg: #1e293b;
            --card-hover: #2d3748;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --chart-bg: #1e293b;
            --elevation-1: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --elevation-2: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --elevation-3: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
        }

        .stApp {
            background: var(--bg-primary);
            color: var(--text-color);
            transition: all 0.3s ease;
        }
        
        .main-header {
            background: #1e293b;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #334155;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .main-title {
            font-family: 'Inter', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.5px;
        }
        
        @keyframes titleGlow {
            from { filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.8)); }
            to { filter: drop-shadow(0 0 20px rgba(123, 104, 238, 0.8)); }
        }
        
        .subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: var(--text-secondary);
            margin: 0;
            font-weight: 400;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: var(--elevation-1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-hover));
            opacity: 0.8;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--elevation-3);
            border-color: var(--accent);
            background: rgba(255, 255, 255, 0.05);
        }
        
        .metric-value {
            font-family: 'Inter', sans-serif;
            font-size: 2rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
            margin: 0;
        }

        .stChatMessage {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid #334155;
            border-radius: 12px;
            margin: 0.75rem 0;
            padding: 1.25rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stChatMessage::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(to bottom, var(--accent), var(--accent-hover));
            opacity: 0.8;
        }

        /* Form Elements */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>div>div,
        .stNumberInput>div>div>input,
        .stDateInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: var(--text-primary) !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus,
        .stSelectbox>div>div>div>div:focus,
        .stNumberInput>div>div>input:focus,
        .stDateInput>div>div>input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
            outline: none !important;
        }

        .stSelectbox>div>div>div>div {
            background-color: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            border: 1px solid #334155;
            border-radius: 8px;
        }

        .stMultiSelect>div>div>div>div>span {
            background-color: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            border: 1px solid #334155;
            border-radius: 8px;
        }

        /* Plotly background */
        .js-plotly-plot .plotly .main-svg {
            background: var(--chart-bg) !important;
        }
        .js-plotly-plot .plotly .plotly-svg {
            background: var(--chart-paper) !important;
        }

        .stDataFrame {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border: 1px solid #334155;
            box-shadow: var(--card-shadow);
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #1e293b;
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Creates the main header component with material design elements."""
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span class="material-icons" style="font-size: 2.5rem; margin-right: 1rem; color: var(--accent);">water_drop</span>
            <h1 class="main-title">HydroAI</h1>
        </div>
        <p class="subtitle">Advanced Groundwater Intelligence & Predictive Analytics</p>
        <div style="margin-top: 1.5rem; display: flex; gap: 1rem; justify-content: center;">
            <span class="material-icons" style="color: var(--success);">check_circle</span>
            <span class="material-icons" style="color: var(--info);">insights</span>
            <span class="material-icons" style="color: var(--warning);">warning</span>
            <span class="material-icons" style="color: var(--error);">error</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_header():
    """Creates the sidebar header with material design elements."""
    st.sidebar.markdown("""
    <div style="text-align: left; padding: 1.25rem 1.25rem 0.75rem 1.25rem; border-bottom: 1px solid var(--border);">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span class="material-icons" style="color: var(--accent);">tune</span>
            <h3 style="font-family: 'Inter', sans-serif; color: #f8fafc; font-weight: 600; margin: 0; font-size: 1.1rem;">
                Control Panel
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(title: str, value: str, delta: str = None, icon: str = None, trend: str = None):
    """Creates a material design metric card component.
    
    Args:
        title: The title of the metric
        value: The value to display
        delta: Optional delta value to show change
        icon: Optional Material Icon name
        trend: Optional trend direction ('up' or 'down')
    """
    # Create a clean container for the metric card
    container = st.container()
    
    # Apply custom CSS for the metric card
    container.markdown("""
    <style>
        .metric-card {
            background: var(--background-color);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            height: 100%;
        }
        .metric-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the card content
    with container:
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            # Add icon if provided
            if icon:
                st.markdown(f"""
                <div style="font-size: 2rem; color: var(--accent); margin-bottom: 0.5rem;">
                    <span class="material-icons">{icon}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Display the title
            st.markdown(f"""
            <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;">
                {title}
            </div>
            """, unsafe_allow_html=True)
            
            # Display the value with trend icon if provided
            cols = st.columns([1, 1, 1])
            with cols[1]:
                if trend == 'up':
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span>{value}</span>
                        <span class="material-icons" style="color: var(--success);">trending_up</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif trend == 'down':
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span>{value}</span>
                        <span class="material-icons" style="color: var(--error);">trending_down</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        {value}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display delta if provided
            if delta:
                st.markdown(f"""
                <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
                    {delta}
                </div>
                """, unsafe_allow_html=True)

def loading_spinner(text: str = "Loading..."):
    """Creates a loading spinner with a message.
    
    Args:
        text: The text to display below the spinner
    """
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; padding: 2rem;">
        <div style="display: inline-flex; flex-direction: column; align-items: center;">
            <div class="material-icons" style="font-size: 2.5rem; color: var(--accent); animation: spin 1s linear infinite;">
                autorenew
            </div>
            <p style="margin-top: 1rem; color: var(--text-secondary);">{text}</p>
        </div>
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """, unsafe_allow_html=True)
    return st.empty()

def info_card(title: str, content: str, icon: str = "info"):
    """Creates a material design info card.
    
    Args:
        title: Card title
        content: Card content
        icon: Material Icon name
    """
    st.markdown(f"""
    <div style="background: rgba(96, 165, 250, 0.1); border-left: 4px solid var(--accent); border-radius: 8px; padding: 1.25rem; margin: 1rem 0;">
        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
            <span class="material-icons" style="color: var(--accent); margin-top: 2px;">{icon}</span>
            <div>
                <div style="font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary);">{title}</div>
                <div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.5;">{content}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
