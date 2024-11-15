import whisper
import pyaudio
import numpy as np
from queue import Queue

# Load the Whisper model
model = whisper.load_model("base")  # Or another size as needed

# Queue for real-time audio data
audio_queue = Queue()

def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
    audio_queue.put(audio_data)
    return (in_data, pyaudio.paContinue)

# Set up audio streaming
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4096,
                    stream_callback=callback)

stream.start_stream()

print("Listening...")

# Process the audio in real-time
while True:
    if not audio_queue.empty():
        audio_segment = audio_queue.get()

        # Convert audio segment to the format Whisper expects
        result = model.transcribe(audio_segment)
        print("Detected speech:", result["text"])

stream.stop_stream()
stream.close()
audio.terminate()