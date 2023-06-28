# midi_fuzzer

It goofs up your midi output


Requirments:
mido
pyfluidsynth (https://github.com/FluidSynth/fluidsynth/wiki/Download)
librosa
A soundfont file (preferably something like a piano)
    - for testing we used 'Casio PX-860 Concert Grand Piano.sf2'

Usage:
Plug your computer into the keyboard using the midi port on the keyboard, ours is USB-B, you may need an adapter.
>python midi_in.py
Start playing! the output will come from the connected computer with some keys remapped.

Future features:
modes : time dependent / sequence dependent remapping, full random, 'rage mode' (transpose into the wrong key at the right time).