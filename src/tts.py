import asyncio
import edge_tts


class TextToSpeech:

    @staticmethod
    def generate_audio(text):

        output_file = "output.mp3"

        async def speak():
            communicate = edge_tts.Communicate(
                text=text,
                voice="en-US-GuyNeural"
            )
            await communicate.save(output_file)

        asyncio.run(speak())

        return output_file