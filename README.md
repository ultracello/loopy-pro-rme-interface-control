# Loopy Pro Interface Control

Reusable controls for RME audio interfaces from Loopy Pro, with device-specific MIDI paths and TotalMix behavior documented separately.

**Independent software. Not affiliated with RME.**

**Status: research and early development.** This repository publishes documentation, contribution templates and a browser-only planning configurator. It does not yet contain a released hardware-control module, an importable Loopy Pro project, or a reproducible hardware-validation package.

## Why control an interface from Loopy?

Keep main/headphone controls within reach beside the looping controls, without switching apps or reaching down to an interface. The aim is reusable controls that fit into an existing Loopy project while preserving its audio routing.

An ordinary Loopy audio fader changes the signal in Loopy. Interface output level, preamp gain and an independently routed hardware direct-monitor mix are different parameters. This project investigates device-specific controls for those hardware functions, starting with outputs. Input gain and hardware-monitor mix controls still need separate implementation and tests.

The intended path uses model-specific USB MIDI/SysEx with StreamByter processing and a MidiFire return path. It does not assume that TotalMix FX for iPad accepts desktop Mackie Control or OSC commands. Reliable operation with TotalMix closed, a complete iPhone-only setup and a validated minimum end-user setup remain unproven.

Read the [project overview](docs/PROJECT_OVERVIEW.md) for signal-path examples, iPad/iPhone/Mac roles, effects limitations, earlier prototype results and ways to contribute. Loopy also documents device-dependent hardware-gain controls; this project does not establish whether those support a particular Babyface setup.

## Planning website

