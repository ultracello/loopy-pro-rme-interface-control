# Equaliser and low cut measured; a message has to arrive whole; what the peak meter counts

Completed 18 November 2026, 11:52 to 12:13 (Europe/Berlin). Evidence: project-reported, offline tests and bounded native iPad/Babyface Pro FS runs of two sessions, with a cable from XLR output 1 to XLR input 1. This is not a live approval.

## A direct way to send

The equaliser message of the unit is 87 bytes long. The tool the project sends with passes at most 16 bytes in one piece, and a message that reaches the unit in pieces has no effect (shown the night before with a message that is known to work). So the project's diagnostic app on the iPad, which until now only asked the unit for its state, was given a way to send a whole message.

Every message has to pass a gate inside that app first. The gate takes only complete messages of this protocol and of a known kind, with values inside fixed limits; a request with one message that does not pass sends nothing. Phantom power never passes, and there is no way to lift that. Limits that depend on the wiring of the moment (main output above −30 dB, microphone gain above 12 dB, levels above 0 dB, inputs to the main output, loopback, device settings) can only be lifted by name, one request at a time; none was lifted in this run.

Offline, the gate was compiled from the very file that goes into the app and compared with an independent second implementation over 71,562 cases, among them every combination of the six setting bits and 60,000 random messages; none differed. A countercheck built the gate with one fault at a time, forty in all, and the tests noticed every one. The send path itself was run on the Mac against two virtual MIDI ports: nine cases, each message arrived whole, in one packet and in order, and a refused request put nothing on the wire.

The first build of the app sent nothing at all, because one name was used for two things. The run noticed it at once (the app reported that it had been asked for no message), nothing reached the unit, and the test against the virtual ports was added because of it; it fails on the faulty version.

## The gate on the device

Seven requests that the gate must refuse were sent to the app on the iPad. Each was chosen so that it would have done no harm had it passed: the main output one step above its limit, an unknown kind of message, input 1 to the main output at the lowest level there is, the headphones one step above 0 dB, phantom power of input 1 to "off" (it is off) under every lift, a message without its closing byte, and loopback without its lift. All seven were refused, each for the expected reason, and the state of the unit was the same before and after.

Then known messages were sent directly: the headphones one step of 0.5 dB down and back (read from the unit), two mixer messages in one request 5, 30 and 100 ms apart (both took effect each time), and four messages of two kinds 5 ms apart (all four took effect).

## Equaliser and low cut

The layout of the message is from the protocol notes of the oscmix project. On this unit it does what the notes say. The message went to the output channel Main left with the main output at −30 dB; the result was read behind the unit, at input 1 over the loop cable. The test signal was a music loop with most of its content below 2 kHz. Changes are from the peak values, to 0.01 dB.

| Setting on Main left | Expected | Measured |
|---|---|---|
| flat bands, overall gain 0.5 | −6.02 dB | −6.02 dB |
| flat bands, overall gain 0.25 | −12.04 dB | −12.04 dB |
| flat bands, overall gain 1.0 | 0 dB | 0.00 dB |
| low shelf −12 dB at 15 kHz in band 1 / band 2 / band 3 | about −12 dB | −12.01 / −12.01 / −12.02 dB |
| the same shelf in bands 1 and 2 | about −24 dB | −23.93 dB |
| high shelf −12 dB at 20 Hz | lower by up to 12 dB | −10.64 dB |
| peak −12 dB at 1 kHz, Q 0.3 | lower | −3.47 dB |
| low cut at 2 kHz with 1 / 2 / 3 / 4 poles | lower with every pole | −13.89 / −19.07 / −19.96 / −20.42 dB |
| low cut with 4 poles at 500 Hz / 100 Hz | less than at 2 kHz | −8.56 / −0.71 dB |
| low cut 1 pole at 2 kHz and overall gain 0.5 | −19.91 dB | −19.90 dB |
| equaliser off | 0 dB | 0.00 dB |

On an input channel (input 1, heard alone on the left headphone channel and read at the headphone meter) the overall gain 0.5 gave −6.02 dB, the low cut with 4 poles at 2 kHz −20.43 dB, and off 0.00 dB.

Three things a host has to know came out of it:

- **The slot number in the message is a shared memory.** Main left was given slot 5 with gain 0.5; then Main right was given the same slot with gain 0.25, and Main left went to −12.04 dB. Every channel with the equaliser on needs a slot of its own, 0 to 20.
- **Switching off goes by channel.** "Off" for Main left worked although the message named another slot than the one in use.
- **The unit's own meters do not show the equaliser.** The meter of the main output stayed where it was while the level behind the output fell, and the meter of input 1 did not move when the equaliser of input 1 was on.

## What the peak meter counts

The first measurement of this run read "no change" for a message that had worked. A series of readings three times a second showed why: each answer of the unit carries the peak since the previous request. The unit holds the highest value until it is asked and starts anew after every answer. After pauses of 2.0 to 5.2 seconds without a request the first answer showed the loudest spot of the 2-second test loop every time (8 of 8), while the answers 0.3 seconds later lay up to 6.5 dB lower. After a source was switched off, the first answer four seconds later still showed signal from before, the next one silence.

So a reading taken after a change has to throw the first answer away. Earlier reports of this project described a "lag of the meters of 0.65 to 2.19 seconds"; that was this effect. The values measured in the earlier runs stand, because there the controller asked the unit right after each write. A host that polls twice a second gets a meter with a window of half a second, and two hosts polling the same unit take the peaks away from each other.

## The level of a mixer cell counts down to its lowest bit

Until now only levels that are multiples of 8 had been sent. The field `0x10000` gave exactly half the peak value of `0x20000`; `0x1009C` read one meter step above `0x10098`; the fields `0x10`, `8` and `7` gave −78.4 dB, −84.4 dB and less than `8`. Below about −90 dB the meter itself stops resolving.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) now carries all of this, and its [codec](../protocol/reference/babyface_cc.py) comes with 109 test vectors. The 25 new ones are, byte for byte, messages that this run put on the wire.

At the end of the run every equaliser was off, the main output muted and the unit as at the start; the project that was loaded before stayed loaded and was never changed.

## Remaining boundaries

Not established: corner frequencies and slopes of the equaliser and the low cut (that needs sine tones; the figures above are with music); the sample rate the unit ran at (the coefficients were computed for 48 kHz); the effect of the equaliser on the headphone outputs (the message was sent, but only the unit's own meter could be read there); whether the unit keeps the equaliser when its USB connection is built anew, and whether it reports it; inputs sent to the main output and loopback (left out while the loop cable is in place); phantom power; the device settings. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
