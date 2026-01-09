import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OLYMPIAN PRO 2026",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- AI SAFE INIT ----------------
AI_ENABLED = True
try:
    import google.generativeai as genai
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
    else:
        AI_ENABLED = False
except Exception:
    AI_ENABLED = False

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("workout_history", [])
st.session_state.setdefault("chat_history", [])

# ---------------- STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;700&display=swap');

.stApp {
    background: #0f172a;
    color: #f8fafc;
}
h1,h2,h3 { font-family: Orbitron; letter-spacing:2px; }
.gold { color:#fbbf24; text-shadow:0 0 15px rgba(251,191,36,.4); }

.card {
    background: rgba(30,41,59,.75);
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(251,191,36,.2);
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WORKOUT DB ----------------
WORKOUT_DB = {
    "Chest": {
        "Bodyweight": ["Pushups", "Diamond Pushups"],
        "Dumbbell": ["DB Bench", "DB Fly"],
        "Barbell": ["Bench Press", "Incline Press"]
    },
    "Back": {
        "Bodyweight": ["Pullups", "Inverted Rows"],
        "Dumbbell": ["DB Rows", "Renegade Rows"],
        "Barbell": ["Deadlift", "Barbell Row"]
    },
    "Legs": {
        "Bodyweight": ["Squats", "Lunges"],
        "Dumbbell": ["Goblet Squats", "DB RDL"],
        "Barbell": ["Back Squat", "Front Squat"]
    },
    "Shoulders": {
        "Bodyweight": ["Pike Pushups"],
        "Dumbbell": ["Arnold Press", "Laterals"],
        "Barbell": ["Overhead Press"]
    }
}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<h2 class='gold'>BIOMETRIC HUB</h2>", unsafe_allow_html=True)

    height = st.number_input("Height (cm)", 140, 220, 175)
    weight = st.number_input("Weight (kg)", 35.0, 200.0, 75.0)

    bmi = weight / ((height / 100) ** 2)
    st.metric("BMI", f"{bmi:.1f}")

    goal = st.selectbox("Training Goal", ["Fat Loss", "Muscle Gain", "Strength", "Endurance"])

    if st.button("RESET ALL DATA"):
        st.session_state.workout_history.clear()
        st.session_state.chat_history.clear()
        st.rerun()

# ---------------- MAIN UI ----------------
st.markdown("<h1 class='gold' style='text-align:center'>OLYMPIAN PRO 2026</h1>", unsafe_allow_html=True)

tab_train, tab_stats, tab_ai = st.tabs(["🏋️ TRAINING", "📊 ANALYTICS", "🧠 AI COACH"])

# ---------------- TRAINING TAB ----------------
with tab_train:
    col1, col2 = st.columns([1,1.3])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        muscle = st.selectbox("Muscle Group", WORKOUT_DB.keys())
        equip = st.radio("Equipment", ["Bodyweight","Dumbbell","Barbell"], horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for ex in WORKOUT_DB[muscle][equip]:
            with st.expander(ex):
                s = st.number_input("Sets", 0, 10, key=f"s{ex}")
                r = st.number_input("Reps", 0, 50, key=f"r{ex}")
                w = st.number_input("Weight", 0, 500, key=f"w{ex}")
                if st.button(f"LOG {ex}", key=f"log{ex}"):
                    vol = s * r * w
                    st.session_state.workout_history.append({
                        "time": datetime.now().strftime("%H:%M"),
                        "exercise": ex,
                        "volume": vol
                    })
                    st.toast(f"{ex} logged")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if not st.session_state.workout_history:
            st.info("No workout data logged yet.")
        else:
            for h in st.session_state.workout_history[-5:][::-1]:
                st.write(f"🕒 {h['time']} | {h['exercise']} | {h['volume']} kg")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYTICS TAB ----------------
with tab_stats:
    if not st.session_state.workout_history:
        st.warning("Log workouts to see analytics.")
    else:
        df = pd.DataFrame(st.session_state.workout_history)
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=df["volume"],
            mode="lines+markers",
            line=dict(color="#fbbf24", width=4)
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cbd5f5",
            height=320
        )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Total Volume", int(df["volume"].sum()))
        st.metric("Max Set", int(df["volume"].max()))

# ---------------- AI TAB ----------------
with tab_ai:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.caption(f"BMI {bmi:.1f} | Goal: {goal}")

    q = st.chat_input("Ask about training, nutrition, recovery...")
    if q:
        st.chat_message("user").write(q)
        if AI_ENABLED:
            try:
                with st.spinner("Thinking like an Olympian..."):
                    res = model.generate_content(
                        f"Athlete BMI {bmi:.1f}, Goal {goal}. Answer professionally: {q}"
                    )
                st.chat_message("assistant").write(res.text)
            except Exception:
                st.error("AI temporarily unavailable.")
        else:
            st.warning("AI disabled. Add GEMINI_API_KEY.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center style='color:#64748b'>
OLYMPIAN PRO 2026 • VERSION 4.2.1 • BUILT FOR ELITE PERFORMANCE
</center>
""", unsafe_allow_html=True)
