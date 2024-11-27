import moviepy
import os
from moviepy.editor import VideoFileClip
from utils.audio_extraction import extract_audio_from_video
from utils.stt_transcription import transcribe_audio
from utils.nlp_summarization import summarize_text

print("MoviePy version:", moviepy.__version__)

def process_video(input_video_path: str, base_output_dir: str) -> dict:
    """Process video through multiple stages and return results"""
    results = {
        'success': False,
        'audio_path': None,
        'transcription_path': None,
        'summary_path': None,
        'error': None
    }
    
    try:
        # Define output paths
        output_audio = os.path.join(base_output_dir, 'output_audio', 'audio.wav')
        output_transcription = os.path.join(base_output_dir, 'transcriptions', 'transcription.txt')
        output_summary = os.path.join(base_output_dir, 'summaries', 'summary.txt')
        
        # Create directories if they don't exist
        for path in [output_audio, output_transcription, output_summary]:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Step 1: Extract audio
        print("Extracting audio...")
        if not extract_audio_from_video(input_video_path, output_audio):
            raise Exception("Audio extraction failed")
        results['audio_path'] = output_audio
        
        # Step 2: Transcribe audio
        print("Transcribing audio...")
        transcription = transcribe_audio(output_audio)
        if not transcription:
            raise Exception("Transcription failed")
            
        # Debug print
        print(f"Debug - Transcription length: {len(transcription)}")
        print("Debug - First 100 characters of transcription:", transcription[:100])
        
        # Save transcription to file
        with open(output_transcription, 'w', encoding='utf-8') as f:
            f.write(transcription)
        results['transcription_path'] = output_transcription
        
        # Step 3: Generate summary
        print("Generating summary using nlp_summarization module...")
        try:
            summary_result = summarize_text(transcription)
            
            if not isinstance(summary_result, dict):
                raise Exception("Invalid summary format returned")
            
            # Extract components from summary_result
            summary = summary_result.get('summary', 'No summary available')
            important_points = summary_result.get('important_points', ['No key points available'])
            keywords = summary_result.get('keywords', ['No keywords available'])
            
            # Format key points with bullet points
            formatted_points = '\n'.join(f"• {point}" for point in important_points)
            
            # Format keywords as comma-separated list
            formatted_keywords = ', '.join(keywords)
            
            # Create the formatted summary
            formatted_summary = f"""Summary:
{summary}

Key Points:
{formatted_points}

Keywords:
{formatted_keywords}"""
            
            # Debug print
            print("\nDebug - Summary components:")
            print(f"Summary: {summary}")
            print(f"Key Points: {important_points}")
            print(f"Keywords: {keywords}")
            
            # Save the formatted summary
            with open(output_summary, 'w', encoding='utf-8') as f:
                f.write(formatted_summary)
            results['summary_path'] = output_summary
            
            results['success'] = True
            
        except Exception as e:
            print(f"Error in summary generation: {e}")
            raise Exception(f"Summary generation failed: {str(e)}")
        
    except Exception as e:
        results['error'] = str(e)
        print(f"Error: {str(e)}")
    
    return results

def display_summary(summary_path):
    """Helper function to display the summary content"""
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nGenerated Summary Content:")
            print("-" * 50)
            print(content)
            print("-" * 50)
    except Exception as e:
        print(f"Error displaying summary: {e}")

if __name__ == "__main__":
    # Test the video processing
    input_video = "static/uploaded_videos/videoplayback.mp4"  # Update this path to your video file
    base_dir = "static"
    
    print(f"Processing video: {input_video}")
    results = process_video(input_video, base_dir)
    
    if results['success']:
        print("\nProcessing completed successfully!")
        print(f"Audio saved to: {results['audio_path']}")
        print(f"Transcription saved to: {results['transcription_path']}")
        print(f"Summary saved to: {results['summary_path']}")
        
        # Display the generated summary
        display_summary(results['summary_path'])
        
        # Also display the transcription for verification
        print("\nTranscription Content:")
        print("-" * 50)
        with open(results['transcription_path'], 'r', encoding='utf-8') as f:
            print(f.read())
        print("-" * 50)
    else:
        print(f"\nProcessing failed: {results['error']}")