import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="OLYMPIAN PRO 2026",
    layout="wide",
    page_icon="🏅"
)

# ---------------- OPTIONAL AI (SAFE IMPORT) ----------------
AI_ENABLED = True

try:
    import google.generativeai as genai
    GENAI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    if GENAI_API_KEY:
        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
    else:
        AI_ENABLED = False
except:
    AI_ENABLED = False

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');

.stApp { background-color: #05070A; color: #E0E0E0; }
h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #FFD700; }

.workout-card {
    background: rgba(255,255,255,0.03);
    border-radius: 15px;
    padding: 20px;
    border-left: 4px solid #FFD700;
    margin-bottom: 15px;
}

.stat-box {
    text-align: center;
    padding: 20px;
    background: #0c0c0c;
    border-radius: 15px;
    border: 1px solid #FFD700;
}

.variant-tag {
    background: #FFD700;
    color: black;
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 0.75rem;
    font-weight: bold;
}

.level-badge {
    color: #FFD700;
    border: 1px solid #FFD700;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WORKOUT DATA ----------------
WORKOUT_DATA = {
    "Chest": {
        "Bodyweight": ["Standard Pushups", "Diamond Pushups", "Wide Pushups", "Dips"],
        "Dumbbell": ["Flat DB Press", "Incline DB Press", "DB Flys", "Pullover"],
        "Barbell": ["Bench Press", "Incline Press", "Close Grip Press", "Guillotine Press"]
    },
    "Back": {
        "Bodyweight": ["Pull-ups", "Chin-ups", "Inverted Rows", "Superman Holds"],
        "Dumbbell": ["Single Arm Rows", "Renegade Rows", "Seal Rows", "DB Deadlift"],
        "Barbell": ["Deadlift", "Bent Over Rows", "Pendlay Rows", "T-Bar Rows"]
    },
    "Shoulders": {
        "Bodyweight": ["Pike Pushups", "Wall Walks", "Handstand Hold", "Hindu Pushups"],
        "Dumbbell": ["Shoulder Press", "Lateral Raises", "Front Raises", "Reverse Flys"],
        "Barbell": ["Overhead Press", "Push Press", "Upright Rows", "Shrugs"]
    },
    "Legs": {
        "Bodyweight": ["Air Squats", "Bulgarian Squats", "Lunges", "Jump Squats"],
        "Dumbbell": ["Goblet Squats", "RDL", "Step-ups", "Weighted Lunges"],
        "Barbell": ["Back Squat", "Front Squat", "RDL", "Hip Thrust"]
    },
    "Arms": {
        "Bodyweight": ["Bench Dips", "Chin-ups", "Cobra Pushups", "Towel Curls"],
        "Dumbbell": ["Alt Curls", "Hammer Curls", "Overhead Ext", "Kickbacks"],
        "Barbell": ["Barbell Curls", "EZ Curls", "Skull Crushers", "Close Grip Bench"]
    }
}

LEVEL_CONFIG = {
    "Beginner": "3 Sets • 12–15 Reps • Focus on Form",
    "Intermediate": "4 Sets • 8–12 Reps • Hypertrophy",
    "Advanced": "5 Sets • 5–8 Reps • Strength"
}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("ATHLETE PROFILE")
    weight = st.number_input("Weight (kg)", 40, 200, 75)
    level = st.select_slider("Select Rank", ["Beginner", "Intermediate", "Advanced"])

    st.divider()
    st.subheader("🤖 AI COACH")

    user_query = st.text_input("Ask about nutrition or form")

    if user_query:
        if AI_ENABLED:
            with st.spinner("Analyzing..."):
                response = model.generate_content(
                    f"You are an elite strength coach. Answer briefly for a {level} athlete: {user_query}"
                )
                st.info(response.text)
        else:
            st.warning("AI disabled. Add GEMINI_API_KEY to Streamlit secrets.")

# ---------------- MAIN UI ----------------
st.markdown("<h1>OLYMPIAN <span style='color:white'>PRO 2026</span></h1>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    target = st.selectbox("Target Muscle Group", WORKOUT_DATA.keys())
with c2:
    equip = st.radio("Equipment", ["Bodyweight", "Dumbbell", "Barbell"], horizontal=True)

st.write("---")

intensity = LEVEL_CONFIG[level]
exercises = WORKOUT_DATA[target][equip]

left, right = st.columns([1, 1])

with left:
    st.markdown(f"""
    <div class='stat-box'>
        <span class='level-badge'>{level.upper()}</span>
        <h2>{equip.upper()} PROTOCOL</h2>
        <p>{intensity}</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.subheader("Training Sequence")
    for ex in exercises:
        st.markdown(f"""
        <div class='workout-card'>
            <span class='variant-tag'>{equip}</span><br>
            <b>{ex}</b><br>
            <small>{intensity}</small>
        </div>
        """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center style='color:#555;font-size:0.8rem'>
<b>OLYMPIAN AI LABS © 2026</b><br>
Precision Engineering for Human Performance
</center>
""", unsafe_allow_html=True)
