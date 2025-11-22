import streamlit as st
import json
import os

# -------------------------------
# Load Quran JSON with error handling
# -------------------------------
@st.cache_data
def load_quran():
    json_path = "quran.json"
    if not os.path.exists(json_path):
        st.error(f"❌ quran.json file not found in {os.getcwd()}")
        return {}  # Return empty dict if file missing
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

quran = load_quran()

if not quran:
    st.stop()  # Stop the app if JSON not loaded

# -------------------------------
# UI Settings
# -------------------------------
st.set_page_config(
    page_title="Quran Reader",
    page_icon="📖",
    layout="centered"
)

# Custom Arabic font CSS
st.markdown("""
<style>
.arabic {
    font-size: 32px;
    font-family: 'Amiri', serif;
    direction: rtl;
    text-align: center;
    line-height: 2.2;
}
.translation {
    font-size: 18px;
    text-align: center;
    padding: 10px;
}
.box {
    border: 1px solid #555;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# APP TITLE
# -------------------------------
st.title("📖 Quran Reading App")
st.subheader("Arabic • English • Urdu")

# -------------------------------
# Surah Selection
# -------------------------------
surah_numbers = list(quran.keys())
surah_selected = st.selectbox(
    "Select Surah",
    surah_numbers,
    format_func=lambda x: f"{x} – {quran[x]['name']}"
)

# Get selected surah data
surah_data = quran[surah_selected]
ayah_numbers = list(surah_data["ayahs"].keys())

# -------------------------------
# Ayah Selection
# -------------------------------
if "ayah" not in st.session_state:
    st.session_state["ayah"] = ayah_numbers[0]

ayah_selected = st.selectbox(
    "Select Ayah",
    ayah_numbers,
    index=ayah_numbers.index(st.session_state["ayah"])
)

st.session_state["ayah"] = ayah_selected

# Get ayah details
ayah = surah_data["ayahs"][ayah_selected]

# -------------------------------
# Display Ayah
# -------------------------------
st.markdown("<div class='box'>", unsafe_allow_html=True)

st.markdown(f"<p class='arabic'>{ayah['arabic']}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='translation'><b>English:</b> {ayah['english']}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='translation'><b>Urdu:</b> {ayah['urdu']}</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Previous / Next Buttons
# -------------------------------
col1, col2 = st.columns(2)
current_index = ayah_numbers.index(ayah_selected)

with col1:
    if current_index > 0 and st.button("⬅️ Previous Ayah"):
        st.session_state["ayah"] = ayah_numbers[current_index - 1]
        st.experimental_rerun()

with col2:
    if current_index < len(ayah_numbers) - 1 and st.button("Next Ayah ➡️"):
        st.session_state["ayah"] = ayah_numbers[current_index + 1]
        st.experimental_rerun()

st.write("---")
st.success("App Loaded Successfully ✓")
