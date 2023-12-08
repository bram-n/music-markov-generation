import random
from music21 import *

def generate_markov_chain_melody_from_midi(midi_file_path, length=20, output_folder=None, output_name=None):
    # Load the MIDI file
    score = converter.parse(midi_file_path)

    # Extract the melody part (assuming the melody is in the top part)
    melody_part = score.parts[0]

    # Extract note pitches from the melody, skipping rests
    melody_sequence = [note.pitch.midi for note in melody_part.flatten().notes if note.isNote]

    # Create a Markov Chain transition matrix
    transition_matrix = {}
    for i in range(len(melody_sequence) - 1):
        current_note = melody_sequence[i]
        next_note = melody_sequence[i + 1]
        if current_note not in transition_matrix:
            transition_matrix[current_note] = []
        transition_matrix[current_note].append(next_note)

    # Generate a new melody
    generated_melody = [melody_sequence[0]]
    current_note = melody_sequence[0]

    for _ in range(length - 1):
        # Select a random next note based on the transition matrix
        if current_note in transition_matrix:
            next_note = random.choice(transition_matrix[current_note])
            generated_melody.append(next_note)
            current_note = next_note
        else:
            # If the current note is not in the transition matrix, break the loop
            break

    # Output the generated melody as a new MIDI file
    if output_folder is not None and output_name is not None:
        generated_melody_stream = stream.Part()
        for pitch_midi in generated_melody:
            if pitch_midi is not None:
                note_obj = note.Note()
                note_obj.pitch.midi = pitch_midi
                generated_melody_stream.append(note_obj)

        output_midi_path = f"{output_folder}/{output_name}.mid"
        generated_melody_stream.write('midi', fp=output_midi_path)
        print(f"Generated melody saved as MIDI: {output_midi_path}")

    return generated_melody
