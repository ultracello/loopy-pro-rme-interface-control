"""Reference codec for the MIDI SysEx control protocol of the RME Babyface Pro FS in class-compliant mode.

Public domain (Unlicense). Pure Python, no dependencies. It only builds and parses bytes; it sends nothing.

Every message is   F0 00 20 0D 10 <sub ID> <payload> F7   on the second MIDI port of the unit ("Port 2").
The payload is a sequence of 32-bit words, each packed least significant bits first into five 7-bit bytes.

What each part rests on (measured on a unit, reported back by the unit, or taken from other people's notes) is
stated in BABYFACE-PRO-FS-CC-REFERENCE.md. The doc strings below repeat the status in one word.
"""
import cmath
import math

HEADER = bytes([0xF0, 0x00, 0x20, 0x0D, 0x10])
SUB_STATE, SUB_MIXER, SUB_PEAKS, SUB_INPUT_SETTINGS, SUB_GAIN, SUB_REQUEST = 0x00, 0x01, 0x02, 0x03, 0x04, 0x10
UNITY = 0x20000            # mixer level field for 0 dB
FIELD = 1 << 20            # size of the mixer level field
METER_FULL_SCALE = 0x08000000
OUTPUT_RAW_AT_0_DB = 243   # output level: raw = 243 + 2 * dB
OUTPUT_RAW_TOTALMIX_MUTE = 59
# sources and outputs of the mixer, by index
SOURCES = ['AN1', 'AN2', 'IN3', 'IN4', 'AS1', 'AS2', 'ADAT3', 'ADAT4', 'ADAT5', 'ADAT6', 'ADAT7', 'ADAT8'] + ['PB%d' % n for n in range(1, 13)]
OUTPUTS = ['AN1', 'AN2', 'PH3', 'PH4', 'AS1', 'AS2', 'ADAT3', 'ADAT4', 'ADAT5', 'ADAT6', 'ADAT7', 'ADAT8']
# bits of the input settings (sub ID 03) and of the low bits of state word 0
BIT_48V_AN1, BIT_48V_AN2, BIT_SENS_IN3, BIT_SENS_IN4, BIT_PAD_AN1, BIT_PAD_AN2 = 0, 1, 2, 3, 4, 5


# ---- framing ---------------------------------------------------------------------------------------------------------
def pack_word(word):
    """One 32-bit word as five 7-bit bytes, bits 0-6 first. (measured: every message of this file uses it)"""
    if not 0 <= word <= 0xFFFFFFFF:
        raise ValueError('word out of range')
    return bytes((word >> (7 * i)) & 0x7F for i in range(5))


def unpack_word(five):
    if len(five) != 5 or any(b > 0x7F for b in five) or five[4] > 0x0F:
        raise ValueError('not a packed 32-bit word')
    return sum(b << (7 * i) for i, b in enumerate(five))


def frame(sub_id, words=()):
    return HEADER + bytes([sub_id]) + b''.join(pack_word(w) for w in words) + b'\xF7'


def parse_frame(data):
    """(sub ID, list of words) of one complete SysEx message of the unit or for the unit."""
    data = bytes(data)
    if len(data) < 7 or data[:5] != HEADER or data[-1] != 0xF7 or (len(data) - 7) % 5:
        raise ValueError('not a message of this protocol')
    body = data[6:-1]
    return data[5], [unpack_word(body[i:i + 5]) for i in range(0, len(body), 5)]


# ---- host to unit ----------------------------------------------------------------------------------------------------
def request_state():
    """Ask for the state. The unit answers with three messages: sub ID 00 (227 bytes), 01 and 02 (207 bytes each). (measured)"""
    return frame(SUB_REQUEST)


def output_raw_from_db(db):
    """Raw output level for a level in dB: 243 + 2 * dB, half-dB steps, up to +6 dB. (measured from -63.5 to 0 dB, reported back up to +6 dB)"""
    raw = 243 + 2 * db
    if raw != int(raw):
        raise ValueError('output levels move in steps of 0.5 dB')
    return int(raw)


def output_db_from_raw(raw):
    return (raw - 243) / 2


def set_output_level(channel, raw):
    """Level of one output channel. channel: 4 Main left, 5 Main right, 6 Phones left, 7 Phones right (measured),
    8 AS1, 9 AS2 (reported back). Raw values up to 255 (+6 dB) are taken (measured behind the headphone output:
    +0.50, +1.00, +3.00 and +6.00 dB for raw 244, 245, 249 and 255; the lowest steps are up to 0.26 dB lower than the law)."""
    if channel not in (4, 5, 6, 7, 8, 9):
        raise ValueError('channel 4..9')
    if not 0 <= raw <= 255:
        raise ValueError('raw 0..255')
    return frame(SUB_GAIN, [channel | (raw << 16)])


