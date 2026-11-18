"""Writes test-vectors.json from the reference codec. Each vector: the bytes in hex, what they mean, and what the statement rests on:
"measured" (the effect was measured at the unit's meters), "reported" (the unit reported the new value back), "notes" (other people's notes only)."""
import json
import babyface_cc as b
V=[]
def add(name,frame,meaning,status):V.append({'name':name,'hex':bytes(frame).hex().upper(),'meaning':meaning,'status':status})
add('request state',b.request_state(),'ask the unit for its state; it answers with sub ID 00, 01 and 02','measured')
for name,ch in (('Main left',4),('Main right',5),('Phones left',6),('Phones right',7)):
    for db in (0,-0.5,-14.5,-30,-63.5):add('output level %s %.1f dB'%(name,db),b.set_output_level(ch,b.output_raw_from_db(db)),'channel %d, raw %d'%(ch,b.output_raw_from_db(db)),'measured' if db in (-30,-14.5) else 'reported')
    add('output level %s raw 59'%name,b.set_output_level(ch,59),'the value TotalMix FX writes for a muted output (-92 dB by the formula)','reported')
for i in (1,2):
    for db in (0,1,2,3,6,30,59,60,61,65):add('mic gain input %d %d dB'%(i,db),b.set_mic_gain(i,db),'channel %d, packed value %d'%(i-1,b.pack_mic_gain(db)),'measured' if db in (0,3,6) and i==1 else 'reported')
for i in (3,4):
    for k in (0,1,12,18):add('line gain input %d %.1f dB'%(i,k/2),b.set_line_gain(i,k),'channel %d, %d half dB'%(i-1,k)+('; measured with a tone at the input: %.2f dB above step 0'%{0:0,1:0.50,12:6.00,18:9.00}[k] if i==3 else ''),'measured' if i==3 else 'reported')
for settings,bit,on,what,status in ((0x0C,4,True,'pad of input 1 on','measured'),(0x1C,4,False,'pad of input 1 off','measured'),(0x0C,5,True,'pad of input 2 on','reported'),(0x0C,2,False,'sensitivity bit of input 3 cleared','measured'),(0x08,2,True,'sensitivity bit of input 3 set','measured'),(0x0C,3,False,'sensitivity bit of input 4 cleared','reported'),(0x08,4,True,'pad of input 1 on while the sensitivity bit of input 3 is clear','reported')):
    add('input setting: %s (settings before %02X)'%(what,settings),b.set_input_setting(bit,on,settings),'bits 0-15 what changes, bits 16-30 the whole new state',status)
add('mixer: playback 1 to Phones left at 0 dB',b.set_mixer(2,12,b.UNITY),'index 26*2+12 = 64, level 0x20000','measured')
add('mixer: playback 2 to Phones right at 0 dB',b.set_mixer(3,13,b.UNITY),'index 26*3+13 = 91, level 0x20000','measured')
for db in (0,-6,-12,-30,-48,-60):
    add('mixer: input 1 to Phones left at %d dB'%db,b.set_mixer(2,0,b.mixer_level_from_db(db)),'index 52, level %d'%b.mixer_level_from_db(db),'measured' if db>=-48 else 'reported')
