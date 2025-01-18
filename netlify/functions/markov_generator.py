import random
from music21 import *

class MarkovChainMelodyGenerator:
    def __init__(self, midi_file_path):
        self.score = converter.parseFile(midi_file_path)
        self.melody_part = self.score.parts[0]
        key_analysis = self.melody_part.analyze('key')
        self.key_signature = key_analysis 
        self.tonic_note = key_analysis.tonic.midi
        self.time_signature = self.melody_part.getTimeSignatures()[0]
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
        return transition_matrix

    def generate_new_melody(self, length):
        transition_matrix = self.create_transition_matrix()
        generated_melody = [(self.tonic_note, self.get_tonic_length())]
        current_note = self.tonic_note, self.get_tonic_length()

        for _ in range(length - 1):
            if current_note in transition_matrix:
                next_note = random.choice(transition_matrix[current_note])
                generated_melody.append(next_note)
                current_note = next_note
            else:
                current_note = random.choice(list(transition_matrix.keys()))
                generated_melody.append(current_note)
        return generated_melody

    def save_generated_melody(self, generated_melody, output_folder, output_name):
        generated_melody_stream = stream.Part()
        generated_melody_stream.append(self.time_signature)
        
        for note_midi in generated_melody:
            pitch_midi, note_duration = note_midi
            if pitch_midi is not None:
                note_obj = note.Note()
                note_obj.pitch.midi = pitch_midi
                note_obj.duration.quarterLength = note_duration
                generated_melody_stream.append(note_obj)

        output_midi_path = f"{output_folder}/{output_name}.mid"
        generated_melody_stream.write('midi', fp=output_midi_path)

    def generate_markov_chain_melody(self, length=20, output_folder="./result_output", output_name="generated_melody"):
        beats_per_measure = self.time_signature.numerator
        generated_melody = self.generate_new_melody(length * beats_per_measure)

        if output_folder is not None and output_name is not None:
            self.save_generated_melody(generated_melody, output_folder, output_name)

        return generated_melody 