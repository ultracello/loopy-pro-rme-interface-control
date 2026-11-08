# Documentation validation

Date: **2026-11-08**. Scope: the public documentation update for the passive iPad reception milestone. The existing website implementation and workflow are unchanged.

## Local publication checks

- Relative Markdown file links resolve against the documentation package and the repository tree read at revision `dfd5dc10a32f4ba5dcb4e837b1c4a6cd024df9e9`. This checks file targets, not remote page availability or rendered anchors.
- The two issue forms parse as YAML and retain supported body types, unique field IDs, string labels and required top-level keys. The issue-chooser configuration also parses.
- The JSON registry retains six distinct hardware-module IDs, no verified hardware profiles and no executable artifacts. A separate research record links to the scoped passive-reception report without promoting a hardware module.
- Public-content review checks for credentials, private previews, private service/project identifiers, local paths, network details, raw conversations and unrelated personal material. The milestone is a sanitized technical summary, not a raw session log.
- `SHA256SUMS` covers the documentation and template files, excluding itself. It does not cover the website source or establish hardware behavior.
- The report and associated status text received a separate content review for evidence boundaries and public suitability.

## Evidence boundaries

No device test, MIDI query, website test suite or browser interaction was run for this documentation update. The device milestone remains a project-reported observation; its original captures and complete version/profile inventory are not distributed here. Earlier website tests are recorded separately with their exact revisions and runs in `docs/TESTING.md`.

Remote file readback is performed after the publication commit and reported separately. Hosted issue-form rendering has not been exercised by this check; local YAML validation is not a rendering test. No executable hardware-control module or validated installable profile is included.
