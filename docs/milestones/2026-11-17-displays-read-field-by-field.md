# Every display read field by field, and what replugging the interface needed

Completed 17 November 2026, 09:15 to 10:09 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run with a diagnosis in the middle. This is not a live approval.

## The thirteenth revision is on the interface

The thirteenth revision of the candidate rule, SHA-256 `30abe4be9d27f50a555e062b5ff22020ff277ef03ee2ba2c622fe436a99c530c`, no longer scales a value for a display. Every dial of the page has 128 fields, and the rule sends the number of the field. The run converted the sixteen dials of the operator's project that had been scaled until then, loaded the copy and read the page after every step:

| Display | Read from the page | Wrong |
|---|---|---|
| Level of a way to the headphones, on a way that was off, so that nothing was sent | 140 readings, all 121 levels from −60.0 to 0.0 dB | 0 |
| Pan of a way, both ends included | 22 readings | 0 |
| Gain of the inputs, compared with what the unit reported: microphone input 1 through all 66 values, line input 4 through all 19, inputs 2 and 3 in part; Main muted | 130 readings | 0 |
| Step width | shown 3.0 dB, the step then was 3.0 dB; shown 9.0 dB, the step was 9.0 dB; shown 20.5 dB, the step stopped at the end of the range | as shown |

The fault of the eleventh and twelfth revisions, a level display one field off at 21 of 121 levels, is gone. The displays with fewer fields, which had only been looked at before, are now read value by value.

## Measurements repeated and extended

With the cable from an output into an input still in place, Main at −30 dB and input 1 at −26.6 dBFS:

| State | Headphone output left | right | Difference from expected |
|---|---|---|---|
| Playback off, nothing monitored | no signal | no signal | |
| Input 1 at −12 dB, middle | −53.1 dBFS | −53.1 dBFS | 0.0 dB |
| Four positions right | −59.1 dBFS | −53.1 dBFS | 0.0 dB |
| Fully right | no signal | −53.1 dBFS | 0.0 dB |
| Four positions left | −53.1 dBFS | −59.1 dBFS | 0.0 dB |
| Input 1 at −30 dB | −71.1 dBFS | −71.1 dBFS | 0.0 dB |
| Input 1 at −48 dB | −89.2 dBFS | −89.2 dBFS | −0.1 dB |
| Input 1 off | no signal | no signal | |
| Playback at 0 dB, middle | −20.5 dBFS | −20.5 dBFS | 0.0 dB |
| Playback four positions right | −26.5 dBFS | −20.5 dBFS | 0.0 dB |
| Input 1 at −12 dB and the playback at 0 dB together | −20.4 dBFS | −20.4 dBFS | not judged |

New against the earlier runs: a monitoring level below −30 dB, the pan of the playback, and an input and the playback on the headphones at the same time. All 49 presses showed the expected reason. At the end the inputs, the pads and the levels stood where they had stood, and Main was muted again.

## What replugging the interface needed

During the night the interface had disappeared for the iPad and was plugged in again by the operator. After that the first attempt of this run stopped at its first step: the page did not read. The diagnosis, step by step:

- The helper read the unit directly, state and meters.
- A READ on the page did not reach the unit, and no feedback reached the page, not even "waiting".
- The copy with the twelfth revision behaved the same. The new rule was not the cause.
- The controller in the host took the presses and showed that it had asked and then locked.
- The identifiers of the virtual ports of the routing app matched those in the project. The project differed from the installed one only in what its displays showed.
- The playback of the host arrived at the unit. The headphone output carried nothing: the unit had lost the way of the playback to the headphones, as after every loss of power.
- The routing app showed all its modules and reported the port of the interface as newly added.
- Loading the scene of the routing app again changed nothing.
- Ending both apps and opening them again, the routing app first, restored reading at once.

So after the interface had been replugged, MIDI between the host and the routing app was dead in both directions until both apps had been started anew. Which of the two apps held the stale connection was not separated. Together with the routing app being ended in the background, recorded in the report before this one, this is the second way in which the present setup depends on that app.

One more fact about the test rig, not about the interface: the helper on the iPad could not start twice because the iPad was waiting for its device code. It started once the operator sat at the iPad.

## Remaining boundaries

Not established: which of the two apps needs the restart after a replug, and whether a setup with the ways to and from the interface inside the host survives a replug without one; why the interface disappeared in the night; why the system ended the routing app in the background. No microphone or instrument was connected. Monitoring was measured down to −48 dB, not at −60 dB.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
