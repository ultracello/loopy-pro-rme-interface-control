# Operating by hand with a looping clip: transport position, stuck wait, and the Phones route without TotalMix

Completed 10 November 2026, 20:05 to 23:13 (Europe/Berlin). Evidence: project-reported. Several bounded native iPad/Babyface Pro FS runs, the operator's own use between them, and offline tests. This is not a live approval.

## What the operator found

After the [Interface copy with mute switches](2026-11-10-interface-copy-mute-switches.md) had passed its automated run, the operator used it by hand for the first time, with a clip looping in the same project. The automated runs had never played a clip. Three things went wrong:

- READ and ARM had to be pressed again and again before the next control would act.
- A Phones mute never completed. The device stayed at raw 59/59, the page stayed at "waiting" for more than 20 minutes, and the controller no longer knew the level from before. One press on LOCK released the page. In TotalMix the muted output showed with its fader at the bottom, not with a lit mute button.
- With the page locked, nothing showed whether a group was muted.

Sound through the interface also dropped several times during the evening.

## Causes

**Host transport position.** The rule compared the host transport position at a press and at a reply with the position at the last read, and refused when it had gone backwards. According to the StreamByter manual this value is the host transport position in milliseconds. With a clip that loops, the position of the host goes backwards at each turn. In the offline interpreter a position set backwards reproduces both effects in the rule that was on the iPad: a new READ is demanded, and a mute confirmed across the jump loses its reference while the pair stays muted. Whether the position in Loopy Pro actually jumps this way was not measured on the device.

**Delayed internal events.** The check read after a write and the one-second watchdog both depended on delayed internal events. If both fail to arrive, the page waits for ever. Why they failed to arrive on the device is not established.

**Refused operations.** A later revision still locked the page whenever it refused an operation without writing anything: a step beyond the software range, any step or fader on a pair that stands muted, a fader released where it was or held for more than ten seconds.

**USB.** At 22:50 the iPad no longer listed the interface as a MIDI device at all, although the interface was on its own power supply by then. After the cable was plugged in again, the interface answered a direct query: playback arrived, the Phones gain was open (raw 228), and the peak meters of all outputs read zero. The interface had lost the mixer levels that put playback on the Phones output. Until now only TotalMix restored them, and there is no TotalMix for the iPhone.

## What changed in the rule

Three revisions of the candidate rule were built offline during the evening. The last one, SHA-256 `71a6e23841fedf7432d002f8566a28188e5172d60874e9a2c60624a5f8568985`, does the following:

- The host transport position decides nothing. Ages are bounded by the local timers, as before.
- The page stays read and armed for 60 seconds after the last accepted answer instead of 10. Before every write the controller still reads fresh and compares.
- A wait that is overdue by 1.5 seconds is resolved by the next press. A write whose check read was never sent gets that read then, so an own mute keeps its reference. Any other overdue wait locks, and the press is handled afterwards.
- A mute switch pressed over a pair that stands at raw 59/59 without a reference writes one fixed level, raw 183 (−30 dB), to that pair. This changes an earlier rule of the project: until now there was no way back without a reference.
- An own mute stays shown while its reference is held, also when the page is locked.
- A refused operation leaves the page read and armed. A fader problem ends the fader gesture only.
- One new control writes two fixed mixer levels: playback 1 to output 3 and playback 2 to output 4, at unity. The message follows the [protocol notes of the oscmix project](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro) for the mixer (sub ID 1). The outbound filter in MidiFire passes exactly these two messages, byte for byte, and no other mixer message (filter SHA-256 `f88bf42a411269d8448b37255a41a0226f5a1b48f258cf473d91cb5d6e686457`).

Offline, 33 new tests passed across the three revisions. Against the last revision the tests written for the earlier two and the 16 tests of the session gain-mute still pass, 38 in all. Each new property was also shown to fail against the rule it replaced. In counter-checks, 32 deliberate falsifications of the rule and the filter were noticed, two of them only after a test had been added.

## Results on the interface

The new rule was built into the operator's own saved project, so that his clip stayed, and put on the iPad under a new name. The clip, four seconds long, looped during the checks. Levels were read by an independent query each time.

| Check | Result |
|---|---|
| New rule compiles and answers | Yes, first READ accepted in each run |
| Eight Phones steps in 29 seconds without a new READ | All accepted; raw 228 to 224 after four steps down, back to 228 after four steps up |
| Phones mute and back, three times in a row | raw 59/59 each time, exactly 228/228 after each return |
| Mute, then LOCK | The status "own mute" stays lit; after READ and ARM the switch returns exactly |
| Refused Main steps (Main at raw 59 from outside) | Page stays armed, no level changed; Phones steps then accepted without a new READ |
| Phones route control with the route present | No level changed, no signal appeared at Main |
| Phones route control after a USB loss | Output peak at Phones from 0 to a level matching the gain (−7.5 dB below the playback peak); Main stayed at 0; no level changed; TotalMix closed |

Not every problem was a fault of the system: for part of the late evening the operator's headphones were not plugged in. The measurements above do not depend on what was heard.

## After a USB loss

After the interface was plugged in again, no query from the controller reached it: not after LOCK, a transport stop and start, bringing MidiFire to the front, or loading the scene again. Reads worked again after MidiFire had been quit and started and the project had been loaded again, both by hand. Which of the two is needed was not separated. An earlier check the same day, without the power supply, had seen the route come back by itself after a replug.

A key sequence from the interface manual that should copy playback to the Phones output without any app did nothing on this unit.

## Remaining boundaries

Not established: anything on Main, which stood at raw 59 from outside all day; fader writes in an automated run; the fixed level from a foreign mute on the interface; the late check read on the interface (no stuck wait occurred under the new rule); the cause of the USB losses; a return after a USB loss without restarting MidiFire and loading the project again; the seven existing routes of the scene in playing use; operation alongside TotalMix; endurance; crash-safe recovery.

The mixer message is taken from third-party protocol notes and was observed to work for these two levels on one unit. No other mixer level was written.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
