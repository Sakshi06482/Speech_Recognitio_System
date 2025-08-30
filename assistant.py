import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import pywhatkit
import pyjokes
import time
import sys

# Initialize recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()

def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

# Function to process commands
def process_command(text):
    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        SpeakText("The time is " + now)
        print("The time is:", now)

    elif "date" in text:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        SpeakText("Today's date is " + today)
        print("Today's date:", today)

    elif "google" in text:
        SpeakText("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "youtube" in text:
        SpeakText("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "wikipedia" in text:
        try:
            SpeakText("Searching Wikipedia")
            query = text.replace("wikipedia", "").strip()
            result = wikipedia.summary(query, sentences=2)
            print("Wikipedia:", result)
            SpeakText(result)
        except:
            SpeakText("Sorry, I could not fetch Wikipedia results.")

    elif "play music" in text:
        # Local music folder example:
        music_dir = "C:\\Users\\YourName\\Music"  # change this path
        try:
            songs = os.listdir(music_dir)
            if songs:
                SpeakText("Playing music")
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                SpeakText("No music found in your folder")
        except Exception as e:
            SpeakText("Sorry, could not play music.")
            print("Error:", e)

    elif "whatsapp" in text:
        try:
            phone = "+91 9029861998"  
            message = "Hello from Jarvis Assistant!"
            pywhatkit.sendwhatmsg_instantly(phone, message)
            SpeakText("Message sent successfully")
        except Exception as e:
            SpeakText("Sorry, I couldn't send the message.")
            print("Error:", e)

    elif "joke" in text:
        joke = pyjokes.get_joke()
        SpeakText(joke)
        print("😂 Joke:", joke)

    elif "notepad" in text:
        SpeakText("Opening Notepad")
        os.system("notepad")

    elif "exit" in text or "quit" in text:
        SpeakText("Goodbye! Have a nice day.")
        print("Exiting...")
        return False  # Stop loop

    else:
        SpeakText("I heard " + text)
        print("Command not recognized, repeating back:", text)

    return True  # Continue loop


# Main Loop
def main():
    start_time = time.time()  # Timer start

    with sr.Microphone() as source:
        print("Calibrating background noise... please wait")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Calibration done. Say something (say 'exit' to quit).")

        while True:
            try:
                # Auto stop after 60 sec
                if time.time() - start_time > 60:
                    print("Time limit reached, stopping assistant...")
                    SpeakText("Time limit reached, shutting down")
                    break

                print("\nListening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

                print("Recognizing...")
                text = r.recognize_google(audio)
                text = text.lower()
                print("You said:", text)

                if not process_command(text):
                    break

            except sr.WaitTimeoutError:
                print("No speech detected, trying again...")
            except sr.UnknownValueError:
                print("Sorry, could not understand.")
                SpeakText("Sorry, I could not understand.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                SpeakText("Speech recognition service is not available.")
                break
            except KeyboardInterrupt:
                print("\n Keyboard interrupt received. Exiting...")
                SpeakText("Goodbye! Shutting down now.")
                sys.exit()

if __name__ == "__main__":
    main()