import streamlit as st

# ---------------- IMPORTS ----------------
from utils.db import create_table, complete_chapter, get_progress
from utils.xp import calculate_xp, get_level
from utils.chapters import chapters
from utils.content import content

from utils.auth import create_user_table, register, login
from utils.quiz import quiz_data
from utils.streak import create_streak_table, update_streak, get_streak
from utils.graphs import show_progress_chart

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CIT PRO App", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;
background: linear-gradient(90deg,#6366f1,#8b5cf6);
-webkit-background-clip: text;
color: transparent;'>
🚀 CIT Learning PRO
</h1>
""", unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {background-color: #0f172a;}
.main {background-color: #0f172a;}

.card {
    background: linear-gradient(135deg, #1e293b, #334155);
    padding: 20px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    border: none;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}

h1, h2, h3 {color: white;}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
create_table()
create_user_table()
create_streak_table()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if not st.session_state.user:
    st.title("🔐 Login / Register")

    choice = st.radio("Select", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Register"):
            if register(username, password):
                st.success("Registered! Now login")
            else:
                st.error("User already exists")

    if choice == "Login":
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid login")

# ---------------- MAIN APP ----------------
else:
    user = st.session_state.user

    update_streak(user)
    streak = get_streak(user)

    st.sidebar.write(f"👤 {user}")
    st.sidebar.write(f"🔥 Streak: {streak}")

    page = st.sidebar.radio("Menu", ["Dashboard", "Chapters", "Quiz"])

    data = get_progress(user)
    xp = calculate_xp(data)
    level = get_level(xp)

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.markdown("## 🚀 Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
            <h3>🎯 Level</h3>
            <h1>{level}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
            <h3>⚡ XP</h3>
            <h1>{xp}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
            <h3>📚 Completed</h3>
            <h1>{len(data)}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📊 Progress")
        st.progress(min(xp / 500, 1.0))

        show_progress_chart(user)

    # ---------------- CHAPTERS ----------------
    elif page == "Chapters":
        st.markdown("## 📚 Chapters")

        completed = [row[2] for row in data]

        for ch in chapters:
            st.subheader(ch["name"])
            st.write(content.get(ch["name"], "Content coming soon..."))

            if ch["name"] in completed:
                st.success("✅ Completed")
            else:
                if st.button(f"Complete {ch['name']}", key=ch["name"]):
                    complete_chapter(user, ch["name"], ch["xp"])
                    st.rerun()

    # ---------------- QUIZ ----------------
    elif page == "Quiz":
        st.markdown("## 🧪 Quiz")

        for ch_name, questions in quiz_data.items():
            st.subheader(ch_name)

            score = 0
            for q in questions:
                ans = st.radio(q["question"], q["options"], key=q["question"])
                if ans == q["answer"]:
                    score += 1

            if st.button(f"Submit {ch_name}"):
                st.success(f"🎉 Score: {score}/{len(questions)}")

    # ---------------- FOOTER ----------------
    st.markdown("""
    <hr style="margin-top:50px;">
    <p style='text-align:center; color:gray;'>
    ⚡ Built by Dev Hub
    </p>
    """, unsafe_allow_html=True)
