import random
from music21 import converter, stream, note

class MarkovChainMelodyGenerator:
    def __init__(self, midi_path):
        self.score = converter.parseFile(midi_path)
        self.melody = self.score.parts[0]
        self.key = self.melody.analyze('key')
        self.time_sig = self.melody.getTimeSignatures()[0]
        self.sequence = self._extract_melody()
        
    def _extract_melody(self):
        """Extract pitch and duration pairs from the melody."""
        return [(note.pitch.midi, note.duration.quarterLength) 
                for note in self.melody.flatten().notes 
                if note.isNote]
    
    def _build_transitions(self):
        """Build the Markov chain transition matrix."""
        transitions = {}
        for curr, next_note in zip(self.sequence, self.sequence[1:]):
            if curr not in transitions:
                transitions[curr] = []
            transitions[curr].append(next_note)
        return transitions
    
    def generate(self, measures=8, output_dir="./output", filename="generated"):
        """Generate a new melody using Markov chains.
        
        Args:
            measures: Number of measures to generate
            output_dir: Directory to save the MIDI file
            filename: Name of the output file (without extension)
            
        Returns:
            List of (pitch, duration) tuples representing the melody
        """
        transitions = self._build_transitions()
        length = measures * self.time_sig.numerator
        
        # Start with a random note from the sequence
        melody = [random.choice(self.sequence)]
        
        # Generate the rest of the melody
        for _ in range(length - 1):
            curr = melody[-1]
            if curr in transitions:
                melody.append(random.choice(transitions[curr]))
            else:
                melody.append(random.choice(self.sequence))
        
        if output_dir and filename:
            self._save_midi(melody, output_dir, filename)
            
        return melody
    
    def _save_midi(self, melody, output_dir, filename):
        """Save the generated melody as a MIDI file."""
        melody_stream = stream.Part()
        melody_stream.append(self.time_sig)
        
        for pitch, duration in melody:
            if pitch is not None:
                n = note.Note()
                n.pitch.midi = pitch
                n.duration.quarterLength = duration
                melody_stream.append(n)
        
        melody_stream.write('midi', fp=f"{output_dir}/{filename}.mid") 