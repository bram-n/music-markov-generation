import random
from music21 import *

class MarkovChainMelodyGenerator:
    """
    A class for generating new melodies using a Markov Chain based on an input MIDI file.
    Attributes:
    - midi_file_path (str): Path to the input MIDI file.
    - score (music21.stream.Score): The parsed score from the input MIDI file.
    - melody_part (music21.stream.Part): The first part of the score, assumed to contain the melody.
    - key_signature (music21.key.Key): The key signature of the melody.
    - tonic_note (int): The MIDI note of the tonic in the key signature.
    - melody_sequence (list): The MIDI note sequence extracted from the melody part.

    Methods:
    - extract_melody_sequence(): Extracts the melody note sequence from the melody part.
    - create_transition_matrix(): Creates a Markov Chain transition matrix from the melody sequence.
    - generate_new_melody(length): Generates a new melody of the specified length using the transition matrix.
    - save_generated_melody(generated_melody, output_folder, output_name): Saves the generated melody as a new MIDI file.

    Usage:
    Example usage:
    generator = MarkovChainMelodyGenerator("path/to/your/midi/file.mid")
    generator.generate_markov_chain_melody(length=20, output_folder="output", output_name="generated_melody")
    """

    def __init__(self, midi_file_path):
        self.score = converter.parseFile(midi_file_path)
        self.melody_part = self.score.parts[0]
        key_analysis = self.melody_part.analyze('key')
        self.key_signature = key_analysis 
        self.tonic_note = key_analysis.tonic.midi
        self.time_signature = self.melody_part.getTimeSignatures()[0]  # Get the time signature
        self.melody_sequence = self.extract_melody_sequence()

    def get_tonic_length(self):
        for note in self.melody_part.flatten().notes:
            if note == self.tonic_note:
                tonic_note_length = note.duration
            else:
                tonic_note_length = 1.0
        return tonic_note_length
    
    def extract_melody_sequence(self):
        return [(note.pitch.midi, note.duration.quarterLength) for note in self.melody_part.flatten().notes if note.isNote]

    def create_transition_matrix(self):
        transition_matrix = {}
        for i in range(len(self.melody_sequence) - 1):
            current_note = self.melody_sequence[i]
            next_note = self.melody_sequence[i + 1]
            if current_note not in transition_matrix:
                transition_matrix[current_note] = []
            transition_matrix[current_note].append(next_note)
        # print(transition_matrix)
        return transition_matrix



    def generate_new_melody(self, length):
        """Algorithm for generating the melody"""
        transition_matrix = self.create_transition_matrix()
        generated_melody = [(self.tonic_note, self.get_tonic_length())]  # Start with the tonic note
        current_note = self.tonic_note, self.get_tonic_length()

        for _ in range(length - 1):
            # Select a random next note based on the transition matrix
            if current_note in transition_matrix:
                next_note = random.choice(transition_matrix[current_note])
                generated_melody.append(next_note)
                current_note = next_note
                
            else:
                current_note = random.choice(list(transition_matrix.keys()))
                generated_melody.append(current_note)
        return generated_melody

    def save_generated_melody(self, generated_melody, output_folder, output_name):
        """Save the generated melody to a file location"""
        generated_melody_stream = stream.Part()
        # Add time signature
        generated_melody_stream.append(self.time_signature)
        
        # Add notes
        for note_midi in generated_melody:
            pitch_midi, note_duration = note_midi
            if pitch_midi is not None:
                note_obj = note.Note()
                note_obj.pitch.midi = pitch_midi
                note_obj.duration.quarterLength = note_duration
                generated_melody_stream.append(note_obj)

        output_midi_path = f"{output_folder}/{output_name}.mid"
        generated_melody_stream.write('midi', fp=output_midi_path)
        print(f"Generated melody saved as MIDI: {output_midi_path}")

    def generate_markov_chain_melody(self, length=20, output_folder="./result_output", output_name="generated_melody"):
        """Main function. Generate a new melody and save it to a file location

        Args:
            measures (int): Number of measures to generate
            output_folder (str): folder location you want to save your file
            output_name (str): name you want for the file

        Returns:
            list of midi note: the generated melody
        """
        # Calculate notes per measure based on time signature
        beats_per_measure = self.time_signature.numerator
        # Generate a new melody
        generated_melody = self.generate_new_melody(length * beats_per_measure)

        # Output the generated melody as a new MIDI file
        if output_folder is not None and output_name is not None:
            self.save_generated_melody(generated_melody, output_folder, output_name)

        return generated_melody

# # Example usage:
# generator = MarkovChainMelodyGenerator('/Users/bram/Desktop/Projects/music-markov-generation/input_reference/Meditation_from_Thais.mid')
# generated_melody = generator.generate_markov_chain_melody(length=20, output_folder='./result_output', output_name='generated_melody4')
