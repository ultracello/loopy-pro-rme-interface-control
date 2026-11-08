# Module status

Snapshot: **2026-11-08**. The repository currently ships documentation and templates only.

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

## Promotion rule

Promote a hardware status only when a completed [device profile](../templates/device-profile.md) and test report meet [the acceptance gates](ACCEPTANCE.md). If only one control passed, promote only that control for that profile and revision. Keep failed and not-run cases visible.

The [module registry](../verification/module-status.json) is the machine-readable counterpart. Keep it synchronized with this page. Do not backfill evidence from unrelated or inaccessible experiments.
