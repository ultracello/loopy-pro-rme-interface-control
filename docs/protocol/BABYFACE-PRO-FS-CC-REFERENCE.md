# RME Babyface Pro FS in class-compliant mode: control protocol reference

Version 1.6, 22 November 2026. Public domain (Unlicense).

This document describes how a host application on iPadOS can read and set the Babyface Pro FS without TotalMix FX, over MIDI SysEx. It is written for someone who wants to build native support. Everything in it was worked out on one unit (Babyface Pro FS, iPad, iPadOS 27.2.1) between 8 and 22 November 2026.

Each statement carries one of four marks, so that nothing has to be taken on trust:

| Mark | Meaning |
|---|---|
| **measured** | The effect was measured at the unit's own meters, usually with a loop cable from XLR output 1 to XLR input 1 (what leaves output 1 is then read at the meter of input 1). The test signal was a music loop, or, for the frequency responses in 2.5, a sine tone from the iPad. Since 18 November some values are read digitally instead: through loopback (2.6) a test app on the iPad reads the level of what an output sends, with no cable and no converter in the way. |
| **reported** | The message was sent and the unit reported the new value back in its state. The effect on audio was not measured. |
| **notes** | Taken from other people's notes and not tried on our unit. Sources: the protocol notes on the oscmix wiki by Michael Forney (github.com/michaelforney/oscmix/wiki/Babyface-Pro) and the Babyface Pro part of the Linux kernel driver (`sound/usb/mixer_quirks.c`). |
| **unknown** | We found no source and no way to observe it. |

The folder `reference/` holds a small codec in Python (`babyface_cc.py`), 233 test vectors (`test-vectors.json`), the equaliser curves measured with sine tones (`eq-curves-measured.json`), the level of an output for every raw value (`output-level-law-measured.json`), the gain of a microphone input for every value (`mic-gain-measured.json`) and tests. The codec was checked against 1871 messages of the controller that was used on the unit: byte for byte the same.

## 1. Transport

- The unit shows two MIDI ports in CoreMIDI. Control runs on the second one, named "Port 2", as source and as destination. **measured**
- Every message is a SysEx: `F0 00 20 0D 10 <sub ID> <payload> F7`. **measured**
- The payload is a sequence of 32-bit words. Each word travels as five bytes of seven bits, least significant bits first: bits 0-6, 7-13, 14-20, 21-27, 28-31. **measured**
- We saw no message from the unit that was not the answer to a request (section 3). **measured**
- **A message has to arrive whole.** A SysEx that reaches the unit in several pieces has no effect. A mixer message that works when sent in one piece did nothing when sent as two pieces of 6 bytes, three of 4, or 11 bytes and the closing byte. **measured** The longest message, 87 bytes (2.5), is taken when it comes in one piece. **measured**
- **Messages may follow each other closely.** Two mixer messages 5, 30 or 100 ms apart both took effect, and so did four messages of two kinds 5 ms apart. **measured**

## 2. Messages from the host to the unit

### 2.1 Request state: sub ID `10`

`F0 00 20 0D 10 10 F7`, no payload. The unit answers with three messages (section 3). **measured**

The oscmix notes say TotalMix FX sends this about every 0.1 s. **notes** We polled at about three requests per second for a quarter of an hour, and more slowly for hours, and saw every request answered. **measured**

### 2.2 Levels and gains: sub ID `04`

One word: bits 0-15 channel, bits 16-23 value.

| Channel | What | Value | Status |
|---|---|---|---|
| 0, 1 | Gain of microphone input 1, 2 | 0 to 65 dB in whole dB, packed (see below) | **measured** on input 1 with a tone for every one of the 66 values (below); input 2 **reported** for all 66 values |
| 2, 3 | Gain of line input 3, 4 | count of half dB, 0 to 18 (0 to 9 dB) | **reported** for all 19 values; **measured** on input 3 with a tone: every step 0.50 dB, 9.00 dB at step 18 |
| 4, 5 | Main output left, right | raw level, see below | **measured** |
| 6, 7 | Headphone output left, right | raw level | **measured** |
| 8, 9 | AS1, AS2 output | raw level | **measured** through loopback for every raw value: the law of the headphone output (below). The state reports the value (word 3) |
| 10 to 15 | Nothing that we could find | raw level as above | **measured**: each was written with raw 183, 163 and 62 while all six ADAT outputs were read through loopback; all six stayed at 0.00 dB in all 24 readings, and no word of the state followed. The level of the ADAT outputs is set as a mixer entry instead (2.4). Channels above 15 are **unknown** |

**Output level.** `raw = 243 + 2 × dB`, in steps of 0.5 dB. Raw 243 is 0 dB, raw 183 is −30 dB, raw 116 is −63.5 dB. We wrote and read back values across the range 116 to 243. **reported** At raw 183 the output meter stood exactly 30.0 dB below the playback. **measured** The oscmix notes give the same law as `dB = 6 + (raw − 255) / 2`, which puts the top at raw 255 = +6 dB. Raw 249 and 255 were written to the left headphone channel, with no signal on the headphones, and the unit reported them back. **reported**

**Behind the output.** The headphone output left was read at line input 3 over a cable, with a sine tone. From raw 243, raw 244, 245, 249 and 255 gave +0.50, +1.00, +3.00 and +6.00 dB, and raw 223, 203 and 183 gave −10.00, −20.00 and −29.98 dB. From raw 183, raw 203, 163 and 143 gave +10.00, −10.01 and −20.02 dB. The lowest steps come out a little lower than the formula: raw 123 gave −30.12 dB and raw 116 gave −33.76 dB where the formula says −30 and −33.5. At raw 59 the output was silent (below the noise of the input, more than 97 dB under raw 243). **measured**