add('mixer: input 1 to Phones left off',b.set_mixer(2,0,0),'level 0','measured')
add('mixer: input 4 to Phones right at -12 dB',b.set_mixer(3,3,b.mixer_level_from_db(-12)),'index 81','measured')
add('mixer: input 1 to Phones left at 0 dB, phase inverted',b.set_mixer(2,0,b.UNITY,True),'field = 2^20 - 0x20000 = 0xE0000','measured')
add('mixer: input 1 to Phones left at -12 dB, phase inverted',b.set_mixer(2,0,b.mixer_level_from_db(-12),True),'field = 2^20 - level','measured')
add('mixer: playback 1 to Phones left at -20.5 dB, phase inverted',b.set_mixer(2,12,b.mixer_level_from_db(-20.5),True),'index 64, inverted','measured')
add('mixer: playback 1 to Main left at 0 dB',b.set_mixer(0,12,b.UNITY),'index 12; the cell the unit has after power-up','measured')
add('mixer: playback 1 to Main left at -6 dB',b.set_mixer(0,12,65688),'index 12, level 65688','measured')
add('mixer: playback 1 to Main left off',b.set_mixer(0,12,0),'index 12, level 0','measured')
add('mixer: playback 2 to Main right at -6 dB',b.set_mixer(1,13,65688),'index 39','measured')
add('mixer: playback 1 to Phones left at +6 dB',b.set_mixer(2,12,2*b.UNITY),'index 64, level 0x40000','measured')
add('mixer: playback 1 to Phones left at +3 dB',b.set_mixer(2,12,185144),'index 64, level 185144','measured')
add('mixer: input 1 to Main left at -12 dB',b.set_mixer(0,0,b.mixer_level_from_db(-12)),'index 0; same message as for the headphones, other output','notes')
add('output level Phones left raw 255 (+6 dB)',b.set_output_level(6,255),'channel 6, raw 255; measured behind the output: +6.00 dB above raw 243','measured')
add('output level AS1 raw 183 (-30 dB)',b.set_output_level(8,183),'channel 8; read through loopback: 30.00 dB below raw 243','measured')
add('output level AS2 raw 59',b.set_output_level(9,59),'channel 9; read through loopback: silent','measured')
add('output level AS2 raw 163',b.set_output_level(9,163),'channel 9; read through loopback: 40.02 dB below raw 243, the law of the headphone output','measured')
add('output level AS1 raw 62',b.set_output_level(8,62),'channel 8; read through loopback: silent, as on the headphone output','measured')
for src,name,index in ((0,'input 1',104),(1,'input 2',105),(2,'input 3',106),(3,'input 4',107)):add('mixer: %s to AS1 at 0 dB'%name,b.set_mixer(4,src,b.UNITY),'index %d; read through loopback of AS1 with the noise of the open input: the same RMS level as on the input channel itself, within 0.002 dB'%index,'measured')
add('mixer: input 3 to AS1 at half level',b.set_mixer(4,2,b.UNITY//2),'index 106, level 0x10000; read through loopback with the noise of the open input: 6.20 dB below the input channel','measured')
add('mixer: input 3 to ADAT3 at 0 dB',b.set_mixer(6,2,b.UNITY),'index 158; read through loopback of ADAT3 with the noise of the open input: the same RMS level as on the input channel','measured')
add('mixer: input 3 to ADAT8 at 0 dB',b.set_mixer(11,2,b.UNITY),'index 288; read through loopback of ADAT8 with the noise of the open input: the same RMS level as on the input channel','measured')
add('mixer: playback 1 to Main left, level field 0x10000',b.set_mixer(0,12,0x10000),'index 12; the Main peak value was exactly half of the one at 0x20000','measured')
add('mixer: playback 1 to Main left, level field 0x1009C',b.set_mixer(0,12,0x1009C),'a level that is no multiple of 8; read one meter step above 0x10098','measured')
add('mixer: playback 1 to Main left, level field 8',b.set_mixer(0,12,8),'-84.4 dB below the level at 0x20000','measured')
add('mixer: playback 1 to Main left, level field 7',b.set_mixer(0,12,7),'read lower than level 8: the lowest bits count','measured')
# equaliser and low cut, as sent in run D1 on 18 November 2026; "measured" changes were read behind the output over a loop cable
FS=48000;FLAT=b.FLAT_BAND;LS=b.biquad('lowshelf',15000,-12,0.7,FS);HS=b.biquad('highshelf',20,-12,0.7,FS);PK=b.biquad('peak',1000,-12,0.3,FS)
lc=lambda f,p:dict(low_cut_poles=p,low_cut=b.low_cut_coefficient(f,p,FS))
for name,frame,meaning in (
    ('equaliser: slot 20 on output Main left, flat bands, overall gain 0.5',b.set_eq(20,0,True,True,overall_gain=0.5),'87 bytes; -6.02 dB'),
    ('equaliser: slot 20 on output Main left off',b.set_eq(20,0,True,False),'bit 31 of word 0 clear; 0.00 dB'),
    ('equaliser: slot 6 on output Main left, flat bands, overall gain 0.25',b.set_eq(6,0,True,True,overall_gain=0.25),'-12.04 dB'),
    ('equaliser: slot 0 on output Main left, flat bands, overall gain 1.0',b.set_eq(0,0,True,True,overall_gain=1.0),'0.00 dB'),
    ('equaliser: slot 0 on output Main left, low shelf -12 dB at 15 kHz Q 0.7 in band 1 (48 kHz)',b.set_eq(0,0,True,True,bands=(LS,FLAT,FLAT)),'-12.01 dB with music below 2 kHz'),
    ('equaliser: the same low shelf in band 2',b.set_eq(0,0,True,True,bands=(FLAT,LS,FLAT)),'-12.01 dB'),
    ('equaliser: the same low shelf in band 3',b.set_eq(0,0,True,True,bands=(FLAT,FLAT,LS)),'-12.02 dB'),
    ('equaliser: the same low shelf in bands 1 and 2',b.set_eq(0,0,True,True,bands=(LS,LS,FLAT)),'-23.93 dB'),
    ('equaliser: slot 0 on output Main left, high shelf -12 dB at 20 Hz Q 0.7 in band 1 (48 kHz)',b.set_eq(0,0,True,True,bands=(HS,FLAT,FLAT)),'-10.64 dB with music'),
    ('equaliser: slot 0 on output Main left, peak -12 dB at 1 kHz Q 0.3 in band 2 (48 kHz)',b.set_eq(0,0,True,True,bands=(FLAT,PK,FLAT)),'-3.47 dB with music'),
    ('low cut: output Main left, 1 pole at 2 kHz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(2000,1)),'word 14 = 1 - k; -13.89 dB with music below 2 kHz'),
    ('low cut: output Main left, 2 poles at 2 kHz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(2000,2)),'-19.07 dB'),
    ('low cut: output Main left, 3 poles at 2 kHz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(2000,3)),'-19.96 dB'),
    ('low cut: output Main left, 4 poles at 2 kHz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(2000,4)),'-20.42 dB'),
    ('low cut: output Main left, 4 poles at 500 Hz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(500,4)),'-8.56 dB'),
    ('low cut: output Main left, 4 poles at 100 Hz (48 kHz), slot 0',b.set_eq(0,0,True,True,**lc(100,4)),'-0.71 dB'),
    ('low cut and gain: output Main left, 1 pole at 2 kHz and overall gain 0.5, slot 0',b.set_eq(0,0,True,True,overall_gain=0.5,**lc(2000,1)),'-19.90 dB, the sum of the two'),
    ('equaliser: slot 1 on input 1, flat bands, overall gain 0.5',b.set_eq(1,0,False,True,overall_gain=0.5),'-6.02 dB at the headphones with input 1 monitored'),
    ('low cut: input 1, 4 poles at 2 kHz (48 kHz), slot 1',b.set_eq(1,0,False,True,**lc(2000,4)),'-20.43 dB at the headphones'),
    ('equaliser: slot 1 on input 1 off',b.set_eq(1,0,False,False),'0.00 dB')):
    add(name,frame,meaning,'measured')
add('equaliser: slot 2 on output Phones left, flat bands, overall gain 0.5',b.set_eq(2,2,True,True,overall_gain=0.5),'sent; the unit\'s own headphone meter does not show the EQ, so the effect could not be read','notes')
# equaliser and low cut, as sent in run T1 on 18 November 2026 with sine tones; the whole measured curves stand in eq-curves-measured.json
PKT=lambda f,g,q:b.biquad('peak',f,g,q,FS);lx=lambda f,p:dict(low_cut_poles=p,low_cut=b.low_cut_coefficient_exact(f,p,FS))
T1=[('low cut 100 Hz, 1 pole',lc(100,1)),('low cut 100 Hz, 2 poles',lc(100,2)),('low cut 100 Hz, 3 poles',lc(100,3)),('low cut 100 Hz, 4 poles',lc(100,4)),('low cut 20 Hz, 2 poles',lc(20,2)),('low cut 500 Hz, 4 poles',lc(500,4)),
    ('peak +6 dB at 1 kHz, Q 1, band 2',dict(bands=(FLAT,PKT(1000,6,1),FLAT))),('peak -12 dB at 1 kHz, Q 5, band 2',dict(bands=(FLAT,PKT(1000,-12,5),FLAT))),('peak +12 dB at 100 Hz, Q 0.7, band 1',dict(bands=(PKT(100,12,0.7),FLAT,FLAT))),
    ('low shelf +6 dB at 200 Hz, Q 0.7, band 1',dict(bands=(b.biquad('lowshelf',200,6,0.7,FS),FLAT,FLAT))),('high shelf -9 dB at 4 kHz, Q 0.7, band 3',dict(bands=(FLAT,FLAT,b.biquad('highshelf',4000,-9,0.7,FS)))),
    ('peak +6 dB at 12 kHz, Q 2, band 3',dict(bands=(FLAT,FLAT,PKT(12000,6,2)))),('low pass 2 kHz, Q 0.707, band 3 (a filter TotalMix does not offer there)',dict(bands=(FLAT,FLAT,b.biquad('lowpass',2000,0,0.7071,FS)))),
    ('all at once: low cut 80 Hz 2 poles, low shelf +4 dB 150 Hz, peak -6 dB 800 Hz Q 2, high shelf +3 dB 6 kHz',dict(bands=(b.biquad('lowshelf',150,4,0.7,FS),PKT(800,-6,2),b.biquad('highshelf',6000,3,0.7,FS)),**lc(80,2)))]
TX=[('exact low cut 100 Hz, 4 poles',lx(100,4)),('exact low cut 500 Hz, 4 poles',lx(500,4)),('exact low cut 100 Hz, 2 poles',lx(100,2)),('exact low cut 250 Hz, 1 pole',lx(250,1))]
CURVES={c['name']:c for c in json.load(open('eq-curves-measured.json'))['settings']}
def sine(where,label,frame):
    c=CURVES['sine: %s, %s'%(where,label)];assert bytes.fromhex(c['hex'])==bytes(frame),'the codec does not build the message that was sent: '+label
    add(c['name'],frame,'curve of 67 frequencies in eq-curves-measured.json; %d points compared, largest deviation from the calculation %.3f dB (in the stop band), rms %.4f dB'%(c['points_counted'],c['largest_deviation_db'],c['rms_deviation_db']),'measured')
for label,kw in T1:sine('output Main left, slot 0',label,b.set_eq(0,0,True,True,**kw))
for label,kw in (T1[1],T1[6],T1[10]):sine('input 1, slot 1',label,b.set_eq(1,0,False,True,**kw))
for label,kw in TX:sine('output Main left, slot 0',label,b.set_eq(0,0,True,True,**kw))
assert len(CURVES)==len(T1)+3+len(TX)+3+8+2
# run K1 on 18 November 2026: a cable from the 6.3 mm headphone socket to line input 3, a sine tone on playback 1, no other audio app open
for raw,db in ((244,0.5),(245,1.0),(249,3.0)):add('output level Phones left raw %d (+%.1f dB)'%(raw,db),b.set_output_level(6,raw),'measured behind the output: +%.2f dB above raw 243'%db,'measured')
add('output level Phones left raw 203 (-20 dB)',b.set_output_level(6,203),'measured behind the output: -20.00 dB below raw 243 and +10.00 dB above raw 183','measured')
add('output level Phones left raw 116 (-63.5 dB)',b.set_output_level(6,116),'measured behind the output: -33.76 dB below raw 183, 0.26 dB lower than the formula','measured')
for out,name in ((0,'left'),(1,'right')):
    add('mixer: input 3 to Main %s at 0 dB'%name,b.set_mixer(out,2,b.UNITY),'index %d; with Main at -30 dB its meter read 30.00 dB below the meter of input 3'%(26*out+2),'measured')
    add('mixer: input 3 to Main %s at -6.02 dB'%name,b.set_mixer(out,2,0x10000),'the Main meter read 36.02 dB below the meter of input 3','measured')
    add('mixer: input 3 off Main %s'%name,b.set_mixer(out,2,0),'the Main meter read 0','measured')
add('mixer: playback 1 to AS1 at 0 dB',b.set_mixer(4,12,b.UNITY),'index 116; peak word 30 then read the level of playback 1 (with AS1 at raw 243)','measured')
add('output level AS1 raw 243 (0 dB)',b.set_output_level(8,243),'peak word 30 read the level of playback 1 exactly','measured')
FS2=44100
for label,kw in (('low cut 100 Hz, 2 poles, corner solved',dict(low_cut_poles=2,low_cut=b.low_cut_coefficient_exact(100,2,FS2))),('peak +6 dB at 1 kHz, Q 1, band 2',dict(bands=(FLAT,b.biquad('peak',1000,6,1,FS2),FLAT))),('high shelf -9 dB at 4 kHz, Q 0.7, band 3',dict(bands=(FLAT,FLAT,b.biquad('highshelf',4000,-9,0.7,FS2))))):
    c=CURVES['sine: output Phones left, slot 2, %s (44.1 kHz)'%label];frame=b.set_eq(2,2,True,True,**kw);assert bytes.fromhex(c['hex'])==bytes(frame),'the codec does not build the message that was sent: '+label
    add(c['name'],frame,'coefficients for 44.1 kHz; curve of 66 frequencies in eq-curves-measured.json, read at line input 3; %d points compared, largest deviation %.3f dB, rms %.4f dB'%(c['points_counted'],c['largest_deviation_db'],c['rms_deviation_db']),'measured')
# runs R1 and R2 on 18 November 2026: no cable; a test app on the iPad reads the levels of the twelve input channels; no other audio app open
EXPECT={0:'-30.00 dB (Main at raw 183)',1:'-30.00 dB (Main at raw 183)',2:'-14.50 dB (headphones at raw 214)',3:'-14.50 dB (headphones at raw 214)',4:'0.00 dB (AS at raw 243)',5:'0.00 dB (AS at raw 243)'}
for k in range(12):
    name=b.OUTPUTS[k]
    add('loopback of output %d (%s) on'%(k,name),b.set_loopback(k,True),'input channel %d then carried playback 1 as that output sends it: %s relative to the tone; no other input channel changed'%(k+1,EXPECT.get(k,'0.00 dB (the ADAT outputs stood at 0 dB)')),'measured')
    add('loopback of output %d (%s) off'%(k,name),b.set_loopback(k,False),'input channel %d back to what its hardware input carries'%(k+1),'measured')
    if k not in (0,2,4):add('mixer: playback 1 to %s at 0 dB'%name,b.set_mixer(k,12,b.UNITY),'index %d; read through loopback of that output'%(26*k+12),'measured')
for raw,db in ((163,'-40.02'),(123,'-60.21'),(116,'-63.87'),(83,'-80.77'),(71,'-90.31'),(63,'-90.31')):add('output level Phones left raw %d'%raw,b.set_output_level(6,raw),'read through loopback: %s dB below raw 243; the law is floor(2^15 * 10^(dB/20)) / 2^15'%db,'measured')
add('output level Phones left raw 62',b.set_output_level(6,62),'read through loopback: silent, not one sample differed from zero; so is every lower value','measured')
add('output level Phones left raw 59, read through loopback',b.set_output_level(6,59),'the mute value of TotalMix FX: silent','measured')
FLAT2=b.FLAT_BAND
for out,ch,slot in (('Main right',1,3),('headphones right',3,4),('AS1',4,5),('ADAT3',6,6)):
    for label,kw in (('low cut 80 Hz 2 poles (corner solved), low shelf +4 dB 150 Hz, peak -6 dB 800 Hz Q 2, high shelf +3 dB 6 kHz',dict(bands=(b.biquad('lowshelf',150,4,0.7,FS2),b.biquad('peak',800,-6,2,FS2),b.biquad('highshelf',6000,3,0.7,FS2)),low_cut_poles=2,low_cut=b.low_cut_coefficient_exact(80,2,FS2))),
                     ('peak +12 dB at 100 Hz, Q 0.7, band 1',dict(bands=(b.biquad('peak',100,12,0.7,FS2),FLAT2,FLAT2)))):
        c=CURVES['sine through loopback: output %s, slot %d, %s (44.1 kHz)'%(out,slot,label)];frame=b.set_eq(slot,ch,True,True,**kw);assert bytes.fromhex(c['hex'])==bytes(frame),'the codec does not build the message that was sent: '+label
        add(c['name'],frame,'coefficients for 44.1 kHz; curve of 66 frequencies in eq-curves-measured.json, read digitally through loopback; %d points compared, largest deviation %.3f dB (below 20 Hz), rms %.4f dB'%(c['points_counted'],c['largest_deviation_db'],c['rms_deviation_db']),'measured')
# runs S1 and S2 on 18 November 2026: "EQ for Record", and one equaliser message before and after the sample rate changed
add('device settings: equaliser in the recording (bit 6 clear, clock bit set)',b.set_eq_in_recording(True),'read through loopback of an output with a peak of +12 dB: the recorded tone stood 12.0 dB higher than without equaliser','measured')
add('device settings: equaliser not in the recording (bit 6 set, clock bit set)',b.set_eq_in_recording(False),'the recorded tone stood at 0.0 dB, the equaliser of the output still on','measured')
for tag in ('coefficients for 44.1 kHz, read at 44.1 kHz','coefficients for 44.1 kHz, read at 48 kHz after the rate had changed'):
    c=CURVES['sine through loopback: output AS1, slot 5, peak +12 dB at 1 kHz, Q 2 (%s)'%tag];frame=b.set_eq(5,4,True,True,bands=(FLAT2,b.biquad('peak',1000,12,2,FS2),FLAT2));assert bytes.fromhex(c['hex'])==bytes(frame)
    add(c['name'],frame,'one message, sent once; curve of 66 frequencies in eq-curves-measured.json; %d points compared, largest deviation %.3f dB, rms %.4f dB'%(c['points_counted'],c['largest_deviation_db'],c['rms_deviation_db']),'measured')
# one synthetic state message: Main muted by raw 59, Phones -14.5 dB, mic gains 0, line gains 6.0 and 0 dB, both sensitivity bits set
w=[0]*44;w[0]=0x0090000C;w[1]=59|(59<<9);w[2]=(214<<14)|(214<<23);w[3]=(12<<19)
add('state (built for this file from the values our unit reported)',b.frame(0,w),'word 0 0x0090000C, Main raw 59/59, Phones raw 214/214, gains 0, 0, 12 half dB, 0','reported')
json.dump({'protocol':'RME Babyface Pro FS, class-compliant mode, MIDI SysEx on Port 2','vectors':V},open('test-vectors.json','w'),indent=1)
print(len(V))
