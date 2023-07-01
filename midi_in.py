import mido
import fluidsynth
import time
import librosa as libr
import key_mapper as kmp
import argparse
import sys
import key_configs
import asyncio
from pylsl import StreamInfo, StreamOutlet


# Function to parse command line arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description="Script to run MIDI sound synthesis with custom mappings.")
    parser.add_argument("mode", nargs=1, help="Mode to use for key_mapper.")
    return parser.parse_args(args)

# Function to initialize the FluidSynth synthesizer
def initialize_synth(soundfont_file):
    fs = fluidsynth.Synth(gain=2.0,samplerate=44100.0)
    fs.start()
    sfid = fs.sfload(soundfont_file)
    fs.program_select(0, sfid, 0, 0)
    return fs

async def play_note_later(fs, chan, key, vel, delay):
    await asyncio.sleep(delay)  # Introduce the delay.
    fs.noteon(chan, key, vel)

async def stop_note_later(fs, chan, key, delay):
    await asyncio.sleep(delay)  # Introduce the delay.
    fs.noteoff(chan, key)

# Function to handle incoming MIDI messages
def process_midi_messages(midi_in, nm, fs):
    #breakpoint()
    #midi_input_name = mido.get_input_names()[0]  # Select the correct one if there are multiple
    #sender = midiLSLSender(midi_input_name)

    #sender.start()
    # Get MIDI input name
    midi_input_name = mido.get_input_names()[0]  # Select the correct one if there are multiple

    # Create an LSL Stream for MIDI events
    info = StreamInfo('MIDIStream', 'MIDI', 3, 100, 'int32', 'timsterriblekeyborb')
    outlet = StreamOutlet(info)

    # Define MIDI input callback
    def on_midi(msg):
        # MIDI messages have three primary attributes: type, note, and velocity
        data = [0, msg.note, msg.velocity]
        outlet.push_sample(data)

    # Open MIDI input and attach callback
    inport = mido.open_input(midi_input_name)
    inport.callback = on_midi

    # Your main loop here. MIDI events will automatically trigger the on_midi callback.
    delay=0
    #vel_attn = nm.kmap_config.start_attn
    for msg in midi_in:
        #print("played note: " + msg)
        # Handle note-on event
        if msg.type == 'note_on' and msg.velocity > 0:
            nm.inc_counter()
            if nm.mode == 'delay_ramp':
                if nm.counter > nm.kmap_config.start_delay:
                    delay = nm.kmap_config.rate * (nm.counter - nm.kmap_config.start_delay)
                    if delay > nm.kmap_config.shift_max:
                        delay = nm.kmap_config.shift_max
                print('Delay magnitude:'+str(delay))
                asyncio.run(play_note_later(fs,0,msg.note,msg.velocity,delay))
            elif nm.mode == 'velocity_ramp':
                if nm.counter > nm.kmap_config.start_vel:
                    vel = nm.kmap_config.rate * (nm.counter - nm.kmap_config.start_vel)
                    vel_attn = nm.kmap_config.start_attn + vel
                    if vel_attn>nm.kmap_config.shift_max:
                        vel_attn = nm.kmap_config.shift_max
                print('Velocity attenutation:'+str(vel_attn))
                fs.noteon(0,msg.note, int(msg.velocity/vel_attn))
            else:
                if msg.note in nm.mmap.keys():
                    #print("Remapped note: "+ nm.mmap[msg.note])
                    fs.noteon(0, nm.mmap[msg.note], msg.velocity)
                else:
                    fs.noteon(0, msg.note, msg.velocity)
        # Handle note-off event
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if nm.mode == 'delay_ramp':
                asyncio.run(stop_note_later(fs,0,msg.note,delay))
            else:
                if msg.note in nm.mmap.keys():
                    #print("Remapped note: "+ nm.mmap[msg.note])
                    fs.noteoff(0, nm.mmap[msg.note])
                else:
                    fs.noteoff(0, msg.note)
        #sender.stop()

def main(args):
    # Parse command line arguments
    parsed_args = parse_args(args)

    # Create a MIDI input port
    midi_in = mido.open_input()

    # Initialize the FluidSynth synthesizer
    soundfont_file = 'Casio PX-860 Concert Grand Piano.sf2'
    fs = initialize_synth(soundfont_file)

    # Define the note mapping

    if parsed_args.mode[0] == 'MTR':
        kmap_config = key_configs.static_multi_remap()
    elif parsed_args.mode[0] == 'RRZ':
        kmap_config = key_configs.random_zone_remap()
    elif parsed_args.mode[0] == 'SRZ':
        kmap_config = key_configs.random_zone_shift()
    elif parsed_args.mode[0] == 'schedule':
        kmap_config = key_configs.schedule()
    elif parsed_args.mode[0] == 'delay_ramp':
        kmap_config = key_configs.delay_ramp()
    elif parsed_args.mode[0] == 'velocity_ramp':
        kmap_config = key_configs.velocity_ramp()
    else:
        kmap_config = None


    note_mapper = kmp.key_mapper(parsed_args.mode[0], kmap_config = kmap_config)

    print(note_mapper.mmap)

    # Process incoming MIDI messages
    process_midi_messages(midi_in, note_mapper, fs)

    # Cleanup after done
    fs.delete()
    fs.stop()
    midi_in.close()

if __name__ == "__main__":
    main(sys.argv[1:])
