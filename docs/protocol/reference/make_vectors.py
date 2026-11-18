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
# one synthetic state message: Main muted by raw 59, Phones -14.5 dB, mic gains 0, line gains 6.0 and 0 dB, both sensitivity bits set
w=[0]*44;w[0]=0x0090000C;w[1]=59|(59<<9);w[2]=(214<<14)|(214<<23);w[3]=(12<<19)
add('state (built for this file from the values our unit reported)',b.frame(0,w),'word 0 0x0090000C, Main raw 59/59, Phones raw 214/214, gains 0, 0, 12 half dB, 0','reported')
json.dump({'protocol':'RME Babyface Pro FS, class-compliant mode, MIDI SysEx on Port 2','vectors':V},open('test-vectors.json','w'),indent=1)
print(len(V))
