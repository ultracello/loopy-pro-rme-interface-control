# Step selection: offline calculation and native widget simulation

Later checkpoint: [Main/Phones physical steps and gain-mute restoration](2026-11-09-main-phones-steps-gain-mute.md). This report keeps its original scope; the later tests do not retroactively validate this revision.

Date: **8 November 2026**. Evidence level: **project-reported offline checks and native Loopy widget-only simulation**. This follows the [bounded Phones-fader hardware test](2026-11-08-phones-fader-write-restore.md). It is not another hardware test and does not extend the observed physical change beyond that single mapped half-dB operation.

## 1. Exact-rule offline preview

A complete no-SND StreamByter preview accepted only synthetic balanced seeds and preview controls. It had no hardware query, sender, injection or message mutation; inputs were blocked. Its synthetic baseline never changed. Targets outside its conservative software domain were rejected as a pair. That domain is not a verified hardware range.

Reported source SHA-256: `071a4021a54f7b784b6f8cb3cfded54755118c7bfd54c13bbc894f6ea68ac06a`.

- **Six groups / 34,102 cases** passed, including all 127 supported custom half-dB magnitudes across every software-grid starting value and both directions.
- All five presets were compared with the separate exact-decimal parameter planner across the software grid.
- **1,792 additional independent malformed-after-selection regressions** and explicit preset-label checks were reported. Invalid channel-16 data cleared a prior step selection. Presets displayed dB; custom fallback labels identified half-dB units.
- A separate portable synthetic-only copy passed the same 34,102 cases. That is a repeated run of the same reported case set, not twice as many distinct cases.

The full no-SND source also compiled natively and its saved text matched the pinned source. **Its preview commands were not driven into StreamByter at native runtime in this phase.** The interpreter is not Audeonic's compiler, and successful compilation is not a runtime integration test.

The source, interpreter and portable tests are described in the development evidence but are not reviewed or distributed as executable artifacts by this documentation update. These counts are reported results, not a newly reproduced public test suite.

## 2. Separate native Loopy widget-only simulation

A silent test project offered five radio choices: **0.5 / 1 / 2 / 3 / 6 dB**. Each selected paired internal Plus and Minus stores. Buttons explicitly retriggered the selected store, nudging only a **simulated 128-step dB display**.

The native profiles contained only internal TriggerWidget actions. MIDI destinations were empty, there was no SendMIDI action, master was zero and tracks/clock were stopped. This arrangement did not connect the selector to the StreamByter preview or a hardware sender.

Ten native preset/direction cases passed from a simulated **−10.5 dB** baseline:

| Selected simulated step | Minus result | Plus result |
|---|---:|---:|
| 0.5 dB | −11.0 dB | −10.0 dB |
| 1 dB | −11.5 dB | −9.5 dB |
| 2 dB | −12.5 dB | −8.5 dB |
| 3 dB | −13.5 dB | −7.5 dB |
| 6 dB | −16.5 dB | −4.5 dB |

The visible radio choice and both internal stores agreed. These are **simulated display values**, not new Babyface output-level observations.

## Startup, invalid defaults and persistence

The first native test exposed a selection trap: retriggering a list with NoSelection selected and executed its first item, changing only the simulated display by half a dB. The corrected v3 used an explicit inert first item with no actions, followed by the five presets. Plus and Minus then remained inert until an explicit radio selection; that behavior was tested natively.

An unknown-default control had no action and did not change the simulated value. Saving, opening a different simulation and reloading v3 preserved the selected **6-dB step** and unchanged simulated baseline. Loading itself produced no adjustment. An explicit Plus then reached simulated −4.5 dB, and an internal Reset restored −10.5 dB.

That Reset is a **simulation reference reset**, not a discovered device factory default or a hardware restoration command. Observed native widget/project-format details apply to the tested Loopy build; they are not a stable external API.

## Limits

- This verifies native widget selection, dispatch, display and persistence in a **send-free simulation**. It does not verify native MIDI-backend integration.
- Native Loopy widget range handling is not the offline backend's pair-rejection policy. Their separate passes do not prove the combined system.
- No asymmetric pair, hardware boundary, device default, arbitrary physical gain, new mute operation or larger real step was tested.
- Connecting the selector to the real sender and validating larger physical steps remain open. The [earlier bounded hardware test](2026-11-08-phones-fader-write-restore.md) remains the hardware limit of this evidence.
- The displayed diagnostic controls are not a final live layout, and no portable-media or device-controller release is provided.

## End state

The original Loopy project was restored. Original database objects and controller profiles matched, including rules, routing, widgets and audio references. Recording audio bytes were not newly hashed. Original clip/transport remained stopped; MidiFire scenes and routes were not touched.

Temporary diagnostic services and the runner stopped, local diagnostic ports closed and music apps remained present. Screenshots, device records and native projects remain private. Publishing this report did not run a device test or expand the tested hardware range.
