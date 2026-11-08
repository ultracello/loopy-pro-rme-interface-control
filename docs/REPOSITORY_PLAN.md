# Repository organization

This is a dedicated public home for the Loopy Pro RME Interface Control project's documentation, contribution workflow, and future reviewed control modules. It is not a mirror of private research archives or personal working projects.

## Keep it small

Use Issues for proposed changes and reproducible reports, and draft pull requests for review. The included forms need no custom labels, external project IDs or preselected assignees. A separate board, wiki, bot or CI workflow is not required to begin.

Suggested labels, if useful later: `bug`, `feature`, `documentation`, `needs-evidence`, and `hardware-test`. The template files do not create labels.

## Adding real source later

- Preserve the application's actual build/setup instructions, lockfile and licensing information.
- Review the full staged diff for credentials, private URLs, personal data, runtime state and unrelated material before each push.
- Add `profiles/<profile-id>/` only when a real profile and evidence exist.
- Add `modules/<module-id>/` only for actual implementations with installation and removal/rollback instructions.
- Add `tests/` for reproducible tests of shipped code.

Those directories are suggestions, not modules currently shipped. Do not add placeholder scripts that resemble functioning hardware-control code.

## Release and access boundaries

Repository visibility is public. That does not make private previews, recordings or working projects public, and does not grant access to those sources. The repository contains no credentials or configuration for private services.

No automatic deployment, Pages, collaborator invitation, third-party integration, or credential creation is required by this structure. Decide those separately if needed. Select licensing before code reuse or substantial contributions.

A `.gitignore` can reduce accidental additions; it does not remove tracked secrets or make an attachment private. Public posts and attachments must be reviewed before submission.
