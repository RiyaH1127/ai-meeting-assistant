import streamlit as st
import whisper
import os
import tempfile
import imageio_ffmpeg as ffmpeg

# ✅ Fix FFmpeg for Streamlit Cloud
os.environ["PATH"] += os.pathsep + ffmpeg.get_ffmpeg_exe()

st.title("🎙️ AI Meeting Assistant")

# Upload file
audio_file = st.file_uploader("Upload Meeting Audio", type=["wav", "mp3"])

if audio_file:
    st.write("Processing... ⏳")

    # ✅ Save uploaded file safely (IMPORTANT FIX)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe
    result = model.transcribe(temp_path)
    text = result["text"]

    # Summary
    sentences = text.split(". ")
    summary = ". ".join(sentences[:2])

    # Action items
    actions = []
    for sentence in sentences:
        s = sentence.lower()
        if "will" in s or "should" in s or "need to" in s:
            actions.append(sentence)

    # OUTPUT
    st.subheader("📄 Transcript")
    st.write(text)

    st.subheader("🧠 Summary")
    st.write(summary)

    st.subheader("✅ Action Items")
    if actions:
        for a in actions:
            st.write("-", a)
    else:
        st.write("No action items found")