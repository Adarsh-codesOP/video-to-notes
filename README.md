Video-to-Notes Feature

This project extracts notes from lecture videos using NLP and AI. The pipeline includes video upload, audio extraction, speech-to-text conversion, text preprocessing, and summarization.

Features

Upload lecture videos via a web interface.

Extract audio from uploaded videos.

Convert audio to text using Whisper (speech-to-text).

Preprocess and clean the transcribed text.

Summarize the cleaned text for concise notes.



---

Project Structure

project-folder/
├── data/                # Store videos or audio files here
├── uploads/             # Store uploaded videos here
├── models/              # Store or load AI models here
├── scripts/             # Python scripts for each task
├── outputs/             # Store generated notes
├── app.py               # Flask application for video upload
└── templates/           # HTML files for the web interface


---

Setup and Usage

Step 1: Setup Development Environment

1. Install Python and create a virtual environment:

python -m venv venv
source venv/bin/activate  # Use venv\Scripts\activate on Windows
pip install openai-whisper moviepy nltk transformers flask


2. Clone this repository:

git clone <repository-url>
cd project-folder




---

Step 2: Run the Application

1. Start the Flask application:

python app.py


2. Open the browser and navigate to:

http://127.0.0.1:5000/


3. Upload a video file and start the processing pipeline.




---

Pipeline Details

1. Video Upload

The Flask application (app.py) provides a web interface for uploading videos.

2. Audio Extraction

The extract_audio.py script uses MoviePy to extract audio from the uploaded video.

3. Speech-to-Text Conversion

The stt.py script transcribes the extracted audio into text using OpenAI Whisper.

4. Text Preprocessing

The preprocess.py script removes unnecessary stop words and formats the transcription.

5. Summarization

The summarize.py script summarizes the cleaned transcription using Hugging Face's Transformers library.


---

Outputs

Raw Transcription: Stored in outputs/transcription.txt.

Cleaned Transcription: Stored in outputs/cleaned_transcription.txt.

Summary: Stored in outputs/summary.txt.



---

Future Enhancements

Add support for translating summarized text into regional languages.

Implement real-time speech recognition for live lectures.



---

Dependencies

Install the following Python libraries:

Flask

MoviePy

Whisper

NLTK

Transformers



---

License

This project is licensed under the MIT License.


--

