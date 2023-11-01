
import pyttsx3
import asyncio

async def text_to_speech_consumer(message):
    text = message.content['text']
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0)