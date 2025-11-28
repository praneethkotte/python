import speech_recognition as sr
import pyttsx3
from agents import AIAgentSystem


class VoiceAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.ai_system = AIAgentSystem()

    def speak(self, text: str):
        print(f"🤖 AI: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Speech service error")
            return ""

    def run(self):
        self.speak("AI Agent System ready! Say your query or 'exit' to quit.")
        while True:
            query = self.listen()
            if not query:
                continue
            if "exit" in query or "stop" in query:
                self.speak("Goodbye!")
                break
            response = self.ai_system.process_query(query)
            self.speak(response)
