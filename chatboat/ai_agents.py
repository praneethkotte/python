# ai_agents.py
import os
import time
from dotenv import load_dotenv
from voice_interface import VoiceAgent
from web_interface import run_web_interface
import pyttsx3
import speech_recognition as sr

load_dotenv()

# ---------- GLOBAL TTS + RECOGNIZER ----------

engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text: str):
    """Print and speak text."""
    print(text)
    try:
        engine.stop()
    except Exception:
        pass
    engine.say(text)
    engine.runAndWait()


def listen_choice(timeout: int = 6) -> str:
    """Listen once for spoken menu choice."""
    try:
        with sr.Microphone() as source:
            print("🎤 Listening for option (say 1, 2, or 3)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=timeout)
        text = recognizer.recognize_google(audio).lower()
        print(f"👤 You said: {text}")
        return text
    except Exception as e:
        print(f"⚠️ Voice not captured: {e}")
        return ""


# ---------- MENU LOGIC ----------


def get_menu_choice() -> str:
    """Show + speak menu; allow voice (2 tries) or typed choice."""

    # 1) PRINT OPTIONS
    print("🤖 AI Agent System")
    print("=" * 40)
    print("1. 🎤 Voice Mode (like Alexa)")
    print("2. 🌐 Web Mode (like ChatGPT)")
    print("3. 🧪 Test Agent (console)")
    print()

    # 2) SPEAK OPTIONS
    speak("Welcome to your A I agent system.")
    speak("Option one. Voice mode, like Alexa.")
    speak("Option two. Web mode, like Chat G P T.")
    speak("Option three. Test agent in console.")
    speak("You can say one, two, or three, or type your choice on the keyboard.")
    time.sleep(0.5)

    # 3) VOICE: UP TO 2 ATTEMPTS
    for attempt in range(2):
        voice = listen_choice()

        if "one" in voice or "1" in voice:
            return "1"
        if "two" in voice or "2" in voice:
            return "2"
        if "three" in voice or "3" in voice:
            return "3"

        if attempt == 0:
            speak("You missed, please try again. Say one, two, or three.")
        else:
            speak("You have reached the number of attempts.")

    # 4) KEYBOARD FALLBACK
    choice = input("Enter choice (1/2/3): ").strip()
    return choice


# ---------- MAIN ----------


def main():
    choice = get_menu_choice()

    if choice == "1":
        speak("Starting voice mode.")
        agent = VoiceAgent()
        agent.run()

    elif choice == "2":
        speak("Starting web mode in your browser.")
        os.system("streamlit run web_interface.py")

    elif choice == "3":
        speak("Starting console test mode.")
        from agents import AIAgentSystem

        ai = AIAgentSystem()
        while True:
            query = input("You: ")
            if query.lower() in ["exit", "quit"]:
                break
            print("🤖 AI:", ai.process_query(query))

    else:
        speak("Invalid option selected. Please restart the program.")


if __name__ == "__main__":
    main()
