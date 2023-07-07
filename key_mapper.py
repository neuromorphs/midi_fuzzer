import librosa as libr
import random

class key_mapper():
    """
    This class is used for mapping midi keys, given a 'mode' and a 'standard_map'.
    """
    def __init__(self,mode, kmap_config=None):
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
        #self.counter = None if mode not in ['MTR', 'SRZ','RRZ','RAGE'] else 0
        self.counter = 0
        self.standard_map = {}
        self.change = random.randint(5,30)
        self.currently_random = False
        self.kmap = {}
        self.mmap = {}
        self._generate_standard_map()
        if kmap_config is not None:
            self.kmap_config = kmap_config
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
        standard_map = {}

        for midi_note_number in range(21, 109):
            octave = (midi_note_number // 12) - 2
            note_index = midi_note_number % 12
            note_name = note_names[note_index]
            standard_map[note_name+str(octave)] = note_name + str(octave)
            standard_keymap[midi_note_number] = note_name + str(octave)

        self.standard_map = standard_map
        self.kmap = standard_map

    def _shift_remap_zone(self):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        
        for key, value in self.kmap_config.kmap.items():
            start = key
            end = value

        #start, end = self.kmap_config.kmap.items()
        start_midi = libr.note_to_midi(start)
        end_midi = libr.note_to_midi(end)

        shift = random.randint(-self.kmap_config.shift_max,self.kmap_config.shift_max)

        shifted_map = {}
        shifted_keymap = {}
        for midi_note_number in range(start_midi, end_midi):
            smidi_note_number = midi_note_number + shift
            soctave = (smidi_note_number // 12) - 2
            snote_index = smidi_note_number % 12
            snote_name = note_names[snote_index]
            octave = (midi_note_number // 12) - 2
            note_index = midi_note_number % 12
            note_name = note_names[note_index]
            shifted_map[note_name+str(octave)] = snote_name + str(soctave)
            shifted_keymap[midi_note_number] = snote_name + str(soctave)

        return shifted_keymap, shifted_map
    
    def _random_remap_zone(self):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        start, end = self.kmap_config.kmap.items()
        start_midi = libr.note_to_midi(start)
        end_midi = libr.note_to_midi(end)

        shifted_map = {}
        shifted_keymap = {}
        for midi_note_number in range(start_midi, end_midi):
            octave = (midi_note_number // 12) - 2
            note_index = midi_note_number % 12
            note_name = note_names[note_index]
            shifted_map[note_name+str(octave)] = snote_name + str(soctave)
            shifted_keymap[midi_note_number] = snote_name + str(soctave)

        shuffled_keymap = self._shuffle_dictionary_values(shifted_keymap)

        return shuffled_keymap

    def _remap_keys(self, note_mapping):
        """
        Remap the keys in a note mapping to their MIDI equivalents.

        Parameters:
        note_mapping (dict): Dictionary with note-to-note mappings.
        """
        note_mapping_midi = {}
        for key, value in note_mapping.items():
            print(key,value)
            midi_key = libr.note_to_midi(key)
            midi_value = libr.note_to_midi(value)
            note_mapping_midi[midi_key] = midi_value

        self.mmap = note_mapping_midi

    def _remap_one_key(self, kmap_config):
        """
        Remap the keys in a note mapping to their MIDI equivalents.

        Parameters:
        note_mapping (dict): Dictionary with note-to-note mappings.
        """
        note_mapping_midi = {}
        key2map = kmap_config.change_keys[np.argwhere(self.counter == kmap_config.change_timings)]

        midi_key = libr.note_to_midi(key2map[0])
        midi_value = libr.note_to_midi(key2map[1])
        note_mapping_midi[midi_key] = midi_value

        self.mmap = note_mapping_midi

    def _shuffle_dictionary_values(self,dictionary):
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
    
    def inc_counter(self):
        self.counter = self.counter+1
        print(self.counter)
        print(self.change)
        if self.mode == 'schedule':
            if self.counter in self.kmap_config.change_timing:
                self._generate_map_from_mode(self.mode)
            elif self.counter -1 in self.kmap_config.change_timing:
                self._remap_keys(self.standard_map)
        elif self.mode == 'delay_ramp' or self.mode == 'velocity_ramp' or self.mode == 'standard':
            pass
        else:
            if self.counter>self.change and self.counter is not None:
                self.currently_random = not self.currently_random
                self.counter = 0
                if self.currently_random:
                    self.change = self.kmap_config.random_length
                else:
                    self.change = random.randint(20,self.kmap_config.periodicity)
                self._generate_map_from_mode(self.mode)
            else:
                pass

    def _generate_map_from_mode(self,mode):
        """
        Generates a key map based on the specified mode.

        Parameters:
        mode (str): Mode for key mapping. It can be either 'static' or 'random'.
        """
        
        #standard keyboard
        if mode == 'standard':
            self._remap_keys(self.standard_map)

        #statically remaps a set of keys for the entire experiment
        if mode == 'static':
            self._remap_keys(self.kmap_config)

        #Multikey time random - randomly flips a set of keys to a new set static set of keys and back ove some number of keystrokes
        if mode == 'MTR':
            if self.currently_random:
                self._remap_keys(self.standard_map)
            else:
                self._remap_keys(self.kmap_config)

        #Random Zone remap - randomizes a continuous section of keys
        if mode == 'RRZ':
            if self.currently_random:
                self._remap_keys(self.standard_map)
            else:
                random_remap = self._random_remap_zone()
                self._remap_keys(random_remap)

        #Random Zone shift - transposes a continuous section of keys
        if mode == 'SRZ':
            if self.currently_random:
                shift_keymap, shift_map = self._shift_remap_zone()
                self._remap_keys(shift_map)
            else:
                self._remap_keys(self.standard_map)


        if mode == 'schedule':
            if self.currently_random:
                self._remap_keys(self.standard_map)
            else:
                self._remap_one_key(self.kmap_config)

        #Fully randomizes the keyboard
        if mode == 'random':
            self.kmap = self._shuffle_dictionary_values(self.kmap)
            self._remap_keys(self.kmap)
