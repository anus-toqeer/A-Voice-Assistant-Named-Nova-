import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary  
import wikipedia
from datetime import datetime
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
app_paths = {
    "notepad": "notepad.exe",
    "vs code": r"C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "calculator": "calc.exe",
    "my projects": r"C:\Users\User\Desktop\Work\Mini-Projects",
    "downloads": r"C:\Users\User\Downloads",
    "documents": r"C:\Users\USer\Documents"
}
def open_local_app(command):
    cl = command.lower()
    for name, path in app_paths.items():
        if name in cl and any(verb in cl for verb in ["open", "launch", "start", "show"]):
            try:
                os.startfile(path)
                speak(f"Opening {name}")
                return True
            except Exception as e:
                print(f"Failed to open {name}: {e}")
                speak(f"Sorry, I couldn't open {name}.")
                return True
    return False

def calculator(cl):
    # add 5 and 3
    if "add" in cl and "and" in cl:
        parts = cl.replace("add", "").split("and")
        try:
            a = float(parts[0].strip())
            b = float(parts[1].strip())
            return a + b
        except:
            return None
    if "subtract" in cl and "from" in cl:
        parts = cl.replace("subtract", "").split("from")
        try:
            a = float(parts[1].strip())
            b = float(parts[0].strip())
            return a - b
        except:
            return None
    if ("multiply" in cl or "times" in cl) and "and" in cl:
        key = "multiply" if "multiply" in cl else "times"
        parts = cl.replace(key, "").split("and")
        try:
            a = float(parts[0].strip())
            b = float(parts[1].strip())
            return a * b
        except:
            return None
    if "divide" in cl and "by" in cl:
        parts = cl.replace("divide", "").split("by")
        try:
            a = float(parts[0].strip())
            b = float(parts[1].strip())
            if b == 0:
                return "zero_error"
            return a / b
        except:
            return None
    return None

def get_datetime():
    now = datetime.now()
    time = now.strftime("%I:%M %p")
    date = now.strftime("%A, %B %d, %Y")
    speak(f"Today is {date} and the time is {time}.")
    print(f"Today is {date} and the time is {time}.")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        print("Wikipedia:", result)
        print(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The term is ambiguous, please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find anything on Wikipedia for that.")
    except Exception as e:
        print("Wikipedia Error:", e)
        speak("Something went wrong while searching Wikipedia.")

def sourcecommand(c):
    c1=c.lower()
    print("Command received:", c)
    calc_result = calculator(cl)
    if calc_result is not None:
        if calc_result == "zero_error":
            speak("Division by zero is not possible .")
            print("Division by zero is not possible .")
        else:
            speak(f"Result is {calc_result}")
            print(f"Result is {calc_result}")

        return

    if  open_local_app(cl):
        return
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening YOutube")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/")
        speak("Opening Linkedin")

    elif "open chat gpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
        speak("Opening CHat GPT")

    elif "open gmail" in c.lower():
        webbrowser.open("https://gmail.com")
        speak("Opening Gmail")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I could not find that song.")
    elif any(phrase in cl for phrase in [
        "what time", "tell me the time", "current time", "time now",
        "what's the time", "what is the time", "show time",
        "what date", "tell me the date","tell me the date and time", "today's date", "current date"
        ]):
        get_datetime()
    elif "wikipedia" in cl or "search wikipedia" in cl:
        query = cl.replace("wikipedia", "").replace("search wikipedia", "").strip()
        if query:
            speak(f"Searching Wikipedia for {query}")
            search_wikipedia(query)
        else:
            speak("Please say what you want to search on Wikipedia.")
    elif c.lower() in ['goodbye','good bye','exit']:
        speak("Have a Nice Day Good Bye")
        exit()
        exit()
    else:
        speak("Sorry, I didn't understand the command.")


if __name__ == "__main__":
    print("Initializing Nova...")
    speak("Initializing Nova...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Say 'Nova' to activate...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                wake_word = recognizer.recognize_google(audio)
                print("Heard: Nova" )

            if wake_word.lower() in ['nova', 'novaa','noova','noovaa','noba','nooba','nobaa' ,'noba', 'no va','innova','nov']:
                engine.say("Yes how can Nova help you?")
                print("Nova Activated... Waiting for command...")
                while True:
                        try:
                            with sr.Microphone() as source:
                                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                                c = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                                command = recognizer.recognize_google(c)
                                print("Recognized Command:", command)
                                cl = command.lower()
                                if cl in ['cancel', 'never mind', 'stop']:
                                      speak("Okay, cancelling. Say Nova when you need me again.")
                                      break 
                                sourcecommand(command)
                                break

                        except sr.UnknownValueError:
                            print("Please repeat your command.")
                        except sr.WaitTimeoutError:
                            speak("still listening say your command.")

                        except Exception as e:
                            print("Unexpected error while listening for command:", e)
                            speak("Let's try again.")
        

        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("I didn't catch that.")
        except Exception as e:
            print("Unexpected error:", e)
