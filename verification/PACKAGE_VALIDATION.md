# Documentation validation

Date: **2026-11-09**. Scope: the completed Sync LIVE1 native-fader startup, bounded writes and activation-gate result, public status and planning website. Base: `b73a4346ae4f46562ad38da7ec5a6f151c22a661`.

## Publication checks

- Relative Markdown targets, issue-template YAML, JSON registry structure and documentation checksums are checked before publication.
- Six hardware-module entries remain unreleased/unverified as public profiles. No executable native artifact or complete source project is included.
- The latest research record distinguishes three startup checks, bounded independent fader tests and two specific activation/stop gates from auxiliary feedback, gain-mute lifecycle, physical USB reconnect, duration and full-range/recovery work.
- Public-content review excludes private conversation identifiers, credentials, device/network identifiers, local paths and original native projects.
- `SHA256SUMS` covers documentation/templates, excluding itself and website source. It proves content integrity, not device behavior.

## Evidence boundaries

No interface access, MIDI, music-app operation or Mac UI input was used for this publication. Device observations are project-reported. Three starts are not a complete recovery matrix; a missing-return gate is not USB reconnect proof; bounded gestures are not full-range validation. Gain-mute remains level-based and its lifecycle restriction is not lifted. No complete live approval is claimed.

Website checks are recorded in [TESTING.md](../docs/TESTING.md). Exact-commit remote readback, CI and hosted-page verification follow publication and are reported separately.
