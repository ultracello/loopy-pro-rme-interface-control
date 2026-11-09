# v09b3: bounded Phones test with automatic follow-up reads

Date: **9 November 2026** (Europe/Berlin). Revision: **v09b3**. Evidence level: project-reported, scoped device observation. This is a new checkpoint, separate from the [8 November v09 TEST result](2026-11-08-phones-fader-write-restore.md) and [send-free step-selection simulation](2026-11-08-native-step-simulation.md).

## Observed result

The controlled test ran after more than 75 seconds of transport runtime:

| Check | Reported result |
|---|---|
| Phones left and right | Both changed from −10.5 to −11.0 dB, then returned to −10.5 dB |
| Executed level changes | Exactly one reduction and one restoration |
| Automatic follow-up queries | Issued after 101 ms and 100 ms respectively; both received successful replies |
| Native StreamByter status | BEREIT / AKTIV after both operations |
| Separate confirmation | Additional device queries confirmed the change and exact restoration |
| Main Out | Unchanged at −8.0 dB |
| Cleanup | Original project and previous scene verified restored; diagnostic processes ended |

The dB values describe the mapped device/display levels. See the [output-gain evidence](../protocol/output-gain-evidence.md) for the distinction from an acoustic measurement.

## What this advances

This checkpoint records a bounded paired Phones operation with successful automatic follow-up reads and separate confirming device queries after more than 75 seconds of transport runtime. The 101/100 ms observations are two query timings in this run, not a latency distribution or a sustained reliability claim.

The earlier v09 TEST and simulation reports retain their own revision, dates and limitations. Their test counts and rule hashes must not be reassigned to v09b3.

## What remains unverified

- Full-range fader behavior, large gestures, pickup and repeated rapid operation.
- A reusable native step-button/selector integration and larger physical steps.
- New mute toggles, native mute synchronization and stereo Main writes.
- Suspend, reconnect, extended-duration behavior and broad freshness/query-correlation guarantees.
- Operation with TotalMix terminated, a complete iPhone workflow and other device/firmware combinations.
- A reproducible, installable end-user package with its complete version/profile inventory and acceptance tests.

More than 75 seconds of transport runtime is not long-duration or lifecycle validation. This test does not establish general live readiness or promote a released hardware module.

## Publication scope

This report summarizes the completed device-test result. The publication did not repeat the device test, access the interface or send MIDI. Raw captures, the native project, complete controller source and a source checksum for v09b3 are not distributed with this report. No new acoustic measurement is claimed. It is not an installation guide or authorization for further hardware writes.
