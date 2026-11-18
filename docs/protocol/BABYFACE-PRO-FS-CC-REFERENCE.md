# RME Babyface Pro FS in class-compliant mode: control protocol reference

Version 1 draft, 18 November 2026. Public domain (Unlicense).

This document describes how a host application on iPadOS can read and set the Babyface Pro FS without TotalMix FX, over MIDI SysEx. It is written for someone who wants to build native support. Everything in it was worked out on one unit (Babyface Pro FS, iPad, iPadOS 27.2.1) between 8 and 18 November 2026.

Each statement carries one of four marks, so that nothing has to be taken on trust:

| Mark | Meaning |
|---|---|
| **measured** | The effect was measured at the unit's own meters, usually with a loop cable from XLR output 1 to XLR input 1 (what leaves output 1 is then read at the meter of input 1). The test signal was a music loop, or, for the frequency responses in 2.5, a sine tone from the iPad. |
| **reported** | The message was sent and the unit reported the new value back in its state. The effect on audio was not measured. |
| **notes** | Taken from other people's notes and not tried on our unit. Sources: the protocol notes on the oscmix wiki by Michael Forney (github.com/michaelforney/oscmix/wiki/Babyface-Pro) and the Babyface Pro part of the Linux kernel driver (`sound/usb/mixer_quirks.c`). |
| **unknown** | We found no source and no way to observe it. |

The folder `reference/` holds a small codec in Python (`babyface_cc.py`), 130 test vectors (`test-vectors.json`), the equaliser curves measured with sine tones (`eq-curves-measured.json`) and tests. The codec was checked against 1871 messages of the controller that was used on the unit: byte for byte the same.

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
| 0, 1 | Gain of microphone input 1, 2 | 0 to 65 dB in whole dB, packed (see below) | **reported** for all 66 values; **measured** at 0, 3 and 6 dB (3.0 and 6.0 dB at the input meter) |
| 2, 3 | Gain of line input 3, 4 | count of half dB, 0 to 18 (0 to 9 dB) | **reported** for all 19 values |
| 4, 5 | Main output left, right | raw level, see below | **measured** |
| 6, 7 | Headphone output left, right | raw level | **measured** |
| 8, 9 | AS1, AS2 output | raw level | **reported** (state word 3) |
| 10 and up | Presumably the ADAT outputs | | **unknown** |

**Output level.** `raw = 243 + 2 × dB`, in steps of 0.5 dB. Raw 243 is 0 dB, raw 183 is −30 dB, raw 116 is −63.5 dB. We wrote and read back values across the range 116 to 243. **reported** At raw 183 the output meter stood exactly 30.0 dB below the playback. **measured** The oscmix notes give the same law as `dB = 6 + (raw − 255) / 2`, which puts the top at raw 255 = +6 dB. Raw 249 and 255 were written to the left headphone channel, with no signal on the headphones, and the unit reported them back. **reported** The effect on audio above 0 dB was not measured.

**Mute.** There is no mute bit per output. TotalMix FX mutes an output by writing raw 59 to both of its channels (−92 dB by the formula) and restores the fader value on unmute. **reported** (watched on the same unit while TotalMix FX on a Mac was operated). A host that mutes should do the same and keep the previous value itself.

**Microphone gain packing.** The value written is not the dB number:

```
if dB < 60:  value = ((dB mod 3) << 5) | (dB div 3)
else:        value = ((dB mod 6) << 5) | 20
```

The state reports the gain as the plain dB number (section 3.1), so a write of packed 83 reads back as 59. **reported**

### 2.3 Input settings: sub ID `03`

One word: bits 0-15 say which setting changes (one bit set), bits 16-30 carry the complete new state of all settings.

| Bit | Setting | Status |
|---|---|---|
| 0, 1 | Phantom power (48 V) of microphone input 1, 2 | **notes**. Never sent by us, on purpose. |
| 2, 3 | Sensitivity of line input 3, 4. Set = "+4dBu", clear = "-10dBV" in the naming of the Linux driver | Switching **reported**, eight of eight. The naming is **notes**: the effect on a signal was not measured, and the idle noise of the inputs did not move with the bit. |
| 4, 5 | Pad of microphone input 1, 2 | **measured**: −10.2 dB at the input meter, exact return |
| 15 | Labelled "AN1->2" in the oscmix notes | **unknown** |

