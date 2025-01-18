from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from markov_generator import MarkovChainMelodyGenerator
import music21
import time
from pathlib import Path

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'result_output'
ALLOWED_EXTENSIONS = {'mid', 'midi'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files(directory, max_age_hours=24):
    """Remove files older than max_age_hours from the specified directory"""
    current_time = time.time()
    for file_path in Path(directory).glob('*'):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > (max_age_hours * 3600):
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Clean up old files before processing new ones
    cleanup_old_files(app.config['UPLOAD_FOLDER'])
    cleanup_old_files(app.config['RESULT_FOLDER'])
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Get the number of measures from the form data
    measures = int(request.form.get('measures', 8))  # Default to 8 measures if not specified
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate new melody with specified length
        generator = MarkovChainMelodyGenerator(filepath)
        output_name = f"generated_{filename}"
        generated_melody = generator.generate_markov_chain_melody(
            length=measures,  # Use the specified number of measures
            output_folder=app.config['RESULT_FOLDER'],
            output_name=output_name.rsplit('.', 1)[0]
        )
        
        # Convert MIDI to MusicXML for visualization
        output_midi_path = os.path.join(app.config['RESULT_FOLDER'], f"{output_name.rsplit('.', 1)[0]}.mid")
        score = music21.converter.parse(output_midi_path)
        
        # Clean up the score - corrected version
        for part in score.parts:
            part.partName = "Generated Melody"
            # Remove instruments one by one
            for instrument in part.getElementsByClass('Instrument'):
                part.remove(instrument)
        
        xml_path = os.path.join(app.config['RESULT_FOLDER'], f"{output_name.rsplit('.', 1)[0]}.xml")
        score.write('musicxml', fp=xml_path)
        
        return jsonify({
            'message': 'File processed successfully',
            'download_file': f"{output_name.rsplit('.', 1)[0]}.mid",
            'xml_file': f"{output_name.rsplit('.', 1)[0]}.xml"
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['RESULT_FOLDER'], filename),
            as_attachment=True,
            mimetype='audio/midi' if filename.endswith('.mid') else 'application/xml'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 