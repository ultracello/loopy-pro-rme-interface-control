# Changelog

Dates use Europe/Berlin. This records the documentation repository separately from any future application or hardware-module release.

## 2026-11-08 · Website 0.2.2: scoped milestones and source links

- **Updated:** the public planner now highlights one bounded native Phones-fader reduction/restore and links separate display-only and fixed-button checkpoints at documentation commit `1bf9b91149590be331b75897af24a4f388b34ca3`.
- **Evidence:** both Phones channels -10.5 → -11.0 → -10.5 dB, fresh full readback before restore and Main unchanged. Mapped register/display values, not acoustic calibration, a full-range pass or a new complete outbound trace.
- **Exports:** JSON plans and readable checklists carry the dated reports, source links and remaining validation gates. Historical evidence remains separate. No executable hardware code or new native step-selector result is included.
- **Preserved:** browser-only demo, saved plans, independence notice, existing docs/workflow and unreleased hardware-profile status.
- **Checks:** 16 website regression tests, TypeScript/production build and static React rendering passed. Deployment status is recorded separately in GitHub Actions. No device or music-app UI actions are part of this publication.

## 2026-11-08 · Bounded native Phones-fader write/restore

- **Added:** [v09 test report](docs/milestones/2026-11-08-phones-fader-write-restore.md) for both Phones channels −10.5 → −11.0 → −10.5 dB with fresh complete readback before restore, Main unchanged and original project/scene restored.
- **Evidence:** native display, diagnostic gesture and actual write phases distinguished; no new complete outbound trace, acoustic measurement, Main or mute test claimed. [Mapping notes](docs/protocol/output-gain-evidence.md) explain the raw-unit/dB relationship without generalizing software bounds into hardware limits.
- **Reported software checks:** 16 groups / 18,511 interpreter cases, repeated by a separate synthetic portable copy; parameter planner 25 tests including 32,768 stereo boundary cases. These counts are not a newly run public test suite; source/test artifacts are not shipped in this docs update.
- **Still open:** full-range native fader, native step selector, new mute toggles, stereo Main, query correlation, stale/suspend/reconnect/long-duration behavior, TotalMix independence and portable release artifacts.
- **Scope:** documentation and evidence status. The planning website remains a browser-only planner, not the tested controller.

## 2026-11-08 · Filtered Phones step and native fader display

- **Added:** [receive-filter/Phones report](docs/milestones/2026-11-08-phones-step-restore.md): nine offline groups, 1,265 packet cases and a 3,200-short-message flood; three native READs; one paired Phones raw-unit reduction and exact restoration, Main unchanged. No mute or acoustic test.
- **Added:** [native display report](docs/milestones/2026-11-08-native-fader-display.md): 2,506 offline decoder cases, native text/compiler checks, and automatic Main/Phones slider updates after a helper-triggered query. No hardware-write SysEx from that UI decoder.
- **Clarified:** displayed feedback is not human write intent; the two receive scenes are separate experiments; original working scenes/projects were restored. Hardware-writing faders, mute, stereo Main, other step sizes and lifecycle validation remain open.
- **Updated:** README, overview, developer setup, source register and research registry; historical checkpoints preserved. Selectable step sizes remain profile-driven requirements, not claims that all proposed values work.
- **Checks:** documentation, public-content and checksum validation. No device or acoustic test was performed by this publication. The public planning site remains a non-executable hardware-planning tool.

## 2026-11-08 · Loopy READ reaches READY / LOCKED

- **Added:** [sanitized READ follow-up](docs/milestones/2026-11-08-loopy-read-ready-locked.md), using existing v06 Loopy controls and the verified MidiFire return path. One fixed seven-byte request was observed; complete 227/207/207-byte replies reached Loopy. A passive receiver reassembled five chunks without an incomplete remainder and sent no second request.
- **Observed:** native READY / LOCKED after READ, then READ / LOCKED after clock stop. Output-gain fields remained unchanged. The tested scene was saved natively, the original scene restored, clip/transport stopped and temporary remote services shut down.
- **Still open:** no new gain/mute/fader validation, no TotalMix-terminated test, no portable MFR export or complete versioned profile. No hardware module is promoted.
- **Documentation:** linked the follow-up from the overview, README, developer setup, source register and machine-readable research evidence. Kept the earlier passive report as a historical checkpoint with a forward link.
- **Checks:** publication checks only; this documentation update did not repeat the device test or alter the website.

