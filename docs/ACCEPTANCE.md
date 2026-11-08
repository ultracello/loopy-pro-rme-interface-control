# Acceptance gates

## Documentation structure

- Every local link resolves.
- GitHub forms parse and use supported fields; hosted rendering remains a separate check.
- No invented repository URL, code release, test result, device mapping, or collaborator appears.
- Changelog dates and module records match the evidence.
- The repository contains no original projects, recordings, private service links, runtime state, or secrets.

## Planning app release

Record the exact commit/build ID, test date, commands and results. Run the app's actual lint/type/build checks and the [browser checklist](TESTING.md), including exports, reload, reset, empty selection, repeated controls, and narrow screens. Mark environments not exercised as **not run**. Do not call a build check a browser test.

## First hardware-verified module

All items below must be evidenced for the exact profile before executable code export is enabled:

1. **Identity:** exact RME model, firmware, iPad/iPhone or desktop OS, Loopy Pro, TotalMix, and any bridge/plugin versions.
2. **Path:** actual transport, target output, complete message mapping and encoding, and authoritative reference or measured evidence. Keep audio routing separate from control routing.
3. **State:** initial synchronization; independent level and mute state; feedback after local device changes; duplicate input; stale feedback; disconnect/reconnect; restart; and an honest unknown-state display when synchronization fails.
4. **Behavior:** intended output changes only; the other output remains untouched. Up/down steps are measured over the supported range. Bounds, saturation and out-of-range values are handled. Mute/unmute semantics and restoration behavior are explicit.
5. **Safety:** a reviewed isolated test procedure with safe monitoring, abort conditions, and restoration of a working copy. Do not modify the original project or existing routing as an incidental setup step.
6. **Installation:** a novice can follow the complete step-by-step guide in a separate working copy. Record prerequisites, missing-capability messages, removal/rollback, and what is preserved.
7. **Evidence:** completed profile, test report, exact source revision and artifact hashes; passed, failed, blocked and not-run cases remain visible.
8. **Review:** maintainers approve the limited compatibility claim and review the complete release artifact for public distribution.

Passing headphones does not verify main output. Passing a fader does not verify mute. Passing one model or host route does not verify another. An iPad pass does not verify iPhone.
