"""Tests of the reference codec against test-vectors.json. Run: python3 test_babyface_cc.py"""
import json,math,unittest
from pathlib import Path
import babyface_cc as b
V={v['name']:bytes.fromhex(v['hex']) for v in json.loads((Path(__file__).resolve().parent/'test-vectors.json').read_text())['vectors']}
class Codec(unittest.TestCase):
    def test_framing(self):
        for word in (0,1,0x7F,0x80,0x20000000,0xE0000034,0xFFFFFFFF):self.assertEqual(b.unpack_word(b.pack_word(word)),word)
        self.assertEqual(b.pack_word(0x20000040),bytes([0x40,0,0,0,2]));self.assertEqual(V['request state'],bytes.fromhex('F000200D1010F7'))
        self.assertEqual(b.parse_frame(V['mixer: playback 1 to Phones left at 0 dB']),(1,[0x20000040]))
        with self.assertRaises(ValueError):b.parse_frame(b'\xF0\x00\x20\x0D\x10\x01\x40\x00\x00\x00\xF7')
    def test_output_levels(self):
        self.assertEqual([b.output_raw_from_db(x) for x in (0,-0.5,-14.5,-30,-63.5)],[243,242,214,183,116])
        self.assertEqual(V['output level Phones left -14.5 dB'],bytes.fromhex('F000200D10040600580600F7'))
        self.assertEqual(b.output_db_from_raw(59),-92.0);self.assertEqual(b.output_raw_from_db(6),255);self.assertEqual(V['output level AS1 raw 183 (-30 dB)'],bytes.fromhex('F000200D100408005C0500F7'))
        with self.assertRaises(ValueError):b.output_raw_from_db(-0.25)
    def test_gains(self):
        self.assertEqual([b.pack_mic_gain(x) for x in (0,1,2,3,59,60,61,65)],[0,32,64,1,83,20,52,180])
        for db in range(66):self.assertEqual(b.unpack_mic_gain(b.pack_mic_gain(db)),db)
        self.assertEqual(b.parse_frame(V['mic gain input 1 3 dB']),(4,[0|(1<<16)]));self.assertEqual(b.parse_frame(V['line gain input 3 6.0 dB']),(4,[2|(12<<16)]))
    def test_input_settings(self):
        self.assertEqual(b.parse_frame(V['input setting: pad of input 1 on (settings before 0C)']),(3,[0x10|(0x1C<<16)]))
        self.assertEqual(b.parse_frame(V['input setting: sensitivity bit of input 3 cleared (settings before 0C)']),(3,[0x04|(0x08<<16)]))
        self.assertEqual(V['input setting: pad of input 1 on (settings before 0C)'],bytes.fromhex('F000200D10031000700000F7'))
    def test_mixer(self):
        self.assertEqual(V['mixer: playback 1 to Phones left at 0 dB'],bytes.fromhex('F000200D10014000000002F7'));self.assertEqual(V['mixer: playback 2 to Phones right at 0 dB'],bytes.fromhex('F000200D10015B00000002F7'))
        self.assertEqual(b.parse_mixer(V['mixer: input 1 to Phones left at 0 dB, phase inverted']),(2,0,b.UNITY,True));self.assertEqual(V['mixer: input 1 to Phones left at 0 dB, phase inverted'][6:11],bytes([52,0,0,0,0x0E]))
        self.assertEqual(b.parse_mixer(V['mixer: input 4 to Phones right at -12 dB']),(3,3,b.mixer_level_from_db(-12),False))
        self.assertAlmostEqual(b.mixer_db_from_level(b.mixer_level_from_db(-12)),-12,places=3);self.assertEqual(b.mixer_level_from_db(0),0x20000);self.assertEqual(b.mixer_level_from_db(-6),65692)
        self.assertEqual(b.parse_mixer(b.set_mixer(2,0,0,True)),(2,0,0,False))
        self.assertEqual(V['mixer: playback 1 to Phones left at +6 dB'],bytes.fromhex('F000200D10014000000004F7'));self.assertEqual(V['mixer: playback 1 to Main left at -6 dB'],bytes.fromhex('F000200D10010C00260001F7'))
        with self.assertRaises(ValueError):b.set_mixer(2,0,2*b.UNITY+1)
    def test_state(self):
        s=b.parse_state(V['state (built for this file from the values our unit reported)'])
        self.assertEqual((s['main_raw'],s['phones_raw'],s['phones_db'],s['mic_gain_db'],s['line_gain_half_db'],s['settings']),((59,59),(214,214),(-14.5,-14.5),(0,0),(12,0),0x0C))
        self.assertEqual((s['pad'],s['line_sensitivity_bit'],s['phantom_48v'],s['dim']),((False,False),(True,True),(False,False),False))
    def test_equaliser(self):
        self.assertEqual(b.fixed_5_27(-2.375),0xED000000);self.assertEqual(b.fixed_5_27(1.0),0x08000000)
        sub,w=b.parse_frame(V['equaliser: slot 0 on input 1, flat bands, overall gain 0.5, enabled']);self.assertEqual((sub,len(w),w[0],w[13],w[1:13]),(6,16,1<<31,0x04000000,[0]*12))
        sub,w=b.parse_frame(V['low cut: input 1, 4 poles at 2 kHz at 48 kHz, slot 0']);self.assertEqual(w[0],(1<<31)|(0xF<<8));self.assertEqual(w[13],0x08000000);self.assertAlmostEqual(w[14]/(1<<27),0.10686,places=4)
        a1,a2,b1,b2,g=b.biquad('peak',1000,0,0.7,48000);self.assertAlmostEqual(g,1.0);self.assertAlmostEqual(a1,b1);self.assertAlmostEqual(a2,b2)
        self.assertEqual(len(V['equaliser: slot 0 on input 1 disabled']),87)
    def test_meters(self):
        self.assertEqual(b.meter_dbfs(b.METER_FULL_SCALE),0.0);self.assertAlmostEqual(b.meter_dbfs(b.METER_FULL_SCALE//2),-6.0206,places=3);self.assertEqual(b.meter_dbfs(0),-math.inf)
        w=[0]*40;w[0]=b.METER_FULL_SCALE//2;w[28]=b.METER_FULL_SCALE//4;p=b.parse_peaks(b.frame(2,w));self.assertAlmostEqual(p['inputs_1_to_4'][0],-6.0206,places=3);self.assertAlmostEqual(p['phones_out'][0],-12.0412,places=3)
if __name__=='__main__':unittest.main()
