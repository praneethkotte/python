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
import subprocess
import os
from datetime import datetime

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "bcb884ea1ae74c0a9d558fe2100b0898"


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
        api_key="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",
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
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
    if c.lower().startswith("open "):
        import subprocess
        import os

        site_name = c.lower()[5:].strip().replace(" ", "")
        if not site_name.startswith("http"):
            url = f"https://www.{site_name}.com"
        else:
            url = site_name

        print(f"🌐 Opening in Chrome: {url}")

        # YOUR EXACT CHROME PATH FROM STEP 1
        chrome_path = (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # ← CHANGE THIS
        )

        subprocess.Popen([chrome_path, url, "--new-window"])
        speak(f"Opening {site_name}")

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
        print("🔥 NEWS BLOCK - Country/State + Category mode!")

        # Announce date
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Top news for {today}")

        # COUNTRY SELECTION with 2 retries
        country_code = "in"
        country_name = "India"
        for attempt in range(2):
            speak("News for which country? Say India, USA, UK, or world")
            try:
                with sr.Microphone() as source:
                    print("Listening for country...")
                    audio = recognizer.listen(source, timeout=5)
                country_cmd = recognizer.recognize_google(audio).lower()
                print(f"Country input: '{country_cmd}'")

                countries = {
                    "in": "in",
                    "india": "in",
                    "us": "us",
                    "usa": "us",
                    "united states": "us",
                    "uk": "gb",
                    "united kingdom": "gb",
                    "world": "us",
                    "global": "us",
                }
                if country_cmd in countries:
                    country_code = countries[country_cmd]
                    country_name = (
                        "India"
                        if country_code == "in"
                        else "USA" if country_code == "us" else "UK"
                    )
                    break
                else:
                    speak("Input not recognized. You missed, please try again.")
            except Exception as e:
                print(f"Country recognition error: {e}")
                speak("You missed, please try again.")

            if attempt == 1:
                speak("You have reached maximum attempts for country. Using India.")

        # STATE SELECTION - ANY STATE ACCEPTED
        state_name = "national"
        for attempt in range(2):
            speak(f"{country_name} news. Say any state name or national")
            try:
                with sr.Microphone() as source:
                    print("Listening for state...")
                    audio = recognizer.listen(source, timeout=5)
                state_cmd = recognizer.recognize_google(audio).lower()
                print(f"State input: '{state_cmd}'")

                if state_cmd == "national":
                    state_name = "national"
                    break
                else:
                    # ACCEPT ANY STATE NAME
                    state_name = state_cmd.title()
                    speak(f"Getting news for entire {state_name} state")
                    break
            except Exception as e:
                print(f"State recognition error: {e}")
                speak("You missed, please try again.")

            if attempt == 1:
                speak("Using national news for " + country_name)

        # CATEGORY SELECTION - ANY CATEGORY ACCEPTED
        category = ""
        for attempt in range(2):
            speak(
                f"Which category for {state_name} {country_name} news? Say sports business tech general entertainment or any category"
            )
            try:
                with sr.Microphone() as source:
                    print("Listening for category...")
                    audio = recognizer.listen(source, timeout=5)
                cat_cmd = recognizer.recognize_google(audio).lower()
                print(f"Category input: '{cat_cmd}'")

                # Map common categories + accept ANY word as category
                categories = {
                    "sports": "sports",
                    "sport": "sports",
                    "business": "business",
                    "biz": "business",
                    "tech": "technology",
                    "technology": "technology",
                    "it": "technology",
                    "general": "general",
                    "news": "general",
                    "entertainment": "entertainment",
                    "movies": "entertainment",
                }
                if cat_cmd in categories:
                    category = categories[cat_cmd]
                else:
                    # ACCEPT ANY CATEGORY WORD
                    category = "general"  # default for unknown
                    speak(f"Getting {cat_cmd} category news")
                break
            except Exception as e:
                print(f"Category recognition error: {e}")
                speak("You missed, please try again.")

            if attempt == 1:
                speak("Using general category news")
                category = ""

        # Build final URL
        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={newsapi}"
        if category:
            url += f"&category={category}"

        print(f"🌐 Fetching: {url}")
        speak(f"Here are {category or 'top'} news for {state_name} from {country_name}")

        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            print(f"📈 Found {len(articles)} articles")
            if articles:
                for i, article in enumerate(articles[:3]):
                    title = (
                        article["title"][:80] + "..."
                        if len(article["title"]) > 80
                        else article["title"]
                    )
                    print(f"🗞️ News {i+1}: {title}")
                    speak(f"News {i+1}: {title}")
            else:
                speak("No news available right now")
        else:
            speak("News service unavailable")

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
