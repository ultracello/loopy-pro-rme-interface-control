# One native Phones fader reduction and restoration

Later checkpoint: [v09b3 on 9 November](2026-11-09-phones-v09b3-follow-up.md) adds automatic follow-up reads and separate confirmation. This historical report still describes v09 TEST only.

Date: **8 November 2026**. Device-test interval: **21:02:26–21:02:41 UTC**. Evidence level: **project-reported, scoped native device/register observation**. This advances the earlier [display-only checkpoint](2026-11-08-native-fader-display.md); it is not a full-range fader release or a live-safety guarantee.

**Later UI-only checkpoint:** [native step-selection simulation](2026-11-08-native-step-simulation.md) added five preset choices and persistence checks without MIDI sending. It does not expand the hardware test below.

## Display, human gesture and hardware write were tested separately

1. **Display:** a separate passive MidiFire scene branched the hardware input through a complete-state filter to one virtual return, and through a state-to-UI decoder to another. It had no hardware output or connected virtual feedback input. Actual device values updated the native outer Loopy faders.
2. **Diagnostic gesture:** with gain sending disabled, incoming read feedback generated no Press/commit before the actual gesture. One Phones slider gesture produced channel 16 CC34=127, then CC21=105, a fixed read request and logged targets 221 for channels 6/7. Automatic value changes selected an internal 128-step store; Release explicitly retriggered it. The native per-item binding format was `91:Select#n`.
3. **Bounded write:** a fresh full state of `[227, 227, 222, 222]` preceded one native Phones reduction. A separate complete readback then showed `[227, 227, 221, 221]`, and the native Phones display showed **−11.0 dB**. A new read first confirmed that exact four-field target. Only then did one opposite gesture restore `[227, 227, 222, 222]` and **−10.5 dB**. Both Main fields remained 227 throughout.

The four fields above are Main left/right followed by Phones left/right. The observed result was **both Phones channels −10.5 → −11.0 → −10.5 dB**, with Main unchanged. This is device/register readback and displayed dB evidence; no new analogue level measurement or acoustic test was performed. The [mapping report](../protocol/output-gain-evidence.md) shows the conversion, tested points and conservative software bounds separately.

There was no new mute or Main test. The outgoing monitor was first opened after the write test and was empty, so this report **does not claim a new complete outbound-packet trace**.

## Exact candidate scope and test context

The test copy had master zero, clip stopped and metronome off. The physical interface responded to the gain change. iPadOS **27.2 / build 24B119** was checked in this phase. Exact current interface firmware and every music-app version were not independently inventoried again; older version metadata must keep its original date. TotalMix-independent operation was not proved.

The bounded **v09 TEST** candidate allowed only channels 6/7 and exactly one raw step. It exposed no Main/mute/legacy write path and no implicit restoration. Native saved rules matched the candidate completely and compiled successfully. The native state began READ / LOCKED and became READY / ACTIVE before the bounded write.

Reported rule-file identities:

- v09 DIAG SHA-256: `57cc5408d2fec9227fadcb951e9f7c20681c60474f592bd372b59aaa464e1e61`
- v09 TEST SHA-256: `86d536485dc8414ede06548f35be6f946669b5ab3ff4278a6ad6bb9e4fe453c5`

Hashes identify the tested text; they do not distribute it or make this report an installable controller. The existing v06 original remained unchanged.

## Reported offline checks, separate from hardware evidence

- The rule-subset interpreter passed **16 groups / 18,511 cases**. A portable copy using a synthetic, zero-filled protocol-shaped state fixture passed the same counts. These are two runs of the same reported case set, not 37,022 distinct test cases.
- The separate parameter planner passed **25 tests including 32,768 stereo boundary cases**. It has no sender.
- The emulator is not Audeonic's compiler, a USB test or proof of native host dispatch. The native compiler/gesture/write observations above are separate evidence.
- The parameter work distinguishes documented device limits, conservative software limits, measured points, user caps, factory defaults, conditional reset actions and user references. Unknown factory defaults remain null and disable the associated action.

The source package describes portable test material, but those files have not been reviewed or published as part of this documentation update. The test counts are therefore **reported results**, not a newly reproduced public test suite. No local test command in this repository currently recreates this controller validation.

Proposed native quick-step presets of 0.5, 1, 2, 3 and 6 dB, plus supported-grid custom values, remain plans. Only the bounded half-dB fader operation above was newly device-tested. Other parameter families need their own ranges, encoding and acceptance gates.

## End state

The immediately preceding original Loopy project and MidiFire scene were restored. Original database objects and controller profiles compared equal, including rules, routing, widgets and audio references. Recording audio bytes were **not newly hashed** in this phase.

Phones returned to the fresh baseline; Main stayed unchanged. Diagnostic services and the runner stopped, local diagnostic ports closed, and music apps remained present. Existing helper records were unchanged, without installation, signing or new permissions. Separate diagnostic/test projects and the receive scene remain saved; media portability and a native MFR export are not verified.

## Remaining safety and release gates

- A Press marker is a protocol input, not proof that a human originated it. Full-range gesture handling, feedback separation and pickup still require acceptance tests.
- There is no protocol transaction ID. Identical valid states do not prove query correlation or replay resistance.
- An early pre-query frame during the 100 ms post-write delay can fail closed and cancel the delayed read. Production behavior needs explicit query-emission tracking.
- A cancel-after-commit defect was reported fixed before native testing and covered by regression. That does not establish every interruption/cancellation case.
- No proactive stale-display guarantee, suspend/reconnect/long-duration guarantee, full-range native fader, selectable-step native UI, stereo Main write, new mute-toggle validation or complete TotalMix coverage is claimed.
- Exact versioned profiles, portable reviewed artifacts, reproducible tests and novice-friendly installation/removal instructions remain required by the [release gates](../ACCEPTANCE.md).

Primary references: [RME Babyface Pro FS manual](https://rme-audio.de/downloads/bface_pro_fs_e.pdf), [Forney's unofficial Babyface Pro protocol notes](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro), [StreamByter manual](https://audeonic.com/streambyter/manual/), and [Loopy persistent MIDI widgets](https://wiki.loopypro.com/Tech_Note:_Persistent_Send_MIDI_Widgets). These references do not establish a general Pro FS/iOS compatibility claim. UCX II register or mute mappings must not be substituted.

Raw captures, native projects, screenshots and device/service records remain private. This publication did not perform a new hardware or acoustic test.
