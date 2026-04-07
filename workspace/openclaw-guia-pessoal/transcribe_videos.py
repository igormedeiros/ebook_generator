
import os
import subprocess
import whisper
import json

def process_video(video_url, output_name):
    print(f"Processando {video_url}...")
    audio_file = f"{output_name}.mp3"
    
    # Download audio using yt-dlp
    try:
        subprocess.run([
            "venv/bin/yt-dlp", 
            "-x", 
            "--audio-format", "mp3", 
            "-o", f"{output_name}.%(ext)s", 
            video_url
        ], check=True)
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")
        return

    # Transcribe using Whisper
    print(f"Transcrevendo {audio_file}...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    
    # Save transcript
    with open(f"{output_name}_transcript.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Concluído: {output_name}_transcript.txt")
    # Clean up audio
    # os.remove(audio_file)

videos = {
    "c0nJB1y-SQI": "antigravity",
    "L-SQ0HyRVo8": "openclaw_jarvis",
    "54nFKv9a7NA": "openclaw_extra",
    "XmweZ4fLkcI": "claude_code_openclaw"
}

for vid, name in videos.items():
    url = f"https://www.youtube.com/watch?v={vid}"
    process_video(url, name)
