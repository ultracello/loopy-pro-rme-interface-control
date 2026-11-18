# RME Babyface Pro FS, controlled from Loopy Pro

This repository documents how an RME Babyface Pro FS is controlled from inside Loopy Pro on an iPad, without TotalMix FX, over the MIDI port the unit offers in class-compliant mode.

**Website: https://ultracello.github.io/loopy-pro-rme-interface-control/**

The website shows what can be controlled and how far each function is measured, the open points and the list of all reports. It is built from the documents in this repository, and its tests fail when it falls behind them, so it is the place to look for the current state.

## What is here

- [Protocol reference](docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md): every message byte for byte, with the formulas for the dB values. Each statement is marked as measured on the unit, reported back by the unit, taken from other people's notes, or unknown. It is written for anyone who wants to build native support into a host application.
- [Reference codec, test vectors and measured curves](docs/protocol/reference/): a small codec in Python that builds and parses bytes and sends nothing, the test vectors for it, and the equaliser curves measured with sine tones.
- [Reports](docs/milestones/): one dated report for every step of the work, with what was done, what was measured and what went wrong.
- [Website generator](website/).

## What is not here

The controller page that runs in Loopy Pro is a private working copy and is not published. There is nothing to download and install. The aim is native support in a host; the reference is written for that.

## Checks

```
python3 docs/protocol/reference/test_babyface_cc.py
cd website && npm test && npm run build
```

## Older documents

[Project overview](docs/PROJECT_OVERVIEW.md), [module status](docs/MODULE_STATUS.md), [testing](docs/TESTING.md), [development setup](docs/DEVELOPMENT_SETUP.md), [repository plan](docs/REPOSITORY_PLAN.md), [sources](docs/SOURCES.md) and the [acceptance gates](docs/ACCEPTANCE.md) were written in the first days of the project, 8 to 10 November 2026. They are kept as they were. Where they differ from the protocol reference or from a later report, the later document is right.

## License

Public domain under the [Unlicense](LICENSE). Do whatever you want with it.

Independent work. Not affiliated with RME or with A Tasty Pixel, the maker of Loopy Pro.
