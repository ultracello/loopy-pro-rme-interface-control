# Native faders: startup state, bounded writes and activation gates

> Later current-policy update: [Restricted control and Interface integration](2026-11-09-restricted-control-interface-integration.md). Gain-mute and old saved-level restore are blocked in that later revision; the observations below retain their historical scope.

Date: **9 November 2026** (Europe/Berlin). Candidate: **Sync LIVE1**. Evidence level: project-reported, scoped iPad/Babyface device checks. This follows the [Main/Phones step-button and gain-mute checkpoint](2026-11-09-main-phones-steps-gain-mute.md); it is not a general live release.

## Completed checks

| Check | Reported result |
|---|---|
| Fader initialization | Three project starts showed correct current device values without touching the faders first. The observed initialization defect was resolved in the tested candidate. |
| Main fader | Reduced and increased the device levels; original values were independently checked and restored exactly. Phones stayed unchanged. |
| Phones fader | Reduced and increased the device levels; original values were independently checked and restored exactly. Main stayed unchanged. |
| Transport stop | Locked the controls in the tested state. |
| Missing return path | Prevented activation, including in the write-enabled candidate. |
| Restored return input | All output values were checked again and remained unchanged. |
| Preservation and cleanup | The tested candidate was saved. Original project and previous MidiFire scene were restored; diagnostic processes ended. |

These were bounded fader gestures, not a full-range sweep or an exhaustive arbitrary-gesture test. Gesture displacement must not be interpreted as a fixed dB step: actual device-state readback was used to check the result and restore the saved baseline. The dB interpretation remains [mapped device/display evidence](../protocol/output-gain-evidence.md), not new acoustic calibration.

## What the gate checks establish

The observed transport-stop state locked control, and a missing return path prevented activation. These checks advance specific safety-gate evidence. Restoring a test return input does **not** establish physical USB disconnect/reconnect recovery. Neither result proves all timing, interruption, stale-state or recovery cases.

Three successful starts cover those three starts only. They do not prove every host/app lifecycle or a full reload/recovery matrix. No test counts, hashes or guarantees from earlier candidates are reassigned to Sync LIVE1.

## Still open

- Auxiliary displays/indicators and their confirmed device-state feedback.
- Gain-mute lifecycle, including recovery across lock, transport stop and other interruptions.
- Physical USB reconnect and long-duration checks.
- Full-range/arbitrary or rapid fader operation, broad freshness/correlation guarantees and a complete recovery matrix.
- Native hardware-mute bits, TotalMix-independent operation, a complete iPhone workflow and other hardware/firmware combinations.
- A reproducible public device profile, reviewed distributable artifacts and end-user installation/removal instructions.

Gain-mute still means level reduction with a saved restore value, not a verified hardware mute bit or acoustic silence. The earlier candidate restriction to clear its own gain-mute before lock/transport stop has **not** been lifted by these fader checks. There is **no full live approval**.

## Publication scope

This report summarizes the completed device result. Publication did not access the interface, send MIDI or perform Mac mouse/keyboard input. No private paths, native source projects, complete controller code, raw captures or device identifiers are included. A source checksum and complete reproducible version/profile inventory for Sync LIVE1 are not distributed here. The public browser planner still sends no MIDI, OSC or audio and does not install a controller.
