from markov_generator import generate_markov_chain_melody_from_midi

if __name__ == "__main__":
    # Replace 'path/to/your/melody.mid' with the path to your MIDI file
    midi_file_path = "./input_reference/reference.mid"

    # Set the length of the generated melody
    generated_length = 20

    # Set the output folder and name
    output_folder = "./result_output"
    output_name = "generated_melody"

    # Generate a new melody using Markov Chain from MIDI
    generated_melody = generate_markov_chain_melody_from_midi(midi_file_path, generated_length, output_folder, output_name)

    # Print the generated melody
    print("Generated Melody:")
    print(generated_melody)
