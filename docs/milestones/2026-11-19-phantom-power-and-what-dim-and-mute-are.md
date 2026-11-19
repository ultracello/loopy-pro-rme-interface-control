# Phantom power, and what dim and mute are

Completed 19 November 2026, 15:26 to 15:30 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run in two parts, with nothing connected to the unit but USB. This is not a live approval.

Phantom power had never been sent in this project, on purpose. And for dim and the global mute it was known where the unit reports them, but not how a host switches them. The owner decided that phantom power may be tried on open inputs; both questions are answered now.

## How

Loopy Pro was closed for the run. The main output and the headphones were muted while phantom power was switched. The gate inside the project's diagnostic app, which lets only known messages through to the unit, was widened for this: phantom power and the three flag bits pass only in a request that names them.

Before anything was switched, the run checked that the two microphone inputs were open: both read −117 dBFS RMS at gain 0, the value found for open inputs the day before. Otherwise it would have stopped.

## Phantom power

The settings message switches it, bit 0 for microphone input 1 and bit 1 for input 2. There was no voltmeter; what could be read is the state of the unit and the audio of the inputs.

| Step | State reports | Peak at input 1 | Peak at input 2 |
|---|---|---|---|
| before | `0C` | −105 dBFS | −104 dBFS |
| 48 V on at input 1 | `0D` | −55 | −105 |
| 48 V off at input 1 | `0C` | −69 | −105 |
| 48 V on at input 2 | `0E` | −95 | −58 |
| 48 V off at input 2 | `0C` | −104 | −71 |

The peaks are the unit's own peak meters, which hold the highest value since the reading before. Each switch showed as a transient on its own input, 35 to 50 dB above the noise, and left the other input alone (the −95 at input 1 is the end of its own discharge from the step before). The recorded noise of the input took seconds to settle after each switch.

One more thing was tried while phantom power was on at input 1: the pad of input 2 was switched with a message whose state part said "phantom power off". Phantom power stayed on. The unit followed the one bit the message names and not the rest of the state part. That is one case and nothing to build on; a host should still send the settings back as read.

## Dim and mute are flags

The state reports dim in bit 13 and the global mute of TotalMix FX in bits 14 and 15, next to the input settings. The guess was that the settings message writes these bits too. It does: each was set and cleared, and the state reported it each time.

But nothing else happened. A tone stood on all twelve outputs, each read digitally through [loopback](2026-11-18-loopback-and-the-exact-level-law.md): not one output moved by 0.001 dB, and not one level field of the state changed. Earlier in this project, when TotalMix FX on a Mac dimmed the main output, the level fields stood 40 steps lower while bit 13 was set. So the attenuation is the host's own write of the level, and the bit only says that it is in force.

For a host that means: dim is the level written 20 dB down plus the flag, and mute is the level written to its mute value, as before. Mono, solo, cue and talkback are, by RME's manual, functions of the control room of TotalMix FX; the unit has nothing of its own for them that we know of, and a host builds them from levels and mixer cells. The coverage table lists them apart now, with the entries that do not belong to the unit.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries the results and is no longer called a draft. In its coverage table 17 of 18 functions of the unit are measured. The one left is clock source and optical format, which needs a device at the optical socket. Eight of the 229 [test vectors](../protocol/reference/test-vectors.json) are messages of this run.

At the end phantom power was off on both inputs, the settings as found, the three flags clear, the main output muted and the headphones at their level; Loopy Pro was opened again with the same project.

## Remaining boundaries

Not established: the voltage at the socket, and phantom power with a microphone connected; what the DIM key of the unit does in this mode and whether its lamp follows the flag; clock source and optical format. The unit was powered over USB alone.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
