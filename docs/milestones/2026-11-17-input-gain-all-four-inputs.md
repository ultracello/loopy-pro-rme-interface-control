# Input gain of all four analog inputs

Completed 17 November 2026, 00:46 to 01:28 (Europe/Berlin). Evidence: project-reported, two bounded native iPad/Babyface Pro FS runs and offline tests. This is not a live approval.

## Reading first

The operator asked for the gain of all four analog inputs on the operating page. Phantom power stays out of reach.

Nothing was written until the unit had shown how it reports these gains. In a read-only run the operator turned the gain of input 1 and of input 4 on the unit itself from the lower end upwards and back, while the state of the interface was queried about three times a second for 15 minutes.

| Finding | Result |
|---|---|
| Input 1 (microphone) | state word 2, bits 0 to 6; one count per dB; 0 to 59 seen without a gap |
| Input 4 (line/instrument) | state word 3, bits 24 to 28; one count per half dB; stop at 18 (9 dB) |
| Inputs 2 and 3 | not turned; unchanged at 0 and 12 where the notes of the oscmix project place them |
| A turn of the knob | shows in the state at once |

The field positions agree with the protocol notes of the [oscmix project](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro). The operator stopped at 59 dB on input 1; the manual gives 65 dB as the upper end, which was not measured.

## Writing

For the write the sources were the same notes and the Babyface Pro code of the Linux kernel: the gain message that the outputs already use, with channels 0 to 3; a line input takes the count of half dB; a microphone input takes a packed value, the dB divided by three in the low five bits and the remainder above them.

A seventh revision of the candidate rule, SHA-256 `9b315a4adcf01613d34522c7327aa782e42a78645f0650387bea6045d096c40d`, adds the inputs next to everything the sixth does:

- every state of the interface shows the four gains on the page, 0 to 65 dB for the microphone inputs and 0 to 9 dB in half dB for the line inputs;
- per input a control down and a control up with a free count of steps, 1 dB at a microphone input and half a dB at a line input;
- a press is taken only while the page is read and armed. It reads the state first, so a knob turned at the unit in the meantime cannot make the gain jump; then it writes, held at the ends of the range; then it reads again and compares. The reason row reports the outcome;
- no input step locks the page or touches the outputs and their mute references.

The filter before the interface, SHA-256 `f65d0d679958fb892556049b8de1af4bf474b675bf2b95a1b31f57df67f11aad`, additionally passes exactly these messages: channels 0 and 1 with one of the 66 packed values, channels 2 and 3 with 0 to 18. The message for phantom power and pad does not pass.

Offline, 32 new tests passed and the 66 tests of the earlier revisions still pass. Thirty-one deliberate falsifications were noticed.

## On the interface

The project got a page of its own for the inputs, with copies of READ, ARM, LOCK, the status row and the reason row. The acceptance was ordered so that a wrong reading of the sources would have stayed harmless: a line input first, then +3 dB at a microphone input standing at 0, which is raw 1 in the packed form and would have been 1 dB if the unit took plain dB.

After each press the unit was read directly.

| Press | Inputs 1 to 4 as the unit reports them | Reason row |
|---|---|---|
| Start | 0, 0, 12, 0 | |
| Input 4 up 0.5 dB | 0, 0, 12, 1 | ok |
| Input 4 down 0.5 dB | 0, 0, 12, 0 | ok |
| Input 1 up 3 dB | 3, 0, 12, 0 | ok |
| Input 1 down 3 dB | 0, 0, 12, 0 | ok |
| Input 1 up 1 dB | 1, 0, 12, 0 | ok |
| Input 1 up by the width of the page (0.5 dB, a whole dB here) | 2, 0, 12, 0 | ok |
| Input 1 down 3 dB, held at the end | 0, 0, 12, 0 | ok |
| Input 2 up 1 dB, down 1 dB | 0, 1, 12, 0 then 0, 0, 12, 0 | ok |
| Input 3 up 0.5 dB, down 0.5 dB | 0, 0, 13, 0 then 0, 0, 12, 0 | ok |
| Input 4 down at the lower end | 0, 0, 12, 0 | refused |

All twelve checks passed. The displays on the page showed the same values. The output gains did not change at any point, and every input ended where it started.

This establishes on this unit the write of the input gains: the channel numbers, the count of half dB for the line inputs, and the packed form for the microphone inputs up to 3 dB.

## Remaining boundaries

Not established: microphone gains above 3 dB, the upper end and the special case of the packing from 60 dB; the outcomes "level differs", "no answer" and "read first" of an input step on the interface; the pad and instrument switches; an evening of playing; operation alongside TotalMix; crash-safe recovery. Phantom power is deliberately not reachable.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
