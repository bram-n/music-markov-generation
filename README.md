# ClefAI - AI Music Generation

A web application that generates new melodies using Markov chains based on input MIDI files.

## Deployment Instructions

1. Fork this repository to your GitHub account
2. Sign up for a Netlify account if you haven't already
3. Connect your GitHub repository to Netlify:
   - Go to https://app.netlify.com
   - Click "New site from Git"
   - Choose GitHub and select your repository
   - Configure build settings:
     - Build command: `pip install -r requirements.txt`
     - Publish directory: `.`
4. Configure environment variables in Netlify:
   - Go to Site settings > Build & deploy > Environment
   - Add the following variables:
     - `PYTHON_VERSION`: `3.9`
     - `NODE_VERSION`: `18`
     - `PYTHONPATH`: `/opt/buildhome/python3.9/lib/python3.9/site-packages`

## Development

To run the project locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
npm install -g netlify-cli
```

2. Run the development server:
```bash
netlify dev
```

3. Open http://localhost:8888 ie your browser

## Project Structure

- `index.html`: Frontend web interface
- `netlify/functions/`: Serverless functions
  - `app.js`: Main function handling MIDI file processing
  - `markov_generator.py`: Python module for melody generation
- `requirements.txt`: Python dependencies
- `netlify.toml`: Netlify configuration
