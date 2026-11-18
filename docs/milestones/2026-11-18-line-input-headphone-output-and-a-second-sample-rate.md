# Line input, headphone output and a second sample rate, measured over one cable

Completed 18 November 2026, 14:26 to 14:41 (Europe/Berlin). Evidence: project-reported, bounded native iPad/Babyface Pro FS runs of one session, with a cable from the 6.3 mm headphone socket to line input 3. This is not a live approval.

One instrument cable from the headphone output to line input 3 made it possible to measure, with the sine tone of the project's diagnostic app, several things that had only been "reported back by the unit" or taken from other people's notes. The cable between the XLR sockets was not in place this time.

## What went wrong first

The first pass gave readings that did not add up, and for about seven seconds the headphone output rang at full scale into the cable. The cause was outside the unit: Loopy Pro, open in the background, passes line input 3 on to its outputs. With the cable that closes a way round, headphone output, input 3, Loopy Pro, playback, headphone output. Below a headphone level of 0 dB this coloured every reading; at 0 dB and above the loop gain reached one. It showed in the data: the playback meter of the right channel, which should have been silent, read the very word of input 3. The owner had been asked to unplug his headphones before the run, the right headphone channel and the main output were muted, and the levels involved are within what the sockets are built for.

The planning had ruled out a way round inside the unit and over the cable, but not one through an app on the host. For everything that follows Loopy Pro was ended for the time of the measurement (transport stopped, project saved) and opened again afterwards. With no other audio app open, the playback meter read exactly half of full scale for a tone of half of full scale, and the silent channel read zero.

The first step of the plan, input 1 on the main output, could not be measured: it needed the cable between the XLR sockets, which had been removed. The run noticed that no tone arrived at input 1 and stopped before sending anything of that step.

## Line input 3

- **Reference level.** Clearing the setting bit of input 3 raised the level at the input meter by 8.74 dB; setting it again brought it back. Set is therefore the less sensitive setting, "+4 dBu" in the naming of the Linux driver, and clear is "−10 dBV". RME's manual gives the maximum input levels of the two settings as +13 dBu and +4 dBu, 9 dB apart.
- **Gain.** All 19 steps, 0 to 9 dB: each step added 0.50 dB, the last one stood 9.00 dB above the first.
- **On the main output.** Input 3 was sent to Main left and to Main right, with the main output at −30 dB and playback taken off it. The main meter read 30.00 dB below the meter of input 3 at unity and 36.02 dB below at −6.02 dB, and nothing when the cell was off. The cell index follows the same law as all the others.

## Headphone output

- **Level behind the output.** From 0 dB, the raw values for +0.5, +1, +3 and +6 dB gave +0.50, +1.00, +3.00 and +6.00 dB, and those for −10, −20 and −30 dB gave −10.00, −20.00 and −29.98 dB. The lowest steps come out a little lower than the law of half a dB per step: −60 dB gave −60.12 dB and −63.5 dB gave −63.76 dB. The mute value was silent, below the noise of the input.
- **Equaliser.** Three settings on the headphone output left were measured as whole curves at input 3, 66 frequencies from 10 Hz to 18.2 kHz: low cut 100 Hz with two poles and the corner solved (−3 dB at 100.1 Hz), peak +6 dB at 1 kHz (+5.99 dB), high shelf −9 dB at 4 kHz (−9.00 dB at 18.2 kHz). All 198 points were compared with the calculation; from 20 Hz up and above −20 dB every one lies within 0.01 dB.

## A second sample rate

With Loopy Pro ended the iPad reported 44,100 Hz for the connection instead of 48,000 Hz. The coefficients of the three headphone settings were computed for 44.1 kHz, and the measured curves fit that calculation (0.004 to 0.009 dB rms per curve) and not the one for 48 kHz (0.22 to 0.65 dB). So the unit runs at the rate the host sets, the rate can change when an app opens or closes, and a host has to compute the equaliser coefficients for the current rate and send them again when it changes. After Loopy Pro was opened again the iPad reported 48,000 Hz.

## AS1 and loopback

Playback 1 was sent to the output AS1 at 0 dB: a peak word that had been unassigned so far (word 30) then read the level of playback 1, so it is the meter of AS1. Loopback was switched on and off for that output: no peak meter changed. By RME's manual loopback replaces what the host records from the input of that channel; seeing it needs a host that records, which the diagnostic app does not do. Loopback therefore stays unverified.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries all of this. Its [codec](../protocol/reference/babyface_cc.py) now comes with 148 test vectors; the new ones are, byte for byte, messages that this run put on the wire, and the [measured curves](../protocol/reference/eq-curves-measured.json) include the three at 44.1 kHz.

At the end of the run the unit was as at the start (main output muted, headphone level, line gain and settings as before, every equaliser off), and Loopy Pro was open again with the project that had been loaded, its transport stopped.

## Remaining boundaries

Not established: input 1, 2 and 4 on the main output (input 3 was measured); the reference level and gain of input 4 with a signal; the equaliser of the headphone output right, and of any output at a rate other than 44.1 or 48 kHz; what the unit does with equaliser coefficients it holds when the rate changes, and whether it keeps them across a reconnect; loopback; the device settings; phantom power. The readings come from the unit's own peak meters, through its converters and one cable; no external measuring instrument was used. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
