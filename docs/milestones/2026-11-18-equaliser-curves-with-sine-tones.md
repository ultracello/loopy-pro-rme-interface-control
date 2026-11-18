# Equaliser and low cut: whole frequency responses, measured with sine tones

Completed 18 November 2026, 13:35 to 13:56 (Europe/Berlin). Evidence: project-reported, offline tests and bounded native iPad/Babyface Pro FS runs of one session, with a cable from XLR output 1 to XLR input 1. This is not a live approval.

The [run before this one](2026-11-18-equaliser-and-low-cut-measured.md) measured the equaliser with music: levels to 0.01 dB, but no corner frequencies, and the sample rate of the unit was assumed. This run closes both.

## A tone of its own

The project's diagnostic app on the iPad was given a sine generator. Its limits are fixed in the app and cannot be lifted by a request: at most half of full scale, 10 Hz to 22 kHz, at most 60 seconds per start; after that the tone fades out by itself. The tone goes out on the iPad's audio output, which is USB playback 1 and 2 of the unit; the levels are read at the unit's own peak meters, as before.

Offline, the generator was run on the Mac without any sound, from the very file that goes into the app: 81 checks, among them amplitude and frequency of the samples (a pure sine to 2 parts in 10 million), the same samples whatever the block size, no jump at a change of frequency, the fade to exact silence, the generator inside an audio engine that renders to memory, the sweep against two virtual MIDI ports, and 7,948 cases of the limits against a second statement of them. A countercheck built the generator with one fault at a time, thirty in all, and the tests noticed every one.

On the device iPadOS refused to start the tone while another app was in front, so the diagnostic app was brought to the front for the time of the measurement and Loopy Pro back afterwards. A sine sent at 0.5, 0.25 and 0.125 of full scale read 0.50000, 0.25000 and 0.12501 at the unit's playback meter, on the left channel only; with the main output at −30 dB its meter read 30.00 dB below that. The iPad reported 48,000 Hz and twelve output channels for the connection.

## How a curve was measured

The sine, at half of full scale, went through the output channel Main left with the main output at −30 dB. Main right and the headphones were muted. The level was read behind the unit, at input 1 over the loop cable, at 67 frequencies from 10 Hz to 20 kHz. For each frequency the app set the tone, waited, asked the unit (which empties its peak meters), waited 0.15 seconds (0.35 below 40 Hz) and asked again; the second answer carries the peak of that time. Eleven of the frequencies were moved off their round values, by 0.14 % at most, where the samples of that time could otherwise miss the top of the wave (at exactly 20 kHz and 48 kHz they can miss 3.4 % of it).

A curve is the level with a setting minus the mean of the curves without equaliser before and after it. The calculated curve comes from the words of the very message that was sent: three biquads, the overall gain, and the low cut as the filter (k − k·z⁻¹)/(1 − k·z⁻¹) once per pole.

## Results

| Setting on Main left | Measured | Calculated |
|---|---|---|
| low cut 100 Hz with 1 / 2 / 3 / 4 poles, k as in the protocol notes | −3 dB at 100.7 / 103.0 / 105.2 / 107.1 Hz; at 20 Hz −14.17 / −21.38 / −27.02 / −31.71 dB | 100.7 / 103.0 / 105.2 / 107.1 Hz; −14.15 / −21.39 / −27.05 / −31.77 dB |
| low cut 20 Hz, 2 poles | −3 dB at 20.5 Hz | 20.4 Hz |
| low cut 500 Hz, 4 poles | −3 dB at 572.8 Hz; −0.52 dB at 20 kHz | 572.8 Hz; −0.52 dB |
| low cut with k solved for the corner: 100 Hz 4 poles / 100 Hz 2 poles / 250 Hz 1 pole / 500 Hz 4 poles | −3 dB at 100.1 / 100.1 / 250.2 / 500.6 Hz | 100.1 / 100.1 / 250.2 / 500.6 Hz |
| peak +6 dB at 1 kHz, Q 1 | +5.99 dB at 1016 Hz, +0.27 dB at 202 Hz, +0.39 dB at 4064 Hz | +5.99, +0.27, +0.39 dB |
| peak −12 dB at 1 kHz, Q 5 | −11.61 dB at 1016 Hz | −11.61 dB |
| peak +12 dB at 100 Hz, Q 0.7 | +12.00 dB at 101 Hz, +5.81 dB at 50 Hz, +5.68 dB at 202 Hz | +12.00, +5.82, +5.68 dB |
| low shelf +6 dB at 200 Hz | +6.00 dB at 20 Hz, +2.96 dB at 202 Hz | +6.00, +2.96 dB |
| high shelf −9 dB at 4 kHz | −4.63 dB at 4064 Hz, −9.00 dB at 20 kHz | −4.64, −9.00 dB |
| peak +6 dB at 12 kHz, Q 2 | +5.58 dB at 11.5 kHz, +0.13 dB at 20 kHz | +5.58, +0.13 dB |
| low pass 2 kHz, Q 0.707 (a filter TotalMix FX does not offer in a band) | −0.28 dB at 1016 Hz, −12.86 dB at 4064 Hz, −34.00 dB at 11.5 kHz | −0.28, −12.86, −34.07 dB |
| low cut, low shelf, peak and high shelf together | −13.93 dB at 20 Hz, +1.14 dB at 101 Hz, −3.17 dB at 1016 Hz, +2.81 dB at 11.5 kHz | −13.93, +1.14, −3.17, +2.81 dB |

