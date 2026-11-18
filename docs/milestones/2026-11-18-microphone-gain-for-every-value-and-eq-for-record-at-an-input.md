# Microphone gain for every value, and EQ for Record at an input

Completed 18 November 2026, 17:18 to 17:23 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run, with a cable from XLR output 1 to XLR input 1 and nothing else connected. This is not a live approval.

Until now the gain of the microphone inputs had been written and reported back for all 66 values, but measured at three of them. And whether "EQ for Record" also decides about the equaliser of an input was known from RME's manual alone. The owner plugged in one XLR cable; both are measured now.

## How

Loopy Pro was closed for the run, so the unit ran at 44.1 kHz. The headphones were muted and the right main output stayed muted. The project's diagnostic app on the iPad played a sine at half of full scale; it left the unit on XLR output 1 at −60 dB or lower, came back over the cable into microphone input 1, and was read in what the iPad records on input channel 1. Input 1 was never sent to an output: with this cable that would be a way round.

## The gain of microphone input 1

A microphone input with 65 dB of gain cannot be measured with one source level. So the gain was stepped from 0 to 45 dB with the output at raw 123 (−60.21 dB), and from 20 to 65 dB with the output at raw 83 (−80.77 dB). The input stayed more than 10 dB under full scale throughout. Over the 26 values both parts share, the same steps of gain agreed within 0.011 dB, and the upper part was shifted by the mean difference found there.

| Written | Measured | | Written | Measured |
|---|---|---|---|---|
| 1 dB | 1.00 dB | | 36 dB | 36.04 dB |
| 3 | 3.00 | | 45 | 45.04 |
| 6 | 6.00 | | 54 | 54.11 |
| 9 | 9.11 | | 55 | 55.11 |
| 12 | 12.07 | | 59 | 59.06 |
| 15 | 14.99 | | 60 | 59.97 |
| 24 | 23.95 | | 61 | 60.97 |
| 30 | 29.98 | | 65 | 64.98 |

- Every one of the 66 values lies within 0.11 dB of the gain written. The state of the unit reported every value as written.
- The steps inside a group of three, and the five steps from 60 to 65 dB, are 0.99 to 1.01 dB. The steps onto a multiple of 3 dB are between 0.91 and 1.21 dB. That fits the way the value is written to the unit, as a count of 3 dB and a rest.
- The step of the output between the two parts came out at 20.565 dB. The [level law](2026-11-18-loopback-and-the-exact-level-law.md), found digitally, gives 20.561 dB for these two raw values. So the law holds at the socket as well.

All 66 values are [published](../protocol/reference/mic-gain-measured.json).

## EQ for Record at an input

At gain 0 an equaliser was put on input 1 that makes +12 dB at the test tone. Bit 6 of the device settings was then switched back and forth, and the tone read in the recording each time, relative to the tone without equaliser:

| Bit 6 | Recorded tone |
|---|---|
| clear, as the unit was found | +12.00 dB |
| set | 0.00 dB |
| clear | +12.00 dB |
| set | 0.00 dB |
| clear | +12.00 dB |

So the setting works for an input as it does for [an output in loopback](2026-11-18-equaliser-across-a-rate-change-and-eq-for-record.md): with the bit clear the host records the input with its equaliser, with the bit set without it.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries the results; the row for the gains in its coverage table now counts as measured, which makes 14 of 18 functions. The tests of the [codec](../protocol/reference/babyface_cc.py) compare all 66 values. Ten of the 209 [test vectors](../protocol/reference/test-vectors.json) are gain messages of input 1 with the level measured for each, and one is the equaliser message of this run.

At the end the gain of input 1 was back at 0 dB, the equaliser off, bit 6 clear as found, the main output muted and the headphones at their level; Loopy Pro was opened again with the same project.

## Remaining boundaries

Not established: the gain of microphone input 2 at a signal (it is written the same way and was reported back for every value); the gain with the pad switched in; any gain with a microphone, which has another source impedance than an output of the unit; phantom power. The readings come through one cable and the unit's own converters; no external measuring instrument was used.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
