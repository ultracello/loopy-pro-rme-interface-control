# The clock source shows in the state

Completed 19 November 2026, 16:12 to 16:21 (Europe/Berlin). Evidence: project-reported, runs of the [helper tool](../../tools/babyface_helper.py) and one script with the project's Babyface Pro FS connected to a Mac in class-compliant mode. This is not a live approval.

Clock source and optical format are the one function of the unit that is not measured. The plan was that the owner reads both from the unit's own display while the tool switches them. That did not work, and something better came out of it for one of the two.

## What went wrong

With "Opt" selected, SET is meant to show the optical format on the level meters. It showed nothing. The same had happened with the DIM key an hour before: while a computer asks the unit for its state, these keys do not do what the manual describes for the unit on its own. So the display cannot serve as a witness while a host is connected. The task of the tool that relied on it was a mistake of ours and has been rebuilt.

## What was found instead

Each of the four messages was sent again, one at a time, and the whole state read after each.

| Message | Bit 30 of state word 0 | Any other word |
|---|---|---|
| optical format, bit 10 set | clear | none |
| optical format, bit 10 clear | clear | none |
| clock source, bit 0 clear | clear | none |
| clock source, bit 0 set | **set** | none |
| clock source, bit 0 clear | clear | none |

- **The state reports the clock source.** Bit 30 follows the bit written, both ways. The rebuilt task of the tool did the same again on its own: set, read, clear, read. The unit was found with the bit clear; by the notes that is AutoSync, which RME's manual names as the default of this mode.
- **The unit follows the bit a message names.** The two messages for the optical format carried the clock bit set in their second half, as all our earlier messages for "EQ for Record" had. Bit 30 stayed clear. So those earlier messages switched nothing but what they named.
- **The optical format shows nowhere in the state.** It needs a device at the optical output that says what it receives.

What the clock source does to audio was not measured: without a digital input signal the unit is its own master either way.

## The reference and the tool

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md), version 1.2, marks the clock source as reported and the optical format as before. The count of measured functions stays at 17 of 18. The tool's task `clock-optical` now switches the clock source and reads it back by itself, and asks about the optical format only when a device hangs at the optical output. [Help wanted](../help-wanted/README.md) says what such a helper needs.

At the end the clock bit was clear, as found, and the optical format bit clear, as the first attempt had left it. Whether it was clear before that attempt is not known.

## Remaining boundaries

One unit, on a Mac, powered over USB. Not established: the optical format; the clock source with a signal at the optical input; when exactly the unit hands its keys to a host and when it takes them back.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
