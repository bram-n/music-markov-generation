from markov_generator import MarkovChainMelodyGenerator


if __name__ == "__main__":
    midi_file_path = "input_reference/Violin_Concerto_Bach_Double_3rd_Movement.mid"
    generator = MarkovChainMelodyGenerator(midi_file_path)
    generator.generate_markov_chain_melody( length=100, output_folder="./result_output", output_name="generated_bachmelody")