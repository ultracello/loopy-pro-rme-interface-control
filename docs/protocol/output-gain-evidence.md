# Output-gain mapping and tested points

Reviewed: **9 November 2026**. Scope: the Babyface prototype's reported output-state mapping and its isolated test points. This is model-specific reverse-engineering evidence, not an official RME API or a general compatibility guarantee.

The primary [Babyface Pro protocol notes, Device State sub-ID 0](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro#device-state-sub-id-0), describe this output-volume conversion:

`dB = 6 + (raw - 0xFF) / 2`, equivalently `(raw - 243) / 2`.

| Raw value | Calculated display | Reported native observation |
|---|---:|---|
| 227 / 0xE3 | −8.0 dB | Main, unchanged during the bounded Phones test |
| 222 / 0xDE | −10.5 dB | Phones baseline and restored value |
| 221 / 0xDD | −11.0 dB | Phones after the bounded native fader gesture |

One raw unit corresponds to **0.5 dB in this mapping**. Complete state captures were reported to show both Phones fields changing 222 → 221 → 222, while the native outer-widget display matched the calculated values. See the [native fader test](../milestones/2026-11-08-phones-fader-write-restore.md).

The displayed scale itself uses this conversion. It is **not an independent acoustic calibration**, and no new analogue measurement was made. The earlier [fixed-button test](../milestones/2026-11-08-phones-step-restore.md) establishes a raw-unit change with exact restoration. The formula and separate display evidence support describing it as a **mapped 0.5-dB step**, not an acoustically measured 0.5-dB change.

The [9 November v09b3 checkpoint](../milestones/2026-11-09-phones-v09b3-follow-up.md) reports the same Phones display sequence, −10.5 → −11.0 → −10.5 dB, with Main at −8.0 dB. Its automatic follow-up and separate confirming reads add scoped feedback evidence; they do not expand the tested gain range or provide acoustic calibration.

## Receive-field and validity boundaries

Each 32-bit word is packed into five 7-bit bytes. After the six-byte header, word 1 bits 0–7 and 9–16 contain the mapped Main left/right fields; word 2 bits 14–21 and 23–30 contain Phones left/right. The current return filter accepts only complete valid **227-byte state frames**. RMS/peak messages, short states and malformed payloads do not refresh gain readiness.

Those field descriptions guide the candidate implementation. They do not establish that every possible device state, stereo mode or firmware variant has been decoded correctly. Unknown values and stale data must remain distinguishable from known gain and mute.

## Software bounds are not hardware specifications

The candidate's conservative raw bounds **116–243** map to **−63.5–0 dB**. The isolated native test points do not verify that full interval, a full-range native fader or the device's maximum hardware gain. The bounded write candidate allowed only channels 6/7 and one raw step; the [test report](../milestones/2026-11-08-phones-fader-write-restore.md) records its rule hashes and other restrictions.

No 0.1-dB output-master resolution, native mute bit, universal factory default or complete Babyface Pro FS/iOS compatibility follows from this mapping. The generic oscmix protocol documentation concerns another RME family; its register/mute mappings must not be substituted here.

This publication reviewed the sanitized mapping report and arithmetic. Original screenshots/captures and complete rules are not included or independently reproduced here. It is not a command recipe or permission to write to hardware.
