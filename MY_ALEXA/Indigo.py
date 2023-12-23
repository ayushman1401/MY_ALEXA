import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyttsx4
import pyaudio

listener = sr.Recognizer()
machine = pyttsx4.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def search_web(query):
    talk("Searching the web for " + query)
    pywhatkit.search(query)
    
def tell_joke():
    joke = pyjokes.get_joke()
    talk(joke)

def input_instruction():
    global instruction
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)  
            audio = listener.listen(source, timeout=5)  
            instruction = listener.recognize_google(audio)
            instruction = instruction.lower()
            if "python" in instruction:
                instruction = instruction.replace('python', "")
            return instruction
    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        talk("Sorry, there was an issue with the speech recognition service.")
    return None

def set_alarm():
    try:
        with sr.Microphone() as source:
            talk("Sure, please tell me the time you want to set the alarm for.")
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source, timeout=5)
            time_input = listener.recognize_google(audio)
            time_input = time_input.lower()

            if "cancel" in time_input:
                talk("Alarm setting canceled.")
                return

            # Convert the time_input to a time object
            alarm_time = datetime.datetime.strptime(time_input, "%I:%M %p")

            current_time = datetime.datetime.now().time()

            if alarm_time.time() < current_time:
                talk("Sorry, the specified time has already passed. Please try again.")
                return

            while True:
                current_time = datetime.datetime.now().time()
                if alarm_time.time() <= current_time:
                    talk("Time to wake up!")
                    break

    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        talk("Sorry, there was an issue with the speech recognition service.")
    except ValueError:
        talk("Sorry, there was an error while processing the time. Please try again.")


def play_Python():
    instruction = input_instruction()
    print(instruction)
    
    if "play" in instruction:
        song = instruction.replace('play', "")
        pywhatkit.playonyt(song)
    
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M:%p')
        talk('Current time is ' + time)
        
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)
        
    elif 'how are you' in instruction:
        talk('I am fine, how about you?')
    
    elif 'search' in instruction:
        query = instruction.replace("search", "")
        talk("Searching the web for " + query)
        pywhatkit.search(query)
    
    elif 'what is your name' in instruction:
        talk('My name is Python, and I am here to assist you.')
        
    elif 'who is' in instruction:
        human = instruction.replace("who is", "")
        info = wikipedia.summary(human, 2)
        print(info)
        talk(info)

    elif 'joke' in instruction:
        tell_joke()
    
    
    else:
        talk("Please repeat")

play_Python()