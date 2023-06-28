import librosa as libr

class key_mapper():
    """
    This class is used for mapping midi keys, given a 'mode' and a 'standard_map'.
    """
    def __init__(self,mode, standard_map):
        """
        Initialize the key_mapper object.

        Parameters:
        mode (str): Mode for key mapping. It can be either 'static' or 'random'.
        standard_map (dict): The initial key-value map to be used.

        Attributes:
        mode (str): Mode for key mapping.
        counter (int): Counter variable, initialized as 0.
        standard_map (dict): The initial key-value map to be used.
        kmap (dict): An empty dictionary to hold the final key map.
        mmap (dict): An empty dictionary to hold the MIDI key map.
        """
        self.mode = mode
        self.counter = 0
        self.standard_map = {}
        self.kmap = {}
        self.mmap = {}
        self._generate_standard_map
        self._generate_map_from_mode(mode)

    def _generate_standard_map(self):
        """
        Generates a standard keymap for an 88-key MIDI keyboard. 

        The function maps MIDI note numbers to their corresponding note names in the format 'NoteOctave' 
        (e.g., 'C4', 'A#3', etc.), where the MIDI note numbers range from 21 (A0) to 108 (C8).

        Returns:
        standard_keymap (dict): A dictionary where keys are MIDI note numbers and values are note names.
        """
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        standard_keymap = {}

        for midi_note_number in range(21, 109):
            octave = (midi_note_number // 12) - 2
            note_index = midi_note_number % 12
            note_name = note_names[note_index]
            standard_keymap[midi_note_number] = note_name + str(octave)

        self.standard_keymap = standard_keymap

    def _remap_keys(self, note_mapping):
        """
        Remap the keys in a note mapping to their MIDI equivalents.

        Parameters:
        note_mapping (dict): Dictionary with note-to-note mappings.
        """
        for key, value in note_mapping.items():
            print(key,value)
            midi_key = libr.note_to_midi(key)
            midi_value = libr.note_to_midi(value)
            note_mapping_midi[midi_key] = midi_value

        self.mmap = note_mapping_midi

    def _shuffle_dictionary_values(selfdictionary):
        """
        Shuffles the values of a given dictionary.

        Parameters:
        dictionary (dict): Dictionary with key-value pairs to be shuffled.

        Returns:
        shuffled_dictionary (dict): Dictionary with the same keys but shuffled values.
        """
        values = list(dictionary.values())
        random.shuffle(values)

        shuffled_dictionary = {}
        keys = list(dictionary.keys())
        for i in range(len(keys)):
            shuffled_dictionary[keys[i]] = values[i]

        return shuffled_dictionary

    def _generate_map_from_mode(self,mode):
        """
        Generates a key map based on the specified mode.

        Parameters:
        mode (str): Mode for key mapping. It can be either 'static' or 'random'.
        """
        if mode == 'static':
            self._remap_keys(self.kmap)

        if mode == 'random':
            self.kmap = self._shuffle_dictionary_values(self.kmap)
            self._remap_keys(self.kmap)
