# The phase of each way to the headphones

Completed 18 November 2026, 00:16 to 00:27 (Europe/Berlin). Evidence: project-reported, offline tests and two bounded native iPad/Babyface Pro FS runs of one session each, with a cable from XLR output 1 to XLR input 1. This is not a live approval.

## What was added

Each of the five ways to the headphones, the four inputs and the playback, can now be inverted in phase from the page: one button per way, and one display that names the inverted ways.

The protocol notes the project uses say of the level field of the mixer message: "level (reference 20000000), negative if phase inverted". The sixteenth revision of the candidate rule, SHA-256 `1c1b2ab8af47c08d268e99f6e8f5f3abef971449cf7daa0c461ef8a56c50e40f`, reads "negative" as the two's complement of the 32-bit word: an inverted level L stands in the 20-bit field as 2^20 − L. No new kind of message is sent. While a way is on, a press sends both of its sides again with the new sign and then asks the unit for its state; while it is off or unknown, only the kept sign changes. Level, pan, on and off, and the re-send on arming carry the sign with them.

The filter before the interface, SHA-256 `d86ef258fc00da6d9fb672eaa0819762e86e2ba0563a355c11fa9ebc0084cff2`, passes the inverted levels for the same ten mixer positions as before, and only up to unity.

Offline, 17 new tests passed, the 177 tests of the earlier revisions still pass, and all 26 deliberate falsifications of rule and filter were noticed. Without a phase press the revision sends the bytes of the revision before.

## Room for more displays

The page had run out of feedback numbers: the routing app that carries the displays passed a fixed range, and every number in it was in use. Its scene was replaced by one whose page filter passes a wider range, with nothing else changed. After the change the page read at the first try, armed, and a step on the headphones arrived and went back, with the project of the revision before. The scene before stays available.

## Measured on the unit

With the cable in place, the playback reaches input 1 through the main output, so the same signal can be put on the headphones twice: monitored from input 1, and directly as playback. The playback was lowered until both ways were equally strong at the headphone output.

| Measurement at the headphone output | left | right |
|---|---|---|
| Input 1 alone at −12 dB, normal | −53.1 dBFS | −53.1 dBFS |
| Input 1 alone, inverted | −53.1 dBFS | −53.1 dBFS |
| Input 1 inverted, four positions right | −59.1 dBFS | −53.1 dBFS |
| Input 1 and the playback, both normal | −35.8 dBFS | −35.8 dBFS |
| Input inverted, playback normal | −44.6 dBFS | −44.6 dBFS |
| Input normal, playback inverted | −44.6 dBFS | −44.6 dBFS |
| Both inverted | −35.8 dBFS | −35.8 dBFS |
| Both normal, repeated | −35.8 dBFS | −35.8 dBFS |
| Input inverted, repeated | −44.6 dBFS | −44.6 dBFS |
| After locking and arming again, input inverted | −44.6 dBFS | −44.6 dBFS |

So the unit takes the negative level as an inverted one. A way alone keeps its level exactly, and the pan law holds inverted. The sum of the two ways depends only on whether their signs are equal: 8.8 dB lie between the two cases, and every combination gave the same value twice. That the sum does not vanish for unequal signs follows from the travel time of the way through converters and cable.

Also seen: after loading the display names no way; a press on a way that is not on changes the display and no level; the button that restores the way of the playback sets its phase back to normal. At the end the unit stood as at the start, the main output muted again.

## Remaining boundaries

Not established: the phase of inputs 2 to 4 on the unit (tested offline for all five ways; measured on the unit for input 1 and the playback); how it sounds with a microphone or an instrument; a setup that recovers from a replug without any touch. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
