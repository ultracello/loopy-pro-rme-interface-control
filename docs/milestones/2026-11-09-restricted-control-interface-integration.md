# Restricted Main/Phones control and same-project Interface integration

Date: **9 November 2026 (UTC)**. Evidence: project-reported, bounded native iPad/Babyface Pro FS observations. These are two distinct saved working copies using the same Restricted LIVE1 rule revision. **No general live approval, complete TotalMix implementation, or installable integration for other users is released.**

Current controller rule SHA-256: `6d1149cc2e798d3de28426d658b28945af1f671cf8d67493c2ea86635b4639b7`.

## Separate control copy

The separate restricted Main/Phones copy was tested on the Babyface with paired −0.5 dB and +0.5 dB steps and small native fader movements. Fresh hardware-state readback confirmed each direction. The other output group remained unchanged throughout each group's test, and the current-session baseline was restored exactly.

| Output group | Half-dB step sequence | Fader sequence, including exact return | Other group |
|---|---|---|---|
| Main stereo | −8.0 → −8.5 → −8.0 dB | −8.0 → −9.5 → −9.0 → −8.0 dB | Unchanged |
| Phones stereo | −10.5 → −11.0 → −10.5 dB | −10.5 → −12.0 → −11.5 → −10.5 dB | Unchanged |

These are mapped device/display values, not a new acoustic calibration, full-range test or validation of arbitrary/rapid step sequences. The other step sizes were not all repeated in this restricted native run. Older tests retain their own rule revisions and boundaries.

## Same-project integration

A separate copy of the existing test project now contains an **Interface** page. Its existing audio objects, master, loop placement and media were preserved. The legacy MIDI controls were replaced by explicit mapped bindings around one existing StreamByter instance and the restricted MidiFire route.

Native checks on this integration copy confirmed:

- The Loopy **READ/LESEN** widget obtained the complete device state through the prepared MidiFire return path, and both displayed faders matched the fresh Main/Phones values.
- The successful read used a running Loopy transport. The preceding stopped-transport read produced no complete reply; this copy must not treat its cached display as a new hardware observation.
- **Return to music / lock** issued LOCK and showed the music page of the same project. It was checked with stopped transport and with transport running; the running transport continued.

No new output-gain or mute action was performed for this integration check. The separate copy's gain tests above must not be relabeled as new gain-write tests on this remapped composition. A running transport and unchanged loop objects do not prove acoustic continuity of an actually playing loop.

The combined MidiFire scene preserved the previous seven-module configuration and appended the separately reviewed restricted route. Loading a scene restarts its transient timer state; unchanged scene configuration does not mean an in-progress timer was continued.

## Current restrictions and restored state

**Gain-mute and the old saved-level restore path are blocked in this Restricted revision; their action buttons were removed.** Earlier bounded gain-mute observations are historical evidence, not permission to use the current copy as an interruption-safe mute controller.

Silent USB/receiver loss or replacement and crash-safe automatic restoration remain **unproven**. No physical USB reconnect, endurance, complete F-01–F-12 pass, complete TotalMix coverage or full live release is claimed here.

After both bounded checks, the original project and previous MidiFire scene were restored. After the integration check, the original's four central project files were checked byte-for-byte against the saved baseline. The temporary helper and diagnostic processes were stopped, local diagnostic ports closed and temporary access retired.

## Reproducibility boundary

The exact saved native copies, scene, binding map, captures and before/after records are retained privately with content checksums. The rule SHA above pins the common control revision. This report publishes the tested sequences, provenance distinction and limits; it does **not** include an independently rerunnable public native package, device profile, original project, audio recording, controller source or new license grant. Exact public installation/version/firmware requirements remain part of a future reviewed profile.

The [module registry](../../verification/module-status.json) keeps public shipped-profile status separate from these scoped observations. [Acceptance gates](../ACCEPTANCE.md) still apply.
