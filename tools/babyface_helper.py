#!/usr/bin/env python3
"""Guided hardware checks for an RME Babyface Pro or Babyface Pro FS in class-compliant mode.

For people who own such a unit and want to help this project. Each task talks you through a few steps, sends a small,
fixed set of messages to the unit, asks what you see or hear, and writes a report file that you can attach to a GitHub
issue. See docs/help-wanted/README.md.

What the tool never does: it never switches phantom power, never raises a level, and sends nothing but the messages
listed for the task (you can read them below, in the functions that start with "task_").

Needs Python 3.9 or later and one package:  pip install python-rtmidi
Try it without a unit first:                python3 tools/babyface_helper.py check --simulate
Run a task:                                 python3 tools/babyface_helper.py check
Tasks: ports, check, dim-key, clock-optical, replug
"""
import argparse
import datetime
import json
import platform
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'docs' / 'protocol' / 'reference'))
import babyface_cc as cc  # the reference codec of this repository: builds and parses bytes, sends nothing

TOOL_VERSION = 'babyface-helper-4'
STATE_LENGTH = 227          # bytes of a state message (sub ID 00)
HEADER = bytes([0xF0, 0x00, 0x20, 0x0D, 0x10])
FLAG_BITS = 0xE03F          # the bits of state word 0 that the settings message carries: 0-5 and 13-15
HEADPHONES_LEFT = 6         # level channel of the gain message
CELL_PLAYBACK_1_TO_HEADPHONES_LEFT = (2, 12)    # (output, source) of the mixer
CELL_PLAYBACK_2_TO_HEADPHONES_RIGHT = (3, 13)


# ---- talking to the unit ---------------------------------------------------------------------------------------------
class RtMidiTransport:
    """One MIDI output and input of the computer, through the package python-rtmidi."""

    def __init__(self, out_index, in_index):
        import rtmidi
        self.out, self.inp, self.frames = rtmidi.MidiOut(), rtmidi.MidiIn(), []
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        self.inp.set_callback(lambda event, data=None: self.frames.append(bytes(event[0])))
        self.name = self.out.get_ports()[out_index]
        self.out.open_port(out_index)
        self.inp.open_port(in_index)

    def send(self, frame):
        self.out.send_message(list(frame))

    def collect(self, seconds):
        time.sleep(seconds)
        got, self.frames = self.frames, []
        return got

    def close(self):
        self.out.close_port()
        self.inp.close_port()

    def hint(self, what):
        pass  # only the simulated unit reacts to hints ("the helper pressed DIM")


def port_pairs():
    """(output index, input index, name) for every MIDI port that exists in both directions, Babyface ports first."""
    import rtmidi
    outs, ins = rtmidi.MidiOut().get_ports(), rtmidi.MidiIn().get_ports()
    pairs = [(o, ins.index(name), name) for o, name in enumerate(outs) if name in ins]
    return sorted(pairs, key=lambda p: ('babyface' not in p[2].lower(), p[0]))


def find_unit(simulate=False, port=None):
    """Asks every candidate port for its state and returns a transport for the one that answers like a Babyface."""
    if simulate:
        return SimulatedUnit()
    try:
        pairs = port_pairs()
    except ImportError:
        sys.exit('The package python-rtmidi is missing. Install it with:  pip install python-rtmidi')
    if port is not None:
        pairs = [p for p in pairs if p[0] == port]
    for out_index, in_index, name in pairs:
        transport = RtMidiTransport(out_index, in_index)
        transport.send(cc.request_state())
        if any(is_state(f) for f in transport.collect(0.6)):
            return transport
        transport.close()
    sys.exit('No port answered like a Babyface in class-compliant mode. Run the task "ports" to see what the computer '
             'offers, and check that the unit shows CC when it starts (docs/help-wanted/README.md, "Class-compliant mode").')


def is_state(frame):
    return len(frame) == STATE_LENGTH and frame[:5] == HEADER and frame[5] == 0x00


def read_state(transport):
    """Asks for the state and returns the parsed fields (see parse_state in the codec), or stops if the unit is silent."""
    for attempt in range(4):
        transport.send(cc.request_state())
        for frame in transport.collect(0.4):
            if is_state(frame):
                return cc.parse_state(frame)
    sys.exit('The unit stopped answering. Nothing more was sent. Check the cable and start again.')