## 2026-11-08 · Purpose and platform explanations

- **Added:** [project overview](docs/PROJECT_OVERVIEW.md) explaining the performance use case, ordinary Loopy faders versus interface output/preamp/direct-monitor controls, and the experimental USB MIDI/SysEx path.
- **Clarified:** iPad/iPhone/Mac roles; TotalMix FX for iPad versus desktop TotalMix/TotalMix Remote; the still-unproven TotalMix-independent workflow; and Babyface Pro FS hardware processing versus host-calculated Reverb/Echo.
- **Evidence:** added official RME/Loopy references and separated historical maintainer-reported iPad/iPhone experiments from the published passive-reception checkpoint, offline checks and browser-only planner.
- **Preserved:** independent-project notices, existing module status and all release gates. No new hardware compatibility, native mute synchronization, hardware fader or complete iPhone support is claimed.
- **Checks:** documentation link, YAML/JSON, checksum and public-content review only. No device actions or new hardware/software behavior tests. Website source, workflow and Pages settings are unchanged.

## 2026-11-08 · Passive iPad reception milestone

- **Added:** [sanitized development report](docs/milestones/2026-11-08-passive-ipad-reception.md) for full 227/207-byte reception in a fresh MidiFire monitor and the temporary path into Loopy's StreamByter input monitor. The Loopy output monitor was empty during the passive check.
- **Evidence:** scoped project-reported device observations using existing TotalMix traffic; the original MidiFire scene was restored afterwards. No new Loopy state query, output gain or mute test was executed in that check.
- **Documentation:** linked the result from the overview, module status, source register and developer setup. Corrected stale documentation-only/browser-planned wording to reflect the existing planning website, retaining pinned software-test evidence separately.
- **Checks:** local documentation link, YAML, JSON, checksum and public-content checks. These are publication checks, not a repeat of the device observation or website test suite; see [validation record](verification/PACKAGE_VALIDATION.md).
- **Still open:** complete version/profile inventory, reproducible receiver artifacts, independent Loopy-only operation, query/decoder readiness, control feedback, hardware faders, stereo main output and iPhone support. No hardware module is promoted or released.
- **Scope:** documentation only; website implementation, workflow, Pages settings and audio/control behavior are unchanged.

## 2026-11-08 · Website 0.2.1: consistent project name

- Corrected website branding to **Loopy Pro Interface Control** in the header, footer, demo and browser title.
- Updated the downloadable planning-guide heading and export filenames to match, plus the website README and visible changelog.
- Added a clear independent-software and non-affiliation notice on the website and near the top of the GitHub README. Updated the README project heading; the repository name and URLs are unchanged.
- Preserved existing browser-saved plans, control behavior, evidence and hardware-verification boundaries.
- Added a branding regression test. `npm test` passed all 12 tests; `npm run build` passed TypeScript and production-build checks. This is a website correction, not a hardware-control release.

## 2026-11-08 · Documentation and collaboration structure

### Added
- Project README, contribution guide and dated changelog.
- Six requested control-module IDs with an explicit unverified status.
- Future browser-test checklist and hardware acceptance gates.
- Test-report and device-profile templates.
- GitHub test-report and feature-request forms, plus a pull-request checklist.
- Source register, machine-readable module status and documentation validation record.
- Developer/test setup guide separating Mac/iPad automation from end-user requirements, with unverified topology and versions left open.

### Limits at that initial checkpoint
- No runnable application, device-control script or importable Loopy project is included.
- No hardware-verified profile is included.
- Local documentation/YAML/JSON checks are separate from GitHub rendering or hardware testing.

## 2026-11-08 · Project overview

- Published the README with the confirmed repository name and project goals.
- Distinguished direct RME interface control from remote control of TotalMix software.
- Marked faders and iPhone support as unconfirmed and kept unpublished profiles separate from compatibility claims.

## Next entry template

### YYYY-MM-DD · Version or change name
- **Changed:** what a user or contributor can now do.
- **Evidence:** file, commit and test-report references.
- **Checks run:** exact command/procedure and result.
- **Not run / failed / blocked:** remaining limits and why.
- **Compatibility:** exact affected profile; do not imply all RME devices.
- **Migration / rollback:** only if behavior or stored data changes.
