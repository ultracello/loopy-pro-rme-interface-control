# Transfer-copy write pair and a session gain-mute check

Completed 10 November 2026 (Europe/Berlin). Evidence: project-reported, bounded native iPad/Babyface Pro FS checks. This report holds two separate results on two different rule revisions, one observation about TotalMix, and three findings about the iPad routing environment. None of it is a live approval.

## Write pair in the transferred Interface copy

The copy from the [other-project transfer](2026-11-10-other-project-interface-transfer.md) had only passed READ, feedback and navigation. With the unchanged Restricted rule, SHA-256 `6d1149cc2e798d3de28426d658b28945af1f671cf8d67493c2ea86635b4639b7`, each output group was now lowered by 0.5 dB once and returned exactly:

| Group | Before | Lowered | After |
|---|---|---|---|
| Main | raw 227/227 | raw 226/226 | raw 227/227 |
| Phones | raw 222/222 | raw 221/221 | raw 222/222 |

Each step was confirmed by a fresh complete 227-byte state, and the other group stayed unchanged. Four control presses were dispatched; none was repeated. No other step size, no fader write and no mute was exercised in this copy. The earlier [step-width tests](2026-11-10-restricted-step-widths.md) belong to other copies and keep their own limits.

A passive pre-check refused the first start. With TotalMix FX running on the iPad the interface sent about 57 compact 27-byte status messages per second, and none with TotalMix closed. That stream would have overrun the bounded passive receiver during the run. The pair was therefore run with TotalMix closed. Operation alongside TotalMix is not verified.

## How TotalMix mutes on this path

In a passive recording, while the operator pressed mute in TotalMix, the gain value of the muted output became raw 59. No separate per-channel mute bit was seen on this path. TotalMix's display and the device can disagree: later the same day the device held Main at raw 59 while TotalMix showed its mute as off. Raw 59 was not measured acoustically, so it is not claimed to be silence.

## Session gain-mute candidate

Gain-mute stays blocked in the Restricted rule. A separate candidate rule, SHA-256 `d57eea28c32b34565c2e9512a73d212efd23525e1d9412c19d11cc19b0ecadb9`, lets the controller mute a pair itself by writing raw 59 and keeps the level before the mute as a volatile reference. The reference is meant to survive LOCK, a transport stop and start, and a toggle press without a preceding READ, and to be discarded after a foreign change or an explicit forget.

**Behaviour without the interface.** In an isolated copy with no MIDI destination, synthetic states were fed to the real StreamByter. All five cases matched the prediction of the offline interpreter. Among them: the reference was kept through LOCK, a press without READ and a transport change, and it was discarded after a foreign change and after an explicit forget.

**On the interface.** One pass for Phones:

| Step | Main L/R, Phones L/R (raw) | Group status shown |
|---|---|---|
| READ before the mute | 59, 59, 222, 222 | normal |
| Toggle, once | 59, 59, 59, 59 | own mute |
| LOCK, transport stop and start, toggle without READ | unchanged | locked |
| READ before the return | 59, 59, 59, 59 | still own mute |
| Toggle, once | 59, 59, 222, 222 | normal |
| Separate fixed read | 59, 59, 222, 222 | |

Fresh complete states confirmed each step. Two presses were dispatched; none was repeated. Main was not touched: the device held it at raw 59 from outside, and the candidate does not adopt a 59 it did not write.

This was the third attempt of the day. Two earlier attempts ended before any gain message. In the first, the test copy did not react at all after the interface had dropped off the iPad and been reconnected. In the second, the passive receiver lost the first packet of one reply. Before the passing attempt the gate in front of the mute was changed during the run: instead of one clean READ it required six consecutive clean READs immediately before the mute.

## Findings about the routing environment

- **MidiFire in the background.** After some minutes in the background without use, the route through MidiFire went silent: no controller query reached the interface, and no feedback reached Loopy. Bringing MidiFire to the foreground once restored the route at once. Cause and settings were not examined. Until this is resolved, unattended use is not dependable.
- **First reply after loading the routing scene.** In two of two cases the first complete-state reply after loading the scene lacked its first 9 bytes. In the case where the display was recorded, the controller missed that reply as well. The next 53 replies were complete. The candidate gives up after one second without a complete reply; while a pair is muted, that would discard the reference.
- **Loopy's unsaved mark.** Loopy marked a loaded project as unsaved when it did not find the audio interface stored in the project. Reloading the saved project in a healthy state cleared the mark.

## Closeout and remaining boundaries

After every run the original project and the previous MidiFire scene were restored and the loaded original was checked against its saved baseline; in the one run that began with Loopy's unsaved mark, that mark was the only difference before the reload. Diagnostic services were stopped and temporary access was retired. The last read showed Main raw 59/59, set from outside, and Phones raw 222/222.

Not established: a mute of Main; a mute from any level other than raw 222; a foreign change during an own mute on the real interface; that raw 59 is silence; operation alongside TotalMix; endurance; behaviour after USB or receiver replacement; crash-safe restoration. The session gain-mute candidate is a test rig and is not released; gain-mute and old saved-level restore remain blocked in the Restricted copy.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