def pack_mic_gain(db):
    """Microphone gain 0..65 dB as the unit wants it written: coarse part in bits 0-4, fine part in bits 5-7. (reported back for every value)"""
    if not (isinstance(db, int) and 0 <= db <= 65):
        raise ValueError('microphone gain 0..65 dB in whole dB')
    return ((db % 3) << 5) | (db // 3) if db < 60 else ((db % 6) << 5) | 20


def unpack_mic_gain(raw):
    return (raw & 31) * 3 + (raw >> 5)


def set_mic_gain(input_number, db):
    """Gain of microphone input 1 or 2 in whole dB, 0..65. (measured at 3 and 6 dB, reported back for 0..65)"""
    if input_number not in (1, 2):
        raise ValueError('microphone input 1 or 2')
    return frame(SUB_GAIN, [(input_number - 1) | (pack_mic_gain(db) << 16)])


def set_line_gain(input_number, half_db_steps):
    """Gain of line input 3 or 4 as a count of half dB, 0..18 (0 to 9 dB). (reported back for every value; measured on
    input 3 with a tone: 0.50 dB per step)"""
    if input_number not in (3, 4) or not (isinstance(half_db_steps, int) and 0 <= half_db_steps <= 18):
        raise ValueError('line input 3 or 4, 0..18 half dB')
    return frame(SUB_GAIN, [(input_number - 1) | (half_db_steps << 16)])


def set_input_setting(bit, on, current_settings):
    """Switch one input setting. current_settings: the six setting bits as the unit reports them (state word 0, bits 0-5).

    The message carries "what changes" in bits 0-15 and the complete new state in bits 16-30, so every other setting
    must be sent back as read. (reported back for bits 2-5; measured: pad -10.2 dB, and clearing bit 2 raises the level of
    input 3 by 8.74 dB; bits 0 and 1 are phantom power and were never sent)"""
    if bit not in range(6) or current_settings & ~0x3F:
        raise ValueError('bit 0..5, settings within six bits')
    new = (current_settings | (1 << bit)) if on else (current_settings & ~(1 << bit))
    return frame(SUB_INPUT_SETTINGS, [(1 << bit) | (new << 16)])


def mixer_level_from_db(db):
    """Linear level of the mixer for a gain in dB; 0 dB is 0x20000, +6 dB is 0x40000. (measured between -48 and +6 dB)"""
    return int(round(UNITY * 10 ** (db / 20)))


def mixer_db_from_level(level):
    return -math.inf if level == 0 else 20 * math.log10(level / UNITY)


def set_mixer(output, source, level, inverted=False):
    """One cell of the mixer: source (0-11 hardware inputs, 12-23 playback) to output (0-11), linear level, optional phase inversion.

    An inverted level stands in the 20-bit field as 2^20 - level. Level 0 switches the cell off. The unit keeps the
    mixer only until its USB connection is built anew and never reports it. Levels up to +6 dB (0x40000) are taken.
    Every bit of the level counts (measured down to level 7 against 8).
    (measured for the headphones with sources 0-3, 12, 13 and for playback 1/2 to the Main output)"""
    if not (0 <= output <= 11 and 0 <= source <= 23):
        raise ValueError('output 0..11, source 0..23')
    if not 0 <= level <= 2 * UNITY:
        raise ValueError('level 0..0x40000 (+6 dB)')
    field = (FIELD - level) & (FIELD - 1) if (inverted and level) else level
    return frame(SUB_MIXER, [(26 * output + source) | (field << 12)])


def parse_mixer(data):
    """(output, source, level, inverted) of a mixer message."""
    sub, words = parse_frame(data)
    if sub != SUB_MIXER or len(words) != 1:
        raise ValueError('not a mixer message')
    index, field = words[0] & 0xFFF, words[0] >> 12
    inverted = field > FIELD // 2
    return index // 26, index % 26, (FIELD - field) if inverted else field, inverted


# ---- equaliser and low cut (sub ID 06) ---------------------------------------------------------------------------------
SUB_EQ = 0x06
LOW_CUT_CORRECTION = (1.0, 0.655, 0.528, 0.457)   # per number of poles 1..4, keeps -3 dB at the cutoff


def fixed_5_27(x):
    """A coefficient as signed 5.27 binary fixed point in a 32-bit word. Example of the notes: -2.375 -> 0xED000000."""
    if not -16 <= x < 16:
        raise ValueError('coefficient out of the range of 5.27')
    return int(round(x * (1 << 27))) & 0xFFFFFFFF


def biquad(kind, f0, gain_db, q, fs):
    """One band after the Audio EQ Cookbook, normalised as the unit wants it: (a1/a0, a2/a0, b1/b0, b2/b0, b0/a0).
    kind: 'peak', 'lowshelf', 'highshelf' (the types TotalMix FX offers) or 'lowpass' (gain_db is not used there; it shows
    that a band takes any biquad whose b0 is not zero). fs: the sample rate the unit runs at. (measured with sine tones at
    48 kHz, 10 Hz to 20 kHz: the unit follows these coefficients to 0.03 dB wherever the curve lies above -20 dB)"""
    A = 10 ** (gain_db / 40); w = 2 * math.pi * f0 / fs; cw, sw = math.cos(w), math.sin(w); alpha = sw / (2 * q)
    if kind == 'peak':
        b0, b1, b2 = 1 + alpha * A, -2 * cw, 1 - alpha * A; a0, a1, a2 = 1 + alpha / A, -2 * cw, 1 - alpha / A
    elif kind == 'lowshelf':
        r = 2 * math.sqrt(A) * alpha
        b0, b1, b2 = A * ((A + 1) - (A - 1) * cw + r), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - r)
        a0, a1, a2 = (A + 1) + (A - 1) * cw + r, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - r
    elif kind == 'highshelf':
        r = 2 * math.sqrt(A) * alpha
        b0, b1, b2 = A * ((A + 1) + (A - 1) * cw + r), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - r)
        a0, a1, a2 = (A + 1) - (A - 1) * cw + r, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - r
    elif kind == 'lowpass':
        b0, b1, b2 = (1 - cw) / 2, 1 - cw, (1 - cw) / 2; a0, a1, a2 = 1 + alpha, -2 * cw, 1 - alpha
    else:
        raise ValueError('kind')
    return a1 / a0, a2 / a0, b1 / b0, b2 / b0, b0 / a0


