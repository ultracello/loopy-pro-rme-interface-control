# The optical format, read from the unit's own display

Completed 19 November 2026, 16:27 to 16:31 (Europe/Berlin). Evidence: project-reported, three single messages sent to the project's Babyface Pro FS on a Mac, and the owner reading the unit's display after each. This is not a live approval.

An hour earlier the unit's display [could not be read](2026-11-19-clock-source-in-the-state.md): while a computer asks the unit for its state, SET shows nothing. So the unit was plugged in anew, and this time nothing asked for its state. Only single messages were written.

## What was seen

With "Opt" selected as output, the owner pressed SET. By RME's manual the level meters then show the format of the optical output: eight lamps for ADAT, two for S/PDIF.

| Step | Lamps | Format |
|---|---|---|
| after plugging in, format bit clear as it had been left | 8 | ADAT |
| format bit (bit 10 of the device settings) written set | 2 | S/PDIF |
| written clear | 8 | ADAT |

The display followed each message at once, while the owner was looking at it.

## What it means

- **Bit 10 clear is ADAT, bit 10 set is S/PDIF.** The message switches the format, by the unit's own account.
- **It seems to be the state request that takes the keys.** With writes alone the display stayed alive; an hour earlier, with a tool asking for the state, it was dark and the DIM key did nothing. If that is so, a host that asks for the state takes over the keys of the unit and should offer what they did.
- This is the unit reporting its setting, on its display instead of in its state. What leaves the optical socket was not measured: there is no device at it. In the [coverage table](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) the entry stays "reported", and the count of measured functions at 17 of 18.

## The reference and the tool

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md), version 1.3, carries the mapping, and two [test vectors](../protocol/reference/test-vectors.json) more, 233 in all. The [helper tool](../../tools/babyface_helper.py) names the mapping where it asks a helper with a device at the optical output.

At the end the format bit was clear, ADAT, as the unit showed after it was plugged in.

## Remaining boundaries

One unit, the lamps read by eye, three messages. Not established: the format at a receiving device; whether the device settings survive a loss of power (the unit showed ADAT after it, with the bit clear before); how the unit takes its keys back other than by being plugged in again.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
