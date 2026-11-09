# Main and Phones: five step sizes and gain-mute restoration

Later checkpoint: [Sync LIVE1 fader startup, bounded writes and activation gates](2026-11-09-live-faders-startup-gates.md). This report retains the scope and open items of its own completed test.

Date: **9 November 2026** (Europe/Berlin). Evidence level: project-reported, scoped iPad/Babyface device tests. These later tests are separate from the [v09b3 half-dB follow-up-read checkpoint](2026-11-09-phones-v09b3-follow-up.md) and the [8 November send-free widget simulation](2026-11-08-native-step-simulation.md).

## Completed device checks

| Tested control | Reported result |
|---|---|
| Paired Phones step buttons | Each of 0.5 / 1 / 2 / 3 / 6 dB was applied as a reduction followed by exact restoration. Main stayed unchanged. |
| XLR2 alone | A 0.5-dB reduction and exact restoration passed. XLR1 and both Phones values stayed unchanged. |
| Stereo Main step buttons | Both XLR channels were reduced together and restored exactly for each of 0.5 / 1 / 2 / 3 / 6 dB. Phones stayed unchanged. |
| Main gain-mute toggle | One button reduced the level and restored the freshly read, saved level exactly. The following 0.5-dB step check also passed. |
| Phones gain-mute toggle | The equivalent one-button reduction/restoration and following 0.5-dB step check passed. |
| Saved combined candidate | Complete controller code and all 22 button actions were checked in the saved project, including its separate AU-state resource. |
| Cleanup | Original project and previous MidiFire scene restored; diagnostic processes ended. |

The five sizes were tested in **reduction-and-restoration pairs**, not an exhaustive sequence of arbitrary upward moves, rapid repeated presses or full-range sweeps. The dB descriptions are mapped device/display values, not new acoustic calibration. No numeric baseline or attenuation floor is inferred where the completed summary does not specify it.

## Gain-mute is not a hardware mute bit

The candidate's MUTE/ON controls use **gain reduction with a saved restoration value**. They do not establish a native RME/TotalMix mute bit, synchronization with TotalMix's mute state, or measured acoustic silence. A successful restore proves the reported level was recovered in these tests; it does not prove all interruption or reconnection cases.

Button colors/indicators were **not confirmed as device-state feedback**. The saved-state content check is not a complete reload/recovery test or a portable public release.

## Remaining acceptance work

- Confirmed button-state indicators and freely movable faders.
- Transport-stop, pause, connection-change and reconnection safety.
- Broad freshness/correlation guarantees, rapid repeated operation and long-duration behavior.
- Native hardware-mute semantics and synchronization, if that control is pursued.
- TotalMix-independent operation, a complete iPhone workflow and other hardware/firmware combinations.
- A versioned, reproducible public device profile, reviewed native artifacts and simple installation/removal instructions.

The tested candidate still requires **READ → ARM** (LESEN → AKTIVIEREN). Its own gain-mute must be cleared before locking or stopping transport. These are current candidate restrictions, not a general safety guarantee or a published hardware-test procedure. There is **no full live release**.

## Publication scope

This is a sanitized summary of completed device tests. No device operation was performed to publish it. Native projects, full controller source, raw captures, exact version inventory and a source checksum for the combined candidate are not included. The browser planner remains a planning tool with no MIDI, OSC or audio transport. Earlier results retain their dates, revisions and evidence limits; their offline counts or hashes are not reassigned to this candidate.
