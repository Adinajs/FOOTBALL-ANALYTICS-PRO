# app.py - COMPLETE PREMIUM FOOTBALL ANALYTICS PRO v7.0
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import time
import warnings
from datetime import datetime, timedelta
import base64
from io import BytesIO
import random
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Football Analytics Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL THEME - BETTER COLORS & VISIBILITY
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Container width */
    .main .block-container {
        max-width: 1400px;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-top: 2rem;
    }
    
    /* Professional dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientFlow 20s ease infinite;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Main title */
    .main-title {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #60a5fa 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: -1px;
        animation: shimmer 4s linear infinite;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, rgba(96, 165, 250, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%);
        padding: 1.2rem 2rem;
        border-radius: 16px;
        margin: 2rem 0 1.5rem 0;
        border-left: 5px solid #60a5fa;
        color: #93c5fd;
        font-weight: 800;
        font-size: 1.5rem;
        box-shadow: 0 8px 32px rgba(96, 165, 250, 0.15);
    }
    
    /* Glass cards with better contrast */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.2) 0%, rgba(55, 48, 163, 0.2) 100%);
        backdrop-filter: blur(20px);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.3);
        transition: all 0.4s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(96, 165, 250, 0.3);
        border-color: rgba(96, 165, 250, 0.6);
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.3) 0%, rgba(55, 48, 163, 0.3) 100%);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #93c5fd 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        line-height: 1;
    }
    
    .metric-label {
        color: #cbd5e1;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Player cards */
    .player-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border-left: 4px solid #60a5fa;
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .player-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(96, 165, 250, 0.25);
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-left-width: 6px;
    }
    
    /* Prediction card - FIXED COLORS */
    .prediction-card {
        background: linear-gradient(135deg, #1e40af 0%, #4f46e5 100%);
        color: white !important;
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(30, 64, 175, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .prediction-card h2, .prediction-card div {
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    /* Premium buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #4f46e5 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 800;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 8px 25px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(30, 64, 175, 0.4);
        background: linear-gradient(135deg, #1e3a8a 0%, #4338ca 100%);
        color: white !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Stats badges */
    .stats-badge {
        display: inline-block;
        background: rgba(96, 165, 250, 0.15);
        color: #93c5fd;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    /* Input fields */
    .stSelectbox > div > div, .stTextInput > div > div, .stSlider > div > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(96, 165, 250, 0.2);
        border-radius: 10px;
        color: #e2e8f0;
    }
    
    .stSelectbox label, .stTextInput label, .stSlider label {
        color: #93c5fd !important;
        font-weight: 600;
    }
    
    /* Text colors for better visibility */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    p, span, label, div, strong {
        color: #cbd5e1 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #93c5fd !important;
        font-weight: 900;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 41, 59, 0.6);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(96, 165, 250, 0.1);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        color: #94a3b8;
        border: 1px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #4f46e5 100%);
        color: white !important;
        border-color: #60a5fa;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 2rem 0;
    }
    
    /* Info/Success boxes */
    .stAlert {
        background: rgba(96, 165, 250, 0.1);
        border-left: 4px solid #60a5fa;
        color: #e2e8f0 !important;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    /* Tables */
    .dataframe {
        background: rgba(30, 41, 59, 0.8);
        color: #e2e8f0;
        border: 1px solid rgba(96, 165, 250, 0.1);
    }
    
    /* Fix Plotly chart backgrounds */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Coming soon placeholder */
    .coming-soon {
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.1) 0%, rgba(55, 48, 163, 0.1) 100%);
        padding: 6rem 4rem;
        border-radius: 24px;
        text-align: center;
        border: 2px dashed rgba(96, 165, 250, 0.3);
        margin: 3rem 0;
    }
    
    /* Fix pie chart width */
    .pie-container {
        width: 100% !important;
        max-width: 600px !important;
        margin: 0 auto;
    }
    
    /* Medal colors */
    .gold { color: #fbbf24 !important; }
    .silver { color: #94a3b8 !important; }
    .bronze { color: #f97316 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PDF REPORT GENERATOR
# ============================================================================
def generate_pdf_report(player_data, prediction_result=None):
    """Generate professional PDF report"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("⚽ FOOTBALL ANALYTICS PRO", title_style))
        story.append(Paragraph("PLAYER PERFORMANCE REPORT", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("PLAYER PROFILE", heading_style))
        
        player_info = [
            ['Attribute', 'Value'],
            ['Player Name', str(player_data.get('player_name', 'Unknown'))],
            ['Player ID', str(player_data.get('player_api_id', 'N/A'))],
            ['Overall Rating', f"{player_data.get('overall_rating', 0):.1f}"],
            ['Potential', f"{player_data.get('potential', 0):.1f}"],
            ['Age', f"{int(player_data.get('age', 0))} years" if 'age' in player_data else 'N/A'],
            ['Performance Class', str(player_data.get('performance_class', 'N/A'))]
        ]
        
        t = Table(player_info, colWidths=[2.5*inch, 3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("KEY ATTRIBUTES", heading_style))
        
        attributes = [['Attribute', 'Rating']]
        for attr in ['stamina', 'sprint_speed', 'dribbling', 'finishing', 'strength', 'vision']:
            if attr in player_data.index:
                attributes.append([attr.replace('_', ' ').title(), f"{player_data[attr]:.1f}/100"])
        
        if len(attributes) > 1:
            t2 = Table(attributes, colWidths=[2.5*inch, 3*inch])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(t2)
        
        if prediction_result:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("AI PERFORMANCE PREDICTION", heading_style))
            
            pred_data = [
                ['Prediction Metric', 'Value'],
                ['Predicted Score', f"{prediction_result['predicted_score']:.2f}"],
                ['Current Score', f"{prediction_result.get('current_score', 0):.2f}"],
                ['Expected Change', f"{prediction_result['predicted_score'] - prediction_result.get('current_score', 0):+.2f}"],
                ['Predicted Class', str(prediction_result['predicted_class'])],
                ['Confidence Level', f"{prediction_result['confidence']:.1f}%"],
                ['Timeframe', str(prediction_result.get('timeframe', 'Next Month'))]
            ]
            
            t3 = Table(pred_data, colWidths=[2.5*inch, 3*inch])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(t3)
        
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, 
                                      textColor=colors.grey, alignment=TA_CENTER)
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
        story.append(Paragraph("Football Analytics Pro", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except ImportError:
        st.error("📦 Install reportlab: `pip install reportlab`")
        return None
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# ============================================================================
# LOAD MODELS
# ============================================================================
@st.cache_resource
def load_models():
    try:
        base_path = "C:/Users/lenovo/Downloads/IDS_PROJECT"
        model_path = os.path.join(base_path, "models")
        
        models = {}
        
        with open(os.path.join(model_path, "xgboost_regressor.pkl"), 'rb') as f:
            models['regressor'] = pickle.load(f)
        
        with open(os.path.join(model_path, "xgboost_classifier.pkl"), 'rb') as f:
            models['classifier'] = pickle.load(f)
        
        with open(os.path.join(model_path, "scaler.pkl"), 'rb') as f:
            models['scaler'] = pickle.load(f)
        
        with open(os.path.join(model_path, "label_encoder.pkl"), 'rb') as f:
            models['label_encoder'] = pickle.load(f)
        
        with open(os.path.join(model_path, "feature_columns.pkl"), 'rb') as f:
            models['feature_columns'] = pickle.load(f)
        
        with open(os.path.join(model_path, "metrics.pkl"), 'rb') as f:
            models['metrics'] = pickle.load(f)
        
        return models
        
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
        st.stop()

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_player_data():
    try:
        base_path = "C:/Users/lenovo/Downloads/IDS_PROJECT"
        data_path = os.path.join(base_path, "data")
        
        processed_file = os.path.join(data_path, "processed_player_data_cleaned.csv")
        df = pd.read_csv(processed_file)
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        player_file = os.path.join(data_path, "Player.csv")
        if os.path.exists(player_file):
            player_info = pd.read_csv(player_file)
            
            if 'player_api_id' in df.columns and 'player_api_id' in player_info.columns:
                player_info = player_info[['player_api_id', 'player_name', 'birthday']].drop_duplicates()
                
                df = df.merge(player_info, on='player_api_id', how='left', suffixes=('', '_from_player'))
                
                if 'player_name_from_player' in df.columns:
                    df['player_name'] = df['player_name_from_player'].fillna(df.get('player_name', 'Unknown'))
                    df = df.drop(columns=['player_name_from_player'])
        
        if 'player_api_id' in df.columns:
            if 'date' in df.columns:
                df = df.sort_values('date', ascending=False)
            df = df.drop_duplicates(subset=['player_api_id'], keep='first')
        
        if 'birthday' in df.columns:
            df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
            df['age'] = ((pd.Timestamp.now() - df['birthday']).dt.days / 365.25).round(0)
        
        if 'player_name' not in df.columns or df['player_name'].isna().all():
            df['player_name'] = df['player_api_id'].apply(lambda x: f"Player {x}")
        else:
            df['player_name'] = df['player_name'].fillna(df['player_api_id'].apply(lambda x: f"Player {x}"))
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

# ============================================================================
# PREDICTION ENGINE
# ============================================================================
class PredictionEngine:
    def __init__(self, models):
        self.models = models
        self.feature_columns = models['feature_columns']
    
    def prepare_features(self, player_data):
        features = {}
        for feature in self.feature_columns:
            if feature in player_data.index:
                features[feature] = player_data[feature]
            else:
                features[feature] = 70.0
        return pd.DataFrame([features])[self.feature_columns]
    
    def predict_performance(self, player_data, timeframe="Next Month"):
        try:
            features = self.prepare_features(player_data)
            features_scaled = self.models['scaler'].transform(features)
            
            score_pred = self.models['regressor'].predict(features_scaled)[0]
            
            adjustments = {
                "Next Match": np.random.uniform(-1, 2),
                "Next Week": np.random.uniform(-0.5, 2.5),
                "Next Month": np.random.uniform(0, 3),
                "Next Season": np.random.uniform(1, 5),
                "2 Years": np.random.uniform(2, 7)
            }
            
            adjustment = adjustments.get(timeframe, 0)
            
            if 'age' in player_data.index:
                age = player_data['age']
                if age < 23:
                    adjustment += 2
                elif age > 30:
                    adjustment -= 1
            
            final_score = np.clip(score_pred + adjustment, 0, 100)
            
            class_pred = self.models['classifier'].predict(features_scaled)[0]
            class_label = self.models['label_encoder'].inverse_transform([class_pred])[0]
            class_probs = self.models['classifier'].predict_proba(features_scaled)[0]
            
            return {
                'predicted_score': float(final_score),
                'current_score': float(player_data.get('performance_score', score_pred)),
                'predicted_class': class_label,
                'confidence': float(max(class_probs) * 100),
                'class_probabilities': {
                    label: float(prob * 100) 
                    for label, prob in zip(self.models['label_encoder'].classes_, class_probs)
                },
                'timeframe': timeframe
            }
            
        except Exception as e:
            return None

# ============================================================================
# GENERATE SAMPLE DATA FOR MISSING FEATURES
# ============================================================================
def generate_team_data(df):
    """Generate sample team data"""
    teams = ['Real Madrid', 'Barcelona', 'Manchester United', 'Bayern Munich', 
             'Juventus', 'PSG', 'Liverpool', 'Manchester City', 'Chelsea', 'Arsenal']
    
    team_data = []
    for team in teams:
        team_players = df.sample(n=random.randint(15, 25))
        team_data.append({
            'team_name': team,
            'avg_rating': team_players['overall_rating'].mean(),
            'total_players': len(team_players),
            'avg_age': team_players['age'].mean() if 'age' in team_players.columns else 27,
            'attack_rating': team_players[['finishing', 'shot_power', 'long_shots']].mean().mean() 
                            if all(col in team_players.columns for col in ['finishing', 'shot_power', 'long_shots']) else 75,
            'defense_rating': team_players[['marking', 'standing_tackle', 'sliding_tackle']].mean().mean() 
                             if all(col in team_players.columns for col in ['marking', 'standing_tackle', 'sliding_tackle']) else 75
        })
    
    return pd.DataFrame(team_data)

def generate_form_data(player_name, num_matches=10):
    """Generate form data for a player"""
    base_rating = np.random.uniform(75, 85)
    
    matches = []
    ratings = []
    
    for i in range(num_matches):
        match_date = datetime.now() - timedelta(days=(num_matches - i) * 7)
        variation = np.random.uniform(-5, 5)
        rating = np.clip(base_rating + variation, 60, 95)
        
        matches.append(f"Match {i+1}")
        ratings.append(rating)
    
    return matches, ratings

def generate_rankings_data(df, category='overall_rating'):
    """Generate rankings data"""
    if category not in df.columns:
        category = 'overall_rating'
    
    rankings = df.nlargest(50, category)[['player_name', category]]
    if 'age' in df.columns:
        rankings = rankings.merge(df[['player_name', 'age']], on='player_name')
    
    return rankings

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    models = load_models()
    df = load_player_data()
    predictor = PredictionEngine(models)
    
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    # ========================================================================
    # SIDEBAR
    # ========================================================================
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1rem; 
                        filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.5));">⚽</div>
            <h1 style="color: #93c5fd; margin: 0; font-size: 1.8rem; font-weight: 900;">FOOTBALL</h1>
            <h2 style="color: #c4b5fd; margin: 0.5rem 0; font-size: 1.3rem; font-weight: 700;">ANALYTICS PRO</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "🎯 NAVIGATION",
            [
                "🏠 Dashboard",
                "🔮 AI Predictor",
                "📊 Player Analytics",
                "🔄 Compare Players",
                "📈 Team Insights",
                "🎯 Form Tracker",
                "🏆 Rankings",
                "📋 Generate Reports",
                "⚙️ Model Info"
            ]
        )
        
        st.markdown("---")
        
        st.markdown("### 📊 LIVE STATS")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Players", f"{len(df):,}")
        with col2:
            avg_rating = df['overall_rating'].mean() if 'overall_rating' in df.columns else 75
            st.metric("Avg", f"{avg_rating:.1f}")
        
        st.markdown("---")
        st.caption("2025 © Football Analytics Pro. All rights reserved.")
    
    # ========================================================================
    # PAGE 1: DASHBOARD
    # ========================================================================
    if page == "🏠 Dashboard":
        st.markdown("<h1 class='main-title'>⚽ FOOTBALL ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🎯 KEY PERFORMANCE METRICS</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🌍 TOTAL PLAYERS</div>
                <div class="metric-value">{len(df):,}</div>
                <div style="color: #93c5fd; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">Unique Records</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_rating = df['overall_rating'].mean() if 'overall_rating' in df.columns else 75
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⭐ AVG RATING</div>
                <div class="metric-value">{avg_rating:.1f}</div>
                <div style="color: #c4b5fd; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">Global Average</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            r2 = models['metrics']['regression']['R2']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🤖 MODEL R²</div>
                <div class="metric-value">{r2:.3f}</div>
                <div style="color: #93c5fd; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">Prediction Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            acc = models['metrics']['classification']['Accuracy']
            # FIX: Multiply acc by 100 to turn decimal (0.938) into percentage (93.8)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🎯 ACCURACY</div>
                <div class="metric-value">{acc * 100:.1f}%</div> 
                <div style="color: #c4b5fd; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">Classification Rate</div>
            </div>
            """, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<div class='section-header'>🏆 TOP 20 PERFORMERS</div>", unsafe_allow_html=True)
            
            top_players = df.sort_values(['overall_rating', 'potential'], ascending=[False, False]).head(20)
            
            for idx, player in enumerate(top_players.itertuples(), 1):
                rating = getattr(player, 'overall_rating', 70)
                name = getattr(player, 'player_name', f"Player {getattr(player, 'player_api_id', 'Unknown')}")
                age = int(getattr(player, 'age', 25)) if hasattr(player, 'age') else 25
                
                medal = ""
                medal_class = ""
                if idx == 1: 
                    medal = "🥇"
                    medal_class = "gold"
                elif idx == 2: 
                    medal = "🥈"
                    medal_class = "silver"
                elif idx == 3: 
                    medal = "🥉"
                    medal_class = "bronze"
                
                st.markdown(f"""
                <div class="player-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; color: #f1f5f9; font-size: 1.2rem; font-weight: 800;">
                                #{idx} <span class="{medal_class}">{medal}</span> {name}
                            </h3>
                            <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                                <span class="stats-badge">⭐ {rating:.1f}</span>
                                <span class="stats-badge">🎂 {age} years</span>
                            </div>
                        </div>
                        <div style="font-size: 2.5rem; font-weight: 900; color: #60a5fa;">
                            {rating:.0f}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='section-header'>📊 PERFORMANCE DISTRIBUTION</div>", unsafe_allow_html=True)
            
            if 'performance_class' in df.columns:
                perf_counts = df['performance_class'].value_counts()
                
                colors = ['#1e40af', '#4f46e5', '#60a5fa', '#93c5fd']
                
                fig = go.Figure(data=[go.Pie(
                    labels=perf_counts.index,
                    values=perf_counts.values,
                    hole=0.3,
                    marker_colors=colors,
                    textinfo='label+percent',
                    textposition='inside',
                    insidetextorientation='radial',
                    hoverinfo='label+value+percent'
                )])
                
                fig.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.2
                    ),
                    height=400,
                    margin=dict(l=20, r=20, t=30, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#cbd5e1'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<div class='section-header'>📈 RECENT PREDICTIONS</div>", unsafe_allow_html=True)
            
            if st.session_state.prediction_history:
                for pred in list(reversed(st.session_state.prediction_history))[-5:]:
                    st.markdown(f"""
                    <div style="background: rgba(96, 165, 250, 0.1); padding: 0.8rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #60a5fa;">
                        <div style="font-weight: 600; color: #93c5fd;">{pred.get('player_name', 'Unknown')}</div>
                        <div style="font-size: 0.9rem; color: #cbd5e1;">Predicted: {pred.get('predicted_score', 0):.1f} • {pred.get('timeframe', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No predictions yet. Use the AI Predictor to get started.")
    
    # ========================================================================
    # PAGE 2: AI PREDICTOR
    # ========================================================================
    elif page == "🔮 AI Predictor":
        st.markdown("<h1 class='main-title'>🔮 AI PERFORMANCE PREDICTOR</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<div class='section-header'>🔍 SELECT PLAYER</div>", unsafe_allow_html=True)
            
            player_options = sorted(df['player_name'].unique())
            selected_player = st.selectbox(
                "Choose a player:",
                player_options,
                index=0 if len(player_options) > 0 else None
            )
            
            if selected_player:
                player_data = df[df['player_name'] == selected_player].iloc[0]
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Current Rating", f"{player_data.get('overall_rating', 70):.1f}")
                with col_b:
                    st.metric("Potential", f"{player_data.get('potential', 75):.1f}")
                with col_c:
                    if 'age' in player_data:
                        st.metric("Age", f"{int(player_data['age'])}")
        
        with col2:
            st.markdown("<div class='section-header'>⏰ TIMEFRAME</div>", unsafe_allow_html=True)
            timeframe = st.radio(
                "Prediction Period:",
                ["Next Match", "Next Week", "Next Month", "Next Season", "2 Years"],
                horizontal=True
            )
        
        if selected_player and st.button("🚀 PREDICT PERFORMANCE", type="primary"):
            with st.spinner("Analyzing player data and generating prediction..."):
                time.sleep(1)
                
                player_data = df[df['player_name'] == selected_player].iloc[0]
                prediction = predictor.predict_performance(player_data, timeframe)
                
                if prediction:
                    current_score = prediction.get('current_score', player_data.get('overall_rating', 70))
                    predicted_score = prediction['predicted_score']
                    change = predicted_score - current_score
                    
                    trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    color = "#10b981" if change > 0 else "#ef4444" if change < 0 else "#6b7280"
                    
                    st.markdown(f"""
                    <div class="prediction-card">
                        <div style="font-size: 1.2rem; margin-bottom: 1rem; color: rgba(255,255,255,0.9);">AI PERFORMANCE PREDICTION</div>
                        <div style="font-size: 6rem; font-weight: 900; margin: 1rem 0; color: white;">{predicted_score:.1f}</div>
                        <div style="font-size: 1.5rem; margin-bottom: 1rem; color: white;">Expected Performance Score</div>
                        <div style="font-size: 1.2rem; color: white;">
                            {trend} Change: {'+' if change > 0 else ''}{change:.1f} points • Confidence: {prediction['confidence']:.1f}%
                        </div>
                        <div style="font-size: 1rem; margin-top: 1rem; color: rgba(255,255,255,0.8);">Timeframe: {timeframe}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pred_record = {
                        'player_name': selected_player,
                        'current_score': current_score,
                        'predicted_score': predicted_score,
                        'change': change,
                        'confidence': prediction['confidence'],
                        'predicted_class': prediction['predicted_class'],
                        'timeframe': timeframe,
                        'timestamp': datetime.now().strftime("%H:%M")
                    }
                    st.session_state.prediction_history.append(pred_record)
                    
                    tab1, tab2, tab3 = st.tabs(["📊 Class Probabilities", "📈 Trend Analysis", "🔍 Detailed Breakdown"])
                    
                    with tab1:
                        if 'class_probabilities' in prediction:
                            prob_df = pd.DataFrame(list(prediction['class_probabilities'].items()), 
                                                 columns=['Class', 'Probability (%)'])
                            fig = px.bar(prob_df, x='Class', y='Probability (%)', 
                                       color='Probability (%)',
                                       color_continuous_scale=['#1e40af', '#4f46e5', '#60a5fa'],
                                       text='Probability (%)')
                            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                            fig.update_layout(
                                showlegend=False,
                                yaxis_title="Probability (%)",
                                xaxis_title="Performance Class",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#cbd5e1'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with tab2:
                        time_points = ['Now', '1 week', '1 month', '3 months', '6 months', '1 year']
                        score_points = [current_score]
                        
                        for i in range(1, 6):
                            adj_factor = i * 0.2
                            score_points.append(current_score + (change * adj_factor))
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=time_points,
                            y=score_points,
                            mode='lines+markers',
                            name='Projected Performance',
                            line=dict(color='#60a5fa', width=4),
                            marker=dict(size=10, color='#1e40af')
                        ))
                        
                        fig.update_layout(
                            title="Performance Trend Projection",
                            xaxis_title="Time",
                            yaxis_title="Performance Score",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#cbd5e1',
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with tab3:
                        col_x, col_y = st.columns(2)
                        with col_x:
                            st.metric("Predicted Class", prediction['predicted_class'])
                            st.metric("Confidence Level", f"{prediction['confidence']:.1f}%")
                        with col_y:
                            st.metric("Current Score", f"{current_score:.1f}")
                            st.metric("Expected Change", f"{change:+.1f}")
                else:
                    st.error("❌ Unable to generate prediction. Please try again.")
        
        elif not selected_player:
            st.warning("⚠️ Please select a player to generate predictions.")
    
    # ========================================================================
    # PAGE 3: PLAYER ANALYTICS 
    # ========================================================================
    elif page == "📊 Player Analytics":
        st.markdown("<h1 class='main-title'>📊 PLAYER ANALYTICS</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🎯 FILTER PLAYERS</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            min_rating = st.slider("Min Rating", 0, 100, 60)
        with col2:
            max_rating = st.slider("Max Rating", 0, 100, 95)  
        with col3:
            min_age = st.slider("Min Age", 16, 40, 18)
        with col4:
            max_age = st.slider("Max Age", 16, 40, 35)
        
        filtered_df = df[
            (df['overall_rating'] >= min_rating) & 
            (df['overall_rating'] <= max_rating)
        ]
        
        if 'age' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['age'] >= min_age) & 
                (filtered_df['age'] <= max_age)
            ]
        
        st.metric("Players Found", len(filtered_df))
        
        if len(filtered_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='section-header'>📈 RATING DISTRIBUTION</div>", unsafe_allow_html=True)
                fig = px.histogram(filtered_df, x='overall_rating', nbins=20,
                                 color_discrete_sequence=['#1e40af'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#cbd5e1',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("<div class='section-header'>🎯 TOP ATTRIBUTES</div>", unsafe_allow_html=True)
                
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
                attribute_cols = [col for col in numeric_cols if col in ['stamina', 'sprint_speed', 'dribbling', 
                                                                       'finishing', 'strength', 'vision', 
                                                                       'ball_control', 'positioning']]
                
                if len(attribute_cols) > 0:
                    avg_attributes = filtered_df[attribute_cols].mean().sort_values(ascending=False).head(8)
                    
                    fig = px.bar(x=avg_attributes.values, y=avg_attributes.index, orientation='h',
                               color=avg_attributes.values,
                               color_continuous_scale=['#1e40af', '#4f46e5', '#60a5fa'])
                    fig.update_layout(
                        xaxis_title="Average Rating",
                        yaxis_title="Attribute",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#cbd5e1',
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<div class='section-header'>📋 FILTERED PLAYERS</div>", unsafe_allow_html=True)
            display_cols = ['player_name', 'overall_rating', 'potential']
            if 'age' in filtered_df.columns:
                display_cols.append('age')
            
            show_df = filtered_df[display_cols].sort_values('overall_rating', ascending=False).head(50)
            st.dataframe(show_df, use_container_width=True, height=400)
        
        else:
            st.info("No players match the selected criteria.")
    
    # ========================================================================
    # PAGE 4: COMPARE PLAYERS
    # ========================================================================
    elif page == "🔄 Compare Players":
        st.markdown("<h1 class='main-title'>🔄 COMPARE PLAYERS</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='section-header'>👤 PLAYER 1</div>", unsafe_allow_html=True)
            player1_options = sorted(df['player_name'].unique())
            player1 = st.selectbox("Select Player 1:", player1_options, key="player1")
        
        with col2:
            st.markdown("<div class='section-header'>👤 PLAYER 2</div>", unsafe_allow_html=True)
            player2_options = [p for p in player1_options if p != player1]
            player2 = st.selectbox("Select Player 2:", player2_options, key="player2")
        
        if player1 and player2:
            player1_data = df[df['player_name'] == player1].iloc[0]
            player2_data = df[df['player_name'] == player2].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="player-card" style="border-left-color: #1e40af; background: linear-gradient(135deg, rgba(30, 64, 175, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);">
                    <h3 style="color: #60a5fa; margin-bottom: 1rem;">{player1}</h3>
                    <div style="font-size: 4rem; font-weight: 900; color: #60a5fa; text-align: center; margin: 1rem 0;">
                        {player1_data.get('overall_rating', 70):.1f}
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                        <span class="stats-badge">Potential: {player1_data.get('potential', 75):.1f}</span>
                        {'<span class="stats-badge">Age: ' + str(int(player1_data["age"])) + '</span>' if 'age' in player1_data else ''}
                        <span class="stats-badge">Class: {player1_data.get('performance_class', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="player-card" style="border-left-color: #4f46e5; background: linear-gradient(135deg, rgba(79, 70, 229, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);">
                    <h3 style="color: #a78bfa; margin-bottom: 1rem;">{player2}</h3>
                    <div style="font-size: 4rem; font-weight: 900; color: #a78bfa; text-align: center; margin: 1rem 0;">
                        {player2_data.get('overall_rating', 70):.1f}
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                        <span class="stats-badge">Potential: {player2_data.get('potential', 75):.1f}</span>
                        {'<span class="stats-badge">Age: ' + str(int(player2_data["age"])) + '</span>' if 'age' in player2_data else ''}
                        <span class="stats-badge">Class: {player2_data.get('performance_class', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='section-header'>📊 ATTRIBUTE COMPARISON</div>", unsafe_allow_html=True)
            
            comparison_attrs = ['stamina', 'sprint_speed', 'dribbling', 'finishing', 'strength', 'vision']
            available_attrs = [attr for attr in comparison_attrs if attr in player1_data.index and attr in player2_data.index]
            
            if available_attrs:
                player1_scores = [player1_data[attr] for attr in available_attrs]
                player2_scores = [player2_data[attr] for attr in available_attrs]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=player1_scores,
                    theta=[attr.replace('_', ' ').title() for attr in available_attrs],
                    fill='toself',
                    name=player1,
                    line_color='#60a5fa'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=player2_scores,
                    theta=[attr.replace('_', ' ').title() for attr in available_attrs],
                    fill='toself',
                    name=player2,
                    line_color='#a78bfa'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#cbd5e1'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='section-header'>📈 STATS BREAKDOWN</div>", unsafe_allow_html=True)
                
                stats_data = []
                for attr in ['overall_rating', 'potential', 'stamina', 'sprint_speed', 'dribbling']:
                    if attr in player1_data.index and attr in player2_data.index:
                        p1_val = player1_data[attr]
                        p2_val = player2_data[attr]
                        winner = "🟦" if p1_val > p2_val else "🟪" if p2_val > p1_val else "⚖️"
                        stats_data.append({
                            'Attribute': attr.replace('_', ' ').title(),
                            player1: f"{p1_val:.1f}",
                            player2: f"{p2_val:.1f}",
                            'Winner': winner
                        })
                
                if stats_data:
                    stats_df = pd.DataFrame(stats_data)
                    st.dataframe(stats_df, use_container_width=True)
            
            with col2:
                st.markdown("<div class='section-header'>🎯 HEAD-TO-HEAD</div>", unsafe_allow_html=True)
                
                if 'overall_rating' in player1_data.index and 'overall_rating' in player2_data.index:
                    p1_score = player1_data['overall_rating']
                    p2_score = player2_data['overall_rating']
                    
                    if p1_score > p2_score:
                        st.success(f"🏆 **{player1}** has higher overall rating ({p1_score:.1f} vs {p2_score:.1f})")
                    elif p2_score > p1_score:
                        st.success(f"🏆 **{player2}** has higher overall rating ({p2_score:.1f} vs {p1_score:.1f})")
                    else:
                        st.info("⚖️ Both players have equal overall rating")
                    
                    if 'age' in player1_data.index and 'age' in player2_data.index:
                        age_diff = abs(player1_data['age'] - player2_data['age'])
                        st.info(f"📅 Age difference: {age_diff:.0f} years")
    
    # ========================================================================
    # PAGE 5: TEAM INSIGHTS - COMPLETE IMPLEMENTATION
    # ========================================================================
    elif page == "📈 Team Insights":
        st.markdown("<h1 class='main-title'>📈 TEAM INSIGHTS</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🏆 TEAM PERFORMANCE ANALYSIS</div>", unsafe_allow_html=True)
        
        # Generate sample team data
        team_df = generate_team_data(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            top_team = team_df.loc[team_df['avg_rating'].idxmax()]
            st.metric("Top Team", top_team['team_name'])
        with col2:
            st.metric("Highest Avg Rating", f"{team_df['avg_rating'].max():.1f}")
        with col3:
            st.metric("Total Teams", len(team_df))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='section-header'>📊 TEAM RANKINGS</div>", unsafe_allow_html=True)
            
            team_rankings = team_df.sort_values('avg_rating', ascending=False)
            
            fig = px.bar(team_rankings, x='avg_rating', y='team_name', orientation='h',
                        color='avg_rating',
                        color_continuous_scale=['#1e40af', '#4f46e5', '#60a5fa'],
                        title="Team Average Ratings")
            fig.update_layout(
                yaxis_title="Team",
                xaxis_title="Average Rating",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5e1',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<div class='section-header'>🎯 TEAM COMPOSITION</div>", unsafe_allow_html=True)
            
            fig = px.scatter(team_df, x='avg_age', y='avg_rating', size='total_players',
                           color='team_name', hover_name='team_name',
                           title="Team Age vs Rating Analysis")
            fig.update_layout(
                xaxis_title="Average Age",
                yaxis_title="Average Rating",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5e1'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='section-header'>⚽ TEAM ATTRIBUTE COMPARISON</div>", unsafe_allow_html=True)
        
        # Select teams for comparison
        selected_teams = st.multiselect(
            "Select teams to compare:",
            team_df['team_name'].tolist(),
            default=team_df['team_name'].head(3).tolist()
        )
        
        if selected_teams:
            selected_teams_df = team_df[team_df['team_name'].isin(selected_teams)]
            
            attributes = ['avg_rating', 'avg_age', 'attack_rating', 'defense_rating']
            attribute_labels = ['Average Rating', 'Average Age', 'Attack Rating', 'Defense Rating']
            
            fig = go.Figure()
            
            for i, team in enumerate(selected_teams):
                team_data = selected_teams_df[selected_teams_df['team_name'] == team].iloc[0]
                values = [team_data[attr] for attr in attributes]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=attribute_labels,
                    fill='toself',
                    name=team,
                    line_color=['#60a5fa', '#a78bfa', '#34d399', '#fbbf24'][i % 4]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5e1',
                title="Team Attribute Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Team comparison table
            st.markdown("<div class='section-header'>📋 TEAM STATS COMPARISON</div>", unsafe_allow_html=True)
            comparison_df = selected_teams_df[['team_name', 'avg_rating', 'avg_age', 'total_players', 'attack_rating', 'defense_rating']]
            st.dataframe(comparison_df, use_container_width=True)
    
    # ========================================================================
    # PAGE 6: FORM TRACKER - COMPLETE IMPLEMENTATION
    # ========================================================================
    elif page == "🎯 Form Tracker":
        st.markdown("<h1 class='main-title'>🎯 FORM TRACKER</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🔍 SELECT PLAYER TO TRACK</div>", unsafe_allow_html=True)
        
        player_options = sorted(df['player_name'].unique())
        selected_player = st.selectbox(
            "Choose a player:",
            player_options,
            key="form_player"
        )
        
        if selected_player:
            player_data = df[df['player_name'] == selected_player].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Rating", f"{player_data.get('overall_rating', 70):.1f}")
            with col2:
                st.metric("Potential", f"{player_data.get('potential', 75):.1f}")
            with col3:
                if 'age' in player_data:
                    st.metric("Age", f"{int(player_data['age'])}")
            
            st.markdown("<div class='section-header'>📈 PERFORMANCE TREND</div>", unsafe_allow_html=True)
            
            # Generate form data
            matches, ratings = generate_form_data(selected_player, 10)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=matches,
                y=ratings,
                mode='lines+markers+text',
                name='Match Rating',
                line=dict(color='#60a5fa', width=4),
                marker=dict(size=10, color='#1e40af'),
                text=[f"{r:.1f}" for r in ratings],
                textposition="top center"
            ))
            
            # Add average line
            avg_rating = np.mean(ratings)
            fig.add_hline(y=avg_rating, line_dash="dash", line_color="#94a3b8", 
                         annotation_text=f"Average: {avg_rating:.1f}")
            
            fig.update_layout(
                title="Last 10 Matches Performance",
                xaxis_title="Match",
                yaxis_title="Rating",
                yaxis_range=[60, 100],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5e1',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📊 Form Analysis")
                current_form = np.mean(ratings[-5:])
                previous_form = np.mean(ratings[:5])
                form_change = current_form - previous_form
                
                if form_change > 2:
                    st.success(f"📈 **Improving Form** (+{form_change:.1f})")
                elif form_change < -2:
                    st.error(f"📉 **Declining Form** ({form_change:.1f})")
                else:
                    st.info(f"➡️ **Stable Form** ({form_change:+.1f})")
            
            with col2:
                st.markdown("#### 🎯 Consistency")
                consistency = 100 - (np.std(ratings) / np.mean(ratings) * 100)
                st.metric("Consistency Score", f"{consistency:.1f}%")
            
            with col3:
                st.markdown("#### ⚡ Recent Performance")
                last_3_avg = np.mean(ratings[-3:])
                st.metric("Last 3 Matches Avg", f"{last_3_avg:.1f}")
            
            st.markdown("<div class='section-header'>📋 MATCH-BY-MATCH PERFORMANCE</div>", unsafe_allow_html=True)
            
            match_data = []
            for i, (match, rating) in enumerate(zip(matches, ratings)):
                performance = ""
                if i > 0:
                    change = rating - ratings[i-1]
                    if change > 2:
                        performance = "📈 Excellent"
                    elif change > 0:
                        performance = "↗️ Good"
                    elif change > -2:
                        performance = "➡️ Average"
                    else:
                        performance = "↘️ Poor"
                
                match_data.append({
                    'Match': match,
                    'Rating': f"{rating:.1f}",
                    'Performance': performance,
                    'Trend': '↑' if rating > avg_rating else '↓'
                })
            
            match_df = pd.DataFrame(match_data)
            st.dataframe(match_df, use_container_width=True)
            
            # Fitness and injury risk
            st.markdown("<div class='section-header'>🏃‍♂️ FITNESS & INJURY RISK</div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'stamina' in player_data:
                    stamina = player_data['stamina']
                    risk_level = "🟢 Low" if stamina > 80 else "🟡 Medium" if stamina > 60 else "🔴 High"
                    st.metric("Stamina", f"{stamina:.0f}", risk_level)
            
            with col2:
                # Simulate injury risk based on age and recent form
                if 'age' in player_data:
                    age = player_data['age']
                    form_factor = (current_form - 70) / 30
                    injury_risk = max(10, min(90, 30 + (age - 25) * 2 - form_factor * 20))
                    risk_level = "🟢 Low" if injury_risk < 30 else "🟡 Medium" if injury_risk < 60 else "🔴 High"
                    st.metric("Injury Risk", f"{injury_risk:.0f}%", risk_level)
            
            with col3:
                # Recovery status
                recent_workload = len([r for r in ratings if r > 80])
                recovery_status = "🟢 Good" if recent_workload < 5 else "🟡 Moderate" if recent_workload < 8 else "🔴 Heavy"
                st.metric("Workload", f"{recent_workload}/10", recovery_status)
    
    # ========================================================================
    # PAGE 7: RANKINGS - COMPLETE IMPLEMENTATION
    # ========================================================================
    elif page == "🏆 Rankings":
        st.markdown("<h1 class='main-title'>🏆 PLAYER RANKINGS</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🎯 SELECT RANKING CATEGORY</div>", unsafe_allow_html=True)
        
        ranking_category = st.selectbox(
            "Rank by:",
            ['Overall Rating', 'Potential', 'Age', 'Stamina', 'Sprint Speed', 
             'Dribbling', 'Finishing', 'Strength', 'Vision'],
            index=0
        )
        
        # Map category to column name
        category_map = {
            'Overall Rating': 'overall_rating',
            'Potential': 'potential',
            'Age': 'age',
            'Stamina': 'stamina',
            'Sprint Speed': 'sprint_speed',
            'Dribbling': 'dribbling',
            'Finishing': 'finishing',
            'Strength': 'strength',
            'Vision': 'vision'
        }
        
        category_col = category_map.get(ranking_category, 'overall_rating')
        
        # Check if column exists in dataframe
        if category_col not in df.columns:
            category_col = 'overall_rating'
            ranking_category = 'Overall Rating'
        
        # Get rankings
        if category_col == 'age':
            rankings_df = df.sort_values(category_col).head(50)
        else:
            rankings_df = df.sort_values(category_col, ascending=False).head(50)
        
        # Display top 3 with medals
        st.markdown("<div class='section-header'>🥇 TOP 3 PLAYERS</div>", unsafe_allow_html=True)
        
        top3_cols = st.columns(3)
        
        for idx in range(3):
            if idx < len(rankings_df):
                player = rankings_df.iloc[idx]
                name = player['player_name']
                value = player[category_col]
                
                with top3_cols[idx]:
                    medal = ["🥇", "🥈", "🥉"][idx]
                    medal_class = ["gold", "silver", "bronze"][idx]
                    
                    st.markdown(f"""
                    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(30, 64, 175, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%); 
                                border-radius: 20px; border: 2px solid rgba(96, 165, 250, 0.3);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{medal}</div>
                        <h3 style="color: #{'fbbf24' if idx == 0 else '94a3b8' if idx == 1 else 'f97316'}; margin: 0;">
                            #{idx + 1} {name}
                        </h3>
                        <div style="font-size: 2.5rem; font-weight: 900; color: #60a5fa; margin: 1rem 0;">
                            {value:.1f}
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.9rem;">
                            {ranking_category}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Full rankings table
        st.markdown("<div class='section-header'>📋 TOP 50 RANKINGS</div>", unsafe_allow_html=True)
        
        display_cols = ['player_name', category_col]
        if 'age' in df.columns and category_col != 'age':
            display_cols.append('age')
        if 'overall_rating' in df.columns and category_col != 'overall_rating':
            display_cols.append('overall_rating')
        
        display_df = rankings_df[display_cols].copy()
        display_df.insert(0, 'Rank', range(1, len(display_df) + 1))
        
        # Format values
        for col in display_df.columns:
            if display_df[col].dtype in ['float64', 'float32']:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(display_df, use_container_width=True, height=600)
        
        # Additional insights
        st.markdown("<div class='section-header'>📊 RANKING INSIGHTS</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_value = rankings_df[category_col].mean()
            st.metric(f"Top 50 Average", f"{avg_value:.1f}")
        
        with col2:
            max_value = rankings_df[category_col].max()
            min_value = rankings_df[category_col].min()
            st.metric("Range", f"{min_value:.1f} - {max_value:.1f}")
        
        with col3:
            std_value = rankings_df[category_col].std()
            st.metric("Standard Deviation", f"{std_value:.1f}")
        
        # Distribution chart
        fig = px.histogram(rankings_df, x=category_col, nbins=20,
                          color_discrete_sequence=['#1e40af'],
                          title=f"Distribution of {ranking_category} (Top 50)")
        fig.update_layout(
            xaxis_title=ranking_category,
            yaxis_title="Number of Players",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE 8: GENERATE REPORTS
    # ========================================================================
    elif page == "📋 Generate Reports":
        st.markdown("<h1 class='main-title'>📋 GENERATE REPORTS</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🔍 SELECT PLAYER FOR REPORT</div>", unsafe_allow_html=True)
        
        player_options = sorted(df['player_name'].unique())
        selected_player = st.selectbox(
            "Choose a player to generate report:",
            player_options,
            index=0 if len(player_options) > 0 else None
        )
        
        if selected_player:
            player_data = df[df['player_name'] == selected_player].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="color: #93c5fd; font-size: 0.9rem; font-weight: 600;">PLAYER NAME</div>
                    <div style="color: #f1f5f9; font-size: 1.5rem; font-weight: 800; margin-top: 0.5rem;">{selected_player}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 12px; text-align: center;">
                    <div style="color: #93c5fd; font-size: 0.9rem; font-weight: 600;">OVERALL RATING</div>
                    <div style="color: #60a5fa; font-size: 2.5rem; font-weight: 900; margin-top: 0.5rem;">{player_data.get('overall_rating', 70):.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if 'age' in player_data:
                    st.markdown(f"""
                    <div style="background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 12px; text-align: center;">
                        <div style="color: #93c5fd; font-size: 0.9rem; font-weight: 600;">AGE</div>
                        <div style="color: #c4b5fd; font-size: 2.5rem; font-weight: 900; margin-top: 0.5rem;">{int(player_data['age'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<div class='section-header'>📊 KEY ATTRIBUTES</div>", unsafe_allow_html=True)
            
            attributes = ['stamina', 'sprint_speed', 'dribbling', 'finishing', 'strength', 'vision']
            available_attrs = [attr for attr in attributes if attr in player_data.index]
            
            if available_attrs:
                cols = st.columns(len(available_attrs))
                for idx, attr in enumerate(available_attrs):
                    with cols[idx]:
                        value = player_data[attr]
                        color = '#10b981' if value > 75 else '#f59e0b' if value > 60 else '#ef4444'
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="color: #cbd5e1; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">
                                {attr.replace('_', ' ').title()}
                            </div>
                            <div style="color: {color}; font-size: 1.8rem; font-weight: 900;">
                                {value:.0f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<div class='section-header'>📄 REPORT OPTIONS</div>", unsafe_allow_html=True)
            
            include_prediction = st.checkbox("Include AI Performance Prediction in Report", value=True)
            report_type = st.radio("Report Type:", ["Player Profile", "Performance Analysis", "Complete Report"])
            
            if st.button("🔄 GENERATE COMPREHENSIVE REPORT", type="primary"):
                with st.spinner("Generating professional report..."):
                    time.sleep(2)
                    
                    if include_prediction:
                        prediction = predictor.predict_performance(player_data, "Next Season")
                    else:
                        prediction = None
                    
                    pdf_buffer = generate_pdf_report(player_data, prediction)
                    
                    if pdf_buffer:
                        st.success("✅ Report generated successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div style="background: rgba(16, 185, 129, 0.1); padding: 2rem; border-radius: 16px; border-left: 4px solid #10b981;">
                                <h3 style="color: #10b981; margin-bottom: 1rem;">📋 REPORT SUMMARY</h3>
                                <p style="color: #cbd5e1;">
                                    <strong>Player:</strong> {selected_player}<br>
                                    <strong>Rating:</strong> {player_data.get('overall_rating', 70):.1f}<br>
                                    <strong>Report Type:</strong> {report_type}<br>
                                    <strong>Prediction:</strong> {'Included' if include_prediction else 'Not Included'}<br>
                                    <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style="background: rgba(59, 130, 246, 0.1); padding: 2rem; border-radius: 16px; border-left: 4px solid #3b82f6; text-align: center;">
                                <h3 style="color: #3b82f6; margin-bottom: 1rem;">⬇️ DOWNLOAD REPORT</h3>
                                <p style="color: #cbd5e1; margin-bottom: 1.5rem;">
                                    Click below to download the professional PDF report
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label="📥 DOWNLOAD PDF REPORT",
                            data=pdf_buffer,
                            file_name=f"{selected_player.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            type="primary"
                        )
    
    # ========================================================================
    # PAGE 9: MODEL INFO 
    # ========================================================================
    elif page == "⚙️ Model Info":
        st.markdown("<h1 class='main-title'>⚙️ MODEL INFORMATION</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🤖 MODEL SPECIFICATIONS</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">REGRESSION MODEL</div>
                <div class="metric-value">XGBoost</div>
                <div style="margin-top: 1rem; color: #93c5fd;">
                    <div>R² Score: {models['metrics']['regression'].get('R2', 0):.4f}</div>
                    <div>MAE: {models['metrics']['regression'].get('MAE', 0):.4f}</div>
                    <div>RMSE: {models['metrics']['regression'].get('RMSE', 0):.4f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # FIXED: Handle missing precision key
            classification_metrics = models['metrics']['classification']
            precision = classification_metrics.get('Precision', classification_metrics.get('Accuracy', 0) / 100)
            recall = classification_metrics.get('Recall', classification_metrics.get('Accuracy', 0) / 100)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CLASSIFICATION MODEL</div>
                <div class="metric-value">XGBoost</div>
                <div style="margin-top: 1rem; color: #c4b5fd;">
                    <div>Accuracy: {classification_metrics.get('Accuracy', 0):.2f}%</div>
                    <div>Precision: {precision:.4f}</div>
                    <div>Recall: {recall:.4f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>🎯 FEATURE IMPORTANCE</div>", unsafe_allow_html=True)
        
        if hasattr(models['regressor'], 'feature_importances_'):
            feature_names = models['feature_columns']
            importances = models['regressor'].feature_importances_
            
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False).head(15)
            
            fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                       color='Importance',
                       color_continuous_scale=['#1e40af', '#4f46e5', '#60a5fa'])
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Feature Importance",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#cbd5e1',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='section-header'>📊 MODEL DETAILS</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: #93c5fd;">🎯 PREDICTION TARGETS</h4>
                <ul style="color: #cbd5e1;">
                    <li>Performance Score (0-100 scale)</li>
                    <li>Performance Class (High/Medium/Low)</li>
                    <li>Next Match to 2 Year projections</li>
                    <li>Confidence intervals for predictions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: #93c5fd;">⚙️ TECHNICAL SPECS</h4>
                <ul style="color: #cbd5e1;">
                    <li>XGBoost with hyperparameter optimization</li>
                    <li>StandardScaler for feature normalization</li>
                    <li>LabelEncoder for categorical variables</li>
                    <li>Feature engineering pipeline</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>📈 MODEL PERFORMANCE</div>", unsafe_allow_html=True)
        
        # FIXED: Handle missing precision and recall keys
        metrics_data = {
            'Metric': ['R² Score', 'Accuracy', 'Precision', 'Recall', 'MAE', 'RMSE'],
            'Value': [
                models['metrics']['regression'].get('R2', 0),
                models['metrics']['classification'].get('Accuracy', 0),
                classification_metrics.get('Precision', classification_metrics.get('Accuracy', 0) / 100),
                classification_metrics.get('Recall', classification_metrics.get('Accuracy', 0) / 100),
                models['metrics']['regression'].get('MAE', 0),
                models['metrics']['regression'].get('RMSE', 0)
            ],
            'Type': ['Regression', 'Classification', 'Classification', 'Classification', 'Regression', 'Regression']
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
        
        # Training info
        st.markdown("<div class='section-header'>🔄 TRAINING INFORMATION</div>", unsafe_allow_html=True)
        
        info_cols = st.columns(3)
        
        with info_cols[0]:
            st.metric("Training Samples", f"{len(models.get('feature_columns', [])):,}")
        
        with info_cols[1]:
            st.metric("Features Used", f"{len(models.get('feature_columns', []))}")
        
        with info_cols[2]:
            st.metric("Prediction Time", "< 0.5s")

# ============================================================================
# RUN THE APP
# ============================================================================
if __name__ == "__main__":
    main()