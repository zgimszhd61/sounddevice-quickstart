import sounddevice as sd
import numpy as np
import wave
from openai import OpenAI
from pathlib import Path
from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-"

## 录音
def record_audio(duration=5, filename='output.wav', samplerate=44100):
    # 录音设置
    print("开始录音，请说话...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # 等待录音完成
    print("录音结束。")

    # 保存录音到WAV文件
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 16 bits = 2 bytes
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())
    print(f"录音已保存到 {filename}")

## 声音到文本:
def voice2text():
    client = OpenAI()
    audio_file= open("output.wav", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription.text)

## 文本到声音:
def text2voice():
    client = OpenAI()
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="今天天气怎么样?"
    )
    response.stream_to_file(speech_file_path)

# 调用函数开始录音
# record_audio()
# voice2text()
text2voice()
