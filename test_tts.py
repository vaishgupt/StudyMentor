from src.tts import TextToSpeech

print("Generating...")

path = TextToSpeech.generate_audio("Hello, Khushi whats up.")

print(path)
print("Done")