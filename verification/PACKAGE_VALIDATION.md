# Documentation validation

Date: 2026-11-08. Scope: the initial public documentation and contribution structure.

## Local checks

- Relative Markdown file links resolve within the structure.
- The two issue forms parse as YAML and use supported body types, unique field IDs, string labels and required top-level keys.
- Issue-chooser configuration parses; blank issues remain available.
- The JSON registry has six distinct expected module IDs, no verified hardware profiles and no executable artifacts.
- Public-content review excludes credentials, private previews, private service/project identifiers, personal setup observations, raw conversations and unrelated projects.
- Per-file SHA-256 values identify the initial documentation content. They do not establish hardware behavior.

## Separate checks

Remote file readback is performed after the publication commit and reported separately. Hosted issue-form rendering has not been exercised by this documentation check; local YAML validation alone is not a rendering test. No application CI, device-control test or hardware validation is supplied by this structure. No application or executable module is included.
