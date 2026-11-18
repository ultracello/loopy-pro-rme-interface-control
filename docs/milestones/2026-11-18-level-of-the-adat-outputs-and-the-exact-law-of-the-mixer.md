# Level of the ADAT outputs, and the exact law of the mixer

Completed 18 November 2026, 17:26 to 17:46 (Europe/Berlin). Evidence: project-reported, two bounded native iPad/Babyface Pro FS runs, read digitally through [loopback](2026-11-18-loopback-and-the-exact-level-law.md); nothing had to be connected for them. This is not a live approval.

How to set the level of the six ADAT outputs was the one output level still unknown. The gain message that sets the main, headphone and AS outputs uses channels 4 to 9, so channels 10 to 15 were the obvious guess. The guess was wrong, and a second one, taken from the Linux driver, was right.

## How

Loopy Pro was closed for both runs, so the unit ran at 44.1 kHz. The main output stayed muted and the headphones were muted; no sound left the unit. The project's diagnostic app played a sine at half of full scale on playback 1, which was put on all six ADAT outputs at 0 dB, with loopback of all six on. So each reading showed all six outputs at once.

The gate inside the diagnostic app, which lets only known messages through to the unit, was widened twice for this, each time for exactly the messages tried here and only when a request names them.

## First run: gain channels 10 to 15 do nothing

Each of the channels 10 to 15 was written with raw 183, 163 and 62, values that take the other outputs to −30 dB, −40 dB and silence. In all 24 readings all six ADAT outputs stayed at 0.00 dB, and no word of the unit's state followed the values.

## Second run: the level is a mixer entry

The Linux driver for the unit's other USB mode sets every output level as a mixer entry at index 992 plus the number of the output. Tried here with the mixer message of this mode, entries 998 to 1003:

| Entry | Level written | ADAT3 | ADAT4 | ADAT5 | ADAT6 | ADAT7 | ADAT8 |
|---|---|---|---|---|---|---|---|
| 998 | half (`0x10000`) | −6.021 dB | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 998 | `0x3333` | −20.002 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 998 | 0 | silent | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1001 | half | 0.00 | 0.00 | 0.00 | −6.021 | 0.00 | 0.00 |
| 1003 | half | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −6.021 |

Every one of the six entries moved exactly its own output, by the same amounts, and came back to 0.00 dB with `0x20000`. With the entry and the cell of playback 1 both at half level the output stood at −12.041 dB: the two multiply. No word of the state follows the entries, so a host has to keep the value itself.

## The exact law of a mixer level

Read digitally, the level of a cell and of such an entry turns out to be a coefficient of 15 bits, like the [output level](2026-11-18-loopback-and-the-exact-level-law.md): the gain is `floor(level / 4) / 2^15`. The two lowest bits of the 20-bit field do not count.

| Level field | By the plain ratio | Measured |
|---|---|---|
| `0x1009C` | −6.00 dB | −6.00 dB |
| `0x3333` | −20.00 | −20.002 |
| `0x51F` | −40.00 | −40.018 |
| `0x83` | −60.00 | −60.206 |
| `0xD` | −80.07 | −80.767 |
| 4 | −90.31 | −90.311 |
| 3 and below | | silent |

Eighteen levels were read on the cell of playback 1 to ADAT3 and eighteen on entry 998; every one that gives a signal lies within 0.002 dB of the law. Earlier reports of this project said that every bit of the level counts; that came from readings at the unit's meter, which fit this law as well, and was said too broadly.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries the results; the level of the ADAT outputs now counts as measured in its coverage table, which makes 15 of 18 functions. The [codec](../protocol/reference/babyface_cc.py) builds the message and computes the gain of a level; its tests compare both rows of [measured values](../protocol/reference/output-level-law-measured.json). Twelve of the 221 [test vectors](../protocol/reference/test-vectors.json) are messages of these two runs.

At the end the six entries stood at 0 dB, as the outputs were found, the cells and loopbacks of the runs were off, and the headphones were back at their level; Loopy Pro was opened again with the same project.

## Remaining boundaries

Not established: levels above 0 dB on these entries; the entries 992 to 997, which by the same reasoning belong to the main, headphone and AS outputs; whether the unit keeps the entries when it loses power; gain channels above 15. Loopback shows what the unit sends to the host, not what leaves its optical socket; nothing was connected there.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
