# The equaliser across a change of the sample rate, and "EQ for Record"

Completed 18 November 2026, 15:59 to 16:09 (Europe/Berlin). Evidence: project-reported, bounded native iPad/Babyface Pro FS runs of one session, with nothing connected to the unit but USB. This is not a live approval.

Two open points of the [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) were settled through loopback, the measuring path of the [run before](2026-11-18-loopback-and-the-exact-level-law.md): a tone goes to an output, loopback of that output lets the iPad record it digitally, and the project's diagnostic app reads its level. The output was AS1, which leads to no socket in use.

## The unit keeps its coefficients when the rate changes

With no other audio app open the iPad runs the unit at 44.1 kHz; when Loopy Pro opens, the rate becomes 48 kHz. One equaliser message was sent once, a peak of +12 dB at 1 kHz with coefficients computed for 44.1 kHz, and its curve was read at 66 frequencies before and after Loopy Pro was opened.

| | Read at 44.1 kHz | Read at 48 kHz, nothing sent in between |
|---|---|---|
| Level at 1016 Hz | +11.94 dB | +10.93 dB |
| Highest point of the 66 | 1016 Hz | 1140 Hz |
| Fits the coefficients evaluated at | 44.1 kHz, within 0.001 dB | 48 kHz, within 0.001 dB |
| Against the other rate | 0.63 dB rms | 0.63 dB rms |

So the unit does not adjust anything: it goes on applying the numbers it was given, and the curve moves with the rate (the peak to about 1.09 kHz). A host has to compute the coefficients anew and send them again when the rate changes. Loopback and the mixer cell stayed as they were across the change.

Before the output level was raised with Loopy Pro open, it was checked at −40 dB that Loopy Pro does not pass that input channel on: the unit's playback meter showed the tone and nothing more.

## "EQ for Record"

The protocol notes name a device setting "eq for record" as bit 6 of a message with sub ID `00`. By RME's manual it decides whether the equaliser is part of what the host records. It was switched with the clock bit sent as "internal", and the level of a tone was read through loopback of an output whose equaliser made +12 dB there.

| State sent | Recorded tone, relative to no equaliser |
|---|---|
| as found | +12.0 dB |
| bit 6 clear | +12.0 dB |
| bit 6 set | 0.0 dB |
| bit 6 set, again | 0.0 dB |
| bit 6 clear | +12.0 dB |

The message sets the state and does not toggle it, and the sense is the reverse of the name: with the bit set the equaliser is not in the recording.

## What went wrong

The first pass read this the wrong way round. It took "bit set" for "on", saw the level fall from +12 dB to 0 dB, and its closing logic then left the bit set, taking that for the state found. For about three minutes the setting of the unit was not the one it had been found with, and the curve at 48 kHz of that pass was read without the equaliser in the recording, so it showed nothing. A second pass in the same session sent each state twice in changing order, put the setting back to the state found (bit clear) and measured both curves again; those are the ones reported.

The state part of the message is said to carry all device settings at once. No word of the unit's state message was found that reports them, so they could not be read first. Both messages carried the bit for the optical output format as zero; whether that changed the format on this unit cannot be told from here. Nothing is connected to the optical sockets. The clock source was not switched.

## The reference

The reference carries both results. Its [codec](../protocol/reference/babyface_cc.py) builds the two messages and comes with 199 test vectors; the four new ones are, byte for byte, messages that this run put on the wire. The two [curves](../protocol/reference/eq-curves-measured.json) are included.

At the end the tone was off, the equaliser off, loopback off, the mixer cell and the levels as before, and Loopy Pro was open again with the project that had been loaded, its transport stopped.

## Remaining boundaries

Not established: "EQ for Record" for the equaliser of an input (it needs a signal at an input); where the unit reports its device settings, if it does; the clock source and the optical format; the equaliser across a reconnect; phantom power. Loopback shows what the unit sends to the host, not what leaves its sockets. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
