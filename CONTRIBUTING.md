# Contributing

The most useful thing you can do is a short test with your own unit. If you own an RME Babyface Pro or Babyface Pro FS and a computer, see **[Help wanted](docs/help-wanted/README.md)**: a small tool guides you, and you need no programming.

Other ways to help:

- Tell us where the [protocol reference](docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) is unclear or wrong. Open an issue and name the section.
- If you build support for the unit into an application, tell us what was missing.

## Rules of the repository

- Issues, pull requests and their attachments are public. Remove private data before posting: no recordings, no serial numbers, no credentials, no private messages.
- A statement about the hardware needs to say how it was established. The reference uses four marks for that: measured, reported, notes, unknown. A result from another unit is recorded as such, with the report it comes from.
- Keep changes small and say what you checked. The checks of the repository:
  ```
  python3 docs/protocol/reference/test_babyface_cc.py
  python3 tools/test_babyface_helper.py
  cd website && npm test
  ```
- Everything here is public domain under [the Unlicense](LICENSE). By contributing you dedicate your contribution to the public domain as well.

The documents under `docs/` that date from 8 to 10 November 2026, and the folder `templates/`, belong to the first days of the project and are kept as they were.
