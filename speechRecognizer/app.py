import streamlit as st
import speech_recognition
import pyttsx3
import webbrowser


# Keep original function/variable names as in the notebook
def Speaknow(command):
    voice = pyttsx3.init()
    voice.say(command)
    voice.runAndWait()


sr = speech_recognition.Recognizer()


def recognize_speech_from_mic(energy_duration: float, timeout: float | None, phrase_time_limit: float | None):
    with speech_recognition.Microphone() as source:
        if energy_duration and energy_duration > 0:
            sr.adjust_for_ambient_noise(source, duration=energy_duration)
        audio = sr.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    text = sr.recognize_google(audio)
    return text


st.set_page_config(page_title="Speech Recognizer", page_icon="🎙️", layout="centered")


# Theming via custom CSS (attractive colors, rounded cards)
st.markdown(
    """
    <style>
      :root {
        --primary: #7C3AED; /* violet-600 */
        --primary-dark: #6D28D9; /* violet-700 */
        --accent: #10B981; /* emerald-500 */
        --bg-grad-start: #0F172A; /* slate-900 */
        --bg-grad-end: #111827; /* gray-900 */
        --card: #0B1220; /* deep */
        --muted: #9CA3AF; /* gray-400 */
        --text: #E5E7EB; /* gray-200 */
      }
      .stApp {
        background: radial-gradient(1200px 800px at 10% 10%, rgba(124,58,237,0.15), transparent 50%),
                    radial-gradient(1000px 600px at 90% 10%, rgba(16,185,129,0.12), transparent 50%),
                    linear-gradient(180deg, var(--bg-grad-start), var(--bg-grad-end));
        color: var(--text);
      }
      .app-title {
        font-weight: 800; font-size: 2.2rem; line-height: 1.2; margin-bottom: .25rem;
        background: linear-gradient(90deg, var(--text), #C4B5FD, var(--accent));
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }
      .subtitle { color: var(--muted); margin-bottom: 1.25rem; }
      .card {
        border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
        border-radius: 16px; padding: 18px; margin: 8px 0 16px 0;
      }
      .pill {
        display:inline-flex; align-items:center; gap:.5rem; padding: .35rem .65rem; border-radius:999px;
        background: rgba(124,58,237,0.12); color:#C4B5FD; border:1px solid rgba(124,58,237,0.35);
        font-size:.82rem; font-weight:600; letter-spacing:.02em;
      }
      .primary-btn button {
        background: var(--primary) !important; border:1px solid var(--primary-dark) !important; color:white !important;
      }
      .secondary-btn button { background: transparent !important; border:1px solid rgba(255,255,255,0.18) !important; }
      .success { color: var(--accent); }
      .danger { color: #F87171; }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='pill'>🎙️ Real‑time Speech Recognition</div>", unsafe_allow_html=True)
st.markdown("<div class='app-title'>Talk to your app 🗣️</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Press listen, speak your phrase, see the transcript, and let the app talk back.</div>", unsafe_allow_html=True)


with st.sidebar:
    st.header("🖥️⚙️Settings")
    energy_duration = st.slider("Noise calibration duration (s)", 0.0, 3.0, 1.0, 0.25)
    timeout = st.slider("Listen timeout (s)", 0.0, 10.0, 3.0, 0.5)
    phrase_time_limit = st.slider("Phrase time limit (s)", 0.0, 15.0, 6.0, 0.5)
    speak_back = st.toggle("Speak back the recognized text", value=True)
    st.caption("Tip: Increase calibration if you are in a noisy room.")


if "⏳history" not in st.session_state:
    st.session_state.history = []


col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Microphone🎤")
    listen = st.button("Start listening", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Transcript🌐")
    transcript_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)


error_box = st.empty()


if listen:
    try:
        with st.spinner("🎧Listening..."):
            recognized_text = recognize_speech_from_mic(
                energy_duration=energy_duration,
                timeout=timeout if timeout > 0 else None,
                phrase_time_limit=phrase_time_limit if phrase_time_limit > 0 else None,
            )
        transcript_placeholder.success(f"You said: {recognized_text}")
        st.session_state.history.append(recognized_text)
        if speak_back and recognized_text:
            Speaknow(recognized_text)
    except speech_recognition.WaitTimeoutError:
        error_box.error("Listening timed out. Try increasing timeout or speak sooner.")
    except speech_recognition.UnknownValueError:
        error_box.error("Sorry, I could not understand the audio.")
    except speech_recognition.RequestError as e:
        error_box.error(f"Speech service error: {e}")
    except Exception as e:
        error_box.error(f"Unexpected error: {e}")


st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("✨History")
if st.session_state.history:
    for idx, item in enumerate(reversed(st.session_state.history), start=1):
        st.write(f"{idx}. {item}")
else:
    st.caption("No transcripts yet.")
st.markdown("</div>", unsafe_allow_html=True)


# Optional: mimic notebook's ability to open a destination via Edge
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Open in Edge by Voice")
open_btn = st.button("🌐Open in Edge (voice)", use_container_width=True)
if open_btn:
    try:
        with st.spinner("Listening for destination..."):
            destination = recognize_speech_from_mic(
                energy_duration=energy_duration,
                timeout=timeout if timeout > 0 else None,
                phrase_time_limit=phrase_time_limit if phrase_time_limit > 0 else None,
            )
        path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
        webbrowser.get(path).open(destination)
        st.success(f"Opened: {destination}")
        # Use existing function name to speak back
        Speaknow(destination)
    except speech_recognition.WaitTimeoutError:
        st.error("Listening timed out before you spoke a destination.")
    except speech_recognition.UnknownValueError:
        st.error("Could not understand the destination. Please try again.")
    except speech_recognition.RequestError as e:
        st.error(f"Speech service error: {e}")
    except Exception as e:
        st.error(f"Could not open destination: {e}")
st.markdown("</div>", unsafe_allow_html=True)


