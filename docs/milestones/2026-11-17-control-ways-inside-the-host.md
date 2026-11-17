# The two ways to and from the interface now run inside the host

Completed 17 November 2026, 10:19 to 11:03 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run in three sessions. This is not a live approval.

## Why

Two reports before this one recorded how the setup depended on the separate MIDI routing app: the system ended that app in the background, and after the interface had been replugged both apps had to be started anew. Every message to and from the interface went through that app.

## What was built

A copy of the operator's project, built offline from the saved project, with the candidate rule unchanged (thirteenth revision, SHA-256 `30abe4be9d27f50a555e062b5ff22020ff277ef03ee2ba2c622fe436a99c530c`):

- The host itself listens to the MIDI port of the interface and hands what arrives to the controller.
- The controller sends to a second instance of the same MIDI plugin inside the host. That instance carries the strict filter that used to sit in the routing app (SHA-256 `cd09357bc0975a22af2da6a69373cbb62ee262599ee36ec4babac14094b2f4ab`, unchanged), and only it sends to the interface. The build checks that the project reaches the interface on no other way.
- The feedback to the page still goes through the routing app, because the host accepts control only from MIDI devices, not from a plugin.

The scene of the routing app keeps its modules and connections; its filter before the interface now passes nothing, so that no message can reach the unit on two ways.

The host loaded the copy as built: the second plugin instance ran, and both ports were bound.

## With the routing app not running

The routing app was ended, the copy loaded. A READ on the page reached the unit: the helper saw one state answer at the port of the interface, twice. After arming, a step of −0.5 dB on the headphones arrived at the unit and the step back as well. The page showed nothing in this phase, as expected.

## With the routing app only for the displays

Nine checks, all passed: READ shows "read" on the page at the first attempt; the unit answered once; arming shows "armed"; a step down and a step up arrive with the reason "OK"; the routing app is ended while the page is armed; a step down and a step up still arrive at the unit; after the routing app is opened again the page reads and shows it.

One limit of these checks, stated plainly: the first pass of this phase ran with the old scene by mistake, because the routing app did not list the new scene right after its start. It showed the same numbers, including "the unit answered once", where two answers would have been expected with two ways open. So this check does not show that the new scene prevents doubles; that follows from its rule text only.

## Displays and measurements repeated on the new copy

| What | Result |
|---|---|
| Level display, pan display, gain displays, read from the page | 147, 22 and 130 readings, none wrong |
| Step width | shown 3.0 dB and 8.5 dB, executed as shown |
| Measurements at the headphone output with the cable from an output into an input: monitoring at −12, −30 and −48 dB, pan of the monitoring and of the playback, both together | the same values as in the run before, at most 0.1 dB from expected; 48 presses with the expected reason |

## One thing not explained

The first of two acceptance attempts on the new copy stopped because twelve presses in a row had changed nothing. The way concerned was off, so nothing was being sent; only the level the rule keeps for it did not move. After those presses it went on by itself. Status and reason were not recorded at that moment. A watch of 150 presses that noted status and reason after each one saw no drop, and the second attempt read its 147 level values without one. The cause is open. Candidates: a touch on the iPad or the unit, a rare case in the rule, or the new direct input, through which the controller now receives everything the interface sends on that port and not only complete states.

A second fault was the test script's own: its measuring block assumed that the rule did not yet know whether the playback was on the headphones. After the first attempt it did. The block was corrected and run on its own.

## Later the same day: replugged three times

Completed 11:41 to 11:58. The operator pulled the cable of the interface at the hub, waited five seconds and plugged it in again, three times. Before, the page read at the first attempt and a step arrived.

| Round | Routing app when the cable went back in | Stage | READ reaches the unit | Step arrives |
|---|---|---|---|---|
| 1 | suspended by the system | as it is | yes | no |
| | | 20 seconds later | yes | no |
| | | routing app brought to the front once | yes | yes |
| 2 | suspended | as it is | yes | no |
| | | home screen and back to the host | yes | no |
| | | routing app brought to the front once | yes | yes |
| 3 | ended beforehand | as it is | yes | no |
| | | home screen and back | yes | no |
| | | 45 seconds later | yes | no |
| | | routing app opened | yes | yes |

Between rounds 2 and 3 the routing app was ended after the recovery, and a step still arrived: the answers of the unit reach the controller through the input of the host, not through the routing app.

What this shows. The way to the unit comes back by itself. The input of the host from the interface stays dead after a replug, also after two minutes and after leaving and re-entering the host, so the controller never sees the answer and writes nothing. It works again the moment the routing app wakes or starts, although that app does not carry the input. A likely reason, not established: the host binds its input again only on a later change in the MIDI service of the system, and the routing app causes one when it wakes. The replug itself suspended the routing app, which had been running in the background before.

Two more rounds followed at 12:03 to 12:16, with the routing app ended beforehand, to find a handle inside the host that would wake its input. None did: opening and closing the mixer, the control settings (which listed the interface again), the synchronization settings, MIDI learn and the Bluetooth MIDI panel, and stopping and starting the transport all left the input dead; opening the routing app restored it at once, both times. So the host knows the device again and sends to it, but does not connect the input of its mixer source again by itself. This is being written up as a report for the developer of the host.

No app had to be restarted in any round; with the earlier setup both had to be. The way of the playback to the headphones was lost each time, as after every loss of power, and its button restored it.

## Remaining boundaries

Not established: why opening the routing app wakes the input of the host after a replug, and a setup that recovers without any touch; the cause of the twelve presses without effect; feedback to the page without the routing app; the operator's seven existing routes of the scene in playing use. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
