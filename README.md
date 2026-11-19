# RME Babyface Pro FS, controlled from Loopy Pro

This repository documents how an RME Babyface Pro FS is controlled from inside Loopy Pro on an iPad, without TotalMix FX, over the MIDI port the unit offers in class-compliant mode.

**Website: https://ultracello.github.io/loopy-pro-rme-interface-control/**

The website shows what can be controlled and how far each function is measured, the open points and the list of all reports. It is built from the documents in this repository, and its tests fail when it falls behind them, so it is the place to look for the current state.

## How far it is

<!-- progress:start (written by website/build.mjs --stamp; do not edit by hand) -->
| | | |
|---|---|---|
| Measured on the unit | `███████████████████░` | **94 %**, 17 of 18 functions |
| Usable today from the controller page | `██████░░░░░░░░░░░░░░` | **28 %**, 5 of 18 functions |
| Native support in Loopy Pro | `░░░░░░░░░░░░░░░░░░░░` | not started |

Counted from the [coverage table](docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md#5-coverage-against-what-totalmix-fx-offers) of the protocol reference. Last report: [Phantom power, and what dim and mute are](docs/milestones/2026-11-19-phantom-power-and-what-dim-and-mute-are.md), 19 November 2026.
<!-- progress:end -->

A function counts as measured when its effect was read at the unit. Native support in Loopy Pro is the aim; it is in the hands of the developer of Loopy Pro, and what he needs is in the protocol reference.

## What is here

- [Protocol reference](docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md): every message byte for byte, with the formulas for the dB values. Each statement is marked as measured on the unit, reported back by the unit, taken from other people's notes, or unknown. It is written for anyone who wants to build native support into a host application.
- [Reference codec, test vectors and measured curves](docs/protocol/reference/): a small codec in Python that builds and parses bytes and sends nothing, the test vectors for it, and the equaliser curves measured with sine tones.
- [Reports](docs/milestones/): one dated report for every step of the work, with what was done, what was measured and what went wrong.
- [Tool for helpers](tools/babyface_helper.py): guided checks for people who test with their own unit, with [instructions](docs/help-wanted/README.md).
- [Website generator](website/).

## Help wanted

Everything here was measured on one unit. If you own a Babyface Pro or Babyface Pro FS and a computer, you can check in a few minutes whether yours behaves the same, and help with the one function that is not measured yet: [how to help](docs/help-wanted/README.md). No programming needed.

## Built on this reference

- [OliSimpleRME](https://github.com/OlivierPersoGit/OliSimpleRME): a small iPad mixer for the Babyface Pro FS, made to sit next to Loopy Pro. By its own README it started from this repository. It is someone else's project and has to be built with Xcode; we have not built or tested it.

## What is not here

The controller page that runs in Loopy Pro is a private working copy and is not published. There is nothing to download and install. The aim is native support in a host; the reference is written for that.

## Checks

```
python3 docs/protocol/reference/test_babyface_cc.py
python3 tools/test_babyface_helper.py
cd website && npm test && npm run build
```

## Older documents

[Project overview](docs/PROJECT_OVERVIEW.md), [module status](docs/MODULE_STATUS.md), [testing](docs/TESTING.md), [development setup](docs/DEVELOPMENT_SETUP.md), [repository plan](docs/REPOSITORY_PLAN.md), [sources](docs/SOURCES.md) and the [acceptance gates](docs/ACCEPTANCE.md) were written in the first days of the project, 8 to 10 November 2026. They are kept as they were. Where they differ from the protocol reference or from a later report, the later document is right.

## License

Public domain under the [Unlicense](LICENSE). Do whatever you want with it.

Independent work. Not affiliated with RME or with A Tasty Pixel, the maker of Loopy Pro.