Twenty-one curves were measured, 1407 points. 1355 of them lay at least 30 dB above the noise and were compared with the calculation. From 20 Hz up and where the curve lies above −20 dB, 1219 points, every point is within 0.02 dB of the calculation except one at 50.4 Hz with 0.05 dB (next to the mains frequency). Deeper in the stop band and below 20 Hz the difference grows to 0.17 dB at most. Between the reference curves of the output the level moved by less than 0.003 dB above 20 Hz.

Three of the settings were also sent to input 1, heard alone on the left headphone channel and read at the headphone meter: low cut 100 Hz with 2 poles, the peak at 1 kHz and the high shelf at 4 kHz gave the same curves as on the output.

## What follows for a host

- **The unit does what the coefficients say.** A host can draw its curve from the numbers it sends.
- **The unit ran at 48 kHz.** The measured curves fit the calculation for 48 kHz, 0.001 to 0.03 dB rms per curve, and not the one for 44.1 kHz, 0.15 to 1.06 dB. Coefficients have to be computed for the rate the unit runs at.
- **The low cut of the protocol notes sits a little high and takes some level.** With their formula the −3 dB point is 0.7 % above the nominal frequency with one pole at 100 Hz, 7 % with four poles at 100 Hz and 15 % with four poles at 500 Hz, and the pass band stays 0.06 to 0.52 dB below 0 dB. With k solved from the filter itself the corner came out at the frequency asked for. Whether TotalMix FX sends the k of the notes is not known here.
- **A band takes any biquad,** not only the peak and shelf types.

## Two things that went wrong on the way

The first trial stopped itself, because its check expected a channel without signal to read below 1000 at the playback meter; such a channel read about 1200 here (−101 dBFS). It put everything back and was repeated with the check corrected.

At the end of the long measurement the last step, bringing Loopy Pro back to the front, was refused three times: the automation session had ended by itself after ten minutes in which only the diagnostic app had been asked. By then the tone was off, every equaliser off and mixer cells and levels were as before, as the unit's state shows. A new session brought Loopy Pro to the front 40 seconds later, and a reading confirmed the unit as at the start.

## The reference

The [protocol reference](../protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) carries the results. Its [codec](../protocol/reference/babyface_cc.py) now calculates the curve of an equaliser message and solves the low cut for an exact corner, and comes with 130 test vectors; the 21 new ones are, byte for byte, messages that this run put on the wire. All [measured curves](../protocol/reference/eq-curves-measured.json) are published, and the tests of the codec compare every one of the 1355 points.

At the end of the run every equaliser was off, the main output muted and the unit as at the start; the project that was loaded before stayed loaded and was never changed.

## Remaining boundaries

Not established: the equaliser of the headphone outputs (no cable from a headphone output to an input); any sample rate other than 48 kHz; whether the unit keeps the equaliser when its USB connection is built anew, and whether it reports it; inputs sent to the main output and loopback (left out while the loop cable is in place); phantom power; the device settings. The readings come from the unit's own peak meters, through its converters and one cable; no external measuring instrument was used. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
