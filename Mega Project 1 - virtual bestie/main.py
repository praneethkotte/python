import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "pub_efd2a7c74921469785539905553be0c4"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(
        api_key="pub_efd2a7c74921469785539905553be0c4",
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named bestie skilled in general tasks like Alexa and Google Cloud. Give short responses please",
            },
            {"role": "user", "content": command},
        ],
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song_name = c[5:].strip()
        print("🎵 Auto-playing first YouTube result for:", repr(song_name))

        search_url = (
            "https://www.youtube.com/results?search_query="
            + song_name.replace(" ", "+")
        )

        options = webdriver.ChromeOptions()
        options.add_argument("--new-window")
        driver = webdriver.Chrome(options=options)

        driver.maximize_window()  # Maximize the browser immediately

        driver.get(search_url)
        time.sleep(4)  # Let results load

        # Click first video title
        first_video = driver.find_element(By.ID, "video-title")
        first_video.click()
        print("▶️ First video clicked")

        # Skip ads loop

        print("🔍 Looking for Skip buttons...")

        skip_selectors = [
            ".ytp-ad-skip-button",
            ".ytp-ad-skip-button-modern",
            ".ytp-skip-ad-button",
            "button.ytp-ad-skip-button",
            "[title*='Skip ad']",
            "[title*='Skip Ads']",
            "[aria-label*='Skip']",
        ]

        max_attempts = 60  # 30 seconds checking
        for attempt in range(max_attempts):
            for selector in skip_selectors:
                try:
                    skip_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if skip_button.is_displayed() and skip_button.is_enabled():
                        driver.execute_script(
                            """
                            arguments[0].scrollIntoView({block: 'center'});
                            arguments[0].click();
                        """,
                            skip_button,
                        )
                        print(
                            f"✅ SKIP CLICKED! (attempt {attempt+1}, selector: {selector})"
                        )
                        time.sleep(1.5)
                        break
                except NoSuchElementException:
                    pass
                except Exception as e:
                    print(f"Exception during skip attempt: {e}")
            time.sleep(0.5)

        print("🎵 Video playing now")
        speak(f"Playing first result for {song_name}")

    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # Print the headlines
            for article in articles:
                speak(article["title"])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing virtual bestie malar....")
    while True:
        # Listen for the wake word "bestie"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "bestie":
                speak("Ya praneeth its your bestie malar")
                # Listen for command
                with sr.Microphone() as source:
                    print("bestie Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("You said EXACTLY:", repr(command))
                    print("Lowercase:", repr(command.lower()))

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