**The exact law.** Read digitally through loopback of the headphone output left, for every raw value from 243 down to 0: the gain is `floor(2^15 × 10^(dB/20)) / 2^15` with `dB = (raw − 243) / 2`. Every one of the 244 values lies within 0.003 dB of it. The steps are therefore half a dB only near the top: raw 183 gives −30.00 dB, raw 163 −40.02, raw 143 −50.05, raw 123 −60.21, raw 116 −63.87, raw 83 −80.77 dB; raw 63 to 74 all give −90.31 dB (the coefficient is 1 of 32768), and raw 62 and below are silent: not one sample differs from zero. On Main left raw 163, 143, 123 and 116 gave the same values relative to raw 183. AS1 and AS2, read the same way for every raw value, follow the same law: all 244 values of each lie within 0.002 dB of it, and raw 62 and below are silent. **measured** The table is in `reference/output-level-law-measured.json`, the law in the codec (`output_gain_from_raw`). A host that shows dB at low levels should compute them from this law.

**Mute.** There is no mute bit per output. TotalMix FX mutes an output by writing raw 59 to both of its channels and restores the fader value on unmute. **reported** Raw 59 is true silence, like every value up to 62. **measured** (watched on the same unit while TotalMix FX on a Mac was operated). A host that mutes should do the same and keep the previous value itself.

**Microphone gain, measured.** A sine left the unit on XLR output 1 and came back over a cable on XLR input 1; the level was read in what the host records, for every gain from 0 to 65 dB (the output 20.6 dB lower for the upper half, so the input stayed more than 10 dB under full scale; the two halves overlap over 26 values and agree within 0.011 dB). Every value lies within 0.11 dB of its nominal gain, 64.98 dB at 65. The steps inside a group of three (and from 60 to 65) are 0.99 to 1.01 dB; the steps onto a multiple of 3 dB are between 0.91 and 1.21 dB. The state reported every value as written. **measured** The table is in `reference/mic-gain-measured.json`. The step of the output between the two halves came out at 20.565 dB, where the law above gives 20.561 dB: the level law holds at the socket too.

**Microphone gain packing.** The value written is not the dB number:

```
if dB < 60:  value = ((dB mod 3) << 5) | (dB div 3)
else:        value = ((dB mod 6) << 5) | 20
```

The state reports the gain as the plain dB number (section 3.1), so a write of packed 83 reads back as 59. **reported**

### 2.3 Input settings: sub ID `03`

One word: bits 0-15 say which setting changes (one bit set), the bits from 16 on carry the complete new state of all settings, bit 16 for setting 0.

