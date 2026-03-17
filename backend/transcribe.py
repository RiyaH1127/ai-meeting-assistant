import whisper
import os

# FFmpeg path
os.environ["PATH"] += r";C:\Users\Jaya\Downloads\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin"

# Load model
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("data/harvard.wav")
text = result["text"]

# Split sentences
sentences = text.split(". ")

# ================= SUMMARY =================
summary = ". ".join(sentences[:2])

# ================= TOPICS =================
topics = []
keywords = ["budget", "project", "report", "meeting", "plan"]

for word in keywords:
    if word in text.lower():
        topics.append(word.capitalize())

# ================= ACTION ITEMS =================
actions = []

for sentence in sentences:
    s = sentence.lower()

    if "will" in s or "should" in s or "need to" in s:
        words = sentence.split()
        person = words[0]

        if "will" in s:
            task_part = sentence.split("will", 1)[1]
        elif "should" in s:
            task_part = sentence.split("should", 1)[1]
        elif "need to" in s:
            task_part = sentence.split("need to", 1)[1]
        else:
            task_part = sentence

        deadline = "Not specified"
        if "by" in task_part:
            parts = task_part.split("by")
            task = parts[0].strip()
            deadline = parts[1].strip()
        else:
            task = task_part.strip()

        actions.append({
            "person": person,
            "task": task,
            "deadline": deadline
        })

# ================= KEY POINTS =================
key_points = sentences[:3]

# ================= OUTPUT =================

print("\n================ 🧾 MEETING SUMMARY ================\n")

print("📌 Topics:")
if topics:
    for t in topics:
        print("-", t)
else:
    print("- General Discussion")

print("\n🧠 Summary:")
print(summary)

print("\n❗ Key Points:")
for kp in key_points:
    print("-", kp)

print("\n✅ Action Items:")
if actions:
    for a in actions:
        print(f"- {a['person']} → {a['task']} (Deadline: {a['deadline']})")
else:
    print("- No action items found")