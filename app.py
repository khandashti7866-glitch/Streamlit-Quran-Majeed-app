import streamlit as st
import json
import os

# -------------------------------
# Load Quran JSON with fallback
# -------------------------------
@st.cache_data
def load_quran():
    json_path = "quran.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.warning("❌ quran.json not found. Loading sample Surah Al-Fatihah")
        # Sample Surah for testing
        return {
            "1": {
                "name": "Al-Fatihah",
                "ayahs": {
                    "1": {
                        "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                        "english": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                        "urdu": "اللہ کے نام سے شروع جو بڑا مہربان نہایت رحم والا ہے۔"
                    },
                    "2": {
                        "arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                        "english": "All praise is due to Allah, Lord of the worlds.",
                        "urdu": "سب تعریفیں اللہ ہی کے لیے ہیں جو سارے جہان کا رب ہے۔"
                    },
                    "3": {
                        "arabic": "الرَّحْمَٰنِ الرَّحِيمِ",
                        "english": "The Entirely Merciful, the Especially Merciful.",
                        "urdu": "بڑا مہربان نہایت رحم والا۔"
                    },
                    "4": {
                        "arabic": "مَالِكِ يَوْمِ الدِّينِ",
                        "english": "Sovereign of the Day of Recompense.",
                        "urdu": "روزِ جزا کا مالک۔"
                    },
                    "5": {
                        "arabic": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                        "english": "It is You we worship and You we ask for help.",
                        "urdu": "ہم تیری ہی عبادت کرتے ہیں اور تجھ ہی سے مدد مانگتے ہیں۔"
                    },
                    "6": {
                        "arabic": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
                        "english": "Guide us to the straight path –",
                        "urdu": "ہمیں سیدھا راستہ دکھا۔"
                    },
                    "7": {
                        "arabic": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
                        "english": "The path of those upon whom You have bestowed favor, not of those who have earned Your anger, nor of those who are astray.",
                        "urdu": "ان لوگوں کا راستہ جن پر تو نے انعام کیا، نہ کہ جن پر غضب ہوا اور نہ گمراہوں کا۔"
                    }
                }
            }
        }

quran = load_quran()

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
