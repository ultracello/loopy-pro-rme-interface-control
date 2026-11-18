# Loopback verified for all twelve outputs; the level law of the outputs, exact

Completed 18 November 2026, 15:02 to 15:31 (Europe/Berlin). Evidence: project-reported, offline tests and bounded native iPad/Babyface Pro FS runs of two sessions, with nothing connected to the unit but USB. This is not a live approval.

The [run before this one](2026-11-18-line-input-headphone-output-and-a-second-sample-rate.md) sent the loopback message and saw nothing: the unit's own meters do not show it. By RME's manual loopback replaces what the host records from an input with the signal of an output, so seeing it takes a host that records. This run gave the project's diagnostic app on the iPad that ability, and with it loopback became a measuring path of its own: digital, with no cable and no converter in the way.

## A reader for the audio input

The diagnostic app now listens on the audio input of the iPad, which with the unit attached is its twelve USB record channels. It returns numbers only, per channel the level at the frequency of the test tone, the highest sample and the RMS of a window; it returns no audio and keeps none. The level at the tone's frequency comes from a windowed sum against sine and cosine, so that noise and other frequencies stay out of it.

Offline the reader was run on the Mac from the very file that goes into the app, with made-up samples: 118 checks in all with those of the tone generator, among them twelve channels over 77 dB of level (each within 1 part in 100,000), a neighbouring frequency, hum and an offset kept out, a window that did not fill, more channels than the reader takes, and the sweep fed by a thread that lags like the real input. A countercheck built the file with one fault at a time, forty-five in all. The first pass noticed 44; the test that should have caught a missing wait before reading was sharpened afterwards (see below), and then the tests noticed all 45.

iPadOS asked once whether the app may use the microphone; the owner had agreed to that beforehand, and the app's own automation confirmed the dialog.

## Loopback

Loopy Pro was ended for every measurement, because it passes an input on to its outputs, and opened again afterwards. With no other audio app open the iPad ran the unit at 44.1 kHz.

A tone at half of full scale went out on playback 1. For each of the twelve outputs in turn it was sent to that output, loopback of the output was switched on and off, and all twelve input channels were read each time.

| Output | Level setting | Input channel that carried the tone | Its level relative to the tone |
|---|---|---|---|
| Main left, right | −30 dB | 1, 2 | −30.00 dB |
| Headphones left, right | −14.5 dB | 3, 4 | −14.50 dB |
| AS1, AS2 | 0 dB | 5, 6 | 0.00 dB |
| ADAT3 to ADAT8 | as found | 7 to 12 | 0.00 dB |

In every case no other input channel changed, and with loopback off the channel carried its hardware input again: noise around −105 dBFS peak on the four analogue inputs, exact silence on the digital ones. That also measures the mixer cell from playback 1 to each of the twelve outputs, eight of which had only been known from other people's notes.

On Main left three more things were tried with loopback on. Ten dB less output level gave 10.02 dB less; the mute value gave exact silence; an overall gain of 0.5 on the output's equaliser gave 6.02 dB less. So the signal is taken behind the output level and behind the output equaliser.

## The level law, value by value

Through loopback of the headphone output left, every raw level value from 243 (0 dB) down to 0 was set and read, 244 values. The gain is

`floor(2^15 × 10^(dB/20)) / 2^15`, with `dB = (raw − 243) / 2`.

Every value lies within 0.003 dB of this. The steps are half a dB only near the top; lower down the coefficient has few bits left:

| Raw | Nominal | Measured |
|---|---|---|
| 183 | −30 dB | −30.00 dB |
| 163 | −40 dB | −40.02 dB |
| 143 | −50 dB | −50.05 dB |
| 123 | −60 dB | −60.21 dB |
| 116 | −63.5 dB | −63.87 dB |
| 83 | −80 dB | −80.77 dB |
| 63 to 74 | −90 to −84.5 dB | −90.31 dB, all twelve alike |
| 62 and below | | silence, not one sample other than zero |

The value 59, which TotalMix FX writes to mute an output, is therefore plain silence. The small shortfall at low levels that the run over a cable had found (−60.12 and −63.76 dB there, through the converters) is this law.

## Equaliser on four more outputs

Main right, headphones right, AS1 and ADAT3 each got two equaliser settings, a peak of +12 dB at 100 Hz and a combination of low cut, low shelf, peak and high shelf, with coefficients for 44.1 kHz. Each was read through loopback at 66 frequencies from 10 Hz to 18.2 kHz, next to curves without equaliser. The four outputs gave the same curves. Of 528 points, the 480 from 20 Hz up lie within 0.012 dB of the calculation (0.002 dB rms); the peak setting alone within 0.004 dB. Below 20 Hz the low-cut curve differs by up to 0.044 dB. With this the equaliser is measured on an input, on both main and both headphone channels, on an AS output and on an ADAT output.

## What went wrong on the way

- **The permission dialog stayed on the screen.** The first script wanted exactly one button named "Erlauben"; the dialog reports each button twice. The script stopped and opened Loopy Pro again, but could not confirm its page behind the dialog. A second step confirmed the dialog within half a minute and found Loopy Pro and the unit as they should be.
- **A check that was too narrow.** The app reported "listening" as the number 1, the script wanted the word true. Nothing was wrong at the unit; the step was repeated.
- **The first equaliser curves were wrong at about every seventh point,** by 0.2 to 2.5 dB. The audio the app reads is older than the moment it asks, by one block of the input plus the way out and back, about 155 ms; the wait after each change of frequency was 100 ms. So some windows began with the previous frequency. The references showed it at once (a digital path must be flat, and was, except at those points). The curves were measured again in a second session with a wait of 300 ms; those are the ones reported here. The level law and the loopback table were read without a change of frequency and were not affected. The offline test that should have caught a wait that is too short could not, because its made-up input did not lag; it does now.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries all of this: loopback as measured, the level law, the cells of all outputs. Its [codec](../protocol/reference/babyface_cc.py) builds the loopback message and computes the gain of a raw level, and comes with 195 test vectors; the 50 new ones are, byte for byte, messages that these runs put on the wire. The [level of every raw value](../protocol/reference/output-level-law-measured.json) and the eight new [curves](../protocol/reference/eq-curves-measured.json) are included, and the tests of the codec compare every point.

At the end of each run loopback was off everywhere, every equaliser off, the mixer cells and levels as before and the main output muted; Loopy Pro was open again with the project that had been loaded, its transport stopped.

## Remaining boundaries

Not established: whether the unit reports loopback in its state and keeps it when its USB connection is built anew; inputs sent to the AS and ADAT outputs; how the level of an ADAT output is set (they stood at 0 dB); loopback next to a host app that passes inputs on (left out on purpose: it closes a way round); the equaliser at rates other than 44.1 and 48 kHz and across a change of rate; the device settings; phantom power. Loopback shows what the unit sends to the host, not what leaves its sockets. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
