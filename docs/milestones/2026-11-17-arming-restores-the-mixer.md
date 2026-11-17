# Arming restores the mixer of the unit

Completed 17 November 2026, 13:28 to 14:25 (Europe/Berlin). Evidence: project-reported, offline tests and one bounded native iPad/Babyface Pro FS run in four sessions with one replug. This is not a live approval.

## Why

The unit forgets its mixer whenever its USB connection is built anew: the way of the playback to the headphones, the monitoring of the inputs and every pan are gone, while the page still shows what had been sent. Until now one button brought back only the playback at 0 dB.

## The fourteenth revision

The fourteenth revision of the candidate rule, SHA-256 `2a9cc28d2b29761113e202b39aac13af92352fc8eb94936904381d7aa527f23a`, sends again, whenever the page is armed, every way to the headphones whose state it knows: a way that is on with its kept level and pan, a way that is off as off. A way whose state is unknown, because it was never switched since the project was loaded, is not touched, so nothing is sent that the operator has not set. After the sends the rule asks the unit for its state, as after every monitoring send. The messages are the ones a switch of that way sends; the filter before the interface did not change.

Offline, 13 new tests passed, the 151 tests of the earlier revisions still pass, and all 18 deliberate falsifications were noticed.

## Measured across a replug

A picture was set: the playback on the headphones at −6 dB, four positions right; input 1 monitored at −12 dB, two positions left. Then the operator pulled the cable of the interface and plugged it in again. The routing app was brought to the front once, as the earlier report found necessary; the page was read and armed. Nothing else was pressed.

| Measurement at the headphone output | left | right |
|---|---|---|
| Before the replug, playback alone | −32.5 dBFS | −26.5 dBFS |
| Before, input 1 alone | −53.1 dBFS | −56.1 dBFS |
| Before, both together | −31.9 dBFS | −26.3 dBFS |
| After the replug, before arming | no signal | no signal |
| After reading and arming, nothing else pressed | −31.9 dBFS | −26.3 dBFS |
| Then the playback switched off: input 1 alone | −53.1 dBFS | −56.1 dBFS |
| Then the playback on and input 1 off: playback alone | −32.5 dBFS | −26.5 dBFS |

So arming brought both ways back with their levels and pans. The button for the way of the playback is only needed now when that way was never switched since loading.

## A deviation, and a soak

The usual block of measurements failed once on this revision: with input 1 panned fully right, the left side read −80.2 dBFS instead of nothing, the level of the pan position before. A targeted repeat, ten times between those two positions, with the routing app running and ended, was silent every time, and the full block then passed with the values of the earlier runs.

A soak followed: the pan of a monitored input went two positions right and back 400 times, and after every press the left side was read from the meters of the unit. All 400 arrived. The soak also measured how long the meters take to show a new level: 0.65 to 2.19 seconds, median 1.38, 24 of 400 above two seconds. The project's measurement starts about two seconds after a press and keeps the maximum over six seconds, so a level the meters still hold can enter the result. That is the likely cause of the one deviation; it is not proven.

With the stopped first attempt of the soak, more than 500 measured presses went through the setup with both ways inside the host without a lost message. The twelve presses without effect of the report before this one remain unexplained; nothing was being sent then.

## Remaining boundaries

Not established: the cause of the twelve presses without effect; a setup that recovers from a replug without any touch (the routing app still has to be brought to the front once); ways restored when more than two are in use at once (tested offline for all five, on the unit for two). No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
