# Purpose, control paths and current limits

Reviewed: **8 November 2026**. This is an independent community project, not an official RME or Loopy Pro product.

## Controls within reach during a performance

The goal is to make useful interface controls available beside the looping controls in Loopy Pro. When an interface is out of reach, a musician could adjust it without switching apps or reaching down to the hardware. Reusable controls could also fit into Loopy widgets, MIDI-controller mappings, actions and follow actions.

The first target is independent main-output and headphone control, while preserving existing audio routing: continuous faders, up/down buttons with verified selectable step sizes, separate mute/unmute controls, actual-device feedback and safe startup/reconnection. Loading a project must not unexpectedly restore an old output level.

Input gain, hardware-monitoring mix levels, pan and other mixer functions are later research areas. A minimal iPhone-and-interface setup, without an additional iPad or Mac, is also a goal. These are intended capabilities, not a released feature list.

## Different controls act at different points

Loopy's mixer and output routing already handle many software-mixing tasks. This project addresses parameters in the interface itself, including signals that may not pass through Loopy.

| Control | What it changes | What must not be inferred |
|---|---|---|
| Ordinary Loopy track/bus/output fader | The relevant signal level within Loopy's software audio path | It does not, by itself, send a device-specific preamp or hardware-mixer command |
| Microphone/instrument input gain | The interface's input amplification or sensitivity, depending on the input | It is not the same parameter as a Loopy or hardware-monitor mix fader |
| Hardware direct-monitor mix level | An input's contribution to a monitor mix routed inside the interface | An independently routed signal can bypass Loopy, so a Loopy audio fader need not change it |
| Interface output-master level | The addressed main/headphone output's level | Correct addressing, stereo behavior, feedback and independence require their own tests |
| Mute/restore | A particular implementation's silence and restoration behavior | A custom level-based mute/restore is not verified synchronization with TotalMix's native mute state |

For a microphone or guitar heard through direct monitoring, adjusting its hardware-monitor mix level can be useful without changing its preamp gain. Those two controls have different effects and must be implemented and tested separately. Neither input-control path is verified by this project's output-control experiments.

Loopy also documents a device-dependent Global Hardware Gain setting. Its availability is separate from software input gain, and support for a particular Babyface configuration has not been established here.

