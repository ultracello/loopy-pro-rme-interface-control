# Any step width, and Main operated for the first time

Completed 13 November 2026, 00:14 to 00:18 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run and offline tests. This is not a live approval.

## Any step width

Until now a step control accepted five widths: 0.5, 1, 2, 3 and 6 dB. The operator asked for any width, for example +10 dB or −12.5 dB.

A sixth revision of the candidate rule, SHA-256 `642050a0bf23e0c689a644877eae2022e533b84741e2b9d8e2b0ea82caf4a57a`, accepts every count of half dB from 1 to 125 on a step control. One value means "the width chosen on the page": a slider whose whole travel maps to 0.5 to 30 dB in half-dB steps. The chosen width is published to a display with 60 fields. A step that would leave the software range is refused as before, not clamped.

The page got six new elements: the slider, the display, and one "down" and one "up" button each for Main and Phones that apply the chosen width. The five fixed buttons per group stay.

Offline, 11 new tests passed and the 56 tests of the earlier revisions still pass. Eight deliberate falsifications were noticed.

On the interface, with a clip looping:

| Check | Result |
|---|---|
| After loading | slider at 0 %, display 0.5 dB; Phones down to raw 213, up to 214 |
| Slider dragged | slider at 35 %, display 10.5 dB; the page stayed armed |
| Phones down by the chosen width | raw 214/214 to 193/193, exactly 10.5 dB |
| Phones up by the chosen width | exactly back to 214/214 |

Large steps upward were deliberately not run.

## Main

Main had stood at raw 59 from outside on every day of testing, so nothing on Main had ever been operated on the interface. With nothing connected to the Main outputs, the operator released Main for testing.

| Check | Main gain | Status | Peak at the Main output | Display |
|---|---|---|---|---|
| Start | 59/59 | 59 without reference | none | |
| Switch over the foreign mute | 183/183 | normal | signal | −30.0 dB |
| Two half-dB steps up | 184, 185 | normal | rises with each step | −29.5, −29.0 dB |
| Two half-dB steps down | 184, 183 | normal | falls with each step | −29.5, −30.0 dB |
| Switch: own mute | 59/59 | own mute | none | |
| Switch: back | 183/183 | normal | signal | |
| Switch: muted again at the end | 59/59 | own mute, also with the page locked | none | |

Phones stayed at raw 214/214 through all of it. The operator saw the Main level LEDs on the unit while the steps ran.

This establishes on the interface what earlier reports listed as open for Main: the fixed level of −30 dB out of a foreign mute, steps, and an own mute with exact return.

## Remaining boundaries

Not established: Main with speakers connected; fader writes in an automated run; large steps upward; three of the seven reason fields on the interface; an evening of playing on the rebuilt USB chain; operation alongside TotalMix; crash-safe recovery.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