def summary(state):
    """The fields of a state that go into the report and onto the screen."""
    w0 = state['words'][0]
    return {'word_0': '0x%08X' % w0, 'main_raw': list(state['main_raw']), 'headphones_raw': list(state['phones_raw']),
            'as_raw': list(state['as_raw']), 'mic_gain_db': list(state['mic_gain_db']),
            'line_gain_half_db': list(state['line_gain_half_db']), 'settings_bits_0_to_5': state['settings'],
            'phantom_48v': list(state['phantom_48v']), 'dim_flag_bit_13': state['dim'],
            'bits_14_15': state['global_mute_bits_14_15'], 'bit_30': bool(w0 >> 30 & 1)}


# ---- the report ------------------------------------------------------------------------------------------------------
class Report:
    def __init__(self, task, transport, answers=None):
        self.transport, self.answers = transport, list(answers) if answers is not None else None
        self.data = {'tool': TOOL_VERSION, 'task': task, 'started_utc': now(), 'simulated': isinstance(transport, SimulatedUnit),
                     'computer': {'system': platform.system(), 'release': platform.release(), 'python': platform.python_version()},
                     'midi_port_name_with_digits_masked': mask(transport.name), 'steps': [], 'sent': []}

    def say(self, text=''):
        print(text)

    def ask(self, question, choices=None):
        """Asks the helper; with choices the answer must be one of them. Every answer goes into the report."""
        while True:
            prompt = question + (' [' + ' / '.join(choices) + '] ' if choices else ' ')
            answer = self.answers.pop(0) if self.answers is not None else input(prompt).strip()
            if self.answers is not None:
                print(prompt + answer)
            if not choices or answer.lower() in choices:
                self.data['steps'].append({'asked': question, 'answered': answer.lower() if choices else answer})
                return answer.lower() if choices else answer
            print('Please type one of: ' + ', '.join(choices))

    def send(self, frame, why):
        frame = bytes(frame)
        self.data['sent'].append({'why': why, 'hex': frame.hex(' ').upper()})
        self.transport.send(frame)
        time.sleep(0.25)

    def state(self, label):
        s = summary(read_state(self.transport))
        self.data['steps'].append({'read': label, 'state': s})
        return s

    def note(self, key, value):
        self.data[key] = value

    def save(self):
        self.data['finished_utc'] = now()
        name = 'babyface-report-%s-%s.json' % (self.data['task'], datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        Path(name).write_text(json.dumps(self.data, indent=1) + '\n')
        print('\nReport written: %s\nPlease attach this file to a GitHub issue (docs/help-wanted/README.md, "Sending your result").' % name)
        return name


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def mask(name):
    """Port names carry the serial number of the unit; the report keeps the name with every run of four or more
    digits replaced (the number of the port stays readable)."""
    return re.sub(r'\d{4,}', lambda found: '#' * len(found.group()), name)


def confirm(report, lines):
    report.say('\n'.join(lines))
    if report.ask('Type yes to start, anything else to stop.') != 'yes':
        sys.exit('Stopped. Nothing was sent.')


def about_the_unit(report):
    report.ask('Which unit is it?', ['pro', 'pro fs'])
    report.ask('How is it powered right now: over USB alone, or by its own power supply?', ['usb', 'supply'])
    report.ask('What is it connected to (for example: MacBook, Windows PC, Linux PC)?')


# ---- the tasks -------------------------------------------------------------------------------------------------------
def task_check(report):
    """Reads the state and makes one small write: the left headphone level one step (0.5 dB) down and back up.

    Sends: the state request; the gain message for the left headphone channel, twice (down, then the value found)."""
    confirm(report, ['This task reads the state of your Babyface a few times. Then it lowers the left headphone level by',
                     'one step of 0.5 dB and puts it back, to see that a write arrives and is reported.', ''])
    about_the_unit(report)
    first = report.state('first reading')
    report.say('The unit reports: Main %s, headphones %s (raw values; 243 is 0 dB, each step is 0.5 dB), microphone gains %s dB.'
               % (first['main_raw'], first['headphones_raw'], first['mic_gain_db']))
    time.sleep(1.0)
    second = report.state('second reading, one second later')
    keys = ('main_raw', 'headphones_raw', 'as_raw', 'mic_gain_db', 'line_gain_half_db', 'settings_bits_0_to_5')
    report.note('two_readings_agree', all(first[k] == second[k] for k in keys))
    level = first['headphones_raw'][0]
    if 60 <= level <= 243:
        report.send(cc.set_output_level(HEADPHONES_LEFT, level - 1), 'left headphone level one step down, to raw %d' % (level - 1))
        down = report.state('after one step down')
        report.send(cc.set_output_level(HEADPHONES_LEFT, level), 'left headphone level back to raw %d' % level)
        back = report.state('after the step back')
        report.note('write_reported', {'down': down['headphones_raw'][0] == level - 1, 'back': back['headphones_raw'][0] == level,
                                       'right_channel_unchanged': down['headphones_raw'][1] == first['headphones_raw'][1]})
        report.say('Write test: %s' % ('the unit reported both steps.' if all(report.data['write_reported'].values()) else 'NOT as expected, see the report.'))
    else:
        report.note('write_reported', 'not tried: the left headphone level stood at raw %d (muted or out of range)' % level)
        report.say('Write test left out: the left headphone level stands at raw %d.' % level)


def task_dim_key(report):
    """What the DIM key of the unit does in this mode, and whether its lamp follows the dim flag.

    Sends: the state request; the settings message for bit 13 (the dim flag), twice (set, clear). The flag changes no
    level by itself, as measured on the project's unit."""
    confirm(report, ['This task looks at the DIM key. You press it twice, the tool reads what the unit reports.',
                     'Then the tool sets the dim flag by a message and clears it again, and asks whether the DIM lamp lights.',
                     'Pressing DIM lowers the selected output by 20 dB; the second press brings it back.', ''])
    about_the_unit(report)
    before = report.state('before')
    report.ask('On the unit, press OUT until "Ch 1/2" is selected. Then press DIM once. Press Enter here when done.')
    report.transport.hint('dim key')
    pressed = report.state('after DIM was pressed once')
    report.ask('Is the DIM lamp of the unit lit now?', ['yes', 'no', 'unsure'])
    report.ask('Press DIM once more. Press Enter here when done.')
    report.transport.hint('dim key')
    released = report.state('after DIM was pressed again')
    report.note('dim_key', {'flag_followed_the_key': [before['dim_flag_bit_13'], pressed['dim_flag_bit_13'], released['dim_flag_bit_13']],
                            'main_raw': [before['main_raw'], pressed['main_raw'], released['main_raw']],
                            'headphones_raw': [before['headphones_raw'], pressed['headphones_raw'], released['headphones_raw']]})
    settings = int(released['word_0'], 16) & FLAG_BITS
    if released['dim_flag_bit_13']:
        report.say('The dim flag is still set after the second press; the message part is left out.')
        return
    report.send(cc.set_input_setting(13, True, settings), 'dim flag set by message (bit 13)')
    flagged = report.state('after the dim flag was set by message')
    report.ask('Is the DIM lamp lit now? (No key was pressed; the tool set the flag.)', ['yes', 'no', 'unsure'])
    report.send(cc.set_input_setting(13, False, settings | 0x2000), 'dim flag cleared by message')
    cleared = report.state('after the dim flag was cleared by message')
    report.note('dim_flag_by_message', {'reported': [flagged['dim_flag_bit_13'], cleared['dim_flag_bit_13']],
                                        'main_raw': [released['main_raw'], flagged['main_raw'], cleared['main_raw']]})


def device_setting(mask_bit, state_bits):
    """Device settings message (sub ID 00): which bit changes, and its new value in the state part. The project's unit
    followed only the bit named in the first half; the tasks send no other bit in the state part."""
    return cc.frame(cc.SUB_STATE, [mask_bit | (state_bits << 16)])


def task_clock_optical(report):
    """Clock source and optical output format, switched by message.

    The clock source needs nothing from you: the state of the unit shows it (bit 30 of word 0 follows the bit written, as
    found on the project's unit), so the tool switches it, reads it and puts it back. The optical format does not show
    in the state, and the unit's own display stays dark while a computer asks for the state; so that part runs only if
    a device at the optical OUTPUT shows what it receives. On the project's unit the display showed ADAT with bit 10
    clear and S/PDIF with it set; what is missing is the same seen at a receiving device.

    Sends: the state request; the device settings message for bit 0 (clock source), three times at most; with a device
    at the optical output, the device settings message for bit 10 (optical format), three times at most. Bit 6 of the
    state part stays clear in all of them."""
    confirm(report, ['This task switches the clock source of your Babyface by message, reads it back from the state of the unit',
                     'and puts it back. If a device at the optical OUTPUT shows what it receives (ADAT or S/PDIF), it also',
                     'switches the format of the optical output and asks what that device shows.',
                     'Stop all playback and turn your monitors and headphones down first: switching can click.', ''])
    about_the_unit(report)
    receiver = report.ask('Is a device connected to the optical OUTPUT of the Babyface that shows what it receives?', ['yes', 'no'])

    # clock source: bit 0 of the device settings; bit 30 of state word 0 reports it
    first = report.state('before the clock source is switched')['bit_30']
    read_back = {}
    for bit_0 in ((0, 1) if first else (1, 0)):   # the other value first, then the value found
        report.send(device_setting(0x001, bit_0), 'clock source: bit 0 %s' % ('set' if bit_0 else 'clear'))
        read_back[bit_0] = report.state('after bit 0 was %s' % ('set' if bit_0 else 'cleared'))['bit_30']
    report.note('clock_source', {'state_bit_30_at_the_start': first, 'with_bit_0_set': read_back[1], 'with_bit_0_clear': read_back[0],
                                 'state_follows_the_bit': read_back[1] is True and read_back[0] is False})
    if read_back[1] is True and read_back[0] is False:
        report.say('Clock source: the state followed the bit both ways, and it is back where it was.')
    else:
        report.say('Clock source: the state did NOT follow the bit as on the project\'s unit; see the report. The last message sent the value found at the start.')

    # optical format: bit 10; only a device at the optical output can show it
    if receiver == 'no':
        report.note('optical_format', 'not tried: no device at the optical output')
        report.say('Optical format left out: without a device at the optical output there is nothing to read it from.')
        return
    start_format = report.ask('What does the device at the optical output show that it receives right now?', ['adat', 'spdif', 'nothing', 'unsure'])
    seen = {}
    for bit_10 in (1, 0):
        report.send(device_setting(0x400, 0x400 if bit_10 else 0), 'optical format: bit 10 %s' % ('set' if bit_10 else 'clear'))
        seen[bit_10] = report.ask('What does the device at the optical output show now?', ['adat', 'spdif', 'nothing', 'unsure'])
    report.note('optical_format', {'at_the_start': start_format, 'with_bit_10_set': seen[1], 'with_bit_10_clear': seen[0]})
    if seen[1] != seen[0] and start_format in (seen[1], seen[0]):
        if seen[1] == start_format:
            report.send(device_setting(0x400, 0x400), 'optical format back to what it was at the start')
        report.say('The optical format is back at %s.' % start_format.upper())
    else:
        report.say('The tool could not tell what the format was at the start; bit 10 is clear now, which was ADAT on the '
                   'project\'s unit. If your device no longer locks, run the task again and note with which value it locks.')


def task_replug(report):
    """Does the unit keep its mixer when the USB cable is pulled while its own power supply keeps it alive?

    Sends: the state request; two mixer cells (playback 1 to the left and playback 2 to the right headphone channel, at
    0 dB), up to three times; and, if you say so at the end, the same two cells with level 0."""
    confirm(report, ['This task needs the power supply of the Babyface (or a second USB power source at its power socket)',
                     'and headphones at the unit. The tool sends the playback of your computer to the headphones. You pull the',
                     'USB cable for a few seconds and plug it in again, and say whether the headphones still play.',
                     'Turn the headphone level down first and play something quiet through the Babyface.', ''])
    about_the_unit(report)
    cells = [cc.set_mixer(*CELL_PLAYBACK_1_TO_HEADPHONES_LEFT, cc.UNITY), cc.set_mixer(*CELL_PLAYBACK_2_TO_HEADPHONES_RIGHT, cc.UNITY)]
    before = report.state('before')
    for cell in cells:
        report.send(cell, 'playback to the headphones at 0 dB')
    heard = report.ask('Play music on the computer through the Babyface. Do you hear it on the headphones?', ['yes', 'no'])
    if heard == 'no':
        report.say('Without sound on the headphones this task cannot go on. Check the headphone level (turn the encoder with OUT on "Phones").')
        return
    report.ask('Now pull the USB cable of the Babyface. Leave its power supply connected. Wait five seconds, plug the USB cable in again, wait until the computer shows the unit, and start the music again. Press Enter here when done.')
    report.ask('Did the unit stay on (lamps lit) while the USB cable was out?', ['yes', 'no', 'unsure'])
    report.ask('Before anything else is sent: do you hear the music on the headphones?', ['yes', 'no'])
    if not report.data['simulated']:   # the computer gave the unit new ports when it came back
        try:
            report.transport.close()
        except Exception:
            pass
        report.transport = find_unit()
    after = report.state('after the replug')
    report.note('levels_kept', {'main_raw': [before['main_raw'], after['main_raw']], 'headphones_raw': [before['headphones_raw'], after['headphones_raw']]})
    for cell in cells:
        report.send(cell, 'playback to the headphones at 0 dB, sent again')
    report.ask('The two cells were sent again. Do you hear the music on the headphones now?', ['yes', 'no'])
    if report.ask('Leave the playback on the headphones, or switch it off again?', ['leave', 'off']) == 'off':
        for output, source in (CELL_PLAYBACK_1_TO_HEADPHONES_LEFT, CELL_PLAYBACK_2_TO_HEADPHONES_RIGHT):
            report.send(cc.set_mixer(output, source, 0), 'playback off the headphones')


def task_ports(simulate):
    if simulate:
        print('Simulated unit: no real ports are used.')
        return
    try:
        pairs = port_pairs()
    except ImportError:
        sys.exit('The package python-rtmidi is missing. Install it with:  pip install python-rtmidi')
    print('MIDI ports that exist as input and output (index, name with the serial number masked):')
    for out_index, in_index, name in pairs:
        print('  %d  %s' % (out_index, mask(name)))
    if not pairs:
        print('  none. Is the unit connected, and does it show CC when it starts?')


TASKS = {'check': task_check, 'dim-key': task_dim_key, 'clock-optical': task_clock_optical, 'replug': task_replug}


# ---- a unit that exists only in this program, for a dry run and for the tests ----------------------------------------
class SimulatedUnit:
    """Answers like the project's unit did, as far as the tasks need it. Not a model of the hardware."""
    name = 'Simulated Babyface Pro (12345678) Port 2'

    def __init__(self):
        self.words = [0] * 44
        self.words[0] = 0x0090000C
        self.words[1] = 183 | (183 << 9)
        self.words[2] = (214 << 14) | (214 << 23)
        self.words[3] = 59 | (59 << 9) | (12 << 19)
        self.out, self.received, self.cells, self.device = [], [], {}, 0x000

    def send(self, frame):
        frame = bytes(frame)
        self.received.append(frame)
        sub, words = cc.parse_frame(frame)
        if sub == 0x10:
            self.out.append(bytes(cc.frame(cc.SUB_STATE, self.words)))
            self.out.append(bytes(cc.frame(0x02, [0] * 40)))
        elif sub == 0x04:
            channel, value = words[0] & 0xFFFF, words[0] >> 16
            field = {4: (1, 0), 5: (1, 9), 6: (2, 14), 7: (2, 23), 8: (3, 0), 9: (3, 9)}.get(channel)
            if field:
                word, shift = field
                self.words[word] = (self.words[word] & ~(0xFF << shift)) | (value << shift)
        elif sub == 0x03:
            mask_bits, state = words[0] & 0xFFFF, words[0] >> 16
            self.words[0] = (self.words[0] & ~mask_bits) | (state & mask_bits)
        elif sub == 0x01:
            self.cells[words[0] & 0xFFF] = words[0] >> 12
        elif sub == 0x00:
            mask_bits, state = words[0] & 0xFFFF, words[0] >> 16
            self.device = (self.device & ~mask_bits) | (state & mask_bits)
            self.words[0] = (self.words[0] & ~(1 << 30)) | ((self.device & 1) << 30)   # as on the project's unit

    def collect(self, seconds):
        got, self.out = self.out, []
        return got

    def hint(self, what):
        if what == 'dim key':   # as TotalMix FX did on a Mac: the flag, and the Main level 40 raw steps lower
            on = not self.words[0] >> 13 & 1
            self.words[0] ^= 1 << 13
            for shift in (0, 9):
                raw = (self.words[1] >> shift) & 0xFF
                self.words[1] = (self.words[1] & ~(0xFF << shift)) | ((raw - 40 if on else raw + 40) << shift)

    def close(self):
        pass


def main(argv=None, answers=None):
    parser = argparse.ArgumentParser(description='Guided checks for an RME Babyface Pro / Pro FS in class-compliant mode.')
    parser.add_argument('task', choices=['ports'] + sorted(TASKS))
    parser.add_argument('--simulate', action='store_true', help='use a simulated unit: a dry run without hardware')
    parser.add_argument('--port', type=int, help='index of the MIDI port, as the task "ports" lists it')
    args = parser.parse_args(argv)
    if args.task == 'ports':
        return task_ports(args.simulate)
    transport = find_unit(args.simulate, args.port)
    report = Report(args.task, transport, answers)
    print('Found the unit on: %s\n' % mask(transport.name))
    try:
        TASKS[args.task](report)
    except KeyboardInterrupt:
        print('\nStopped by Ctrl-C. Nothing more is sent; what was done so far is in the report.')
    finally:
        name = report.save()
        report.transport.close()
    return name


if __name__ == '__main__':
    main()
