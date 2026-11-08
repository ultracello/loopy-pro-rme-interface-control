# Native Loopy faders display actual Babyface levels

Date: **8 November 2026**. Evidence level: **project-reported, scoped native UI/read-feedback observation**. This checkpoint establishes automatic display updates, not hardware-writing faders or a released control package.

**Later follow-up:** a [bounded Phones-fader write/restore](2026-11-08-phones-fader-write-restore.md) was subsequently observed. The report below remains the separate display-only checkpoint, not that later write test.

## Display and receive architecture

Each visible Loopy slider targeted a 128-step internal value store, using action-on-activation and no send actions. Project MIDI bindings targeted the visible sliders. Independent widget changes and distinct synthetic MIDI values first checked both directions and channel separation.

A separate MidiFire scene used the verified Babyface Port 2 input, a validated state-to-UI decoder and an isolated virtual output. There was no hardware output, raw bypass, loop or connected virtual feedback input.

- Only complete valid **227-byte state frames** were decoded.
- Equal in-range stereo pairs became **channel-15 CC60/61** UI values; unequal or out-of-range pairs were marked invalid.
- The decoder emitted only virtual UI CCs, **no RME write SysEx**.
- **2,506 independent offline cases** passed, followed by complete native text comparison and compiler validation.

These are reported development checks. Decoder source, fixtures and portable project artifacts are not included with this report; the counts do not establish a publicly rerunnable release suite.

## Native observed result

Exactly one known fixed state query returned a full state and two meter packets amid continuing short traffic. All **111 raw callbacks** in the bounded capture were retained. The decoded device levels matched the automatically updated native Loopy display:

- Main Out: **−8.0 dB**.
- Phones: **−10.5 dB**.

The query was triggered by a **temporary helper, not the Loopy READ widget**. The data return itself ran directly on the iPad without a Mac MIDI relay. No gain, mute, transport, clip or audio change was made in this checkpoint. Do not combine the query origin here with the separate [Loopy READ tests](2026-11-08-phones-step-restore.md) to claim that the whole path was exercised together.

## Explicit limits

- **Read feedback is not write intent.** Automatic display updates must not become hardware commands. A successful display update does not verify a user's fader gesture, a sent target or hardware readback after that target.
- Unknown/timeout display, freshness, pickup, separate human-gesture commits, toggles, stereo Main writes, mute and long-running/reload/reconnect behavior remain open for this checkpoint.
- Native TotalMix mute remains distinct from custom gain-mute/restore.
- This does not prove operation with TotalMix terminated or a complete Mac-free installation procedure.
- Saved resource references do not constitute a verified portable media export. A safe installable module still needs exact versions, source revisions, fixtures and a complete setup/removal guide.

The [single Phones step/restore report](2026-11-08-phones-step-restore.md) is separate level-changing evidence. Neither result promotes a continuous hardware fader, mute control or general device profile to a verified release.

## End state

The diagnostic scene and project were saved separately. The original scene and original stopped project were restored. Original database objects and controller profiles matched; audio/clip references matched. Recording bytes were **not independently rehashed in this phase**.

Existing helpers only were used, without installation, signing or permission changes. Diagnostics ended and music apps remained. Private identifiers, screenshots and machine-specific details are excluded. This documentation publication did not operate or retest a device.
