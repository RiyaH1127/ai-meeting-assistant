import imageio_ffmpeg as ffmpeg

# set ffmpeg path for whisper
import os
os.environ["PATH"] += os.pathsep + ffmpeg.get_ffmpeg_exe()
import streamlit as st
import whisper
import os

# FFmpeg path
os.environ["PATH"] += r";C:\Users\Jaya\Downloads\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin"

st.title("🎙️ AI Meeting Assistant")

# Upload file
audio_file = st.file_uploader("Upload Meeting Audio", type=["wav", "mp3"])

if audio_file:
    with open("temp.wav", "wb") as f:
        f.write(audio_file.read())

    st.write("Processing... ⏳")

    # Load model
    model = whisper.load_model("base")

    # Transcribe
    result = model.transcribe("temp.wav")
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