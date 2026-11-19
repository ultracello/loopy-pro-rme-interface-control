# The DIM key and its lamp

Completed 19 November 2026, 16:04 to 16:11 (Europe/Berlin). Evidence: project-reported, one run of the [helper tool](../../tools/babyface_helper.py) with the project's Babyface Pro FS connected to a Mac in class-compliant mode; the owner pressed the key and looked at the lamp. This is not a live approval.

The [run before](2026-11-19-phantom-power-and-what-dim-and-mute-are.md) showed that dim is a flag a host can set, and that the flag attenuates nothing. Two things were left: what the DIM key of the unit does in this mode, and whether the lamp of the key follows the flag.

## What was done

This was also the first run of the tool on a real unit. On the Mac the unit offers two MIDI ports, named like the unit with "Port 1" and "Port 2"; the tool found the unit on Port 2, as on the iPad. Its task `check` read the state the project knows from the iPad and wrote one level step down and back; the unit reported both.

Then the task `dim-key`, with "Ch 1/2" selected on the unit:

| Step | Dim flag in the state | Main level fields | DIM lamp |
|---|---|---|---|
| before | clear | 59, 59 | |
| DIM pressed once | clear | 59, 59 | dark |
| DIM pressed again | clear | 59, 59 | |
| flag set by message | set | 59, 59 | **lit** |
| flag cleared by message | clear | 59, 59 | |

## What it means

- **The lamp follows the flag.** A host that sets bit 13 of the settings lights the DIM lamp of the unit.
- **The key does not dim by itself in this mode.** Neither press changed the flag or a level. The state of the unit flashes two bits when a key is pressed, as seen earlier in this project; so the key seems to be left to the host, which has to notice the press and do the dimming itself. That last step is our reading and was not tried.

One limit: the main output stood at its mute value during the run, as the owner keeps it. Whether the key behaves the same with the output open was not tried.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md), now version 1.1, carries the result in its section on the settings message.

## Remaining boundaries

One unit, one press each, the lamp seen by eye. Not established: how a host tells the DIM key from the other keys; the key with the main output not muted; the same on a Babyface Pro without FS.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
