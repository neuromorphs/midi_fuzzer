import mido
import fluidsynth
import time
import librosa as libr
import key_mapper as kmp
from mido import Message, MidiFile, MidiTrack

# Create MIDI file for the played music
midi_played = MidiFile()
track_played = MidiTrack()
midi_played.tracks.append(track_played)

# Create MIDI file for the heard music
midi_heard = MidiFile()
track_heard = MidiTrack()
midi_heard.tracks.append(track_heard)

# Create a MIDI input port
midi_in = mido.open_input()

# Initialize the FluidSynth synthesizer
fs = fluidsynth.Synth(gain=1.0,samplerate=44100.0)
fs.start()

# Load a SoundFont file for the synthesizer
soundfont_file = 'Casio PX-860 Concert Grand Piano.sf2'
sfid = fs.sfload(soundfont_file)
fs.program_select(0, sfid, 0, 0)

# Define the note mapping
note_mapper = kmp.key_mapper('random')
note_mapping = note_mapper.kmap
note_mapping_midi = note_mapper.mmap
# note_mapping = {
#     'G4': 'A6',  # Map G4 to A4
#     'C4':'D6'
# }
# note_mapping_midi = {}
# for key, value in note_mapping.items():
#     print(key,value)
#     midi_key = libr.note_to_midi(key)
#     midi_value = libr.note_to_midi(value)
#     note_mapping_midi[midi_key] = midi_value
print(note_mapping_midi)

# Process incoming MIDI messages
for msg in midi_in:
    print(msg)
    track_played.append(msg)

    # Check if the message is a note-on event
    if msg.type == 'note_on' and msg.velocity > 0:
        # Check if the note is in the mapping
        if msg.note in note_mapping_midi.keys():
            # Get the new note value from the mapping
            new_note = note_mapping_midi[msg.note]

            # Resynthesize the new note using FluidSynth
            fs.noteon(0, new_note, msg.velocity)

            # Save the heard note in a different list
            track_heard.append(Message('note_on', note=new_note, velocity=msg.velocity))
        else:
            fs.noteon(0, msg.note, msg.velocity)

            # Save the heard note in a different list
            track_heard.append(msg)
    # Check if the message is a note-off event
    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
        # Check if the note is in the mapping
        if msg.note in note_mapping_midi.keys():
            # Get the new note value from the mapping
            new_note = note_mapping_midi[msg.note]

            # Resynthesize the new note using FluidSynth
            fs.noteoff(0, new_note)

            # Save the heard note in a different list
            track_heard.append(Message('note_off', note=new_note, velocity=0))
        else:
            fs.noteoff(0, msg.note)

            # Save the heard note in a different list
            track_heard.append(msg)

    midi_played.save('midi_played.mid')
    midi_heard.save('midi_heard.mid')

# Stop the FluidSynth synthesizer
fs.delete()
fs.stop()
# Close the MIDI input port
midi_in.close()