| Bit | Setting | Status |
|---|---|---|
| 0, 1 | Phantom power (48 V) of microphone input 1, 2 | **measured** with nothing connected to the inputs: the state reported the bit, and the switching showed as a transient on that input and no other (below). The voltage at the socket was not measured. |
| 2, 3 | Sensitivity of line input 3, 4. Set = "+4dBu", clear = "-10dBV" in the naming of the Linux driver | **measured** on input 3 with a tone: clearing the bit raised the level at the input meter by 8.74 dB, setting it again brought it back (0.00 dB). Set is therefore the less sensitive setting, as the naming says (the maximum input levels in RME's manual, +13 dBu and +4 dBu, are 9 dB apart). Switching of bit 3 is **reported**. |
| 4, 5 | Pad of microphone input 1, 2 | **measured**: −10.2 dB at the input meter, exact return |
| 13 | Dim, as a flag | **measured**: the unit takes the bit and reports it, and no output and no level field moves (below) |
| 14, 15 | The global mute of TotalMix FX, as flags; bit 15 is labelled "AN1->2" in the oscmix notes | **measured** in the same way: taken, reported, no effect on any output |

The state part carries every setting, so a host should read the current settings first and send them back unchanged except for the one bit. What the unit did with a state part that disagrees was tried once: with phantom power on at input 1, the pad of input 2 was switched with bit 0 left at zero in the state part. Phantom power stayed on: the state still reported it and input 1 showed no transient. So the unit followed the bit named in the first half and not the rest. **measured** for this one case; do not build on it.

**Phantom power, measured.** Inputs 1 and 2 were open (−117 dBFS RMS at gain 0, the noise of an open input). Switching 48 V on at input 1 took the unit's peak meter of that input from −105 to −55 dBFS, and the recorded noise needed seconds to settle; input 2 stayed at −105. Switching it off again gave a peak of −69 dBFS. Input 2 gave −58 and −71 dBFS, with input 1 quiet. The state reported bit 0 and bit 1 each time. A host should expect this transient and keep the input out of the monitoring while it switches.

**Dim and mute are flags.** With a tone on all twelve outputs, read through loopback (2.6), bits 13, 14 and 15 were each set and cleared: the state reported each bit, and not one output and not one level field moved. When TotalMix FX on a Mac dimmed, we had seen the Main level fields stand 40 raw steps lower while bit 13 was set; so the attenuation is the host's own write of the level, and the bit only says that it is in force. A host that dims writes the level 20 dB down and sets bit 13; a host that mutes writes raw 59 (2.2).

**The DIM lamp follows the flag, and the DIM key does not dim by itself.** With the unit on a Mac in this mode and a tool asking for its state, the owner pressed DIM twice with "Ch 1/2" selected: the state read after each press showed no flag and no changed level, and the lamp stayed dark. Then the flag was set by message: the lamp lit, and went out when the flag was cleared. **measured** (the lamp seen by the owner; the Main output stood at its mute value, raw 59, at the time). So in this mode the key is left to the host: it has to notice the press (bits 24 and 28 of state word 0 flash on a key press, 3.1) and do the dimming itself. That last step is our reading, not something we tried.

Example, pad of input 1 on while both sensitivity bits are set (settings `0C`): word = `0x10 | (0x1C << 16)`, message `F0 00 20 0D 10 03 10 00 70 00 00 F7`. **measured**

### 2.4 Mixer: sub ID `01`

One word: bits 0-11 cell index, bits 12-31 level.

- **Cell index** = 26 × output + source. **measured** for the cells listed below; the law itself is from the **notes**.
- **Sources:** 0 AN1, 1 AN2 (microphone inputs), 2 IN3, 3 IN4 (line inputs), 4-5 AS1/2, 6-11 ADAT3-8, 12-23 playback 1-12.
- **Outputs:** 0-1 AN1/2 (Main), 2-3 PH3/4 (headphones), 4-5 AS1/2, 6-11 ADAT3-8.
- **Level:** linear, `0x20000` is 0 dB, 0 is off. `level = round(0x20000 × 10^(dB/20))`. **measured**: at 0, −6 and −12 dB the headphone output stood within 0.0 dB of the expected level, at −30 and −48 dB within 0.1 dB.
- **Phase:** an inverted level L stands in the 20-bit field as `2^20 − L` (the two's complement). **measured**: a cell alone keeps its level exactly; two cells carrying the same signal gave −35.8 dBFS with equal signs and −44.6 dBFS with unequal signs, every combination twice with the same value.
- **Above unity:** levels up to `0x40000` (+6 dB) are taken. **measured**: the headphone output rose by exactly 3.0 dB and 6.0 dB for +3 dB and +6 dB on one cell, the other side unchanged.
- **Granularity:** the unit uses the level without its two lowest bits: the gain of a cell is `floor(level / 4) / 2^15`, a coefficient of 15 bits like that of the output level (2.2). **measured** digitally through loopback (2.6), playback 1 on ADAT3 with the cell at eighteen levels: every level that gives a signal lies within 0.001 dB of this law. `0x3333` (−20.00 dB by the plain ratio) gives −20.002 dB, `0x51F` −40.02, `0x83` −60.21, `0x10` −78.27 dB, and levels 1 to 3 are silent like 0. So below about −40 dB the level moves in visible steps, and −90.3 dB (levels 4 to 7) is the lowest. Earlier readings at the Main meter fit: `0x10000` gave exactly half the peak value of `0x20000`, `0x1009C` read one step above `0x10098`, and levels `0x10`, 8 and 7 gave −78.4 dB, −84.4 dB and less.

Cells measured on the unit: inputs 1-4 to headphones left and right (indices 52-55 and 78-81); playback 1 to headphones left and playback 2 to headphones right (64 and 91); playback 1 to Main left and playback 2 to Main right (12 and 39); input 3 to Main left and right (2 and 28): with the Main output at −30 dB its meter read 30.00 dB below the meter of input 3 at unity, 36.02 dB below at −6.02 dB, and 0 when off; playback 1 to AS1 (116): the meter of the AS1 output read the level of playback 1; and playback 1 to every one of the twelve outputs (12, 38, 64, 90, 116, 142, 168, 194, 220, 246, 272, 298), read through loopback (2.6): each output carried the tone at exactly its own level, −30.00 dB on Main at raw 183, −14.50 dB on the headphones at raw 214, 0.00 dB on AS1/2 at raw 243 and on the six ADAT outputs. For the two Main cells: −6 dB lowered that side of the Main output by exactly 6.0 dB, level 0 silenced it, unity brought it back, and the other side never moved. So the index law holds for outputs 0 to 3. Inputs on the digital outputs were read through loopback with nothing connected, the signal being the noise of the open inputs (−113 to −119 dBFS RMS): the four analogue inputs to AS1 (indices 104 to 107) and input 3 to ADAT3 and ADAT8 (158 and 288). With the cell at 0 dB the loopback channel carried the same RMS level as the input's own channel in the same stretch of time, within 0.002 dB; without a cell it was exactly silent. Input 3 at half level (`0x10000`) came out 6.20 dB lower, where 6.02 dB would be exact; at a signal of some twenty steps of a 24-bit word that is probably the rounding of the unit. **measured** So the index law holds for the AS and ADAT outputs too. The other cells of these outputs, and inputs 1, 2 and 4 to the Main output, were not tried one by one.

**The level of the ADAT outputs is a mixer entry.** Index 992 + output, with the level in the same field as for a cell (`0x20000` is 0 dB): 998 for ADAT3 up to 1003 for ADAT8. **measured** digitally through loopback (2.6), with playback 1 on all six outputs: each of the six entries moved exactly its own output and no other; half level gave −6.021 dB, `0x3333` −20.002 dB, level 0 silence, `0x20000` 0.00 dB again. Eighteen levels on entry 998 follow the law of the cells, `floor(level / 4) / 2^15`, within 0.002 dB. Entry and cell multiply: both at half level gave −12.041 dB. The outputs were found at 0 dB, and no word of the state follows these entries, so a host has to keep the value itself. The index comes from the Linux driver, which sets the output levels this way in the unit's other USB mode (**notes**); the gain message (2.2) with channels 10 to 15 does nothing. Levels above 0 dB, the entries 992 to 997 (Main, headphones, AS, whose level is set with sub ID 04) and whether the unit keeps the entries without power were not tried. The codec builds the message (`set_adat_output_level`).

There is no pan parameter. A stereo position is two cells with two levels; the host chooses the pan law. Ours lowers the far side by 1.5 dB per position and switches it off at the end. **measured** (6.0 dB at four positions).

Two properties a host must build around:

1. **The unit never reports its mixer.** There is no message that returns a cell. **measured** (nothing in the state changes when a cell is written).
2. **The unit forgets its mixer whenever it loses power.** Gains, output levels and input settings survive. After such a loss the playback reaches the Main output only, and the headphones are silent. **measured**, many times. Our unit was powered over its USB cable alone in these runs, so every replug was also a loss of power; a replug with the unit kept alive by a power supply of its own was not tried. Loopback (2.6) and the EQ (2.5) are forgotten in the same way. **measured**

So the host has to keep its own picture of every cell it has set and send it again after the unit reappears. Ours does that when the page is armed; across a real replug the headphone output came back exactly to the levels before.

### 2.5 Equaliser and low cut: sub ID `06`

Sixteen words (87 bytes), for one channel. The layout is from the oscmix **notes**; on our unit it does what the notes say. **measured**

- **Word 0, control:** bits 0-7 slot (0 to 20), bits 8-11 low cut, one bit per pole (1 pole `0001`, 2 poles `0011`, 3 poles `0111`, 4 poles `1111`), bits 16-19 channel 0-11, bit 20 channel type (0 input, 1 output), bit 31 EQ and low cut of that channel on.
- **Words 1-12:** three bands, four coefficients each in the order a1/a0, a2/a0, b1/b0, b2/b0, as signed 5.27 fixed point (−2.375 is `0xED000000`). The bands are biquads after the Audio EQ Cookbook; TotalMix FX uses its peaking, low-shelf and high-shelf types. A flat band is four zeros.
- **Word 13:** the product of b0/a0 of the three bands, the overall gain, in the same fixed point (1.0 is `0x08000000`).
- **Word 14:** the low cut, stored as 1 − k. The filter (k − k·z⁻¹) / (1 − k·z⁻¹) is applied once per pole. **measured** The notes give k = 1 / (2π·c·f0/fs + 1) with c = 1, 0.655, 0.528, 0.457 for 1 to 4 poles; with that k the −3 dB point lies a little above f0 (see below). **Word 15:** 0.

**Levels, with music.** The message went to the output channel Main left (type 1, channel 0) with the Main output at −30 dB, and the result was read behind the unit, at input 1 over the loop cable. The test signal was a music loop with most of its content below 2 kHz. Changes are from the peak values, to 0.01 dB.

| Setting on Main left | Expected | Measured |
|---|---|---|
| flat bands, overall gain 0.5 | −6.02 dB | −6.02 dB (slots 5 and 20) |
| flat bands, overall gain 0.25 | −12.04 dB | −12.04 dB |
| flat bands, overall gain 1.0 | 0 dB | 0.00 dB |
| low shelf −12 dB at 15 kHz, Q 0.7, in band 1 / band 2 / band 3 | about −12 dB | −12.01 / −12.01 / −12.02 dB |
| the same shelf in bands 1 and 2 | about −24 dB | −23.93 dB |
| high shelf −12 dB at 20 Hz in band 1 | lower by up to 12 dB | −10.64 dB |
| peak −12 dB at 1 kHz, Q 0.3 | lower | −3.47 dB |
| low cut at 2 kHz with 1 / 2 / 3 / 4 poles | lower with every pole | −13.89 / −19.07 / −19.96 / −20.42 dB |
| low cut with 4 poles at 500 Hz / 100 Hz | less than at 2 kHz | −8.56 / −0.71 dB |
| low cut 1 pole at 2 kHz and overall gain 0.5 | −13.89 − 6.02 = −19.91 dB | −19.90 dB |
| bit 31 clear | 0 dB | 0.00 dB |

The same on an input channel (type 0, channel 0, input 1 monitored alone on the left headphone channel, read at the headphone meter): overall gain 0.5 gave −6.02 dB, the low cut with 4 poles at 2 kHz −20.43 dB (on Main left: −20.42 and −20.43 dB), bit 31 clear 0.00 dB. **measured**

What follows for a host:

- **The slot is a shared memory.** Main left was given slot 5 with gain 0.5; then Main right was given the same slot with gain 0.25, and Main left went to −12.04 dB. So every channel with EQ or low cut on needs a slot of its own, 0 to 20 (slot 20 works). The host has to keep the list of slots in use. **measured**
- **Switching off goes by channel, not by slot.** A message for Main left with bit 31 clear switched its EQ off although it named another slot than the one in use. **measured**
- **The unit's own meters do not show the EQ.** The meter of an output stayed where it was while the level behind the output fell by 6 and 12 dB; the meter of input 1 did not move when the EQ of input 1 was on. **measured** The EQ of the headphone output was therefore measured behind the output, over a cable into line input 3 (next part).
- **The coefficients depend on the sample rate,** and the rate is the host's: our unit ran at 48 kHz while Loopy Pro was open and at 44.1 kHz when no other audio app was (see the next part).
- **The unit forgets the EQ when it loses power.** An EQ that made +12 dB was read through loopback, the USB cable (the unit's only supply) was pulled and plugged in again: afterwards the level stood at 0.0 dB until the EQ message was sent again. **measured** We found no word of the state message that reports the EQ. **unknown**

**Frequency responses, with sine tones.** A sine at half of full scale went from the iPad to USB playback 1 and through the output channel Main left (Main at −30 dB); the level was read behind the unit at input 1 over the loop cable, at 67 frequencies from 10 Hz to 20 kHz, once with the setting and once without. The difference is the measured curve. The calculated curve comes from the words of the message that was sent: three biquads, the overall gain, and the low cut filter above once per pole (`eq_response_db` in the codec). All curves are in `reference/eq-curves-measured.json`. **measured**

| Setting on Main left | Measured | Calculated |
|---|---|---|
| low cut 100 Hz with 1 / 2 / 3 / 4 poles, k of the notes | −3 dB at 100.7 / 103.0 / 105.2 / 107.1 Hz; at 20 Hz −14.17 / −21.38 / −27.02 / −31.71 dB | 100.7 / 103.0 / 105.2 / 107.1 Hz; −14.15 / −21.39 / −27.05 / −31.77 dB |
| low cut 20 Hz, 2 poles, k of the notes | −3 dB at 20.5 Hz | 20.4 Hz |
| low cut 500 Hz, 4 poles, k of the notes | −3 dB at 572.8 Hz; −0.52 dB at 20 kHz | 572.8 Hz; −0.52 dB |
| low cut with k solved for the corner: 100 Hz 4 poles / 100 Hz 2 poles / 250 Hz 1 pole / 500 Hz 4 poles | −3 dB at 100.1 / 100.1 / 250.2 / 500.6 Hz | 100.1 / 100.1 / 250.2 / 500.6 Hz (read off the same grid of frequencies) |
| peak +6 dB at 1 kHz, Q 1 | +5.99 dB at 1016 Hz, +0.27 dB at 202 Hz, +0.39 dB at 4064 Hz | +5.99, +0.27, +0.39 dB |
| peak −12 dB at 1 kHz, Q 5 | −11.61 dB at 1016 Hz, −0.03 dB at 202 Hz | −11.61, −0.03 dB |
| peak +12 dB at 100 Hz, Q 0.7, in band 1 | +12.00 dB at 101 Hz, +5.81 dB at 50 Hz, +5.68 dB at 202 Hz | +12.00, +5.82, +5.68 dB |
| low shelf +6 dB at 200 Hz, Q 0.7 | +6.00 dB at 20 Hz, +2.96 dB at 202 Hz, +0.01 dB at 1016 Hz | +6.00, +2.96, +0.01 dB |
| high shelf −9 dB at 4 kHz, Q 0.7 | −4.63 dB at 4064 Hz, −9.00 dB at 20 kHz | −4.64, −9.00 dB |
| peak +6 dB at 12 kHz, Q 2, in band 3 | +5.58 dB at 11.5 kHz, +0.13 dB at 20 kHz | +5.58, +0.13 dB |
| low pass 2 kHz, Q 0.707, in band 3 | −0.28 dB at 1016 Hz, −12.86 dB at 4064 Hz, −34.00 dB at 11.5 kHz | −0.28, −12.86, −34.07 dB |
| low cut 80 Hz 2 poles, low shelf +4 dB 150 Hz, peak −6 dB 800 Hz Q 2 and high shelf +3 dB 6 kHz together | −13.93 dB at 20 Hz, +1.14 dB at 101 Hz, −3.17 dB at 1016 Hz, +2.81 dB at 11.5 kHz | −13.93, +1.14, −3.17, +2.81 dB |

Of the 1407 points of the 21 curves, 1355 lay at least 30 dB above the noise and were compared. From 20 Hz up and where the curve lies above −20 dB (1219 points) every point is within 0.02 dB of the calculation, except one at 50.4 Hz with 0.05 dB (next to the mains frequency). Deeper in the stop band and below 20 Hz the difference grows to 0.17 dB at most, which is noise and the short reading time there. Three settings were also measured on input 1 (heard alone on the left headphone channel, read at the headphone meter): low cut 100 Hz with 2 poles, the peak at 1 kHz and the high shelf at 4 kHz gave the same curves as on the output. **measured**

The headphone output left (type 1, channel 2) was measured the same way at line input 3, over a cable from the 6.3 mm headphone socket, at 66 frequencies up to 18.2 kHz. No other audio app was open then, the iPad reported 44,100 Hz, and the coefficients were computed for that rate: low cut 100 Hz with 2 poles (corner solved, −3 dB at 100.1 Hz), peak +6 dB at 1 kHz (+5.99 dB at 1016 Hz) and high shelf −9 dB at 4 kHz (−4.64 dB at 4064 Hz, −9.00 dB at 18.2 kHz). All 198 points were compared; from 20 Hz up and above −20 dB every one is within 0.01 dB of the calculation for 44.1 kHz. **measured**

Four more outputs were read digitally through loopback (2.6), also at 44.1 kHz: Main right, headphones right, AS1 and ADAT3 (output channels 1, 3, 4 and 6), each with two settings, a peak of +12 dB at 100 Hz and a combination of low cut, low shelf, peak and high shelf. The four outputs gave the same curves. Of the 528 points, the 480 from 20 Hz up lie within 0.012 dB of the calculation (0.002 dB rms; the peak setting alone within 0.004 dB); below 20 Hz the low-cut curve differs by up to 0.044 dB. With that the EQ is measured on inputs, on Main, on both headphone channels, on AS and on an ADAT output. **measured**

What follows for a host:

- **The unit does what the coefficients say.** A host can compute the curve it draws from the same numbers it sends.
- **The unit runs at the rate the host sets, and the coefficients must match it.** With Loopy Pro open the iPad reported 48,000 Hz, and the curves fit the calculation for 48 kHz (deviation 0.001 to 0.03 dB rms per curve) and not the one for 44.1 kHz (0.15 to 1.06 dB). With no other audio app open the iPad reported 44,100 Hz, and the curves fit 44.1 kHz (0.004 to 0.009 dB) and not 48 kHz (0.22 to 0.65 dB). So the rate can change when another app opens or closes, and the host then has to compute the coefficients anew and send them again. **The unit keeps the coefficients it holds when the rate changes**, so the curve moves: one message with a peak of +12 dB at 1 kHz, computed for 44.1 kHz, was read through loopback at 44.1 kHz and again after Loopy Pro had been opened and the rate had become 48 kHz. Before, the curve fitted the calculation for 44.1 kHz; after, it fitted what the same coefficients give at 48 kHz, each time within 0.001 dB at 60 frequencies from 20 Hz up (the peak then lies near 1.09 kHz). Loopback and the mixer cell stayed as they were across the change. **measured**
- **The low cut of the notes sits a little high and takes some level.** With the k of the notes the −3 dB point is 0.7 % above f0 with one pole at 100 Hz, 7 % with four poles at 100 Hz, and 15 % with four poles at 500 Hz. The filter also stays below 0 dB in the pass band: −0.06 dB for 100 Hz with one pole, −0.10 dB for 100 Hz with four poles, −0.52 dB for 500 Hz with four poles. Whether TotalMix FX sends the same k we do not know. A host that wants the corner exactly at f0 solves k from the filter (`low_cut_coefficient_exact`); the level in the pass band can be made up with the overall gain (word 13).
- **A band takes any biquad** whose b0 is not zero, not only the three types TotalMix FX offers: a low pass was sent in band 3 and came out as calculated.

The codec builds this message (`set_eq`, `biquad`, `low_cut_coefficient`, `low_cut_coefficient_exact`) and calculates its curve (`eq_response_db`, `eq_from_words`).

### 2.6 Loopback: sub ID `02`; device settings: sub ID `00`

**Loopback.** One word: bits 0-15 output channel (0 to 11, in the order of 2.4), bit 16 on. While loopback of an output is on, the host records the signal of that output on the input channel of the same number, in place of the hardware input. **measured** for all twelve outputs, with a test app on the iPad that reads the level of each of the twelve input channels (the iPad shows the unit with twelve inputs and twelve outputs):

- With a tone on playback 1 sent to output k and loopback of output k on, input channel k+1 carried the tone and no other channel changed; with loopback off the channel carried its hardware input again (noise around −105 dBFS peak on the four analogue inputs, exact silence on the digital ones).
- **The signal is taken behind the output level.** Main left at raw 183 gave the tone 30.00 dB down, at raw 163 a further 10.02 dB (the law of 2.2), and at the mute value exact silence.
- **It is taken behind the output EQ.** An overall gain of 0.5 on the EQ of the output lowered the recorded level by 6.02 dB; EQ off brought it back.
- The unit's own peak meters did not show loopback when it was tried for AS1: no peak word changed.

By RME's manual the hardware input still reaches the mixer of the unit while loopback is on. A host that passes a recorded input on to an output must not switch on loopback of that same output: that is a way round with no cable. **Loopback is forgotten when the unit loses power**: after the same replug the input channel was silent with the mixer cell sent again, and carried the tone once loopback had been sent again. **measured** We found no word of the state message that reports loopback. The codec builds the message (`set_loopback`).

**Device settings.** Sub ID `00`, one word: mask in bits 0-15 and state in bits 16-30, as in 2.3. The oscmix **notes** name bit 0 clock source, bit 6 "eq for record" and bit 10 optical output ADAT or S/PDIF; notes on the unit's other USB mode say that bit 0 set means the internal clock.

Bit 6 was tried, with mask `0x0040` and bit 0 set in the state: **measured** through loopback of an output whose EQ made +12 dB at the test tone.

- State `0x0001` (bit 6 clear): the recorded tone stood 12.0 dB higher than without EQ. The EQ is in what the host records. This is how the unit was found.
- State `0x0041` (bit 6 set): 0.0 dB, with the EQ of the output still on. The EQ is not in what the host records.
- Each was sent twice in changing order; the message sets the state and does not toggle it. So in this mode a set bit 6 takes the EQ out of the recording.

The same setting decides whether the EQ of an input is recorded. **measured** with a tone over a cable into input 1 and an EQ on that input making +12 dB at the tone: with bit 6 clear the recorded tone stood 12.00 dB higher than without EQ, with bit 6 set at 0.00 dB, each state three and two times in turn. **Clock source, reported.** Bit 0 was written with mask `0x0001`, on a Mac and with no digital input signal: set, bit 30 of state word 0 stood set in the next state; clear, it stood clear; each way more than once. The unit was found with the bit clear, which by the notes is AutoSync, the default of this mode by RME's manual. What it does to audio was not measured; without a digital input the unit is its own master either way. **reported**

**The unit follows the bit named in the mask.** Messages that named bit 10 or bit 6 and carried bit 0 set in their state part left bit 30 clear. **reported** So our messages for EQ for Record did not switch the clock source, and by the same rule will not have switched the optical format.

**Optical format, reported on the unit's own display.** Bit 10 clear is ADAT, bit 10 set is S/PDIF. The unit was plugged in anew and nothing asked for its state; with "Opt" selected and SET pressed, its level meters showed eight lamps, which by RME's manual means ADAT. Bit 10 was then written set, with mask `0x0400` and no state request: the meters changed to two lamps, S/PDIF. Written clear: eight lamps again. **reported** (read by the owner). No word of the state follows the bit, and what leaves the optical socket was not measured, for lack of a device there.

**Clock source and optical format, measured on an optical link.** An optical cable led from the unit's optical output into its own optical input. Playback 1 was sent to the outputs AS1, ADAT3 and ADAT8 at 0 dB, loopback off, and the tone read on the input channels 5, 7 and 12, which then carry what arrives at the optical input.

- Format bit clear (ADAT), clock bit set: the tone arrived on all three channels at 0.00 dB, in 8 of 8 readings. Format bit set (S/PDIF): on channel 5 at 0.00 dB, and channels 7 and 12 were exactly silent, in 4 of 4. So S/PDIF carries the first pair only, and the optical input takes either format without being told.
- Clock bit set (state bit 30 set): 0.00 dB on all three channels and exact silence on the other optical channels, in 12 of 12 readings. Clock bit clear: the tone came back damaged, at about −13, −4 and −21 dB on the three channels, with noise around −60 dBFS on the others, in 12 of 12. With the bit clear the unit follows the digital input (AutoSync), and here that input was its own output, a loop with no clock to follow; with the bit set it keeps its own clock.

**measured** A host should set the clock bit before it relies on an optical link it cannot vouch for, and should know that a unit left on AutoSync follows whatever arrives.

**Keys and display belong to the host while it asks.** As long as a host was asking for the state, the unit's own display for the format stayed dark and its DIM key did nothing (2.3); after the unit was plugged in anew, with writes alone, the display worked and followed them. So it seems to be the state request that hands the keys of the unit to the host. We did not find out how the unit takes them back other than by being plugged in again.

The codec builds the messages (`set_eq_in_recording`, `set_device_setting`).

### 2.7 Resolution: which values exist

| Parameter | Range | Smallest step | Any value in between? |
|---|---|---|---|
| Main, headphone and AS output level | −63.5 to 0 dB used here; up to +6 dB accepted | 0.5 dB | yes, every half dB |
| Microphone gain | 0 to 65 dB | 1 dB | every whole dB |
| Line gain | 0 to 9 dB | 0.5 dB | every half dB |
| ADAT output level | off, then −90.3 dB to 0 dB (higher not tried) | 1/32768 of unity | yes; fine down to about −40 dB, coarser below |
| Mixer cell | off, then −90.3 dB to +6 dB | 1/32768 of unity (the level without its two lowest bits) | yes; fine down to about −40 dB, coarser below |
| EQ band, low cut | whatever the coefficients express | continuous | yes |
| Pad, sensitivity, phantom power | on or off | | |

A host can therefore offer both: an absolute value ("headphones to −17.5 dB") and a relative step of any size ("11.5 dB up", "8.5 dB down"), as long as the result lies on the grid of that parameter. Our own page does this with a step width that can be set from 0.5 to 30 dB in half-dB steps; a 10.5 dB step down and back returned exactly to the starting value. **measured**

## 3. Messages from the unit to the host

A request is answered with three messages, in this order: sub ID `00` (227 bytes, 44 words), `01` (207 bytes, 40 words), `02` (207 bytes, 40 words). **measured**

### 3.1 State: sub ID `00`

| Word | Bits | Content | Status |
|---|---|---|---|
| 0 | 0-5 | Input settings, same bit numbers as in 2.3 | **reported** for all six bits |
| 0 | 13 | Dim, a flag. With TotalMix FX on a Mac the Main level fields stood 40 raw steps (20 dB) lower while it was set; written by a host it changes nothing else (2.3) | **reported** |
| 0 | 14, 15 | Global mute of TotalMix FX, flags (2.3) | **reported** |
| 0 | 16-19 | Counter of the encoder, one detent = 1, wraps | **reported** |
| 0 | 20-23 | Mode and selection of the unit's own keys. Read 9 with OUT on "Opt" and IN on "Ch 3/4", 8 with OUT on "Opt" and IN on "Ch 1/2", 4 with both on "Ch 1/2"; and 9 once with OUT on "Ch 1/2" and IN not noted | **reported**, not decoded |
| 0 | 24, 28 | Flash briefly on a key press | **reported** |
| 0 | 9 | The output selection "Opt" of the unit's own OUT key: set in both readings with OUT on "Opt" (IN on "Ch 3/4" and on "Ch 1/2"), clear in both with OUT on "Ch 1/2". Writing a pad or a sensitivity bit left it as it was | **reported** |
| 0 | 30 | Clock source: follows bit 0 of the device settings (2.6) | **reported** |
| 1 | 0-7, 9-16 | Main left, Main right, raw level | **measured** |
| 2 | 0-6, 7-13 | Gain of microphone input 1, 2 in dB (plain number) | **reported** |
| 2 | 14-21, 23-30 | Headphones left, right, raw level | **measured** |
| 3 | 0-7, 9-16 | Level of AS1, AS2 (output channels 8, 9), raw | **reported** |
| 3 | 19-23, 24-28 | Gain of line input 3, 4 in half dB | **reported** |
| 4-43 | | RMS meters | **notes** |

Dim and the global mute are written with the settings message (2.3); they are flags and attenuate nothing.

A change made on the unit itself (encoder, keys) shows in the next state message. **reported** A host can therefore follow the hardware by polling.

### 3.2 Peak meters: sub ID `02`

Forty words. Full scale is `0x08000000`; `dBFS = 20 × log10(word / 0x08000000)`.

| Words | Content | Status |
|---|---|---|
| 0-3 | Inputs 1-4, before the EQ of the input | **measured** |
| 12-13 | Playback 1, 2 | **measured** |
| 26-27 | Main output left, right | **measured** |
| 30 | AS1 output | **measured** (read the level of playback 1 when that was sent to AS1 at 0 dB) |
| 28-29 | Headphone output left, right | **measured** |
| others | Further inputs, playback channels and outputs in the same order | **notes** |

The output meters sit behind the output level and before the EQ of the output. **measured** The meters read the digital peak exactly: a sine sent at 0.5, 0.25 and 0.125 of full scale read 0.50000, 0.25000 and 0.12501 at the playback meter (within 0.0004 dB), and with the Main output at −30 dB the Main meter read 30.00 dB below the playback meter. With no other audio app open the reading for 0.5 was exactly `0x04000000` and a silent channel read 0; next to Loopy Pro a silent channel read about 1200 (−101 dBFS). Over 67 frequencies from 10 Hz to 20 kHz the playback reading of one tone stayed within 0.0002 dB. **measured**

**Each answer carries the peak since the previous request.** The unit holds the highest value until it is asked, and starts anew after every answer. **measured**: after pauses of 2.0 to 5.2 seconds without a request, the first answer showed the loudest spot of a 2-second test loop every time (8 of 8), while the answers 0.3 seconds later lay up to 6.5 dB lower; and after a source was switched off, the first answer four seconds later still showed signal from before, the next one silence. Three things follow:

- The polling interval is the window of the meter. Poll a few times a second for a moving display.
- To verify a write by the meters, throw away the first answer after the write and read on. Our earlier figure of "0.65 to 2.19 seconds of lag" came from not doing so.
- Two hosts that poll the same unit take the peaks away from each other.

Sub ID `01` carries RMS values in the same shape. **notes**

## 4. What a native integration should do

These are the rules our controller follows. Several hundred writes went through them on the unit, among them a soak of 400 that was measured press by press; none was lost.

1. **Read before every write.** Take a fresh state, compute the new value from it, write once.
2. **Read back.** Ask for the state again about 100 ms after the write and compare. The unit answered every time. For the mixer and the EQ there is nothing to compare; the answer only shows that the unit is alive.
3. **Keep the mixer picture and send it again** when the unit reappears. Do not touch cells the user never set. Keep the EQ settings and the slot of each channel in the same way.
4. **Never write a setting without the others as read** (2.3). Bits of word 0 that belong to the keys of the unit (bit 9, bits 16 and up) are not settings: a host that refuses to write while it sees a bit it does not know will lock itself out when the user presses OUT on the unit, as our controller did until it was taught bit 9. With OUT on "Opt" the pad of input 1 and the sensitivity of input 4 were then written and read back, and the selection of the unit stayed. **measured** for these two. Put phantom power behind an explicit confirmation, and expect a transient on the input when it switches.
5. **Offer levels in dB.** Main, headphone and AS outputs: 0.5 dB steps, raw = 243 + 2 × dB. ADAT outputs: the mixer entry 992 + output, linear like a cell. Microphone gain: whole dB, 0 to 65. Line gain: half dB, 0 to 9. Mixer: any dB value through the linear formula.
6. **Mute by level,** raw 59, and keep the value to return to. **Dim by level** as well, 20 dB down, and set the dim flag (2.3) so that the state says so.
7. **Expect foreign changes.** The encoder on the unit and another app can change levels at any time; the state shows it.
8. **Do not run next to TotalMix FX for iPad** without testing: both would poll and write, and each would take meter peaks from the other (3.2). We did not test this.
9. **Send every message in one piece** (section 1).

## 5. Coverage against what TotalMix FX offers

The last column says whether the controller page this project uses in Loopy Pro offers the function today.

| Function | Status here | On our controller page |
|---|---|---|
| Main and headphone level, mute by level | **measured**, the law for every raw value | yes |
| Microphone gain, line gain | **measured**: microphone gain of input 1 for every value 0 to 65 dB, line gain of input 3 step by step; inputs 2 and 4 **reported** | yes |
| Pad | **measured** | yes |
| Line sensitivity (+4 dBu / −10 dBV) | **measured** on input 3 (8.74 dB) | yes |
| Monitoring of inputs and playback to the headphones: level, pan, phase | **measured** | yes |
| Playback to the Main output: level, off | **measured** | no |
| Mixer levels above 0 dB, up to +6 dB | **measured** | no |
| Inputs to the Main output | **measured** (input 3 to Main left and right) | no |
| Cells of the AS and ADAT outputs | **measured** through loopback: playback 1 to each of them; the four analogue inputs to AS1, input 3 to ADAT3 and ADAT8 | no |
| Level of the AS outputs | **measured**, the law for every raw value | no |
| Level of the ADAT outputs | **measured**: mixer entry 992 + output, every one of the six, down to silence; they stood at 0 dB | no |
| Output levels above 0 dB | **measured** behind the headphone output (+0.5 to +6 dB) | no |
| Phantom power | **measured** at open inputs: the switching transient on that input alone, and the bit in the state; the voltage itself not | no |
| EQ and low cut on inputs and outputs | **measured**, whole curves with sine tones: input 1 and Main left at 48 kHz; both headphone channels, Main right, AS1 and ADAT3 at 44.1 kHz | no |
| Loopback | **measured** for all twelve outputs | no |
| EQ for Record | **measured** for the EQ of an output in loopback and for the EQ of an input (bit 6 of the device settings) | no |
| Clock source, optical format | **measured** on an optical link from the unit's output into its own input: ADAT carries all eight channels, S/PDIF the first pair; the clock bit decides between the unit's own clock and the incoming signal | no |
| Dim, global mute | **measured**: the unit keeps and reports a flag for each and attenuates nothing; the host does it with the levels | no |
| Mono, solo, stereo link, cue, talkback | by RME's manual functions of the control room of TotalMix FX; a host builds them from levels and mixer cells, the unit has nothing of its own for them that we know of |  |
| Snapshots, layouts | belong to TotalMix FX, not to the unit |  |
| Reading the mixer back | not possible, the unit does not report it |  |

## 6. Open points we can still close on our unit

- A replug with the unit kept alive by a power supply of its own: does it keep mixer, loopback and EQ then?
- Where the unit reports its device settings, if it does.
- How a host tells a press of the DIM key from the other keys of the unit (which of the bits that flash in state word 0), and whether the key behaves the same with the Main output not muted.
- Clock source and optical format with a second device at the optical sockets (measured so far with the unit's own output as its input).
- How the unit takes its keys back from a host, short of being plugged in again.

## 7. Sources

- Protocol notes on the oscmix wiki, Michael Forney: github.com/michaelforney/oscmix/wiki/Babyface-Pro
- Linux kernel, `sound/usb/mixer_quirks.c`, Babyface Pro part (bit numbers of the settings register, gain ranges)
- RME, Babyface Pro FS user's guide (ranges of the gains, pad)
- Our own measurements; the dated reports are public at the project's repository.
