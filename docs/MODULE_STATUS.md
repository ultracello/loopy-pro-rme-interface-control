# Module status

Snapshot: **2026-11-09**. The repository ships documentation, templates and a software-tested browser-only planning website. It does not ship an executable hardware-control module or a validated installable device profile.

## Status meanings

- **Planned:** desired behavior only.
- **Implemented:** source exists in this repository; no test pass implied.
- **Software tested:** a stated revision passed a recorded software test.
- **Hardware verified:** an exact device/version/profile passed recorded end-to-end tests.
- **Blocked:** a specific required dependency or capability is missing.

Apply each status to its exact scope. A browser preview can pass software tests while its hardware counterpart remains unverified.

| Module ID | Requested control | Shipped implementation | Hardware profile |
|---|---|---|---|
| `phones-fader` | Headphone level fader | None | None; unverified |
| `phones-steps` | Headphone level up/down | None | None; unverified |
| `phones-mute` | Headphone mute/unmute | None | None; unverified |
| `main-fader` | Main-output level fader | None | None; unverified |
| `main-steps` | Main-output level up/down | None | None; unverified |
| `main-mute` | Main-output mute/unmute | None | None; unverified |

Exact dB steps require a verified mapping and measured behavior, not an assumed conversion from a MIDI increment. A simulated range does not establish hardware bounds or safe monitoring levels. Input gain, pan, additional mixer functions and iPhone control need separate research.

## Scoped development observations

The [passive iPad reception milestone](milestones/2026-11-08-passive-ipad-reception.md) records complete Babyface messages reaching MidiFire and the existing Loopy StreamByter input monitor through a temporary return path. The output monitor remained empty during that check. Existing TotalMix traffic supplied the samples; no new Loopy query or gain/mute test was executed.

That observation advances reception evidence only. The [same-day READ follow-up](milestones/2026-11-08-loopy-read-ready-locked.md) adds one query/readiness result: READY / LOCKED with complete replies and unchanged observed levels, while TotalMix remained running in the background. No new gain/mute/fader behavior was tested.

Neither observation promotes any of the six hardware modules above. Raw captures, exact versions and a ready-to-install receive setup are not included. The planning website's software-test status is likewise separate from hardware-module status.

The [project overview](PROJECT_OVERVIEW.md#what-the-evidence-currently-supports) separately records earlier maintainer-reported iPad step/mute experiments and a limited iPhone command followed by a feedback failure. Earlier prototype observations are not validation of a later receiver/decoder, and they do not supply the missing release profiles.

### Later scoped step and display results

- [Filtered reception and Phones step/restore](milestones/2026-11-08-phones-step-restore.md): three native READ checks, one paired raw-unit reduction and exact restore with Main unchanged. No new mute or acoustic test.
- [Native fader display](milestones/2026-11-08-native-fader-display.md): actual levels reached the visible Loopy sliders through UI-only feedback. The triggering query came from a helper, and no hardware-writing fader was tested in that checkpoint.

These observations advance the development evidence without releasing any implementation in the table above. The [later v09 Phones-fader report](milestones/2026-11-08-phones-fader-write-restore.md) adds one bounded native write and exact restore at mapped −10.5/−11.0 dB with Main unchanged. That checkpoint advanced Phones-fader evidence only; it did not cover full-range writes, native/custom mute semantics, other selectable step sizes, stereo Main or longer/reload/reconnect behavior. Later tests are listed below. A selectable step-size UI must not advertise unvalidated hardware values.

### Native step-selection simulation

A [later send-free Loopy widget simulation](milestones/2026-11-08-native-step-simulation.md) checked five 0.5/1/2/3/6-dB choices, both directions, inert startup, unknown-default inactivity and reload. The separate StreamByter preview compiled and passed reported offline tests, but its commands were not exercised at native runtime. No real sender or larger physical step was tested. This advances UI-simulation evidence only and does not promote a step module.

### v09b3 follow-up-read checkpoint

The [9 November v09b3 test](milestones/2026-11-09-phones-v09b3-follow-up.md) adds one paired Phones reduction/restore after more than 75 seconds of transport runtime. Both channels followed −10.5 → −11.0 → −10.5 dB. Automatic follow-up queries at 101/100 ms and separate device queries confirmed the operations; StreamByter showed BEREIT / AKTIV. Main stayed at −8.0 dB and the original project/scene were restored. This is bounded feedback evidence, not full-range, long-duration or general live validation. No module status above is promoted.

### Main/Phones steps and gain-mute

The [later 9 November checkpoint](milestones/2026-11-09-main-phones-steps-gain-mute.md) advances paired Phones and stereo Main step-button evidence: 0.5 / 1 / 2 / 3 / 6 dB reductions with exact restoration, each leaving the other group unchanged. XLR2 was checked separately. One gain-mute/restore toggle per group and the following 0.5-dB checks passed. Complete code and 22 button actions were verified in the saved candidate. Original project/scene restoration and diagnostic cleanup were reported complete.

Gain-mute is level reduction with a saved restore value, not a verified hardware mute bit. That checkpoint did not test confirmed button feedback, free faders or pause/reconnection safety. The later fader/gate result is listed below. The table describes **publicly shipped modules/profiles** and therefore remains unverified: no native artifact or reproducible public profile is released here. Older checkpoints above describe their historical limits, not the latest overall test coverage.

### Sync LIVE1 native faders and activation gates

The [later Sync LIVE1 result](milestones/2026-11-09-live-faders-startup-gates.md) confirmed correct current values after three project starts without first touching the faders. Main and Phones were each reduced/increased by native fader and independently restored exactly, with the other group unchanged. Transport stop locked control; a missing return path prevented activation, including in the write-enabled candidate. Restoring the return input left output values unchanged. The tested copy was saved and originals restored.

This advances bounded native-fader and specific gate evidence, not full-range or complete lifecycle validation. Auxiliary displays, gain-mute lifecycle, physical USB reconnect and duration checks remain open. Public hardware-module/profile status remains unchanged because no reproducible native package is released here.

## Promotion rule

Promote a hardware status only when a completed [device profile](../templates/device-profile.md) and test report meet [the acceptance gates](ACCEPTANCE.md). If only one control passed, promote only that control for that profile and revision. Keep failed and not-run cases visible.

The [module registry](../verification/module-status.json) is the machine-readable counterpart. Keep it synchronized with this page. Do not backfill evidence from unrelated or inaccessible experiments.
