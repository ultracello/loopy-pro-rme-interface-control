# Pan measured, a display fault found, and the routing app ended in the background

Completed 17 November 2026, 03:33 to 04:09 (Europe/Berlin). Evidence: project-reported, three bounded native iPad/Babyface Pro FS runs and offline tests. This is not a live approval. This report records two faults as plainly as the result.

## Pan

An eleventh revision of the candidate rule, SHA-256 `ad324ba0739252d4526e2fab4bda04b62b02814fcdf581efc9c959660c25099b`, gives each of the five ways to the headphones a pan: the monitoring of inputs 1 to 4 and the playback. There are 41 positions. In the middle both sides get the level of the way; towards one side the other side is lowered by 1.5 dB per position and switched off at the end. The filter before the interface did not need to change. Offline, 15 new tests passed and the 135 tests of the earlier revisions still pass; all 20 deliberate falsifications were noticed.

Measured with the cable from an output into an input that the operator had left in place, Main at −30 dB, input 1 at −26.6 dBFS, the playback taken off the headphones for the measurement:

| State of the monitoring of input 1 | Headphone output left | right | Difference from expected |
|---|---|---|---|
| −12 dB, middle | −53.1 dBFS | −53.1 dBFS | 0.0 dB |
| Four positions right | −59.1 dBFS | −53.1 dBFS | 0.0 dB |
| Fully right | no signal | −53.1 dBFS | 0.0 dB |
| One more step right | refused | | |
| Back in the middle | −53.1 dBFS | −53.1 dBFS | 0.0 dB |
| Four positions left | −53.1 dBFS | −59.1 dBFS | 0.0 dB |
| −30 dB, middle | −71.1 dBFS | −71.1 dBFS | 0.0 dB |

All 30 presses showed the expected reason. The run then stopped itself, for the reason in the next section, and put everything back.

## A display fault of the project's own making

At −48 dB the level display on the page showed −48.5 dB. The level sent was right; the display was not. The page shows a level on a dial with 121 fields, and the rule had scaled the level to a MIDI value on the assumption that the 128 values are spread evenly over the fields. They are not.

A twelfth revision corrected the scaling by a reading that fitted the eight pairs seen until then. A run then stepped through all 121 levels on a way that was not switched on, so that nothing was sent, and read the page each time: 21 of the 121 levels were still one field off, too low in the upper part of the scale and too high in the lower part. The distance between value and field grows at the values 9, 25, 41, 57, 75, 96 and 117, not at even steps. The twelfth revision was wrong as well and is not to be used.

The conclusion is to stop scaling. A thirteenth revision, SHA-256 `30abe4be9d27f50a555e062b5ff22020ff277ef03ee2ba2c622fe436a99c530c`, sends every dial the number of its field, and every dial gets 128 fields, as the two level displays of Main and Phones have had from the first day. It is built and tested offline (8 new tests, 144 earlier ones) and prepared for a run that reads every dial field by field. It is not on the interface yet.

The displays with 66, 60, 41 and 19 fields showed the right value every time they were looked at, but they were never read value by value. They are converted with the others.

## The routing app was ended in the background

In the run for the twelfth revision the page stopped answering after about two minutes: LOCK and READ changed nothing, and the status row went on showing "armed". The controller in the host was running and showed that it had locked; its messages reached neither the page nor the interface. Both ways lead through the separate MIDI routing app. Brought to the front once, that app showed that it had just started, and the page answered again at once. It had last been in front about twelve minutes earlier.

This is what the operator had described a week before as the routing app "falling asleep", now observed: the system ended the app in the background, and the page could not show it, because the feedback to the page takes the same way. During that time Main stood at −30 dB instead of muted; it was muted again and read back as muted once the way was restored.

A read-only look at the host followed. It accepts control only from MIDI devices, not from a plugin directly, so the feedback to the page needs a way round even when the two ways to and from the interface are moved into the host.

## Later the same night

The interface then disappeared for the iPad altogether: no port of it was present when the helper started, so the prepared run did not begin. The cause is with the cabling or the power and was not determined in this session.

## Remaining boundaries

Not established: the thirteenth revision on the interface; every value of the displays with 66, 60, 41 and 19 fields; why the system ended the routing app; a setup that does not depend on that app; why the interface disappeared. Monitoring levels were measured down to −30 dB, not below.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