FLAT_BAND = (0.0, 0.0, 0.0, 0.0, 1.0)


def low_cut_coefficient(f0, poles, fs):
    """The word for the low cut as the notes give it: 1 - k with k = 1 / (2*pi*c*f0/fs + 1), c by the number of poles.
    With this k the -3 dB point lies a little above f0 (measured at 48 kHz: 100 Hz gives 100.7 / 103.0 / 105.2 / 107.1 Hz
    with 1 / 2 / 3 / 4 poles, 500 Hz with 4 poles gives 573 Hz). low_cut_coefficient_exact() puts it at f0."""
    k = 1 / (2 * math.pi * LOW_CUT_CORRECTION[poles - 1] * f0 / fs + 1)
    return 1 - k


def low_cut_coefficient_exact(f0, poles, fs):
    """The word for a low cut whose -3.01 dB point lies at f0: 1 - k, with k solved from the filter the unit applies,
    k(1 - z^-1)/(1 - k z^-1) once per pole. (measured: 100 Hz with 4 and with 2 poles, 250 Hz with 1 pole and 500 Hz
    with 4 poles came out at 100.1, 100.1, 250.2 and 500.6 Hz, read off a sixth-octave grid)"""
    g2 = 2 ** (-1 / poles); cw = math.cos(2 * math.pi * f0 / fs)
    a, b, c = 2 * (1 - cw) - g2, 2 * g2 * cw, -g2
    r = math.sqrt(b * b - 4 * a * c)
    k = [x for x in ((-b + r) / (2 * a), (-b - r) / (2 * a)) if 0 < x < 1]
    if len(k) != 1:
        raise ValueError('no low cut for these values')
    return 1 - k[0]


def eq_response_db(f, fs, bands=(FLAT_BAND, FLAT_BAND, FLAT_BAND), low_cut_poles=0, low_cut=0.0, overall_gain=None):
    """Gain in dB at the frequency f of what set_eq() sends with the same arguments: the three biquads
    (1 + b1 z^-1 + b2 z^-2)/(1 + a1 z^-1 + a2 z^-2), the overall gain, and the low cut k(1 - z^-1)/(1 - k z^-1) with
    k = 1 - low_cut once per pole. (measured: this is what the unit does, see biquad(); note that the low cut also
    takes a little level in the pass band, 0.06 dB for 100 Hz with 1 pole and 0.52 dB for 500 Hz with 4 poles)"""
    z = cmath.exp(-2j * math.pi * f / fs)
    h = overall_gain if overall_gain is not None else bands[0][4] * bands[1][4] * bands[2][4]
    for a1, a2, b1, b2 in (band[:4] for band in bands):
        h *= (1 + b1 * z + b2 * z * z) / (1 + a1 * z + a2 * z * z)
    if low_cut_poles:
        k = 1 - low_cut
        h *= (k * (1 - z) / (1 - k * z)) ** low_cut_poles
    return 20 * math.log10(abs(h))


