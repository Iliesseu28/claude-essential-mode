import asyncio
import os
import edge_tts

VOICE = "en-US-ChristopherNeural"

SCRIPT = [
    {
        "id": "scene1",
        "text": "Tired of bloated AI responses that waste your time and burn through tokens?",
        "subtitle": "Tired of bloated AI responses that waste your time and burn tokens?"
    },
    {
        "id": "scene2",
        "text": "Meet Essential Mode. A native output style for Claude Code that cuts 65% of output tokens without sounding like a caveman.",
        "subtitle": "Meet Essential Mode: Cuts 65% of output tokens without sounding like a caveman."
    },
    {
        "id": "scene3",
        "text": "Conclusion first, high-school clarity, structured tables, and zero em-dashes. Answers arrive three times faster.",
        "subtitle": "Conclusion first • High-school clarity • Structured tables • Zero em-dashes"
    },
    {
        "id": "scene4",
        "text": "Zero input token overhead. Open source on GitHub. Star the repo today and start building faster.",
        "subtitle": "Zero input token overhead • Open source on GitHub • Star today!"
    }
]

async def generate():
    os.makedirs("audio", exist_ok=True)
    results = []
    for item in SCRIPT:
        audio_path = f"audio/{item['id']}.mp3"
        comm = edge_tts.Communicate(item["text"], VOICE, rate="+6%")
        await comm.save(audio_path)
        print(f"Generated {audio_path}")

if __name__ == "__main__":
    asyncio.run(generate())
