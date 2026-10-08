import subprocess

# Combine the 4 scene audio clips with exact timing offsets into a master narration track
# Scene 1: 0.3s
# Scene 2: 5.8s
# Scene 3: 15.0s
# Scene 4: 24.0s
# Total length: 33.0s

filter_str = (
    "[0:a]adelay=300|300[a1];"
    "[1:a]adelay=5800|5800[a2];"
    "[2:a]adelay=15000|15000[a3];"
    "[3:a]adelay=24000|24000[a4];"
    "[a1][a2][a3][a4]amix=inputs=4:dropout_transition=0:normalize=0[aout]"
)

cmd = [
    "ffmpeg", "-y",
    "-i", "audio/scene1.mp3",
    "-i", "audio/scene2.mp3",
    "-i", "audio/scene3.mp3",
    "-i", "audio/scene4.mp3",
    "-filter_complex", filter_str,
    "-map", "[aout]",
    "-t", "33.5",
    "audio/master_narration.mp3"
]

subprocess.run(cmd, check=True)
print("Created audio/master_narration.mp3")