Because the state part carries every setting, a host must read the current settings first and send them back unchanged except for the one bit. This matters most for phantom power: a careless write of another setting with bits 0 and 1 at zero would presumably switch phantom power off. **notes**, not tried.

Example, pad of input 1 on while both sensitivity bits are set (settings `0C`): word = `0x10 | (0x1C << 16)`, message `F0 00 20 0D 10 03 10 00 70 00 00 F7`. **measured**

### 2.4 Mixer: sub ID `01`

One word: bits 0-11 cell index, bits 12-31 level.

- **Cell index** = 26 × output + source. **measured** for the cells listed below; the law itself is from the **notes**.
- **Sources:** 0 AN1, 1 AN2 (microphone inputs), 2 IN3, 3 IN4 (line inputs), 4-5 AS1/2, 6-11 ADAT3-8, 12-23 playback 1-12.
- **Outputs:** 0-1 AN1/2 (Main), 2-3 PH3/4 (headphones), 4-5 AS1/2, 6-11 ADAT3-8.
- **Level:** linear, `0x20000` is 0 dB, 0 is off. `level = round(0x20000 × 10^(dB/20))`. **measured**: at 0, −6 and −12 dB the headphone output stood within 0.0 dB of the expected level, at −30 and −48 dB within 0.1 dB.
- **Phase:** an inverted level L stands in the 20-bit field as `2^20 − L` (the two's complement). **measured**: a cell alone keeps its level exactly; two cells carrying the same signal gave −35.8 dBFS with equal signs and −44.6 dBFS with unequal signs, every combination twice with the same value.
- **Above unity:** levels up to `0x40000` (+6 dB) are taken. **measured**: the headphone output rose by exactly 3.0 dB and 6.0 dB for +3 dB and +6 dB on one cell, the other side unchanged.
- **Granularity:** the whole 20-bit field counts, down to its lowest bits. **measured** at the Main meter: field `0x10000` gave exactly half the peak value of `0x20000`; `0x1009C` read one meter step above `0x10098`; fields `0x10`, `8` and `7` gave −78.4 dB, −84.4 dB and less than `8`, as a linear level must. Below about −90 dB the meter itself stops resolving (its values move in steps of 64).

Cells measured on the unit: inputs 1-4 to headphones left and right (indices 52-55 and 78-81); playback 1 to headphones left and playback 2 to headphones right (64 and 91); playback 1 to Main left and playback 2 to Main right (12 and 39). For the two Main cells: −6 dB lowered that side of the Main output by exactly 6.0 dB, level 0 silenced it, unity brought it back, and the other side never moved. So the index law holds for outputs 0 to 3. Inputs to the Main output and every cell of the AS and ADAT outputs are **notes**.

There is no pan parameter. A stereo position is two cells with two levels; the host chooses the pan law. Ours lowers the far side by 1.5 dB per position and switches it off at the end. **measured** (6.0 dB at four positions).

Two properties a host must build around:

1. **The unit never reports its mixer.** There is no message that returns a cell. **measured** (nothing in the state changes when a cell is written).
2. **The unit forgets its mixer whenever its USB connection is built anew** (replug, loss of power). Gains, output levels and input settings survive. After such a loss the playback reaches the Main output only, and the headphones are silent. **measured**, many times.

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
- **The unit's own meters do not show the EQ.** The meter of an output stayed where it was while the level behind the output fell by 6 and 12 dB; the meter of input 1 did not move when the EQ of input 1 was on. **measured** For the headphone outputs we therefore could send the message but not see its effect (no cable there).
- **The coefficients depend on the sample rate.** Our unit ran at 48 kHz (see the next part); we did not try another rate.
- We found no word of the state message that reports the EQ, and did not test whether the unit keeps it when its USB connection is built anew. **unknown**

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

What follows for a host:

- **The unit does what the coefficients say.** A host can compute the curve it draws from the same numbers it sends.
- **The unit ran at 48 kHz.** The iPad reported 48,000 Hz for the connection, and the measured curves fit the calculation for 48 kHz (deviation 0.001 to 0.03 dB rms per curve) and not the one for 44.1 kHz (0.15 to 1.06 dB). The coefficients have to be computed for the rate the unit runs at.
- **The low cut of the notes sits a little high and takes some level.** With the k of the notes the −3 dB point is 0.7 % above f0 with one pole at 100 Hz, 7 % with four poles at 100 Hz, and 15 % with four poles at 500 Hz. The filter also stays below 0 dB in the pass band: −0.06 dB for 100 Hz with one pole, −0.10 dB for 100 Hz with four poles, −0.52 dB for 500 Hz with four poles. Whether TotalMix FX sends the same k we do not know. A host that wants the corner exactly at f0 solves k from the filter (`low_cut_coefficient_exact`); the level in the pass band can be made up with the overall gain (word 13).
- **A band takes any biquad** whose b0 is not zero, not only the three types TotalMix FX offers: a low pass was sent in band 3 and came out as calculated.

The codec builds this message (`set_eq`, `biquad`, `low_cut_coefficient`, `low_cut_coefficient_exact`) and calculates its curve (`eq_response_db`, `eq_from_words`).

### 2.6 Not tried: loopback, device settings

From the oscmix **notes** only:

- **Sub ID `02`, loopback:** bits 0-15 output channel, bit 16 loopback on.
- **Sub ID `00`, device settings:** mask in bits 0-15 and value in bits 16-30, as in 2.3. Bit 0 clock source, bit 6 "eq for record", bit 10 optical output ADAT or S/PDIF.

### 2.7 Resolution: which values exist

| Parameter | Range | Smallest step | Any value in between? |
|---|---|---|---|
| Main, headphone and AS output level | −63.5 to 0 dB used here; up to +6 dB accepted | 0.5 dB | yes, every half dB |
| Microphone gain | 0 to 65 dB | 1 dB | every whole dB |
| Line gain | 0 to 9 dB | 0.5 dB | every half dB |
| Mixer cell | off, then −102 dB to +6 dB | continuous (linear 20-bit value) | yes, any value; we used half-dB values |
| EQ band, low cut | whatever the coefficients express | continuous | yes |
| Pad, sensitivity, phantom power | on or off | | |

A host can therefore offer both: an absolute value ("headphones to −17.5 dB") and a relative step of any size ("11.5 dB up", "8.5 dB down"), as long as the result lies on the grid of that parameter. Our own page does this with a step width that can be set from 0.5 to 30 dB in half-dB steps; a 10.5 dB step down and back returned exactly to the starting value. **measured**

## 3. Messages from the unit to the host

A request is answered with three messages, in this order: sub ID `00` (227 bytes, 44 words), `01` (207 bytes, 40 words), `02` (207 bytes, 40 words). **measured**

### 3.1 State: sub ID `00`

| Word | Bits | Content | Status |
|---|---|---|---|
| 0 | 0-5 | Input settings, same bit numbers as in 2.3 | **reported** for bits 2-5; bits 0-1 by analogy only |
| 0 | 13 | Dim. While set, the Main level fields stand 40 raw steps (20 dB) lower | **reported** (TotalMix FX on a Mac) |
| 0 | 14, 15 | Global mute of TotalMix FX | **reported** (same) |
| 0 | 16-19 | Counter of the encoder, one detent = 1, wraps | **reported** |
| 0 | 20-23 | Mode and selection of the unit's own keys | **reported**, not fully decoded |
| 0 | 24, 28 | Flash briefly on a key press | **reported** |
| 0 | 30 | Clock source | **notes** |
| 1 | 0-7, 9-16 | Main left, Main right, raw level | **measured** |
| 2 | 0-6, 7-13 | Gain of microphone input 1, 2 in dB (plain number) | **reported** |
| 2 | 14-21, 23-30 | Headphones left, right, raw level | **measured** |
| 3 | 0-7, 9-16 | Level of AS1, AS2 (output channels 8, 9), raw | **reported** |
| 3 | 19-23, 24-28 | Gain of line input 3, 4 in half dB | **reported** |
| 4-43 | | RMS meters | **notes** |

How to *write* dim and the global mute is **unknown**.

A change made on the unit itself (encoder, keys) shows in the next state message. **reported** A host can therefore follow the hardware by polling.

### 3.2 Peak meters: sub ID `02`

Forty words. Full scale is `0x08000000`; `dBFS = 20 × log10(word / 0x08000000)`.

| Words | Content | Status |
|---|---|---|
| 0-3 | Inputs 1-4, before the EQ of the input | **measured** |
| 12-13 | Playback 1, 2 | **measured** |
| 26-27 | Main output left, right | **measured** |
| 28-29 | Headphone output left, right | **measured** |
| others | Further inputs, playback channels and outputs in the same order | **notes** |

The output meters sit behind the output level and before the EQ of the output. **measured** The meters read the digital peak exactly: a sine sent at 0.5, 0.25 and 0.125 of full scale read 0.50000, 0.25000 and 0.12501 at the playback meter (within 0.0004 dB), and with the Main output at −30 dB the Main meter read 30.00 dB below the playback meter. Over 67 frequencies from 10 Hz to 20 kHz the playback reading of one tone stayed within 0.0002 dB. **measured**

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
4. **Never write a setting without the others as read** (2.3). Put phantom power behind an explicit confirmation.
5. **Offer levels in dB.** Outputs: 0.5 dB steps, raw = 243 + 2 × dB. Microphone gain: whole dB, 0 to 65. Line gain: half dB, 0 to 9. Mixer: any dB value through the linear formula.
6. **Mute by level,** raw 59, and keep the value to return to.
7. **Expect foreign changes.** The encoder on the unit and another app can change levels at any time; the state shows it.
8. **Do not run next to TotalMix FX for iPad** without testing: both would poll and write, and each would take meter peaks from the other (3.2). We did not test this.
9. **Send every message in one piece** (section 1).

## 5. Coverage against what TotalMix FX offers

| Function | Status here |
|---|---|
| Main and headphone level, mute by level | **measured** |
| Microphone gain, line gain | **reported**, partly **measured** |
| Pad | **measured** |
| Line sensitivity (+4 dBu / −10 dBV) | switching **reported**, effect not measured |
| Monitoring of inputs and playback to the headphones: level, pan, phase | **measured** |
| Playback to the Main output: level, off | **measured** |
| Mixer levels above 0 dB, up to +6 dB | **measured** |
| Inputs to the Main output; all cells of the AS and ADAT outputs | **notes** |
| Level of the AS outputs | **reported** |
| Level of the ADAT outputs | **unknown** (channel numbers) |
| Output levels above 0 dB | **reported**, effect not measured |
| Phantom power | **notes**, never sent |
| EQ and low cut on inputs and outputs | **measured**, whole curves with sine tones at 48 kHz (not on the headphone outputs: no cable there) |
| Loopback, clock source, optical format, EQ for record | **notes** |
| Dim, mono, global mute, solo, stereo link, cue, talkback | reading of dim and global mute **reported**; writing **unknown** |
| Snapshots, layouts | belong to TotalMix FX, not to the unit |
| Reading the mixer back | not possible, the unit does not report it |

## 6. Open points we can still close on our unit

- The effect of the line sensitivity on a signal (needs a source at input 3 or 4).
- Inputs to the Main output (with the loop cable removed, to avoid a feedback path).
- Phantom power on an input with nothing connected.
- Loopback, with the loop cable removed.
- Whether the unit keeps the EQ across a reconnect; EQ at a sample rate other than 48 kHz; the EQ of the headphone outputs (needs a cable from a headphone output to an input).
- Whether a state part with phantom power bits left at zero switches phantom power off.

## 7. Sources

- Protocol notes on the oscmix wiki, Michael Forney: github.com/michaelforney/oscmix/wiki/Babyface-Pro
- Linux kernel, `sound/usb/mixer_quirks.c`, Babyface Pro part (bit numbers of the settings register, gain ranges)
- RME, Babyface Pro FS user's guide (ranges of the gains, pad)
- Our own measurements; the dated reports are public at the project's repository.
