from flask import Flask, render_template, request, jsonify
import os
from test import process_video

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploaded_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


current_video_path = None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle video file upload"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
     
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            
        
            global current_video_path
            current_video_path = filename
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': file.filename
            }), 200
            
    except Exception as e:
        print(f"Error in upload_file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_summary():
    """Generate summary from the uploaded video"""
    try:
        if not current_video_path:
            return jsonify({'error': 'No video file uploaded'}), 400

       
        base_dir = 'static'
        results = process_video(current_video_path, base_dir)
        
        if results['success']:
            try:
               
                with open(results['summary_path'], 'r', encoding='utf-8') as f:
                    summary_content = f.read()
                
                print("Debug - Raw summary content:", summary_content) 
                
     
                sections = {}
                current_section = None
                current_lines = []
                
                for line in summary_content.split('\n'):
                    line = line.strip()
                    if line.startswith('Summary:'):
                        current_section = 'summary'
                        continue
                    elif line.startswith('Key Points:'):
                        if current_section:
                            sections[current_section] = '\n'.join(current_lines)
                        current_section = 'key_points'
                        current_lines = []
                        continue
                    elif line.startswith('Keywords:'):
                        if current_section:
                            sections[current_section] = '\n'.join(current_lines)
                        current_section = 'keywords'
                        current_lines = []
                        continue
                    elif line: 
                        current_lines.append(line)
                
               
                if current_section and current_lines:
                    sections[current_section] = '\n'.join(current_lines)
                
                print("Debug - Parsed sections:", sections)  
                
               
                key_points = sections.get('key_points', '')
                if key_points:
                    
                    if not key_points.strip().startswith('•'):
                        key_points = '\n'.join(f"• {point.strip()}" 
                                             for point in key_points.split('\n') 
                                             if point.strip())
                
                return jsonify({
                    'success': True,
                    'summary': sections.get('summary', 'No summary available').strip(),
                    'key_points': key_points.strip(),
                    'keywords': sections.get('keywords', 'No keywords available').strip()
                })
            
            except Exception as e:
                print(f"Error parsing summary file: {e}")
                return jsonify({
                    'error': 'Error parsing summary file',
                    'details': str(e)
                }), 500
        else:
            return jsonify({
                'error': 'Video processing failed',
                'details': results.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        print(f"Error in generate_summary: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def get_status():
    """Get the current processing status"""
    return jsonify({
        'video_uploaded': current_video_path is not None,
        'current_video': os.path.basename(current_video_path) if current_video_path else None
    })

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    print(f"An error occurred: {error}")
    return jsonify({'error': str(error)}), 500

if __name__ == '__main__':

    for dir_path in ['static/output_audio', 'static/transcriptions', 'static/summaries']:
        os.makedirs(dir_path, exist_ok=True)
    
    app.run(debug=True)