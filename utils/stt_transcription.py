import speech_recognition as sr

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe the given audio file to text using the SpeechRecognition library.
    
    Parameters:
        audio_path (str): Path to the audio file (e.g., .wav, .mp3) to transcribe.
        
    Returns:
        str: The transcribed text.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        
        text = recognizer.recognize_google(audio_data)
        
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None