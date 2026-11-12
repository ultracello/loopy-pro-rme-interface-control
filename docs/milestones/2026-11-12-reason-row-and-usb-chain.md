# A reason row on the page, and a USB chain that held

Completed 12 November 2026, 23:25 to 23:53 (Europe/Berlin). Evidence: project-reported, two bounded native iPad/Babyface Pro FS runs and offline tests. This is not a live approval.

## The USB chain

The [evening of 10 November](2026-11-10-hand-operation-loop-transport-phones-route.md) ended with the iPad losing the interface on USB three times within an hour. Those losses happened with a charging adapter between the iPad and the interface. With the interface plugged straight into the iPad, sound held for ten minutes.

The operator then rebuilt the chain without that adapter: iPad, a hub with its own power-delivery input fed by a wall charger, the interface on a data port of the hub, and the interface's own power supply. The iPad charges in this chain.

In a 20-minute watch the helper sent the fixed read query every ten seconds, 120 times. All 120 were answered, playback arrived each time and the Phones output carried signal each time. Nothing was pressed during the watch.

Twenty minutes are not an endurance test. An evening of playing, with the MIDI controllers on the same hub, has not been observed. What exactly failed in the earlier chain was not determined.

## The Phones route control, second measurement

After the re-cabling the interface answered, playback arrived and the Phones gain was open, but the peak meters of all outputs read zero. After READ, ARM and the Phones route control the Phones output carried signal; Main stayed at zero and no gain changed. This is the second time the two mixer levels were seen to restore the route on this unit.

## Why the page locked

The operator had reported several times that the page fell back to "unknown" after a few step presses. A fast automated series of 72 Phones steps, at least 0.7 seconds apart, never locked the page; the automation cannot press faster. Until now the reason for a lock was visible only inside the controller's own window.

A fifth revision of the candidate rule, SHA-256 `ea12c79f408df6454b56a874e41e12b3b34370cbf0213eb9e4713792870b8d77`, publishes the reason on a feedback controller that the routing scene already passed and that no element of the project had used. A new status row on the page shows one of seven fields: ok, minute over, read first, no answer, level differs, refused, fault. No decision and no message to the interface changed; an offline test compares a sequence of operations between the two revisions.

Offline, 11 new tests passed and the 46 tests of the earlier revisions still pass. Six deliberate falsifications were noticed.

On the interface, with a clip looping:

| Check | Reason row | Otherwise |
|---|---|---|
| READ and ARM | ok | page armed |
| A Main step while Main stood at raw 59 from outside | refused | page stays armed, no gain changed |
| Phones half a dB down, then up | ok | raw 213/213, then 214/214 |
| LOCK, then a Phones step without READ | read first | no gain changed |
| READ, ARM, then 63 seconds without a press | minute over | page locked |

The fields "no answer", "level differs" and "fault" were shown offline only.

## Other observations

- The host app had been updated to a new test build before the runs. The automated steps worked unchanged.
- The routing app offers no setting to bind a port again after a USB reconnect. With a chain that holds, starting it after everything is plugged in is enough. Routing without that app is an idea for later, not a result.

## Remaining boundaries

Not established: anything on Main; an evening of playing on the new chain; the cause of the operator's locks (the reason row is meant to show it); the three reason fields named above on the interface; fader writes in an automated run; operation alongside TotalMix; crash-safe recovery.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
