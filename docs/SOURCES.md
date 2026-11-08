# Sources and evidence boundaries

Reviewed 2026-11-08. These references support narrow documentation claims, not an end-to-end Loopy integration or a verified device profile.

- [RME TotalMix FX](https://rme-audio.de/totalmix-fx.html): documents remote-control options and distinguishes TotalMix Remote, which controls a host system.
- [TotalMix FX for iPad, RME's App Store listing](https://apps.apple.com/us/app/totalmix-fx-for-ipad/id739965887): distinguishes the connected-hardware iPad app from TotalMix Remote and excludes MIDI/OSC and TCP/IP remote control. It does not establish an independent standalone path for a specific interface.
- [RME's TotalMix FX for iPad announcement](https://www.forum.rme-audio.de/viewtopic.php?id=18787): historical vendor corroboration of that distinction. Use current manuals and exact version evidence for new profiles.
- [Babyface Pro FS manual](https://rme-audio.de/downloads/bface_pro_fs_e.pdf), p.45 and section 21.6, p.54: separates analog input gain from mixer levels and distinguishes hardware mixing/EQ/Low Cut from host-CPU Reverb/Echo. These are product capabilities, not tested project controls.
- [Loopy Pro manual](https://loopypro.com/manual/), sections 5.1 and 5.3.1: software input gain and device-dependent Global Hardware Gain are separate. Ordinary software faders do not themselves establish a hardware-control mapping; Babyface support for the Global Hardware Gain setting is not verified here.
- [StreamByter](https://www.audeonic.com/streambyter/) and [MidiFire](https://www.audeonic.com/midifire/): official tool references for the experimental message-processing and return path. Their capabilities do not validate this project's complete integration.
- [GitHub issue-form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms): basis for the included YAML forms. Local parsing is separate from hosted rendering validation.

## Project evidence

- [Bounded native Phones-fader write/restore](milestones/2026-11-08-phones-fader-write-restore.md): one later native gesture/readback/restore sequence with Main unchanged, exact candidate hashes and reported offline counts. Full-range and live/reconnect readiness remain open.
- [Output-gain mapping](protocol/output-gain-evidence.md): reverse-engineered raw-to-dB formula, tested points and conservative software bounds. Matching native display is not independent acoustic calibration.
- [Filtered reception and paired Phones step/restore](milestones/2026-11-08-phones-step-restore.md): later native READ and register/readback observations, with no mute/acoustic test. Raw-unit change is not a general validated dB-step specification.
- [Native Loopy fader display](milestones/2026-11-08-native-fader-display.md): automatic native UI feedback after a helper query; 2,506 offline decoder cases reported separately. Not a hardware-writing-fader test or portable release.
- [Purpose, platform dependencies and earlier prototype observations](PROJECT_OVERVIEW.md): separates documented product behavior, design goals, maintainer-reported prototype results and a released profile. The older iPad/iPhone results do not include a public reproducibility package and do not promote hardware-module status.
- [Loopy READ / READY / LOCKED follow-up, 8 November 2026](milestones/2026-11-08-loopy-read-ready-locked.md): one fixed Loopy query and complete replies, with TotalMix still running. This adds scoped readiness evidence, not a new gain/mute/fader test or a released profile.
- [Passive iPad reception milestone, 8 November 2026](milestones/2026-11-08-passive-ipad-reception.md): sanitized project-reported native monitor observations. Complete-message reception is narrower than decoder or hardware-control verification. The package does not include original captures, a full version inventory or an installable profile.
- [Planning website tests](TESTING.md): pinned software revisions, successful build/deployment runs and the limits of recorded browser checks.

Private conversations, original working projects, personal identifiers, network details and private capture files are not published. Future hardware release claims must link to reproducible, sanitized evidence for the exact module, profile and revision.
