import streamlit as st
from assistant_core import fetch_weather, get_time, gpt_response, speak, recognize_speech
from streamlit.components.v1 import html

st.title("🎙️ Web AI Virtual Assistant")

mode = st.radio("Input mode:", ("Text", "Voice"))

if mode == "Text":
    user_input = st.text_input("Type your message:")
else:
    if st.button("🎤 Speak"):
        user_input = recognize_speech()
        st.write("Heard:", user_input)
    else:
        user_input = None

if user_input:
    cmd = user_input.lower()
    if "weather" in cmd:
        reply = fetch_weather()
    elif "time" in cmd or "date" in cmd:
        reply = get_time()
    elif "search" in cmd:
        query = cmd.replace("search", "").strip()
        import webbrowser
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
        reply = f"Here are the search results for '{query}'."
    else:
        reply = gpt_response(cmd)

    tts_file = speak(reply)
    st.write("**Assistant:**", reply)
    audio_html = f"""
        <audio autoplay>
          <source src="file://{tts_file}" type="audio/mp3">
        </audio>
    """
    html(audio_html)
