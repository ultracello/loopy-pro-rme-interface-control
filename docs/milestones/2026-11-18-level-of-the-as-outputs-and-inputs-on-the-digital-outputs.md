# Level of the AS outputs, and inputs on the digital outputs

Completed 18 November 2026, 16:59 to 17:05 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run, with nothing connected to the unit but USB. This is not a live approval.

Two entries of the [coverage table](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) were only half established: the level of the outputs AS1 and AS2 had been written and reported back, but never read as audio except at 0 dB; and that an input can be sent to an AS or ADAT output was known from other people's notes alone. Both are measured now, through [loopback](2026-11-18-loopback-and-the-exact-level-law.md), without a cable.

## How

Loopy Pro was closed for the run, so the unit ran at 44.1 kHz. The main output stayed muted and the headphones were muted for the run; no sound left the unit. The project's diagnostic app on the iPad played a sine at half of full scale on playback 1 and read the twelve input channels.

## The level of AS1 and AS2

Playback 1 was put on the output at 0 dB and loopback of the output switched on, so the iPad recorded what the output sends. Then the level (channel 8 for AS1, 9 for AS2) was written for every raw value from 243 down to 0, and the tone read each time.

| Raw | AS1 | AS2 | The law |
|---|---|---|---|
| 243 | 0.00 dB | 0.00 dB | 0.00 dB |
| 227 | −8.00 | −8.00 | −8.00 |
| 183 | −30.00 | −30.00 | −30.00 |
| 163 | −40.02 | −40.02 | −40.02 |
| 123 | −60.21 | −60.21 | −60.21 |
| 83 | −80.77 | −80.77 | −80.77 |
| 63 to 74 | −90.31 | −90.31 | −90.31 |
| 62 and below | silent | silent | silent |

Both outputs follow the law found at the headphone output, `floor(2^15 × 10^(dB/20)) / 2^15` with `dB = (raw − 243) / 2`: each of the 181 values that give a signal lies within 0.002 dB of it, and at raw 62 and below not one sample differed from zero. The state of the unit reported the value written.

## Inputs on AS1, ADAT3 and ADAT8

With nothing connected, the only signal an input carries is its own noise. That is enough here, because loopback is digital: with loopback of an output on and no mixer cell set, its input channel read exactly zero. Then one cell at a time was set to 0 dB, and the RMS level on the loopback channel was compared with the RMS level on the input's own channel over the same eight stretches of 0.15 seconds.

| Cell | Index | The input itself | On the output |
|---|---|---|---|
| input 1 to AS1 | 104 | −116.96 dBFS | −116.96 dBFS |
| input 2 to AS1 | 105 | −116.99 | −116.99 |
| input 3 to AS1 | 106 | −113.36 | −113.36 |
| input 4 to AS1 | 107 | −119.21 | −119.21 |
| input 3 to ADAT3 | 158 | −113.40 | −113.40 |
| input 3 to ADAT8 | 288 | −113.28 | −113.28 |

No pair differed by more than 0.002 dB. With every cell off again the channel was back at exactly zero. Input 3 on AS1 at half level came out 6.20 dB below the input, where 6.02 dB would be exact; the signal is only some twenty steps of a 24-bit word there, so this is probably the rounding of the unit.

So the index of a cell, 26 × output + source, holds for the AS and ADAT outputs as it does for the main and headphone outputs.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries the results; two rows of its coverage table changed, and the share of functions measured rose from 12 to 13 of 18. The [level table](../protocol/reference/output-level-law-measured.json) now holds all 244 values for AS1 and AS2 as well, and the tests of the [codec](../protocol/reference/babyface_cc.py) compare each of them with the law. Eleven of the 208 [test vectors](../protocol/reference/test-vectors.json) are messages of this run.

At the end every cell and loopback of the run was off, the AS outputs muted as found and the headphones back at their level; Loopy Pro was opened again with the same project.

## Remaining boundaries

Not established: how to set the level of the ADAT outputs; the other cells of the AS and ADAT outputs one by one; inputs 1, 2 and 4 on the main output. Loopback shows what the unit sends to the host, not what leaves its sockets; nothing was connected to the AS or ADAT sockets. The noise of an open input is a weak signal, good for showing that a cell passes it at the same level and not for more. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
