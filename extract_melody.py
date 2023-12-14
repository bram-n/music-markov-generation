import os
from music21 import *

def extract_melody_to_object(midi_file_path, output_folder=None, output_midi_filename=None):
    

    # Load the MIDI file
    score = converter.parse(midi_file_path)

    # Extract the melody part (assuming the melody is in the top part)
    melody_part = score.parts[0]

    # Create a new stream for the melody
    melody_stream = stream.Score()
    melody_stream.append(melody_part)
    return melody_stream
    
def extract_melody_to_midi(midi_file_path, output_folder=None, output_midi_filename=None):
    # Load the MIDI file
    score = converter.parse(midi_file_path)

    # Extract the melody part (assuming the melody is in the top part)
    melody_part = score.parts[0]

    # Create a new stream for the melody
    melody_stream = stream.Score()
    melody_stream.append(melody_part)

    # Output folder and filename setup
    if output_folder is None:
        output_folder = os.path.dirname(midi_file_path)
    if output_midi_filename is None:
        output_midi_filename = "output_melody.mid"

    # Print out the notes and chords
    for element in melody_part.flat.notesAndRests:
        if isinstance(element, (note.Note, chord.Chord)):
            print(f"{element} {element.offset} {element.duration.quarterLength}")

    # Output the melody as MIDI (optional)
    output_midi_path = os.path.join(output_folder, output_midi_filename)
    melody_stream.write('midi', fp=output_midi_path)
    print(f"Melody saved as MIDI: {output_midi_path}")

# if __name__ == "__main__":
#     # Set the default path to the parent directory
#     default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#     # Replace 'path/to/your/melody.mid' with the path to your MIDI file
#     midi_file_path = "./maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi"

#     # Extract melody and print out notes
#     extract_melody(midi_file_path, "./result_output", "output_melody2.mid")
