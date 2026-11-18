# Single prepared messages: playback to the main output, levels above unity, two more output channels

Completed 18 November 2026, 01:13 to 01:20 (Europe/Berlin). Evidence: project-reported, offline tests and one bounded native iPad/Babyface Pro FS run of one session, with a cable from XLR output 1 to XLR input 1. This is not a live approval.

## A faster way to settle open points

Until now each function of the interface was first built as a finished control on the page and then accepted. To settle the remaining open points of the protocol more quickly, a test rig was built instead: a copy of the project whose rule sends single prepared messages, and whose filter passes exactly these messages, byte for byte, in addition to what it passed before. A message is chosen with the level dial of a monitoring way that is not on and fired with that way's phase button, so no element of any page had to change. Every message that changes something has a counterpart that restores it.

Offline, 6 new tests passed and the 190 tests of the earlier revisions still pass on the rig. The rig is not for playing; the project of the revision before was loaded again at the end of the run.

## Measured on the unit

Sixteen messages were fired, each confirmed by the unit, each followed by a measurement after three seconds of rest. The main output stood at −30 dB for the run and was muted again afterwards; no message of the rig writes the level of the main output.

| Message | Main left | Main right | Headphones left | Headphones right |
|---|---|---|---|---|
| Baseline (playback at −6.0 dBFS) | −36.0 dBFS | −36.0 dBFS | −20.5 dBFS | −20.5 dBFS |
| Playback 1 to Main left at −6 dB | −42.0 | −36.0 | −20.5 | −20.5 |
| Playback 1 to Main left off | no signal | −36.0 | −20.5 | −20.5 |
| Playback 1 to Main left back at 0 dB | −36.0 | −36.0 | −20.5 | −20.5 |
| Playback 2 to Main right at −6 dB | −36.0 | −42.0 | −20.5 | −20.5 |
| Playback 2 to Main right back at 0 dB | −36.0 | −36.0 | −20.5 | −20.5 |
| Playback 1 to Headphones left at +3 dB | −36.0 | −36.0 | −17.5 | −20.5 |
| Playback 1 to Headphones left at +6 dB | −36.0 | −36.0 | −14.5 | −20.5 |
| Playback 1 to Headphones left back at 0 dB | −36.0 | −36.0 | −20.5 | −20.5 |

So the mixer cells of the main output follow the same law as those of the headphones (cell index = 26 × output + source), a cell at level 0 is off, and levels above unity are taken up to +6 dB. Every value came out exact to the tenth of a dB, and the side that was not addressed never moved.

Two things were only read back from the state of the unit, with no signal present:

- The level of the left headphone output was written as raw 249 and raw 255 (+3 dB and +6 dB by the known law) and reported back as written, then returned to its value. The playback had been taken off the headphones first.
- Output channels 8 and 9 were written to −30 dB and back. The unit reported them in the two fields of its state that the protocol notes call AS1 and AS2. Main and headphones stayed untouched.

At the end the unit stood as at the start.

## Remaining boundaries

Not established: inputs sent to the main output (left out while the loop cable is in place, because it would close a feedback path); the audible effect of an output level above 0 dB; the cells and levels of the ADAT outputs; phantom power, loopback and equaliser, which are known from other people's notes only. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
