from markov_generator import raw_maestro_markov_generate_to_file

if __name__ == "__main__":
    # Replace 'path/to/your/melody.mid' with the path to your MIDI file
    # midi_file_path = "maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_06_Track06_wav.midi"
    midi_file_path = "input_reference/Canon_in_D_easy.mid"
    generated_length = 60
    output_folder = "./result_output"
    output_name = "canon2"

    result = raw_maestro_markov_generate_to_file(midi_file_path,generated_length, output_folder, output_name )
    # Print the generated melody
    print("Generated Melody:")
    print(result)
