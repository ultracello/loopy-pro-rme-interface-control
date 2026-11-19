"""Tests of the reference codec against test-vectors.json. Run: python3 test_babyface_cc.py"""
import json,math,unittest
from pathlib import Path
import babyface_cc as b
V={v['name']:bytes.fromhex(v['hex']) for v in json.loads((Path(__file__).resolve().parent/'test-vectors.json').read_text())['vectors']}
class Codec(unittest.TestCase):
    def test_framing(self):
        self.assertEqual(len(V),len(json.loads((Path(__file__).resolve().parent/'test-vectors.json').read_text())['vectors']))   # every vector has a name of its own
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
        # the gain of input 1 as measured with a tone, every value: within 0.12 dB of the number written; inside a group of three the steps are 1 dB
        G=json.loads((Path(__file__).resolve().parent/'mic-gain-measured.json').read_text())['rows'];self.assertEqual([g for g,d in G],list(range(66)));m=dict(G)
        for g in range(66):self.assertAlmostEqual(m[g],g,delta=0.12,msg=g)
        for g in range(1,66):
            if g%3 or g>60:self.assertAlmostEqual(m[g]-m[g-1],1.0,delta=0.011,msg=g)
        self.assertEqual(b.parse_frame(V['mic gain input 1 3 dB']),(4,[0|(1<<16)]));self.assertEqual(b.parse_frame(V['line gain input 3 6.0 dB']),(4,[2|(12<<16)]))
    def test_input_settings(self):
        self.assertEqual(b.parse_frame(V['input setting: pad of input 1 on (settings before 0C)']),(3,[0x10|(0x1C<<16)]))
        self.assertEqual(b.parse_frame(V['input setting: sensitivity bit of input 3 cleared (settings before 0C)']),(3,[0x04|(0x08<<16)]))
        self.assertEqual(V['input setting: pad of input 1 on (settings before 0C)'],bytes.fromhex('F000200D10031000700000F7'))
        self.assertEqual(b.parse_frame(V['input setting: phantom power of input 1 on (settings before 0C)']),(3,[0x01|(0x0D<<16)]));self.assertEqual(b.parse_frame(V['settings flag: dim on (bit 13, settings before 0C)']),(3,[0x2000|(0x200C<<16)]))
        self.assertEqual(b.parse_frame(b.set_input_setting(15,True,0x0C)),(3,[0x8000|(0x800C<<16)]))
        for bad in ((6,True,0x0C),(12,True,0x0C),(0,True,0x4C)):
            with self.assertRaises(ValueError):b.set_input_setting(*bad)
    def test_mixer(self):
        self.assertEqual(V['mixer: playback 1 to Phones left at 0 dB'],bytes.fromhex('F000200D10014000000002F7'));self.assertEqual(V['mixer: playback 2 to Phones right at 0 dB'],bytes.fromhex('F000200D10015B00000002F7'))
        self.assertEqual(b.parse_mixer(V['mixer: input 1 to Phones left at 0 dB, phase inverted']),(2,0,b.UNITY,True));self.assertEqual(V['mixer: input 1 to Phones left at 0 dB, phase inverted'][6:11],bytes([52,0,0,0,0x0E]))
        self.assertEqual(b.parse_mixer(V['mixer: input 4 to Phones right at -12 dB']),(3,3,b.mixer_level_from_db(-12),False))
        self.assertAlmostEqual(b.mixer_db_from_level(b.mixer_level_from_db(-12)),-12,places=3);self.assertEqual(b.mixer_level_from_db(0),0x20000);self.assertEqual(b.mixer_level_from_db(-6),65692)
        self.assertEqual(b.parse_mixer(b.set_mixer(2,0,0,True)),(2,0,0,False))
        self.assertEqual(V['mixer: playback 1 to Phones left at +6 dB'],bytes.fromhex('F000200D10014000000004F7'));self.assertEqual(V['mixer: playback 1 to Main left at -6 dB'],bytes.fromhex('F000200D10010C00260001F7'))
        with self.assertRaises(ValueError):b.set_mixer(2,0,2*b.UNITY+1)
        # the gain of a cell as measured through loopback: the level without its two lowest bits, over 2^15
        M=json.loads((Path(__file__).resolve().parent/'output-level-law-measured.json').read_text())['mixer_cell_rows'];self.assertEqual(len(M),18)
        for field,db in M:
            g=b.mixer_gain_from_level(field)
            if db is None:self.assertEqual(g,0.0,field)
            else:self.assertAlmostEqual(20*math.log10(g),db,delta=0.001,msg=field)
        self.assertEqual([b.mixer_gain_from_level(x) for x in (0,3,4,b.UNITY,2*b.UNITY)],[0.0,0.0,1/32768,1.0,2.0])
        # the level of an ADAT output is a mixer entry at 992 + output and follows the same law
        E=json.loads((Path(__file__).resolve().parent/'output-level-law-measured.json').read_text())['adat_entry_rows'];self.assertEqual(len(E),18)
        for field,db in E:
            g=b.mixer_gain_from_level(field)
            if db is None:self.assertEqual(g,0.0,field)
            else:self.assertAlmostEqual(20*math.log10(g),db,delta=0.003,msg=field)
        self.assertEqual(b.parse_frame(b.set_adat_output_level(6,0x10000)),(1,[998|(0x10000<<12)]));self.assertEqual(b.set_adat_output_level(11,b.UNITY),V['level of ADAT8: mixer entry 1003 at 0 dB'])
        for bad in ((5,b.UNITY),(12,b.UNITY),(6,b.UNITY+1)):
            with self.assertRaises(ValueError):b.set_adat_output_level(*bad)
    def test_state(self):
        s=b.parse_state(V['state (built for this file from the values our unit reported)'])
        self.assertEqual((s['main_raw'],s['phones_raw'],s['phones_db'],s['mic_gain_db'],s['line_gain_half_db'],s['settings']),((59,59),(214,214),(-14.5,-14.5),(0,0),(12,0),0x0C))
        self.assertEqual((s['pad'],s['line_sensitivity_bit'],s['phantom_48v'],s['dim']),((False,False),(True,True),(False,False),False))
    def test_equaliser(self):
        self.assertEqual(b.fixed_5_27(-2.375),0xED000000);self.assertEqual(b.fixed_5_27(1.0),0x08000000)
        sub,w=b.parse_frame(V['equaliser: slot 1 on input 1, flat bands, overall gain 0.5']);self.assertEqual((sub,len(w),w[0],w[13],w[1:13]),(6,16,(1<<31)|1,0x04000000,[0]*12))
        sub,w=b.parse_frame(V['equaliser: slot 20 on output Main left, flat bands, overall gain 0.5']);self.assertEqual(w[0],(1<<31)|(1<<20)|20)
        sub,w=b.parse_frame(V['low cut: input 1, 4 poles at 2 kHz (48 kHz), slot 1']);self.assertEqual(w[0],(1<<31)|(0xF<<8)|1);self.assertEqual([b.parse_frame(V['low cut: output Main left, %s at 2 kHz (48 kHz), slot 0'%n])[1][0]>>8&15 for n in ('1 pole','2 poles','3 poles','4 poles')],[1,3,7,15]);self.assertEqual(w[13],0x08000000);self.assertAlmostEqual(w[14]/(1<<27),0.10686,places=4)
        a1,a2,b1,b2,g=b.biquad('peak',1000,0,0.7,48000);self.assertAlmostEqual(g,1.0);self.assertAlmostEqual(a1,b1);self.assertAlmostEqual(a2,b2)
        self.assertEqual(len(V['equaliser: slot 1 on input 1 off']),87);self.assertEqual(b.parse_frame(V['equaliser: slot 1 on input 1 off'])[1][0],1)
    def test_equaliser_curves_measured_with_sine_tones(self):
        """Every measured point that was compared lies on the curve the codec calculates for the message that was sent."""
        C=json.loads((Path(__file__).resolve().parent/'eq-curves-measured.json').read_text());self.assertEqual((len(C['settings']),C['sample_rate']),(34,48000));n=0;upper=[];digital=[]
        for c in C['settings']:
            self.assertEqual(V[c['name']],bytes.fromhex(c['hex']));index,channel,is_output,enabled,kw=b.eq_from_words(b.parse_frame(V[c['name']])[1]);self.assertTrue(enabled)
            self.assertEqual(b.set_eq(index,channel,is_output,enabled,**kw),V[c['name']]);fs=c.get('sample_rate',C['sample_rate']);self.assertEqual(len(c['points']),67 if fs==48000 and 'through loopback' not in c['name'] else 66)
            for f,measured,calculated,counted in c['points']:
                mine=b.eq_response_db(f,fs,**kw);self.assertAlmostEqual(mine,calculated,delta=0.0006)
                if not counted:continue
                n+=1;self.assertLessEqual(abs(measured-mine),0.2,(c['name'],f))
                if f>=20 and measured>=-20:upper.append(abs(measured-mine))
                if f>=20 and 'through loopback' in c['name']:digital.append(abs(measured-mine))
        # from 20 Hz up and above -20 dB: 1998 points (1219 at 48 kHz over a cable, 179 at 44.1 kHz over a cable, 600 through loopback, of which
        # 60 were read at 48 kHz with coefficients made for 44.1 kHz and are compared with what those coefficients give at 48 kHz),
        # every one within 0.02 dB but one at 50.4 Hz (0.048 dB, next to the mains frequency); the 600 read digitally are within 0.012 dB
        self.assertEqual((n,len(upper),sum(1 for x in upper if x>0.02)),(2213,1998,1));self.assertEqual(len(digital),600);self.assertLessEqual(max(digital),0.0125);self.assertLess(max(upper),0.05)
    def test_output_level_law(self):
        """Every raw value from 243 down to 0, as measured through loopback, lies on the law of the codec."""
        L=json.loads((Path(__file__).resolve().parent/'output-level-law-measured.json').read_text());self.assertEqual([r for r,d in L['rows']],list(range(243,-1,-1)))
        self.assertEqual([[r for r,d in L[k]] for k in ('as1_rows','as2_rows')],[list(range(243,-1,-1))]*2)   # AS1 and AS2 follow the same law
        for raw,db in L['rows']+L['as1_rows']+L['as2_rows']:
            g=b.output_gain_from_raw(raw)
            if db is None:self.assertEqual(g,0.0,raw)
            else:self.assertAlmostEqual(20*math.log10(g),db,delta=0.003,msg=raw)
        self.assertEqual(max(r for r,d in L['rows'] if d is None),62);self.assertEqual(b.output_gain_from_raw(59),0.0);self.assertEqual(b.output_gain_from_raw(243),1.0)
        for raw,db in L['main_left_relative_to_raw_183']:
            g=b.output_gain_from_raw(raw)/b.output_gain_from_raw(183)
            if db is None:self.assertEqual(g,0.0)
            else:self.assertAlmostEqual(20*math.log10(g),db,delta=0.003)
        self.assertEqual(b.set_loopback(4,True),bytes.fromhex('F000200D10020400040000F7'));self.assertEqual(b.parse_frame(b.set_loopback(11,False)),(2,[11]))
    def test_low_cut_corner(self):
        for f0,poles in ((20,1),(100,1),(100,2),(100,4),(250,1),(500,4)):
            self.assertAlmostEqual(b.eq_response_db(f0,48000,low_cut_poles=poles,low_cut=b.low_cut_coefficient_exact(f0,poles,48000)),-3.0103,places=3)
            self.assertLess(b.eq_response_db(f0,48000,low_cut_poles=poles,low_cut=b.low_cut_coefficient(f0,poles,48000)),-3.0103)  # the k of the notes cuts a little higher
        self.assertAlmostEqual(b.eq_response_db(20000,48000,low_cut_poles=4,low_cut=b.low_cut_coefficient(500,4,48000)),-0.516,places=2)  # level the low cut takes in the pass band
        a1,a2,b1,b2,g=b.biquad('lowpass',2000,0,0.7071,48000);self.assertEqual((b1,b2),(2.0,1.0));self.assertAlmostEqual(b.eq_response_db(2000,48000,bands=(b.FLAT_BAND,b.FLAT_BAND,(a1,a2,b1,b2,g))),-3.01,places=1)
    def test_meters(self):
        self.assertEqual(b.meter_dbfs(b.METER_FULL_SCALE),0.0);self.assertAlmostEqual(b.meter_dbfs(b.METER_FULL_SCALE//2),-6.0206,places=3);self.assertEqual(b.meter_dbfs(0),-math.inf)
        w=[0]*40;w[0]=b.METER_FULL_SCALE//2;w[28]=b.METER_FULL_SCALE//4;p=b.parse_peaks(b.frame(2,w));self.assertAlmostEqual(p['inputs_1_to_4'][0],-6.0206,places=3);self.assertAlmostEqual(p['phones_out'][0],-12.0412,places=3)
if __name__=='__main__':unittest.main()
