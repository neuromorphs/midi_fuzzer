
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
python midi_in.py
```
Now, you can start playing your keyboard! The midi output, with some keys remapped, will come from the connected computer.

## Future Features
We are planning to add the following features:
- **Modes**: Various remapping modes including time-dependent remapping, sequence-dependent remapping, and full random remapping.
- **'Rage Mode'**: This mode will transpose your music into the wrong key at the perfect moment to add an element of unexpectedness.
```
```