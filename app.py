from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
from markov_generator import MarkovChainMelodyGenerator
import music21
import os

app = Flask(__name__)

# Configure paths
UPLOAD_DIR = Path('uploads')
OUTPUT_DIR = Path('output')
ALLOWED_EXTENSIONS = {'.mid', '.midi'}

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
        
    if Path(file.filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save uploaded file
    filename = Path(file.filename).stem
    upload_path = UPLOAD_DIR / file.filename
    file.save(upload_path)
    
    try:
        # Generate melody
        measures = int(request.form.get('measures', 8))
        generator = MarkovChainMelodyGenerator(upload_path)
        generator.generate(
            measures=measures,
            output_dir=OUTPUT_DIR,
            filename=f"generated_{filename}"
        )
        
        # Convert to MusicXML for visualization
        midi_path = OUTPUT_DIR / f"generated_{filename}.mid"
        score = music21.converter.parse(midi_path)
        
        # Clean up score
        for part in score.parts:
            part.partName = "Generated Melody"
            for instrument in part.getElementsByClass('Instrument'):
                part.remove(instrument)
                
        xml_path = OUTPUT_DIR / f"generated_{filename}.xml"
        score.write('musicxml', fp=xml_path)
        
        return jsonify({
            'message': 'Melody generated successfully',
            'midi_file': f"generated_{filename}.mid",
            'xml_file': f"generated_{filename}.xml"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = OUTPUT_DIR / filename
        mime_type = 'audio/midi' if filename.endswith('.mid') else 'application/xml'
        return send_file(file_path, as_attachment=True, mimetype=mime_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 