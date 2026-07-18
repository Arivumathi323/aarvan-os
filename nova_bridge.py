import sys
import os

NOVA_PATH = r"D:\NOVA\nova"
sys.path.insert(0, NOVA_PATH)

from voice_out import speak, load_keys
load_keys()

# Import these directly instead of using NOVA's listen()
# so we can tune settings for AARVAN OS
import pyaudio
import wave
import httpx
import struct
import math

GROQ_API_KEY = ""

def load_groq_key():
    global GROQ_API_KEY
    env_path = os.path.join(NOVA_PATH, ".env")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GROQ_API_KEY"):
                GROQ_API_KEY = line.split("=", 1)[1].strip()

load_groq_key()

WAV_PATH = r"D:\AARVAN-OS\temp_audio.wav"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 7
SILENCE_THRESHOLD = 300  # Lower threshold — catches quieter speech

def get_audio_level(data):
    count = len(data) // 2
    shorts = struct.unpack(f"{count}h", data)
    sum_squares = sum(s * s for s in shorts)
    rms = math.sqrt(sum_squares / count) if count > 0 else 0
    return rms

def nova_listen() -> str:
    """Record 7 seconds, send to Groq Whisper, return text"""
    print("\n🎙️  Listening for 7 seconds... Speak clearly da!")

    p = pyaudio.PyAudio()

    # Print available input devices so we can debug mic issues
    print("[dim]Using default mic...[/dim]")

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    audio_levels = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        audio_levels.append(get_audio_level(data))

    stream.stop_stream()
    stream.close()
    p.terminate()

    avg_level = sum(audio_levels) / len(audio_levels)
    max_level = max(audio_levels)
    print(f"Audio: avg={avg_level:.0f} max={max_level:.0f}")

    if max_level < SILENCE_THRESHOLD:
        print("Too quiet — no speech detected da")
        return ""

    # Save WAV
    wf = wave.open(WAV_PATH, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("🧠 Transcribing with Groq Whisper...")

    with open(WAV_PATH, "rb") as f:
        audio_data = f.read()

    response = httpx.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        files={"file": ("audio.wav", audio_data, "audio/wav")},
        data={
            "model": "whisper-large-v3-turbo",
            "language": "en",
            "prompt": "AARVAN OS commands: open YouTube, check RAM, weather in Chennai, take a note"
        },
        timeout=30
    )

    if response.status_code == 200:
        text = response.json().get("text", "").strip()

        # Filter hallucinations
        hallucinations = [
            "you", "thank you", "thanks", "bye", "goodbye",
            "thank you.", "thanks.", "you.", " ", "."
        ]
        if text.lower().strip(".").strip() in hallucinations and max_level < 1500:
            print(f"Filtered hallucination: '{text}'")
            return ""

        if text:
            print(f"✅ Heard: {text}")
        return text
    else:
        print(f"Groq error: {response.status_code} — {response.text}")
        return ""

def nova_speak(text: str):
    """Speak using NOVA's ElevenLabs voice"""
    from voice_out import speak
    speak(text)