A custom Loopy widget can be assigned MIDI actions, but that is a separate mapping from an ordinary Loopy audio fader. Its existence does not establish a correct RME command or feedback loop. See the [Loopy Pro manual](https://loopypro.com/manual/) and the exact interface's manual before interpreting a control.

## The experimental MIDI path

The prototype approach investigates model-specific SysEx over USB MIDI:

- Command processing in Loopy Pro with StreamByter, directed to the Babyface's control MIDI port.
- A MidiFire return path for device messages, reaching the existing StreamByter input monitor in Loopy.
- TotalMix FX used for mixer configuration and inspection during development.

This is separate from using the TotalMix FX for iPad app as a Mackie Control or OSC receiver. The [passive reception milestone](milestones/2026-11-08-passive-ipad-reception.md) demonstrates only the scoped return-path observation described there. Its samples came from existing TotalMix traffic. A [subsequent Loopy READ test](milestones/2026-11-08-loopy-read-ready-locked.md) reached READY / LOCKED after one fixed query and complete replies, while TotalMix remained running in the background. Reliable operation with TotalMix terminated, robust polling, full decoded-state correctness and a complete control loop still need their own evidence.

USB audio compatibility alone does not establish mixer-control compatibility. A mapping for one interface, firmware or operating mode must not be assumed to work on another.

## TotalMix and platform dependencies

| Approach | Role and boundary |
|---|---|
| Direct interface communication | The approach under investigation; needs device-specific control and feedback validation |
| Desktop TotalMix FX remote control | Controls TotalMix running on a Mac or PC; it requires that host and its supported remote-control path |
| TotalMix Remote | A remote client for TotalMix on a host computer, not the directly connected hardware app |
| TotalMix FX for iPad | Controls supported hardware connected to an iPad; its product description excludes MIDI/OSC and TCP/IP remote control |

The directly connected TotalMix FX app is offered for iPad, not as an iPhone version. TotalMix Remote is a different product and does not turn a desktop-host route into an iPhone-only interface setup.

- **iPad:** the main development target. Scoped prototype observations exist; a reliable, installable profile is not released.
- **iPhone:** a limited historical command test exists, but the full workflow and corrected feedback path remain unverified. iPad results do not establish iPhone support.
- **Mac:** used for development and UI testing. That role is separate from a desktop TotalMix host. Neither a permanent Mac requirement nor Mac-free reliability has been established for a future released direct-control profile.
- **iPhone controlling another iPad:** a possible separate architecture for someone using both devices, but it would not meet the iPhone-and-interface-only goal. No such network/Bluetooth setup is verified here.

Read [the official RME overview](https://rme-audio.de/totalmix-fx.html) and [TotalMix FX for iPad's product description](https://apps.apple.com/us/app/totalmix-fx-for-ipad/id739965887). Do not copy desktop remote instructions into an iPad workflow without checking the actual receiver and protocol.

## Class-compliant mode and effects

This project controls functions that the interface actually provides. It does not add missing DSP or unlock desktop effects in class-compliant mode.

For Babyface Pro FS, RME distinguishes the hardware mixer, EQ and Low Cut from Reverb and Echo calculated on the computer in the desktop setup. RME's iPad app description also states that Reverb/Echo are unavailable for Babyface/Babyface Pro in iPad operation. Controlling a hardware mixer parameter therefore does not make those computer-calculated effects available on iPhone or iPad. This is a Babyface-specific distinction; other RME interfaces have different capabilities and need separate investigation.

The initial work concerns mixer/output controls, not adding Reverb/Echo. EQ and other functions also require their own implementation and tests. Consult [the official Babyface Pro FS manual, section 21.6](https://rme-audio.de/downloads/bface_pro_fs_e.pdf#page=54) for the device's DSP and class-compliant-mode limits.

## What the evidence currently supports

The following levels must remain separate. Earlier observations are maintainer-reported prototype results, not a new test run or a downloadable, reproducible release profile.

| Evidence | Result and limit |
|---|---|
| Earlier iPad prototype | Relative steps reported as 0.5 dB and custom mute/restore tested independently for XLR output 1 and stereo headphones; headphone channels addressed together. The first step after reloading and repeated state queries were also reported tested. This did not verify stereo main output, continuous hardware faders or native TotalMix mute synchronization. |
| Limited earlier iPhone test | Both headphone channels were lowered by a reported 0.5 dB, then a feedback error blocked further commands. The corrected setup still requires device testing; this is not a working iPhone-profile claim. |
| Passive iPad reception checkpoint, 8 November 2026 | Complete 227-byte state and 207-byte meter messages reached MidiFire and, temporarily, the existing Loopy StreamByter input monitor. The output monitor remained empty during that check. No new query, gain or mute test was part of it. |
| Loopy READ follow-up, 8 November 2026 | One fixed query was observed alongside complete 227/207/207-byte replies and READY / LOCKED; stopping clock returned READ / LOCKED. Observed levels were unchanged. TotalMix remained running in the background; no new gain/mute/fader test was performed. |
| Later filtered receive/Phones checkpoint | Three native READs passed, followed by one paired Phones-minus raw unit and exact restoration; Main unchanged. No mute or acoustic test. See the [scoped report](milestones/2026-11-08-phones-step-restore.md). |
| Native Loopy fader display | Actual Main/Phones levels automatically updated visible sliders after a helper-triggered query. UI-only decoder, no gain writes in this checkpoint. No hardware write occurred in this display checkpoint; see [report](milestones/2026-11-08-native-fader-display.md). |
| Bounded native Phones-fader write | Both channels −10.5 → −11.0 → −10.5 dB with fresh full readback before restore, Main unchanged. One mapped half-dB operation, not full-range or acoustic validation; see [report](milestones/2026-11-08-phones-fader-write-restore.md) and [mapping](protocol/output-gain-evidence.md). |
| Native step-selection simulation | Five 0.5/1/2/3/6-dB choices, both directions, inert startup and reload passed in send-free Loopy widgets. StreamByter preview compilation/offline checks were separate; no native preview runtime, real sender or larger physical steps were tested. See [report](milestones/2026-11-08-native-step-simulation.md). |
| Offline fader tests | Software checks exercise proposed logic. They do not verify native Loopy widget behavior or actual interface faders. |
| Public planning website | A software-tested browser-only layout planner and brief exporter. It sends no MIDI, OSC or audio and does not install controls. |

The earlier prototype state queries, passive-only checkpoint, READ follow-up, filtered Phones test, native display test, later bounded Phones-fader write and subsequent send-free widget simulation describe different tests. The early READ follow-up and fixed-button filter test used existing v06 controls. The later bounded native fader write used v09 TEST; neither is a released control package. Do not treat an earlier prototype pass as validation of the current receiver/decoder or a future build.

The [module registry](MODULE_STATUS.md) remains unverified for executable hardware releases. Exact firmware, OS/app/plugin versions, source revisions, sanitized artifacts, safe procedures and reproducible results are still needed. The [passive report](milestones/2026-11-08-passive-ipad-reception.md) and [READ follow-up](milestones/2026-11-08-loopy-read-ready-locked.md) each describe their evidence gaps explicitly.

## Selectable steps and release priorities

Selectable up/down sizes are a first-class goal, not a controller permanently fixed at the historical 0.5-dB setting. The available sizes must come from each validated device profile. The 0.5, 1, 2, 3 and 6 dB choices have now passed a [send-free native widget simulation](milestones/2026-11-08-native-step-simulation.md). Their connection to the actual sender and larger physical steps remain unverified. Supported-grid custom values have offline evidence only; neither result fixes the final native UI specification. The bounded mapped half-dB Phones operation does not validate an arbitrary list of hardware steps.

Before advertising a size, test both directions, fresh-state deltas, boundaries, repeated input, stereo pairing and existing balance offsets, unchanged other outputs, external changes and safe startup/reconnection. Faders additionally need no-jump/pickup behavior, bounded update rates and separation of automatic feedback from human write intent. Mute must be explicitly native or custom restore behavior, with unknown state retained when necessary.

## Development equipment versus a musician's setup

The reported development configuration includes an iPad Pro 11-inch M4, RME Babyface Pro FS in class-compliant mode, Loopy Pro, StreamByter, MidiFire, TotalMix FX, and a Belkin Connect USB-C Data + Charge Adapter (WCZ002). A Mac and AI-assisted development tools have supported development and testing.

This is background about the development work, not a universal compatibility list or a complete inventory for every test. It does not fill the missing version/profile fields in the passive milestone.

Mac-based UI testing has involved Appium and WebDriverAgent/XCTest. These are developer tools, not established requirements for musicians using a future finished module. Document the UI-testing connection, USB MIDI/control connection and audio connection separately. See [development setup](DEVELOPMENT_SETUP.md) for the roles and unknowns.

Product references: [StreamByter](https://www.audeonic.com/streambyter/), [MidiFire](https://www.audeonic.com/midifire/), and [Belkin WCZ002](https://www.belkin.com/hk/en/p/usb-c-data-charge-adapter/WCZ002btWH.html). Inclusion here is not a requirement to buy anything or proof that all configurations work.

## Contributing a useful next step

The immediate priorities are robust state/freshness handling, verified mappings and selectable dB behavior, independent output tests, full-range hardware-writing faders and mute semantics, safe reconnect/external-change handling, and reproducible iPad/iPhone profiles. Scoped read, step and display observations do not close those full acceptance gates. A release also needs installation and removal instructions that a non-programmer can follow.

Musicians, developers, testers and documentation contributors are welcome. Useful contributions include one concrete musical use case, an official protocol reference, a focused code review or a reproducible sanitized observation. AI-assisted work is welcome; technical claims still need source and device evidence. Other RME models require separate compatibility work.

Start with [the contribution guide](../CONTRIBUTING.md) and [Issues](https://github.com/ultracello/loopy-pro-rme-interface-control/issues). Use a separate test project and safe monitoring; do not alter an original working setup just to produce a report. Never publish private projects, recordings, credentials or device/network identifiers. Licensing for code contributions still needs to be agreed before a software release.
