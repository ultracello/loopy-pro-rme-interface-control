# Loopy Pro RME Interface Control

Reusable controls for RME audio interfaces from Loopy Pro, with device-specific MIDI paths and TotalMix behavior documented separately.

**Status: research and early development.** This repository currently publishes the project overview. It does not yet contain a released control module, an importable Loopy Pro project, a runnable configurator, or a reproducible hardware-validation package.

## The goal

Make useful interface controls easy to add to an existing Loopy Pro project, without rebuilding its audio routing:

- Independent headphone and main-output volume controls.
- Volume up/down buttons.
- Continuous faders.
- Separate mute/unmute toggles.
- A simple, complete setup guide for each verified hardware/software combination.

The initial research focus is RME Babyface Pro / Babyface Pro FS workflows with iPad. That is a development focus, not a compatibility claim for every model, firmware version, or connection. iPhone support is not confirmed.

## Current scope and verification

| Area | Status |
|---|---|
| Headphone/main-output step controls | Under development; no validated release is published here |
| Continuous faders | Unconfirmed; require their own implementation and tests |
| Independent mute/unmute | Requires verified mute semantics and state feedback |
| Input gain, pan and additional mixer functions | Further research |
| iPhone workflow | Unconfirmed |
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

Mac-based tools such as Xcode, Appium, WebDriverAgent and XCTest can be part of a developer's iPad UI-testing setup. They are not established end-user requirements for these controls. UI automation, the MIDI/control connection and the audio connection must be documented separately, including whether each uses USB or a network.

Exact tool versions and a reproducible developer setup should accompany the corresponding test report. No machine-specific setup or automation script is included in this repository yet.

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

_Last reviewed: 8 November 2026._

