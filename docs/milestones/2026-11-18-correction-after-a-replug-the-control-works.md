# Correction: after a replug the control works at once

Recorded 18 November 2026, 00:44 to 00:58 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run after one replug by the operator, a watch that changed nothing, and an offline reproduction. This is not a live approval.

## What was claimed

The report on [the two ways inside the host](2026-11-17-control-ways-inside-the-host.md) said, after five replugs of the interface on 17 November: the way to the unit comes back by itself, but the input of the host from the interface stays dead until the separate routing app wakes or starts. It called this a fault of the host, and a report for its developer was drafted. Two later reports repeated that the routing app has to be brought to the front once after a replug.

That conclusion was wrong. The report for the developer was never sent and is withdrawn.

## What was measured now

The operator pulled the cable of the interface at the hub and plugged it in again. A watch that only reads was running; it saw the system suspend the routing app at that moment. Then, with the routing app still suspended and untouched:

| Check | Result |
|---|---|
| A READ on the page reaches the unit (answer seen at the unit) | yes |
| Arming brings the signal back to the headphone output | yes |
| A step of 0.5 dB on the headphones arrives and goes back | yes |
| The page shows that it has read, or that it is armed | no |

So the control works at once after a replug: the host receives the answers of the unit, the rule reads, arms, and sends the mixer picture again. Only the displays stay where they were, because they pass through the routing app and the system has suspended it. After the routing app was brought to the front once, the page showed everything again.

## Why the earlier conclusion was wrong

The probe of the five replugs pressed READ and looked at the page. When the page did not show the read, the probe pressed the lock, and that discards the read the rule had just taken. It then armed, which needs a read, and pressed a step, which needs an armed page; nothing could be sent. The project took "no step arrived" as "the answer never reached the controller". Run offline against the same rule, this sequence gives exactly that: a read flag of 1 after the answer, 0 after the lock, no arming, no step.

The measurements of those rounds stand as recorded: the request reached the unit every time, the page showed nothing, no step arrived, and bringing the routing app to the front restored the page. What they show is the suspended display path, not a dead input of the host. The six handles tried inside the host could not help for the same reason.

## A second interruption the same night

Twenty-five minutes earlier the power of the whole chain dropped for a moment, when another device was plugged into the same charger. The unit lost its mixer, as after every such loss, but the routing app was not suspended, and the next READ showed on the page at the first try without the app being touched. Why the system suspended the app in the one case and not in the other is not established.

## What follows for the setup

After a replug: READ, arm, and the sound is back; the routing app only has to be brought to the front for the displays. Arming works even though the page cannot show it yet.

## Remaining boundaries

One replug was measured with the corrected probe; the offline reproduction and the re-reading of the five earlier rounds support it. Not established: why the system suspends the routing app at a replug of the interface cable; displays that do not depend on the routing app; a setup that needs no touch at all after a replug. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