def eq_from_words(words):
    """The arguments of set_eq() and eq_response_db() back from the 16 words of an equaliser message:
    (eq_index, channel, is_output, enabled, keywords)."""
    signed = lambda w: (w - (1 << 32) if w & 0x80000000 else w) / (1 << 27)
    control = words[0]
    bands = tuple(tuple(signed(x) for x in words[1 + 4 * i:5 + 4 * i]) + (1.0,) for i in range(3))
    keywords = dict(bands=bands, low_cut_poles=bin((control >> 8) & 0xF).count('1'), low_cut=signed(words[14]), overall_gain=signed(words[13]))
    return control & 0xFF, (control >> 16) & 0xF, bool(control >> 20 & 1), bool(control >> 31), keywords


def set_eq(eq_index, channel, is_output, enabled, bands=(FLAT_BAND, FLAT_BAND, FLAT_BAND), low_cut_poles=0, low_cut=0.0, overall_gain=None):
    """Equaliser and low cut of one channel: 16 words, to be sent in one piece. eq_index 0..20 is a slot, a memory for one
    set of coefficients: two channels on the same slot share it, so give every channel its own. bands: three tuples as
    biquad() returns them. overall_gain: product of the three b0/a0 unless given. enabled=False switches EQ and low cut
    of the channel off, whatever the slot. (measured on output Main left and on input 1: overall gain to 0.01 dB, and
    with sine tones at 48 kHz the whole curve of peak, shelf, low pass and low cut settings, see eq_response_db())"""
    if not (0 <= eq_index <= 20 and 0 <= channel <= 11 and 0 <= low_cut_poles <= 4 and len(bands) == 3):
        raise ValueError('eq_index 0..20, channel 0..11, poles 0..4, three bands')
    gain = overall_gain if overall_gain is not None else bands[0][4] * bands[1][4] * bands[2][4]
    control = eq_index | (((1 << low_cut_poles) - 1) << 8) | (channel << 16) | ((1 if is_output else 0) << 20) | ((1 if enabled else 0) << 31)
    words = [control]
    for band in bands:
        words += [fixed_5_27(c) for c in band[:4]]
    words += [fixed_5_27(gain), fixed_5_27(low_cut), 0]
    return frame(SUB_EQ, words)


# ---- unit to host ----------------------------------------------------------------------------------------------------
def parse_state(data):
    """The fields of the state message (sub ID 00, 227 bytes, 44 words) that this reference has seen change on a unit."""
    sub, w = parse_frame(data)
    if sub != SUB_STATE or len(w) != 44:
        raise ValueError('not a state message')
    settings = w[0] & 0x3F
    return {
        'main_raw': (w[1] & 0xFF, (w[1] >> 9) & 0xFF),
        'phones_raw': ((w[2] >> 14) & 0xFF, (w[2] >> 23) & 0xFF),
        'main_db': (output_db_from_raw(w[1] & 0xFF), output_db_from_raw((w[1] >> 9) & 0xFF)),
        'phones_db': (output_db_from_raw((w[2] >> 14) & 0xFF), output_db_from_raw((w[2] >> 23) & 0xFF)),
        'mic_gain_db': (w[2] & 0x7F, (w[2] >> 7) & 0x7F),
        'line_gain_half_db': ((w[3] >> 19) & 0x1F, (w[3] >> 24) & 0x1F),
        'as_raw': (w[3] & 0xFF, (w[3] >> 9) & 0xFF),
        'settings': settings,
        'phantom_48v': (bool(settings & 1), bool(settings & 2)),
        'line_sensitivity_bit': (bool(settings & 4), bool(settings & 8)),
        'pad': (bool(settings & 16), bool(settings & 32)),
        'other_bits_of_word_0_bits_6_to_15': (w[0] >> 6) & 0x3FF,
        'dim': bool(w[0] & (1 << 13)),
        'global_mute_bits_14_15': (w[0] >> 14) & 3,
        'encoder_counter': (w[0] >> 16) & 0xF,
        'mode_and_selection': (w[0] >> 20) & 0xF,
        'words': w,
    }


def meter_dbfs(word):
    return -math.inf if word == 0 else 20 * math.log10(word / METER_FULL_SCALE)


def parse_peaks(data):
    """Peak meters (sub ID 02, 207 bytes, 40 words), in dBFS. Each answer carries the peak since the previous request.
    Output meters sit behind the output level and before the EQ of the output; input meters before the input EQ. (measured)"""
    sub, w = parse_frame(data)
    if sub != SUB_PEAKS or len(w) != 40:
        raise ValueError('not a peak meter message')
    db = [meter_dbfs(x) for x in w]
    return {'inputs_1_to_4': db[0:4], 'playback_1_2': db[12:14], 'main_out': db[26:28], 'phones_out': db[28:30], 'words': w}
