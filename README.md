# Markov Chain Melody Generator

Generate musical melodies using Markov chains based on MIDI input. 

## Overview

This project uses Markov chain modeling to generate new melodies based on existing MIDI input. The algorithm analyzes the input, builds a transition matrix, and generates a new melody with user-defined parameters.

## Features

- **Markov Chain Generation:** Create melodies using a Markov chain approach.
- **MIDI Input:** Use MIDI files as input for melody generation.
- **Customization:** Adjust parameters like melody length, output folder, and output name.

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies Music21: `pip install music21`
- Install a midi displayer like MuseScore

### Installation

1. Clone the repository: `git clone https://github.com/yourusername/markov-melody-generator.git`
2. Navigate to the project folder: `cd markov-melody-generator`
3. Run the generator: `python markov_generator.py`

## Usage

1. Provide a MIDI file as input.
2. Adjust parameters like length, output folder, and output name.
3. Run the script and find the generated melody in the specified folder.
4. Once having the midi file in the folder, use MuseScore to display the piece

## Customization

- **Melody Length:** Set the desired length of the generated melody.
- **Output Folder and Name:** Specify where and how the generated melody should be saved.

## Example

```bash
python markov_generator.py --input "path/to/your/midi/file.mid" --length 30 --output_folder "./output" --output_name "generated_melody"
