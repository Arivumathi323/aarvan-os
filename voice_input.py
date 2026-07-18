import whisper
import sounddevice as sd
from rich.console import Console
import numpy as np
import os

console = Console()
SAMPLE_RATE = 48000
MODEL = whisper.load_model("small")

# Fix ffmpeg path for Windows
os.environ["PATH"] += r";C:\Users\System_1\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin"

def load_whisper():
    global MODEL
    if MODEL is None:
        console.print("[dim]🎙️  Loading Whisper voice model (small)...[/dim]")
        MODEL = whisper.load_model("small")   # ← small uses only ~500MB RAM
        console.print("[green]🎙️  Voice model ready![/green]")
    return MODEL

def listen(duration: int = 5) -> str:
    console.print(f"[yellow]🎙️  Listening for {duration} seconds... Speak now da![/yellow]")

    # Record at mic's native rate
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()

    console.print("[dim]🧠 Transcribing...[/dim]")

    # Flatten to 1D
    audio_flat = audio.flatten()

    # Resample 48000 → 16000 (Whisper needs exactly 16000Hz)
    target_length = int(len(audio_flat) * 16000 / SAMPLE_RATE)
    audio_16k = np.interp(
        np.linspace(0, len(audio_flat), target_length),
        np.arange(len(audio_flat)),
        audio_flat
    ).astype(np.float32)

    # Feed numpy array directly — no file, no ffmpeg needed
    model = load_whisper()
    result = model.transcribe(
        audio_16k,
        language="en",
        fp16=False
    )

    text = result["text"].strip()
    return text