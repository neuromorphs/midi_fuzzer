import mido
from pylsl import StreamInfo, StreamOutlet

class midiLSLSender:
    def __init__(self, midi_input_name):
        self.midi_input_name = midi_input_name
        self.outlet = None
        self.inport = None

    def start(self):
        # Create an LSL Stream for MIDI events
        info = StreamInfo('MIDIStream', 'MIDI', 3, 0, 'int32', 'timsterriblekeyboard')
        self.outlet = StreamOutlet(info)

        # Open MIDI input and attach callback
        self.inport = mido.open_input(self.midi_input_name)
        self.inport.callback = self.on_midi

    def stop(self):
        self.inport.callback = None  # Remove callback
        self.inport.close()  # Close MIDI port
        self.outlet = None  # Nullify outlet

    def on_midi(self, msg):
        # MIDI messages have three primary attributes: type, note, and velocity
        data = [msg.type, msg.note, msg.velocity]
        self.outlet.push_sample(data)