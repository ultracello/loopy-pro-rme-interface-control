# Passive iPad reception milestone

Date: **8 November 2026**. Evidence level: **project-reported, scoped device observation**. This report records the development session's monitor observations; it is not an independently repeated test or a released hardware-control profile.

**Later follow-up:** a [same-day Loopy READ test](2026-11-08-loopy-read-ready-locked.md) subsequently reached READY / LOCKED. The report below preserves the earlier passive checkpoint; its unexecuted-query statements describe that earlier test, not the later result.

## What was observed

- After a user-performed USB reconnect, TotalMix again reported the Babyface Pro connected, and both Babyface MIDI ports were present. The app's reported device name does not establish an exact model/firmware profile.
- A fresh native MidiFire scene containing only a Babyface Port 2 input and an Event Monitor received complete 227-byte state messages and 207-byte meter messages, with sub-IDs 00/01/02 observed.
- A temporary extension from that monitor to the virtual MidiFire 1 output passed complete 227/207/207 messages into the existing StreamByter AU input monitor in Loopy Pro. The Loopy output monitor remained empty during this passive check.
- No existing Loopy rule, widget assignment, or Loopy audio/MIDI routing was edited. No TotalMix setting, output gain or mute was changed. No audio clip or transport was started. Diagnostic captures used `requestState=false`.
- The original MidiFire scene was restored, Loopy's clip and transport remained stopped, and temporary remote-control services were shut down.

This establishes a scoped passive return-path observation. Complete message reception does not by itself verify decoded gain/mute state, fader behavior, a write acknowledgment or a safe control loop. An empty output monitor describes the observed interval, not a universal no-echo guarantee.

## Observed path and reproduction outline

The two observed configurations were:

1. **Babyface Port 2 input → MidiFire Event Monitor.** This two-block scene was saved natively in the development session.
2. **Babyface Port 2 input → MidiFire Event Monitor → virtual MidiFire 1 destination → existing Loopy Pro StreamByter AU input monitor.** This temporary return path was observed and recorded, but was not exported as a ready-to-install release.

For a separately reviewed reproduction on an authorized test setup:

1. Back up the current MidiFire scene. Use an isolated temporary scene with a fresh Babyface Port 2 source connected to an Event Monitor.
2. With the existing TotalMix device communication available, inspect the detailed monitor log for complete 227/207/207 messages. The small block summary alone is insufficient to establish message loss.
3. For the return-path check, add only the virtual MidiFire 1 destination after the monitor. Do not add a Babyface hardware destination in MidiFire.
4. Keep the existing Loopy control locked, with clip and transport stopped. Inspect its StreamByter input and output monitors, then restore the original MidiFire scene.

This outline depends on an existing reviewed Loopy receiver/control setup that is **not distributed here**. It is not a standalone installation guide. Do not substitute an arbitrary MIDI binding or feedback path: that could send unintended hardware commands. Preserve the working project and use the [hardware acceptance gates](../ACCEPTANCE.md).

## Limits and untested behavior

- These passive samples used **existing TotalMix traffic**. They prove neither a permanent TotalMix dependency nor independent Loopy-only operation.
- No new Loopy state query or clock start was executed during this passive check. Decoder readiness following a new query and new volume/mute behavior remain untested.
- The earlier unexpected disconnect has no identified cause. Reconnection recovered detection, but the observation does not establish a general hardware or software defect. These were discrete checks, not continuous monitoring or a reconnect endurance test.
- Exact interface variant, firmware, iPadOS and app/plugin versions are not supplied in this milestone package. Neither is a reproducible automation-tool inventory or the original raw monitor capture. Those gaps prevent promotion to a release-ready device profile.
- Stereo main-output control, working hardware faders, native TotalMix mute synchronization and iPhone compatibility are not verified by this result.

## Proposed next test, not a completed result

A separately approved read-only check would preserve the scene, use the verified temporary receive path, keep the audio clip and metronome off, start the clock only, and invoke the existing READ widget once with the fixed state request `F0 00 20 0D 10 10 F7`. It would then check the reply and locked-ready state, stop the clock and restore the original scene.

Do not arm the controller, change gain/mute or add routing changes to that test. This is a bounded proposal for the existing reviewed test setup, not permission to operate another person's hardware or an executable module release.

## Evidence and publication boundary

This public summary was prepared from the development session's sanitized English checkpoint report. Private working projects, monitor captures, machine identifiers, local paths, network details and remote-control credentials are not included. The documentation update did not rerun a device test.

The milestone advances passive reception evidence. It does **not** claim that the full live-control target is complete. See [module status](../MODULE_STATUS.md) for release boundaries.
