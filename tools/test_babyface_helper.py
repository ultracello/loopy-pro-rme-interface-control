"""Tests of tools/babyface_helper.py. No hardware is touched: the tasks run against the simulated unit, and once
against virtual MIDI ports that another process serves (left out when python-rtmidi is not installed, and on systems
without virtual ports).  Run:  python3 tools/test_babyface_helper.py"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import babyface_helper as helper
from babyface_helper import cc

START = ['yes', 'pro fs', 'usb', 'a test']   # the confirmation and the three questions about the unit


def run(task, answers, unit=None):
    """Runs a task against a simulated unit with the answers given. Returns (report, unit)."""
    unit = unit or helper.SimulatedUnit()
    with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
        old = os.getcwd()
        os.chdir(folder)
        try:
            original, helper.find_unit = helper.find_unit, lambda simulate=False, port=None: unit
            try:
                name = helper.main([task, '--simulate'], answers)
            except SystemExit:
                name = sorted(Path('.').glob('babyface-report-*.json'))[-1]
            finally:
                helper.find_unit = original
            report = json.loads(Path(name).read_text())
        finally:
            os.chdir(old)
    return report, unit


def harmless(frame, start):
    """True when a frame is one the tasks may send, given the state the unit started in."""
    sub, words = cc.parse_frame(frame)
    if sub == 0x10:
        return not words
    word = words[0]
    if sub == 0x04:    # only the left headphone level, and never above where it stood
        return len(words) == 1 and word & 0xFFFF == 6 and (word >> 16) <= start['phones_raw'][0]
    if sub == 0x03:    # only the dim flag; phantom power bits as they were, which is off
        return len(words) == 1 and word & 0xFFFF == 0x2000 and (word >> 16) & 3 == start['settings'] & 3
    if sub == 0x01:    # only playback to the headphones, at 0 dB or off
        return len(words) == 1 and word & 0xFFF in (64, 91) and (word >> 12) in (0, cc.UNITY)
    if sub == 0x00:    # only optical format or clock source, and bit 6 of the state part clear
        return len(words) == 1 and word & 0xFFFF in (0x400, 0x001) and not (word >> 16) & 0x40 and not (word >> 16) & ~0x401
    return False


class Tasks(unittest.TestCase):
    def all_harmless(self, unit):
        start = cc.parse_state(cc.frame(cc.SUB_STATE, helper.SimulatedUnit().words))
        for frame in unit.received:
            self.assertTrue(harmless(frame, start), frame.hex())

    def test_check(self):
        report, unit = run('check', START)
        self.assertEqual(report['write_reported'], {'down': True, 'back': True, 'right_channel_unchanged': True})
        self.assertTrue(report['two_readings_agree'])
        self.assertEqual([s['hex'] for s in report['sent']], [bytes(cc.set_output_level(6, 213)).hex(' ').upper(), bytes(cc.set_output_level(6, 214)).hex(' ').upper()])
        self.assertEqual(unit.words, helper.SimulatedUnit().words)   # the unit is as it was
        self.all_harmless(unit)
        self.assertNotRegex(report['midi_port_name_with_digits_masked'], r'\d{4}')
        self.assertTrue(report['simulated'])

    def test_check_leaves_a_muted_output_alone(self):
        unit = helper.SimulatedUnit()
        unit.words[2] = (59 << 14) | (59 << 23)
        report, unit = run('check', START, unit)
        self.assertEqual(report['sent'], [])
        self.assertIn('not tried', report['write_reported'])
        self.assertTrue(all(cc.parse_frame(f)[0] == 0x10 for f in unit.received))

    def test_nothing_is_sent_without_a_yes(self):
        for task in helper.TASKS:
            report, unit = run(task, ['no'])
            self.assertEqual(unit.received, [], task)
            self.assertEqual(report['sent'], [], task)

    def test_dim_key(self):
        report, unit = run('dim-key', START + ['', 'yes', '', 'no'])
        self.assertEqual(report['dim_key']['flag_followed_the_key'], [False, True, False])
        self.assertEqual(report['dim_key']['main_raw'], [[183, 183], [143, 143], [183, 183]])
        self.assertEqual(report['dim_flag_by_message'], {'reported': [True, False], 'main_raw': [[183, 183]] * 3})
        self.assertEqual([cc.parse_frame(bytes.fromhex(s['hex']))[1][0] for s in report['sent']], [0x2000 | (0x200C << 16), 0x2000 | (0x000C << 16)])
        self.assertEqual(unit.words, helper.SimulatedUnit().words)
        self.all_harmless(unit)

    def test_clock_and_optical_are_put_back(self):
        # the helper reports ADAT and AutoSync at the start; bit 10 set shows S/PDIF, bit 0 set shows Master
        answers = START + ['no', 'adat', 'autosync', 'spdif', 'adat', 'autosync', 'master']
        report, unit = run('clock-optical', answers)
        self.assertEqual(report['optical_format'], {'at_the_start': 'adat', 'with_bit_10_set': 'spdif', 'with_bit_10_clear': 'adat'})
        self.assertEqual(report['clock_source']['with_bit_0_set'], 'master')
        words = [cc.parse_frame(bytes.fromhex(s['hex']))[1][0] for s in report['sent']]
        self.assertEqual(words, [0x400 | (0x401 << 16), 0x400 | (0x001 << 16), 0x001, 0x001 | (0x001 << 16), 0x001])
        self.assertEqual(unit.device & 0x401, 0x000)   # optical bit clear (ADAT here), clock bit clear (AutoSync here)
        self.all_harmless(unit)

    def test_clock_and_optical_with_the_other_polarity(self):
        answers = START + ['yes', 'spdif', 'master', 'spdif', 'spdif', 'adat', 'adat', 'autosync', 'master']
        report, unit = run('clock-optical', answers)
        words = [cc.parse_frame(bytes.fromhex(s['hex']))[1][0] for s in report['sent']]
        self.assertEqual(words[:3], [0x400 | (0x401 << 16), 0x400 | (0x001 << 16), 0x400 | (0x401 << 16)])   # back to S/PDIF = bit set
        self.assertEqual(words[3:], [0x001 | (0x400 << 16), 0x001 | (0x401 << 16)])                          # the format bit is carried along; Master = bit set stays
        self.assertEqual(unit.device & 0x401, 0x401)
        self.all_harmless(unit)

    def test_clock_and_optical_when_the_helper_cannot_tell(self):
        answers = START + ['no', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure']
        report, unit = run('clock-optical', answers)
        self.assertEqual(len(report['sent']), 4)   # two per setting, and no guess at a way back
        self.all_harmless(unit)

    def test_replug(self):
        report, unit = run('replug', START + ['yes', '', 'yes', 'no', 'yes', 'off'])
        self.assertEqual([s['why'] for s in report['sent']], ['playback to the headphones at 0 dB'] * 2 + ['playback to the headphones at 0 dB, sent again'] * 2 + ['playback off the headphones'] * 2)
        self.assertEqual(unit.cells, {64: 0, 91: 0})
        self.assertEqual(report['levels_kept']['main_raw'], [[183, 183], [183, 183]])
        self.all_harmless(unit)

    def test_replug_stops_when_nothing_is_heard(self):
        report, unit = run('replug', START + ['no'])
        self.assertEqual(len(report['sent']), 2)
        self.all_harmless(unit)

    def test_every_answer_is_in_the_report(self):
        report, unit = run('dim-key', START + ['', 'unsure', '', 'unsure'])
        asked = [s for s in report['steps'] if 'asked' in s]
        self.assertEqual([s['answered'] for s in asked], ['yes', 'pro fs', 'usb', 'a test', '', 'unsure', '', 'unsure'])

    def test_mask(self):
        self.assertEqual(helper.mask('Babyface Pro (23456789) Port 2'), 'Babyface Pro (########) Port 2')
        self.assertEqual(helper.mask('Unit 123 and 1234 and 12345'), 'Unit 123 and #### and #####')


SERVER = r'''
import sys, time
sys.path.insert(0, sys.argv[1])
import rtmidi, babyface_helper as helper
unit = helper.SimulatedUnit()
ports = []
for number in (1, 2):
    name = 'Babyface Pro (87654321) Port %d' % number
    source, destination = rtmidi.MidiOut(), rtmidi.MidiIn()
    source.open_virtual_port(name); destination.open_virtual_port(name)
    destination.ignore_types(sysex=False)
    if number == 2:   # only the second port answers, as on the unit
        def handle(event, data=None, source=source):
            unit.send(bytes(event[0]))
            for frame in unit.collect(0):
                source.send_message(list(frame))
        destination.set_callback(handle)
    ports.append((source, destination))
print('ready', flush=True)
time.sleep(float(sys.argv[2]))
'''


class Ports(unittest.TestCase):
    def test_the_tool_finds_the_port_that_answers(self):
        try:
            import rtmidi
        except ImportError:
            self.skipTest('python-rtmidi is not installed')
        if sys.platform not in ('darwin', 'linux'):
            self.skipTest('no virtual MIDI ports on this system')
        server = subprocess.Popen([sys.executable, '-c', SERVER, str(HERE), '20'], stdout=subprocess.PIPE, text=True)
        try:
            self.assertEqual(server.stdout.readline().strip(), 'ready')
            time.sleep(0.5)
            with tempfile.TemporaryDirectory() as folder:
                listed = subprocess.run([sys.executable, str(HERE / 'babyface_helper.py'), 'ports'], capture_output=True, text=True, cwd=folder)
                self.assertIn('Babyface Pro (########) Port 2', listed.stdout)
                done = subprocess.run([sys.executable, str(HERE / 'babyface_helper.py'), 'check'], input='\n'.join(START) + '\n', capture_output=True, text=True, cwd=folder, timeout=60)
                self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
                report = json.loads(sorted(Path(folder).glob('babyface-report-check-*.json'))[-1].read_text())
            self.assertFalse(report['simulated'])
            self.assertEqual(report['write_reported'], {'down': True, 'back': True, 'right_channel_unchanged': True})
            self.assertEqual(report['midi_port_name_with_digits_masked'], 'Babyface Pro (########) Port 2')
        finally:
            server.kill()
            server.wait()
            server.stdout.close()


if __name__ == '__main__':
    unittest.main()
