# Development and test setup

This document separates the tools used to develop and inspect an iPad workflow from what a musician would need to use a future released module. It is a reproducibility guide, not a promise that the current repository already automates a device.

## Reported development background

The [project overview](PROJECT_OVERVIEW.md) records the reported development equipment and prototype approach: iPad Pro 11-inch M4, Babyface Pro FS in class-compliant mode, Loopy Pro/StreamByter, MidiFire, TotalMix FX, a Belkin WCZ002 adapter and a Mac used for development/testing. Appium and WebDriverAgent/XCTest have been involved in Mac-based UI testing.

This background is not a complete versioned device profile or proof that every item was present in every checkpoint. Do not infer current running services, USB/WLAN automation transport, a permanent Mac/TotalMix dependency, or a validated shopping list. The version and reproducibility gaps below remain open.

## Three different kinds of connection

| Connection | Purpose | What it does not prove |
|---|---|---|
| Mac to iPad developer/test connection | Inspect and operate the test app UI | A supported Loopy-to-RME control protocol |
| Loopy/control bridge to RME | Send commands and receive state | Correct audio routing or audible output |
| iPad/audio host to RME audio interface | Carry audio | MIDI/OSC mixer-control support |

Record each path independently. A USB cable used for audio is not evidence of a USB automation connection. A network UI session is not evidence that the audio interface itself is remotely controlled over Wi-Fi.

## Developer tooling roles

- **Mac and Xcode:** host-side development and real-device provisioning/build tools. A device automation setup needs its own compatible toolchain and authorized device pairing.
- **Appium with the XCUITest driver:** a possible test-session and command layer on the host. It is distinct from the app under test.
- **WebDriverAgent (WDA):** the device-side automation server used by the XCUITest driver. It uses Apple's XCTest automation APIs for UI actions and inspection.
- **XCTest / XCUITest:** Apple's testing facilities behind that native UI automation. They do not implement TotalMix's audio or MIDI protocol.
- **Screen sharing or another remote desktop tool:** may let a developer view or operate the Mac. It is an additional access layer, not an RME control protocol. Do not list any particular remote-access product as required without evidence.

A typical documented architecture is test client → Appium/XCUITest driver on the Mac → WDA/XCTest on the iPad → app UI. Direct use of an already-running WDA is a different arrangement and must be identified explicitly; do not infer that an Appium server is running merely because WDA is available.

