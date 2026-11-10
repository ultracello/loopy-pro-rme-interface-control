# Restricted Interface transfer into a different project

Completed 10 November 2026 (UTC). Evidence: project-reported, bounded native iPad/Babyface Pro FS checks in a separate copy of a different saved test project. This is one explicit project transfer, not a general importer, public installer or gain-control validation of the transferred composition.

The existing Restricted LIVE1 rule remained unchanged: SHA-256 `6d1149cc2e798d3de28426d658b28945af1f671cf8d67493c2ea86635b4639b7`. Earlier [step-width tests](2026-11-10-restricted-step-widths.md) and [same-project integration checks](2026-11-09-restricted-control-interface-integration.md) retain their separate revisions, cohorts and limits.

## What was transferred

The target used an older, different MIDI-source structure. An empty Interface page and its native Show-return action were first created, saved and checked in a MIDI-isolated copy. The control widgets and explicit binding references were then mapped to that actual page structure; no native page schema was invented.

The target's existing MIDI input source was retargeted completely from its physical-source type to the verified virtual-return type. Changing only a port label would not have handled that structural difference. One existing StreamByter instance received a fresh private AU identity, while the rule itself stayed byte-identical. Its physical output destination was removed; its sole output was the restricted virtual MidiFire route. No new MIDI command family, gain-mute path or old saved-level restore was added.

The target's actual native audio, master and clock values were checked and preserved. In the final natively saved copy, all nine protected audio records and the existing music-page record were byte-identical to their target baselines, and all original target resources were unchanged. No audio from the source test project was copied into the target. The original source archives were not modified. This target contained **zero audio tracks**: that fact limits what this transfer can establish about playing music or complex multitrack projects.

## Actual native acceptance

The transferred copy was loaded and saved natively. A full 227-byte hardware state reached the **READ/LESEN** path; **GELESEN** and both displayed faders matched Main raw227/227 and Phones raw222/222, mapped to −8.0 and −10.5 dB. Reopening the Interface page and returning to the music page were checked. The native return action left the running transport running.

**Activation actions: zero. Gain actions: zero. Repeated step-width tests: zero.** The observed output values stayed unchanged. This is a read/feedback/navigation acceptance of this transferred composition, not a new proof that its remapped write controls operate correctly. The earlier source-copy gain tests must not be relabeled as gain tests of this target.

Running transport does not establish acoustic continuity, especially in this zero-track target. No acoustic measurement, arbitrary-project migration, multitrack guarantee, complete TotalMix coverage or general live approval is claimed.

## Closeout and remaining boundaries

The original project and previous MidiFire scene were restored. After diagnostic shutdown, the original's four central files were checked byte-for-byte against the saved baseline. A fixed read after project and scene restoration confirmed unchanged Main raw227/227 and Phones raw222/222. No gain action was used during closeout.

The attempted full MidiFire Documents copy failed before any MidiFire change. A fresh named scene was therefore saved natively before loading the known route. Restoration used native scene Load followed by a visible graph check. Global MidiFire settings were not changed; no byte-identical comparison of the scene or complete Documents backup is claimed.

Owned diagnostic services and local ports were closed, the temporary helper was absent from a fresh device-process inventory, and temporary access was retired. The installed helper metadata was unchanged. This establishes the recorded closeout of this run, not general receiver continuity or interruption-safe restoration.

Gain-mute and old saved-level restore remain blocked. Silent USB/receiver replacement and crash-safe automatic restoration remain unproven. The transfer adds no physical reconnect, endurance or new parameter-family evidence.

Private native projects, scenes, identity maps, captures, media and access material are not distributed. This facts-only report includes no controller source, new license grant, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
