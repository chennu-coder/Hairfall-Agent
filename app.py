import streamlit as st
from agent.ai_agent import setup_gemini, analyze_with_ai
from agent.chat_agent import setup_model, chat_with_memory
from memory.memory import load_memory, save_memory, update_profile, add_chat

st.set_page_config(page_title="AI Hair Doctor", layout="centered")

st.title("💇‍♂️ AI Hair Doctor (with Memory)")

# Load memory
memory = load_memory()

# API Key
api_key = st.text_input("AIzaSyAMmQHUJN7EKqa31tnMTYtaw9hBHILzCBw", type="password")

# --- USER PROFILE ---
st.subheader("🧾 Your Profile")

age = st.slider("Age", 15, 60, 25)
gender = st.selectbox("Gender", ["Male", "Female"])
hair_fall = st.selectbox("Hair Fall Severity", ["Low", "Medium", "High"])
diet = st.selectbox("Diet Type", ["Healthy", "Average", "Junk"])
sleep = st.slider("Sleep Hours", 3, 10, 6)
stress = st.slider("Stress Level (1-10)", 1, 10, 5)
water = st.slider("Water Intake (Liters/day)", 0, 5, 2)
dandruff = st.selectbox("Dandruff", ["No", "Yes"])

if st.button("Save Profile"):
    user_data = {
        "age": age,
        "gender": gender,
        "hair_fall": hair_fall,
        "diet": diet,
        "sleep": sleep,
        "stress": stress,
        "water": water,
        "dandruff": dandruff
    }
    update_profile(memory, user_data)
    st.success("Profile saved!")

# --- ANALYSIS ---
if st.button("Analyze Hair Health"):
    if not api_key:
        st.error("Enter API Key")
    else:
        model = setup_gemini(api_key)
        result = analyze_with_ai(model, memory["profile"])

        st.subheader("📊 Analysis")
        st.metric("Risk Score", f"{result['risk_score']}%")
        st.write(result)

# --- CHAT ---
st.subheader("💬 Ask Hair Doctor")

user_input = st.text_input("Ask your question...")

if st.button("Send"):
    if not api_key:
        st.error("Enter API Key")
    else:
        model = setup_model(api_key)
        response = chat_with_memory(model, memory, user_input)

        add_chat(memory, user_input, response)

        st.write("🤖 AI Doctor:")
        st.write(response)

# --- CHAT HISTORY ---
st.subheader("📜 Chat History")

for chat in memory["history"][-5:]:
    st.write(f"🧑: {chat['user']}")
    st.write(f"🤖: {chat['ai']}")
    st.write("---")