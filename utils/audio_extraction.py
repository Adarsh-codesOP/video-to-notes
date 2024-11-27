import moviepy.editor as mp

def extract_audio_from_video(video_path: str, audio_path: str) -> bool:
    """
    Extracts audio from the video file and saves it as a .wav file.
    
    Parameters:
        video_path (str): Path to the input video file.
        audio_path (str): Path where the extracted audio will be saved (including the .wav extension).
        
    Returns:
        bool: True if extraction is successful, False if there was an error.
    """
    try:
       
        video = mp.VideoFileClip(video_path)

       
        audio = video.audio

       
        audio.write_audiofile(audio_path, codec='pcm_s16le')

      
        video.close()
        audio.close()

        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False