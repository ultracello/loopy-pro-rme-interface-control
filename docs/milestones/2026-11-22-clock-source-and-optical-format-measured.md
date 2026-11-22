# Clock source and optical format, measured

Completed 22 November 2026, 22:42 to 22:47 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run in two parts, with one optical cable. This is not a live approval.

Clock source and optical format were the last function of the unit that was only reported and not measured: the unit said in its state and on its display what it was set to, but nothing showed what that does on an optical link. No second device was at hand. One cable was enough.

## How

The owner plugged an optical cable from the unit's optical output into its own optical input. Loopy Pro was closed for the run; the main output and the headphones were muted. The project's diagnostic app played a sine at half of full scale on playback 1, which was sent to three outputs at 0 dB: AS1, the first channel of the optical output, and ADAT3 and ADAT8. Loopback was off, so the input channels 5, 7 and 12 carried what arrived at the optical input. The first reading showed the tone on all three: that is how the run knew where the cable led.

A first pass read the format with the clock as the unit was found, and its levels wandered. The reason turned out to be the clock, see below. The second pass is the one reported here: several readings in each position.

## Optical format

With the unit on its own clock:

| Format bit | Channel 5 (AS1) | Channel 7 (ADAT3) | Channel 12 (ADAT8) | Readings |
|---|---|---|---|---|
| clear | 0.00 dB | 0.00 dB | 0.00 dB | 8 of 8 |
| set | 0.00 dB | silent | silent | 4 of 4 |

- **Bit clear is ADAT:** all eight channels of the optical output arrive.
- **Bit set is S/PDIF:** only the first pair arrives; on the other channels not one sample differed from zero.
- The optical input took either format without being told.

This agrees with what the unit's own display [had shown](2026-11-19-optical-format-on-the-units-display.md) three days before.

## Clock source

With the format on ADAT:

| Clock bit | State bit 30 | The tone on channels 5, 7, 12 | Other optical channels | Readings |
|---|---|---|---|---|
| set | set | 0.00 dB on each | silent | 12 of 12 |
| clear | clear | about −13, −4 and −21 dB | noise around −60 dBFS | 12 of 12 |

With the bit set the unit keeps its own clock, and the link is clean to the last digit. With the bit clear the unit follows the digital input, as RME's manual says for AutoSync; here that input was the unit's own output, a loop with nothing to follow, and the audio on the link came back damaged. Switched back and forth twice, the same both times.

That is also why a unit should not be left like this: the owner was asked to pull the cable after the run, because his unit stands on AutoSync, as it was found.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md), version 1.6, marks the last entry of its coverage table as measured. **All 18 functions of the unit are measured now.** The four [test vectors](../protocol/reference/test-vectors.json) for these two settings carry what was measured.

At the end the clock bit and the format bit stood as found, the mixer cells of the run were off, the AS outputs muted and the headphones at their level; Loopy Pro was opened again with the same project.

## Remaining boundaries

The receiver was the unit's own optical input, not a second device. Not established: how a second device sees the two formats; the clock source with a foreign signal of another sample rate at the input. One unit, powered over USB.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
