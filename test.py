from music21 import *
from markov_generator import MarkovChainMelodyGenerator

def test_key_signature(midi_file_path, expected_sharps, expected_tonic_midi):
    # Load the MIDI file
    score = converter.parse(midi_file_path)

    # Extract the key signature
    key_signature = score.analyze('key')

    # Check key signature attributes
    actual_sharps = key_signature.sharps
    actual_tonic_midi = key_signature.tonic.midi
    print(key_signature)
    # Perform assertions
    assert actual_sharps == expected_sharps, f"Expected {expected_sharps} sharps, but got {actual_sharps} sharps."
    assert (actual_tonic_midi == expected_tonic_midi or actual_tonic_midi == expected_tonic_midi-12), f"Expected tonic MIDI note {expected_tonic_midi}, but got {actual_tonic_midi}."

def test_generator():
    midi_file_path = "input_reference/reference.mid"
    generator = MarkovChainMelodyGenerator(midi_file_path)
    generator.generate_markov_chain_melody(output_name="reference2")
    # print(generator.key_signature)
    # print(generator.tonic_note)
    mat = generator.create_transition_matrix()
    print(mat)
    

test_generator()
