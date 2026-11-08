# Filtered state reception and one Phones step/restore

Date: **8 November 2026**. Evidence level: **project-reported, scoped native device and register/readback observation**. This extends the [earlier READ checkpoint](2026-11-08-loopy-read-ready-locked.md). It is not an independently repeated test, acoustic measurement or released control module.

**Later follow-up:** the [bounded native Phones-fader test](2026-11-08-phones-fader-write-restore.md) subsequently added one gesture-driven reduction/restore. The report below preserves the earlier fixed-button/filter checkpoint.

## Receive path and software checks

A separate receive-only MidiFire filter connected the verified Babyface Port 2 source to the existing virtual return output. There was one path, no loop and no hardware destination. Only complete valid **227-byte state frames** passed unchanged. The filter did not send, inject, clone, delay or repair message bytes. Existing Loopy v06 controls and their timing, lock and write gates remained unchanged.

- **Nine offline test groups and 1,265 packet cases** passed.
- A **3,200-short-message flood sequence** also passed.
- The full filter text was compiled natively in a separate saved MidiFire scene.
- Continuous short traffic was observed directly. **Three separate known Loopy READs**, including a read-only TotalMix foreground/return challenge, were each followed by a complete state and native **READY / LOCKED**.
- Short/meter traffic did not appear as new native input after this filter. All raw chunks within the bounded capture windows were retained in the development evidence.

These are reported test results. The filter source, fixtures and raw captures are not distributed with this report, so these counts are not a publicly rerunnable test suite.

## One controlled Phones step and exact restoration

After a further fresh full state and native **READY / ACTIVE**, exactly one existing Phones-minus step changed **both headphone channels by one encoded raw unit**. Both Main values stayed unchanged.

A further fresh full state confirmed the exact one-step target. Exactly one Phones-plus then restored the freshly saved baseline. The native output monitor showed only the **four expected Phones write packets**, with the known readback request 100 ms after each pair. The native state after minus was READY / ACTIVE. The workflow finished locked, with clip and clock stopped.

This confirms one paired Phones step and exact restoration in the observed register values. The [subsequently documented output mapping](../protocol/output-gain-evidence.md) supports calling one raw unit a mapped 0.5-dB step. Neither that formula nor the matching display is an independent acoustic measurement. No mute or audio test was performed.

## What remains unresolved

- Short-state messages were not promoted to write authorization. Initial short-state evidence was static, without a request nonce or device timestamp. Later short patterns matched full-state prefixes before and after the pair change, but independent left/right/Main variation and freshness correlation remain unproved.
- Effects of traffic reduction versus module/framing behavior were not isolated. Earlier loss before MidiFire is not claimed fixed.
- This is not a long-running test, a general disconnect fix, a complete regression pass or a finished live release.
- Other selectable step sizes, repeated step operation, hardware-writing faders, mute/toggles, stereo Main writes, external changes and reload/reconnect behavior need separate validation.
- TotalMix foreground/return handling is narrower than operation with TotalMix explicitly terminated. No TotalMix-independent profile is established here.

The [later native fader-display checkpoint](2026-11-08-native-fader-display.md) adds read-feedback evidence only; it does not turn this single step test into a hardware-fader test.

## End state and reproduction boundary

The original MidiFire scene was restored and the tested scene saved separately. Project routes, complete rules, widgets and recording matched before/after; TotalMix gain/mute/mono displays were preserved. Temporary remote services ended and music apps remained. No helper installation or permission/signing change was made.

The restored original scene intentionally lacks the Babyface return route. A future reviewed test must deliberately select the separately saved tested filter scene rather than assume it is still active. The filter is ordinary MidiFire code without a developer-helper runtime dependency; that fact alone does not validate a complete standalone end-user setup.

The public package does not include a portable scene, exact firmware/app/OS inventory or all source revisions. Reproduction and release require those artifacts plus the [hardware acceptance gates](../ACCEPTANCE.md). Private captures, screenshots and device/network identifiers are excluded. Publishing this report did not repeat a device test.