Sources: [Appium driver architecture](https://appium.github.io/appium-xcuitest-driver/latest/overview/), [device preparation](https://appium.github.io/appium-xcuitest-driver/latest/getting-started/device-setup/), and [WebDriverAgent](https://github.com/appium/WebDriverAgent). Exact compatibility and setup vary with tool and OS versions. Follow current upstream documentation rather than copying old commands blindly.

## Recorded passive-reception checkpoint

The [8 November 2026 milestone](milestones/2026-11-08-passive-ipad-reception.md) documents a narrow result recorded on 8 November 2026: Babyface Port 2 → a fresh MidiFire Event Monitor, temporarily extended through virtual MidiFire 1 to the existing Loopy StreamByter input monitor. Full messages were observed using existing TotalMix traffic; the Loopy output monitor was empty during the check. The original scene was restored and temporary remote-control services were shut down afterwards.

This supplies a scoped control-return-path observation, not a complete inventory. The package does not identify exact OS/app/tool versions, automation transport or a reusable automation script. Do not infer an active Appium/WDA service, a permanent TotalMix requirement, or a hostless end-user setup from it.

## Subsequent READ checkpoint

The [same-day READ follow-up](milestones/2026-11-08-loopy-read-ready-locked.md) used the existing v06 controls and that return path. One fixed Loopy request and complete replies produced READY / LOCKED; clock stop returned READ / LOCKED. The three-block scene was saved natively, with no portable MFR export yet. The Mac handled UI automation and passive observation, not MIDI relaying. TotalMix remained running in the background.

That is a scoped state-query/readiness result. It does not validate new gain/mute/fader behavior or operation with TotalMix terminated, and it does not supply the missing versioned inventory.

## Later receive filter and native display checkpoints

The [filtered-receive test](milestones/2026-11-08-phones-step-restore.md) passed only complete valid state frames through a separate MidiFire return scene while leaving existing Loopy v06 gates unchanged. Three native READs and one paired Phones step/restore were observed. The original scene was restored afterwards; it intentionally does not retain that test return route.

A different [state-to-UI scene](milestones/2026-11-08-native-fader-display.md) decoded complete states into virtual CCs and automatically updated visible Loopy sliders. It had no hardware output or write SysEx. Its query was triggered by a temporary helper; its data return ran directly on iPad without a Mac MIDI relay. The native display setup, receive-only raw-state filter and existing Loopy command path must not be presented as one already packaged installation.

Both scenes were saved separately. No portable, fully versioned release is supplied. These results do not establish operation with TotalMix terminated or complete independence from the development setup.

## Main/Phones step-button and gain-mute checkpoint

The [later 9 November tests](milestones/2026-11-09-main-phones-steps-gain-mute.md) checked XLR2 independently, five physical step sizes for each stereo output group, and one gain-mute/restore toggle per group. The saved candidate's complete code and 22 button actions, including a separate AU-state resource, were checked. This is not a complete reload/recovery or portability test, and no native artifact is released here.

Gain-mute is a level-based method; native mute bits and button-state feedback are not verified. The candidate still requires READ → ARM and clearing its own gain-mute before lock/transport stop. Pause and connection-change safety, free faders and a complete end-user setup remain unverified. Original project/scene restoration and diagnostic cleanup were completed after the reported tests.

## v09b3 automatic follow-up-read checkpoint

The [9 November v09b3 test](milestones/2026-11-09-phones-v09b3-follow-up.md) passed one paired Phones half-dB reduction and exact restoration after more than 75 seconds of transport runtime. Automatic follow-up queries after 101/100 ms received successful replies; separate device queries confirmed both operations. Main remained −8.0 dB and original project/scene restoration was verified. This does not validate a complete end-user installation, arbitrary gestures, reconnect or extended operation. The public report contains no native project or new setup procedure.

## Bounded native Phones-fader follow-up

The [later v09 TEST checkpoint](milestones/2026-11-08-phones-fader-write-restore.md) separated read display, a diagnostic gesture with sending disabled, and one native Phones reduction/restore. Both Phones values returned to their fresh baseline; Main remained unchanged. The original project and scene were restored. The candidate was restricted to Phones and one raw step, without Main/mute/legacy writes.

This phase verified iPadOS 27.2 / build 24B119. The report records rule hashes and reported offline checks, but current firmware and all app versions were not inventoried again. No full-range, long-running, reconnect, native-step-selector or new mute claim follows. Portable test material was described by the test owner but is not reviewed or shipped by this documentation update.

## Separate send-free step-selection simulation

The [later step-selector checkpoint](milestones/2026-11-08-native-step-simulation.md) contains two independent evidence layers: an offline/no-SND StreamByter preview with native compilation, and a native Loopy-only widget simulation. The preview commands were not driven into StreamByter at native runtime. The actual widget simulation used only internal actions, with empty MIDI destinations and no SendMIDI bindings.

Its five preset choices and persistence checks do not establish a native sender connection or larger hardware steps. The original Loopy project was restored; MidiFire scenes and routes were untouched. Do not combine these results into an end-to-end MIDI test.

## Complete current project profile: not yet published

A reproducible current test-session inventory has not been published in this repository. Historical use of Appium/WDA/XCTest in another iPad test workflow must not be treated as proof that the same services, transport or versions are active for this project now. This page does not claim that any remote-control service is currently running.

The following are deliberately **not yet specified as a reproducible current profile**:

- Complete host/device/tool version inventory. Only the iPadOS version explicitly recorded for the later v09 test is current evidence here; Mac/Xcode, firmware and music-app versions still need a dated full inventory.
- Appium, XCUITest driver and WDA versions, and which processes are currently running.
- Current USB versus WLAN automation transport, and whether tunnelling/forwarding is used.
- Complete physical audio/MIDI topology and required released control bridge; only the scoped return paths, READ/step and native-display observations above have been reported.
- Role and current use of any additional remote-access software.

A project test rig can be paused or reconfigured. Every observation needs a timestamp and an explicit historical/current label. Do not publish account names, device identifiers, IP addresses, session IDs, signing assets or credentials to make this section more specific.

## End-user requirements

**There is no validated minimal end-user setup yet**, because no executable hardware profile is shipped here. The intended module prerequisites will be Loopy Pro, a supported RME device and the exact control route required by its verified profile. A desktop-host route may require a Mac/PC; a hostless route must be independently proven.

Appium, WDA and Xcode are development/test tools. They are not established end-user requirements for this project. Do not ask a musician to install them merely to use a future Loopy control. Conversely, do not promise that no computer or bridge is needed until a hostless profile passes.

## Reproduce work without the original maintainer

1. Choose documentation review, software-only testing or a device test. Documentation contributions need only this repository and a text editor; no Mac/iPad automation is required.
2. For a device test, fill in the version/topology inventory in [the device-profile template](../templates/device-profile.md), using generic identifiers in public examples.
3. Prepare a separate test project and reviewed procedure. Define safe monitoring, a stop condition and how to restore the working copy. Do not modify a working production setup incidentally.
4. Set up only the automation tools actually needed. Use your own authorized device, signing and pairing. Security-sensitive permissions and persistent access must be handled deliberately; this document does not authorize changes to someone else's device.
5. Verify transport and UI inspection first. Do not treat this as a successful MIDI command or audio test.
6. Run the chosen case for one output. Record UI state, device state and audible/measurement result separately. Keep mute independent from level.
7. Test startup, stale state, disconnection, reconnection and state changes made outside the UI where applicable.
8. Save the exact code revision, version inventory, sanitized procedure and results. Label failed, blocked and not-run cases. End test sessions and release the device when the run is complete.
9. Submit a sanitized [test report](../templates/test-report.md) or draft pull request. A finding on one rig is not universal compatibility.

Automated tests and reproducible fixtures for this rig are not shipped in the repository yet. Contributors can help by supplying a reviewed, sanitized setup recipe and exact evidence, rather than undocumented claims or machine-specific scripts.
