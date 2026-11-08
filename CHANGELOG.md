# Changelog

Dates use Europe/Berlin. This records the documentation repository separately from any future application or hardware-module release.

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
