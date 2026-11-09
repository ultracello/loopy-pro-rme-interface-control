# Complete read paths and a bounded reply-loss gate

Date: **9 November 2026** (Europe/Berlin). Evidence: project-reported, scoped iPad / Babyface Pro FS checks in class-compliant mode, using Loopy Pro, StreamByter and MidiFire. The new gate test used a **gain-disabled diagnostic copy**. It is separate from the earlier [Sync LIVE1 fader checkpoint](2026-11-09-live-faders-startup-gates.md).

## Read-path comparison

Exactly one fixed state query was triggered through each of two paths: the existing Loopy sender and a MidiFire-generated query. Both used the same continuously registered independent input receiver, with Loopy in the foreground. Each produced a complete **227-byte state message and two 207-byte meter messages**. In both observations the state arrived in chunks of **9 + 75 + 143 bytes**; no orphan bytes or abandoned partial message were added.

This comparison did **not** reproduce the earlier incomplete-prefix observation. It therefore does not isolate its cause or justify changing the parser or sender. There is no protocol transaction nonce: these are observed messages after the triggers, not an independently proven causal acknowledgement scheme.

## Reply-loss and explicit reactivation

The return input was temporarily muted only inside the separate Loopy diagnostic copy. An independent receiver still observed the interface's complete replies.

| Phase | Observed result |
|---|---|
| Fresh initial read, then activation | The diagnostic UI showed active. |
| Return input suppressed, another read, then activation attempted | The UI remained waiting and did not activate, although the independent receiver saw a complete state. |
| Return input restored, new complete read | The UI showed read-ready and stayed inactive. |
| Explicit activation after that read | The UI showed active. |
| Final lock | The UI returned to unknown/inactive. |

The two comparison observations and the three gate observations retained the same four output-gain values. No gain or mute write was requested. The existing audio clip stayed stopped. Original project and previous MidiFire scene were restored and checked, the temporary reader was stopped, and the diagnostic services/helper were ended.

This is a **simulated missing-return test**, not a physical USB disconnect, device replacement, app reload or mute-restoration test. It does not certify the write-enabled controller's complete recovery behavior.

## What remains open

- The sporadic USB/hub failure, the historical missing-prefix cause, physical reconnect and endurance behavior.
- Safe gain-mute restoration across lock, transport stop, reload, receiver-session change or USB interruption. Unknown mute ownership must not cause a blind gain restore.
- Broad freshness/correlation guarantees. Re-arming, a new receiver session and a different device are separate events; equal levels or equal message suffixes cannot establish their identity.
- A complete F-01–F-12 regression against the proposed requirements. Separate synthetic parser checks are not this end-to-end proof; the proposed F-12 freshness rule still needs a precise definition.
- Full range, native hardware-mute bits, absolute acoustic silence and a reproducible installable public profile.

Fragmentation with all bytes present must be distinguished from a collector receiving only a tail. An earlier collector retained 218 continuation bytes without the start of the 227-byte state, alongside complete meter messages. That does not prove where bytes were lost or identify a particular USB cause. An identical 218-byte suffix would not identify a frame instance. Missing bytes are not repaired or invented.

Gain-mute remains level reduction, not a proven native mute bit. Invalid or asymmetric observations must retain their actual left/right values and uncertainty; they must not be flattened into a fabricated shared raw59 value. The earlier instruction to clear the candidate's own gain-mute before lock/transport stop is not lifted. **No complete live approval or finished product is claimed.**

## Publication scope

This is a sanitized result summary. No device identifiers, private paths, raw captures, audio, native projects, complete controller source or endpoint-bound scenes are included. The website remains a browser-only planner and sends no MIDI, OSC or audio. Publishing the report does not promote a hardware module.