The [public planning website](https://ultracello.github.io/loopy-pro-rme-interface-control/) and its [source](website/) let visitors select desired controls, preview a local-only surface and export a setup brief. It sends no MIDI, OSC or audio and is not a tested hardware controller. See [website setup and privacy](website/README.md) and the repository's **Build and deploy planning website** Actions workflow for deployment status.

## Latest development milestones

The [read-path and reply-loss checkpoint](docs/milestones/2026-11-09-read-paths-reply-loss-lock.md) observed complete state and meter replies through both prepared read paths using the same persistent receiver. In a **gain-disabled diagnostic copy**, a suppressed return input blocked activation; restoring it required a new complete read followed by explicit activation. All four output values stayed unchanged, and the original project/scene were restored.

The sporadic USB/hub failure and historical missing-prefix cause were **not resolved**. Safe gain-mute restore across interruptions and the complete proposed F-01–F-12 regression remain open. This result does not establish a finished product or general live approval.

The [Sync LIVE1 fader checkpoint](docs/milestones/2026-11-09-live-faders-startup-gates.md) confirmed correct current values after **three project starts without touching a fader first**. Main and Phones were each reduced and increased with the native fader, independently checked and restored exactly; the other output group stayed unchanged. **Transport stop locked the controls; a missing return path prevented activation.** The tested copy was saved and the original project/scene restored.

These are bounded fader and activation-gate results. Auxiliary displays, gain-mute lifecycle, physical USB reconnect and duration checks remain open. No full-range or complete live approval is claimed.

The [latest Main/Phones checkpoint](docs/milestones/2026-11-09-main-phones-steps-gain-mute.md) tested **0.5 / 1 / 2 / 3 / 6 dB reduction-and-restoration pairs on both stereo output groups**. Phones tests left Main unchanged; stereo Main tests left Phones unchanged. XLR2 was verified separately first. A **gain-mute/restore toggle per group** recovered its saved level, and the following 0.5-dB checks passed. The saved combined candidate's code and 22 button actions were checked; original project and scene were restored.

Gain-mute uses level reduction, **not a verified hardware mute bit**. The later fader checkpoint advances native-fader and activation-gate evidence; auxiliary feedback, gain-mute lifecycle and USB reconnect/duration behavior remain open. This is scoped device evidence, not a full live release or a public installable package.

The [9 November v09b3 checkpoint](docs/milestones/2026-11-09-phones-v09b3-follow-up.md) passed one paired Phones reduction and exact restoration, **−10.5 → −11.0 → −10.5 dB**, after more than 75 seconds of transport runtime. Automatic follow-up queries after **101/100 ms** received successful replies; separate device queries confirmed both operations. StreamByter showed BEREIT / AKTIV, Main stayed at −8.0 dB, and the original project and scene were restored. This is a bounded result, not a general live release or long-duration validation.

The [bounded native Phones-fader test](docs/milestones/2026-11-08-phones-fader-write-restore.md) now records both headphone channels changing **−10.5 → −11.0 → −10.5 dB**, with fresh complete readback before restoration and Main unchanged. These are mapped device/display values, not a new acoustic measurement. The original project and scene were restored.

A later [native step-selection simulation](docs/milestones/2026-11-08-native-step-simulation.md) checked 0.5 / 1 / 2 / 3 / 6 dB choices, both directions, inert startup and reload using only internal Loopy widgets. It sent no MIDI and did not test larger real steps or the native sender connection.

The preceding [filtered receive/step test](docs/milestones/2026-11-08-phones-step-restore.md) and [automatic native fader display](docs/milestones/2026-11-08-native-fader-display.md) remain separate checkpoints. See the [mapping evidence](docs/protocol/output-gain-evidence.md) for the raw-unit/dB distinction.

The checkpoints remain scoped to their own revisions. Bounded native faders, physical step buttons and gain-mute/restore now have separate device observations. Full-range behavior, auxiliary feedback, mute lifecycle, USB reconnect/duration behavior, TotalMix independence and a complete installable profile remain unverified.

The [earlier READ report](docs/milestones/2026-11-08-loopy-read-ready-locked.md) and [passive report](docs/milestones/2026-11-08-passive-ipad-reception.md) remain dated historical evidence, with forward links to later tests.

## The goal

Make useful interface controls easy to add to an existing Loopy Pro project, without rebuilding its audio routing:

- Independent headphone and main-output volume controls.
- Volume up/down buttons with selectable, profile-verified step sizes.
- Continuous faders.
- Separate mute/unmute toggles.
- Feedback showing actual device state, with safe startup and reconnection.
- A simple, complete setup guide for each verified hardware/software combination.

The initial research focus is RME Babyface Pro / Babyface Pro FS workflows with iPad. That is a development focus, not a compatibility claim for every model, firmware version, or connection. iPhone support is not confirmed.

## Current scope and verification

| Area | Status |
|---|---|
| Headphone/main-output step controls | Five physical reduction/restore sizes tested for paired Phones and stereo Main, with the other group unchanged; arbitrary sequences, lifecycle safety and a released profile remain unverified |
| Continuous faders | Three startup checks and bounded native Main/Phones writes with exact restoration passed; full range and complete lifecycle safety remain unverified |
| Independent mute/unmute | Gain-mute/restore tested per output group; native hardware mute bits, confirmed indicators and lifecycle safety remain unverified |
| Input gain, pan and additional mixer functions | Further research |
| iPhone workflow | Limited earlier prototype observation; complete workflow remains unverified |
| Installable module or tested device profile | Not published in this repository yet |

A private experiment or a working browser preview is not a general compatibility guarantee. Each released module needs its exact device model, firmware, software versions, transport, mappings and reproducible results.

Important distinctions:

- A level value does not prove whether an output is muted.
- A MIDI increment is not automatically an exact dB step.
- An input mixer fader is not necessarily microphone-preamp gain.
- A control should obtain the current device state before applying a stored value, so loading a project does not cause an unintended level jump.
- A headphone test does not verify the main output, and an iPad test does not verify iPhone.

## Interface control and TotalMix

The intended target is the RME interface's supported mixer functions. A direct device-control path and remote control of TotalMix software are different approaches.

- **Direct interface control:** must be established for the exact RME model, firmware, operating mode and MIDI/control transport.
- **Desktop TotalMix FX:** RME documents remote-control options, but a particular Loopy-to-host workflow still needs end-to-end verification.
- **TotalMix FX for iPad:** RME's app description excludes MIDI/OSC and TCP/IP remote control. Do not assume desktop TotalMix remote instructions work with this app. This restriction does not establish whether a separate direct hardware path exists.
- **TotalMix Remote:** controls TotalMix on a host computer and is distinct from TotalMix FX for iPad.

USB audio support alone does not establish mixer-control support.

Official references:
- [RME TotalMix FX and TotalMix Remote](https://rme-audio.de/totalmix-fx.html)
- [RME's TotalMix FX for iPad description](https://apps.apple.com/us/app/totalmix-fx-for-ipad/id739965887)

## End-user setup versus development tools

A verified minimal end-user setup has not yet been published. It will depend on the released device profile. A desktop-host route may need a Mac/PC; a hostless route must be proven separately.

Mac-based testing for this project has involved Appium and WebDriverAgent/XCTest. Xcode supports the underlying development/provisioning toolchain. They are not established end-user requirements for these controls. UI automation, the MIDI/control connection and the audio connection must be documented separately, including whether each uses USB or a network.

Exact tool versions and a reproducible developer setup should accompany the corresponding test report. No machine-specific setup or automation script is included in this repository yet.

## Documentation

- [Purpose, control paths, platform requirements and current limits](docs/PROJECT_OVERVIEW.md)
- [Module status and evidence levels](docs/MODULE_STATUS.md)
- [Contributing](CONTRIBUTING.md)
- [Developer setup versus end-user requirements](docs/DEVELOPMENT_SETUP.md)
- [Planning website tests and browser checklist](docs/TESTING.md)
- [Read-path comparison and gain-disabled reply-loss gate](docs/milestones/2026-11-09-read-paths-reply-loss-lock.md)
- [Native fader startup, writes and activation gates](docs/milestones/2026-11-09-live-faders-startup-gates.md)
- [Main/Phones step sizes and gain-mute restoration](docs/milestones/2026-11-09-main-phones-steps-gain-mute.md)
- [v09b3 Phones test with automatic follow-up reads](docs/milestones/2026-11-09-phones-v09b3-follow-up.md)
- [Native step-selection simulation](docs/milestones/2026-11-08-native-step-simulation.md)
- [Bounded native Phones-fader write/restore](docs/milestones/2026-11-08-phones-fader-write-restore.md)
- [Output-gain mapping and tested points](docs/protocol/output-gain-evidence.md)
- [Earlier Phones step/restore milestone](docs/milestones/2026-11-08-phones-step-restore.md)
- [Native Loopy fader-display milestone](docs/milestones/2026-11-08-native-fader-display.md)
- [Earlier Loopy READ / READY / LOCKED milestone](docs/milestones/2026-11-08-loopy-read-ready-locked.md)
- [Earlier passive iPad reception milestone](docs/milestones/2026-11-08-passive-ipad-reception.md)
- [Hardware and release acceptance gates](docs/ACCEPTANCE.md)
- [Test-report template](templates/test-report.md) and [device-profile template](templates/device-profile.md)
- [Sources](docs/SOURCES.md) and [changelog](CHANGELOG.md)

The issue chooser provides forms for test reports and feature requests. These forms do not authorize a hardware test or establish compatibility.

## How to help

Use [Issues](https://github.com/ultracello/loopy-pro-rme-interface-control/issues) to suggest one concrete musical task, point out unclear documentation, or contribute a reproducible observation.

For a useful report, include:

1. Interface model, firmware, device/OS and app versions.
2. Intended control path and the specific output or function.
3. Exact steps, expected behavior and actual result.
4. What passed, failed, was blocked, or was not tested.
5. An official manual section or sanitized evidence where available.

Do not change a working project or routing just to produce a report. Hardware tests need a separate working copy, a reviewed procedure, safe monitoring and a clear stop/restore plan. Do not infer safe hardware values from a browser demo.

Issues and attachments are public. Do not post credentials, private messages, recordings, original working projects, device identifiers, or private network details.

## What unlocks a release

A control module needs a documented profile, verified mappings and feedback, independent-output tests, measured level behavior where relevant, reconnect/restart checks, and a novice-friendly installation and removal guide. Claims must stay within the tested profile and revision.

This repository is independent of RME and Loopy Pro. No software license has been selected yet, and no rights to third-party material are granted. Resolve licensing and attribution before incorporating or distributing code.

_Last reviewed: 9 November 2026._


