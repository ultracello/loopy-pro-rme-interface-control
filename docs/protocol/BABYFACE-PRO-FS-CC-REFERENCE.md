# RME Babyface Pro FS in class-compliant mode: control protocol reference

Version 1 draft, 18 November 2026. Public domain (Unlicense).

This document describes how a host application on iPadOS can read and set the Babyface Pro FS without TotalMix FX, over MIDI SysEx. It is written for someone who wants to build native support. Everything in it was worked out on one unit (Babyface Pro FS, iPad, iPadOS 27.2.1) between 8 and 18 November 2026.

Each statement carries one of four marks, so that nothing has to be taken on trust:

| Mark | Meaning |
|---|---|
| **measured** | The effect was measured at the unit's own meters, usually with a loop cable from XLR output 1 to XLR input 1. |
| **reported** | The message was sent and the unit reported the new value back in its state. The effect on audio was not measured. |
| **notes** | Taken from other people's notes and not tried on our unit. Sources: the protocol notes on the oscmix wiki by Michael Forney (github.com/michaelforney/oscmix/wiki/Babyface-Pro) and the Babyface Pro part of the Linux kernel driver (`sound/usb/mixer_quirks.c`). |
| **unknown** | We found no source and no way to observe it. |

The folder `reference/` holds a small codec in Python (`babyface_cc.py`), 84 test vectors (`test-vectors.json`) and tests. The codec was checked against 1871 messages of the controller that was used on the unit: byte for byte the same.

## 1. Transport

- The unit shows two MIDI ports in CoreMIDI. Control runs on the second one, named "Port 2", as source and as destination. **measured**
- Every message is a SysEx: `F0 00 20 0D 10 <sub ID> <payload> F7`. **measured**
- The payload is a sequence of 32-bit words. Each word travels as five bytes of seven bits, least significant bits first: bits 0-6, 7-13, 14-20, 21-27, 28-31. **measured**
- We saw no message from the unit that was not the answer to a request (section 3). **measured**

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
- **Granularity:** we only sent levels that are multiples of 8. Whether finer values are taken is **unknown**.

Cells measured on the unit: inputs 1-4 to headphones left and right (indices 52-55 and 78-81); playback 1 to headphones left and playback 2 to headphones right (64 and 91); playback 1 to Main left and playback 2 to Main right (12 and 39). For the two Main cells: −6 dB lowered that side of the Main output by exactly 6.0 dB, level 0 silenced it, unity brought it back, and the other side never moved. So the index law holds for outputs 0 to 3. Inputs to the Main output and every cell of the AS and ADAT outputs are **notes**.

There is no pan parameter. A stereo position is two cells with two levels; the host chooses the pan law. Ours lowers the far side by 1.5 dB per position and switches it off at the end. **measured** (6.0 dB at four positions).

Two properties a host must build around:

1. **The unit never reports its mixer.** There is no message that returns a cell. **measured** (nothing in the state changes when a cell is written).
2. **The unit forgets its mixer whenever its USB connection is built anew** (replug, loss of power). Gains, output levels and input settings survive. After such a loss the playback reaches the Main output only, and the headphones are silent. **measured**, many times.

So the host has to keep its own picture of every cell it has set and send it again after the unit reappears. Ours does that when the page is armed; across a real replug the headphone output came back exactly to the levels before.

### 2.5 Not tried: loopback, EQ, device settings

From the oscmix **notes** only:

- **Sub ID `02`, loopback:** bits 0-15 output channel, bit 16 loopback on.
- **Sub ID `06`, EQ and low cut:** 16 words. Word 0: bits 0-7 EQ slot, bits 8-11 low-cut poles, bits 16-19 channel, bit 20 input or output, bit 31 enabled. Words 1-12: three bands of biquad coefficients (a1/a0, a2/a0, b1/b0, b2/b0) as signed 5.27 fixed point. Word 13 overall gain, word 14 the low-cut coefficient.
- **Sub ID `00`, device settings:** mask in bits 0-15 and value in bits 16-30, as in 2.3. Bit 0 clock source, bit 6 "eq for record", bit 10 optical output ADAT or S/PDIF.

### 2.6 Resolution: which values exist

| Parameter | Range | Smallest step | Any value in between? |
|---|---|---|---|
| Main, headphone and AS output level | −63.5 to 0 dB used here; up to +6 dB accepted | 0.5 dB | yes, every half dB |
| Microphone gain | 0 to 65 dB | 1 dB | every whole dB |
| Line gain | 0 to 9 dB | 0.5 dB | every half dB |
| Mixer cell | off, then about −60 dB to +6 dB | continuous (linear value) | yes; we used half-dB values |
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
| 0-3 | Inputs 1-4 | **measured** |
| 12-13 | Playback 1, 2 | **measured** |
| 26-27 | Main output left, right | **measured** |
| 28-29 | Headphone output left, right | **measured** |
| others | Further inputs, playback channels and outputs in the same order | **notes** |

The output meters sit behind the output level. **measured**

**The meters lag.** A new level takes 0.65 to 2.19 seconds to show (median 1.38 s over 400 readings; 24 of them above two seconds). A host that verifies a write by the meters has to wait about three seconds or poll until the value stands. **measured**

Sub ID `01` carries RMS values in the same shape. **notes**

## 4. What a native integration should do

These are the rules our controller follows. Several hundred writes went through them on the unit, among them a soak of 400 that was measured press by press; none was lost.

1. **Read before every write.** Take a fresh state, compute the new value from it, write once.
2. **Read back.** Ask for the state again about 100 ms after the write and compare. The unit answered every time. For the mixer there is nothing to compare; the answer only shows that the unit is alive.
3. **Keep the mixer picture and send it again** when the unit reappears. Do not touch cells the user never set.
4. **Never write a setting without the others as read** (2.3). Put phantom power behind an explicit confirmation.
5. **Offer levels in dB.** Outputs: 0.5 dB steps, raw = 243 + 2 × dB. Microphone gain: whole dB, 0 to 65. Line gain: half dB, 0 to 9. Mixer: any dB value through the linear formula.
6. **Mute by level,** raw 59, and keep the value to return to.
7. **Expect foreign changes.** The encoder on the unit and another app can change levels at any time; the state shows it.
8. **Do not run next to TotalMix FX for iPad** without testing: both would poll and write. We did not test this.

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
| Loopback, EQ, low cut, clock source, optical format | **notes** |
| Dim, mono, global mute, solo, stereo link, cue, talkback | reading of dim and global mute **reported**; writing **unknown** |
| Snapshots, layouts | belong to TotalMix FX, not to the unit |
| Reading the mixer back | not possible, the unit does not report it |

## 6. Open points we can still close on our unit

- The effect of the line sensitivity on a signal (needs a source at input 3 or 4).
- Inputs to the Main output (with the loop cable removed, to avoid a feedback path).
- Phantom power on an input with nothing connected.
- Loopback, with the loop cable removed.
- Whether a state part with phantom power bits left at zero switches phantom power off.

## 7. Sources

- Protocol notes on the oscmix wiki, Michael Forney: github.com/michaelforney/oscmix/wiki/Babyface-Pro
- Linux kernel, `sound/usb/mixer_quirks.c`, Babyface Pro part (bit numbers of the settings register, gain ranges)
- RME, Babyface Pro FS user's guide (ranges of the gains, pad)
- Our own measurements; the dated reports are public at the project's repository.
