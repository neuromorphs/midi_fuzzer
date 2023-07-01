
```markdown
# midi_fuzzer

This tool is designed to add an element of surprise to your midi output.

## Requirements
- `mido`
- `pyfluidsynth` ([download link](https://github.com/FluidSynth/fluidsynth/wiki/Download))
- `librosa`
- A soundfont file (we recommend using a piano soundfont, like 'Casio PX-860 Concert Grand Piano.sf2')

## Usage
First, connect your computer to the keyboard using the midi port. The port we used was a USB-B type; you might need an adapter based on your keyboard's port type.

Then, run the `midi_in.py` script in your terminal:
```
> python midi_in.py
```
Now, you can start playing your keyboard! The midi output, with some keys remapped, will come from the connected computer.

##Current modes:
- **none**   : Does nothing, you have a normal keyboard.
- **static** : Statically remaps a set of keys to another set of keys
- **random** : Shuffles the entire keyboard statically.
- **MTR**    : Multikey Time Random - randomly (in time) remaps a set of keys to a different set of keys (static set)
- **RRZ**    : Random Remap Zone - Randomly (in time) remaps a contiguous section of the keyboard (shuffles the keys in a region)
- **SRZ**    : Shift Random Zone - Transposes a section of keyboard randomly (in time) and by a random amount up or down in pitch.

## Future Features
We are planning to add the following features:
- **Modes**: sequence-dependent remapping and RAGE mode.
- **'Rage Mode'**: This mode will transpose your music into the wrong key at the perfect moment to add an element of unexpectedness.
```
```