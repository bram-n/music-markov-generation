# Clef AI Music Generator

A web application that generates new melodies using Markov chains based on input MIDI files. Upload a MIDI file and get a new, unique melody generated using probabilistic transitions from the original piece.

## Features

- Upload MIDI files to use as source material
- Generate new melodies using Markov chain analysis
- Download generated melodies as MIDI files
- View generated melodies in MusicXML format
- Customize the length of generated melodies

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/music-markov-generation.git
cd music-markov-generation
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

1. Start the Flask server:
```bash
python app.py
```

2. Open http://localhost:5000 in your browser

## Usage

1. Upload a MIDI file through the web interface
2. Choose the number of measures to generate
3. Click "Generate" to create a new melody
4. Download the generated MIDI file or view the MusicXML score

## Requirements

- Python 3.8+
- Flask
- music21

See `requirements.txt` for complete list of dependencies.
