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
    for k in (0,1,12,18):add('line gain input %d %.1f dB'%(i,k/2),b.set_line_gain(i,k),'channel %d, %d half dB'%(i-1,k),'reported')
for settings,bit,on,what,status in ((0x0C,4,True,'pad of input 1 on','measured'),(0x1C,4,False,'pad of input 1 off','measured'),(0x0C,5,True,'pad of input 2 on','reported'),(0x0C,2,False,'sensitivity bit of input 3 cleared','reported'),(0x08,2,True,'sensitivity bit of input 3 set','reported'),(0x0C,3,False,'sensitivity bit of input 4 cleared','reported'),(0x08,4,True,'pad of input 1 on while the sensitivity bit of input 3 is clear','reported')):
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
add('output level Phones left raw 255 (+6 dB)',b.set_output_level(6,255),'channel 6, raw 255','reported')
add('output level AS1 raw 183 (-30 dB)',b.set_output_level(8,183),'channel 8','reported')
add('output level AS2 raw 59',b.set_output_level(9,59),'channel 9','reported')
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
assert len(CURVES)==len(T1)+3+len(TX)
# one synthetic state message: Main muted by raw 59, Phones -14.5 dB, mic gains 0, line gains 6.0 and 0 dB, both sensitivity bits set
w=[0]*44;w[0]=0x0090000C;w[1]=59|(59<<9);w[2]=(214<<14)|(214<<23);w[3]=(12<<19)
add('state (built for this file from the values our unit reported)',b.frame(0,w),'word 0 0x0090000C, Main raw 59/59, Phones raw 214/214, gains 0, 0, 12 half dB, 0','reported')
json.dump({'protocol':'RME Babyface Pro FS, class-compliant mode, MIDI SysEx on Port 2','vectors':V},open('test-vectors.json','w'),indent=1)
print(len(V))
