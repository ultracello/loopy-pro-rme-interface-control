# Interface copy with mute switches: load, read, display and one Phones mute

Completed 10 November 2026, 17:15 to 17:22 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run in which every step ran once. This is not a live approval.

## What was put together

Until now the two halves existed apart. The [transferred Interface copy](2026-11-10-other-project-interface-transfer.md) held the operating page inside a real music project, on the Restricted rule without gain-mute. The session gain-mute had passed for Phones only in a [separate test rig](2026-11-10-transfer-write-pair-session-mute.md).

This run used a new copy of the transferred project that carries both:

- the session gain-mute candidate rule, SHA-256 `d57eea28c32b34565c2e9512a73d212efd23525e1d9412c19d11cc19b0ecadb9`, which contains the fader, step and gain-mute handling in one text;
- the existing page with one fader, one dB display, ten step buttons and one status row per output group;
- two new switches, one per group, that mute the group and return it.

Before the run the copy was compared with its base and with the test rig. Against the base, only the rule text, the two switches, two display titles and the name differ. Against the test rig, every button and fader sends the same message and every feedback message reaches the same kind of element.

The routing scene is the combined 15-module scene of the [Interface integration](2026-11-09-restricted-control-interface-integration.md): the operator's seven existing modules plus the eight routing modules. One rule text was exchanged. The filter in front of the interface now is the strict filter of the mute runs, which lets the gain value raw 59 through. With the previous filter a mute could not have reached the interface.

## Getting the scene file into MidiFire

The host tool that copies files to the iPad cannot reach MidiFire's own folder. The scene file was copied into a new folder of Loopy Pro and then moved into MidiFire's folder in the iPadOS Files app, by automation, along the views recorded during three earlier imports on 9 November. The move took 39 seconds and needed no retry. The step refuses to press the move button unless the picker stands at MidiFire's folder, the button is the move button, the name field shows this file and the folder holds no file of that name.

## Results on the interface

| Step | Result |
|---|---|
| Copy on the iPad | Uploaded under a new name, read back, byte-equal to the built package |
| Scene | Loaded natively; MidiFire's status line names it and exactly its 15 modules are shown |
| Passive stream check | 0 packets in 4 seconds, TotalMix closed |
| READ | Six of six reads clean in a row, including the first read after loading the scene. Main raw 59/59, Phones raw 222/222 |
| Display | Phones fader at 83 % and dB display at −10.5 dB after each of the six reads, matching raw 222. Status rows: Phones normal, Main "59 without reference" |
| Phones mute switch | raw 222/222 to 59/59, status "own mute"; LOCK, a transport stop and start and a press without READ changed nothing; the second press returned exactly to 222/222; an independent query confirmed it |
| Main mute switch | Not touched: the device held Main at raw 59 from outside |

Two control presses were meant to change a level; neither was repeated. The presses came 3.4 and 3.5 seconds after their READ. The passive receiver lost no data and no read had to be repeated.

The first reply after loading the scene was complete this time. Over the day that makes three of five first replies lost or incomplete for the controller.

## Offline checks before the run

69 offline tests passed: 22 for this copy, its scene, the Files step and the choice of scene, and 47 tests of the earlier mute run executed again against this copy. In a counter-check, 21 safeguards were removed one at a time; the tests noticed each removal. One fault was found this way before the run: the screen record of the move dialog also contains the window underneath, with the file itself as an invisible row, and the first version of the Files step would have concluded that MidiFire already held the file.

## Closeout and remaining boundaries

After the run the previous MidiFire scene and the original project were loaded again, the four original files were byte-equal to before, diagnostic services were stopped and temporary access was retired. Final raw values: Main 59/59, Phones 222/222.

Not established: the Main mute switch on the interface; step buttons and fader writes under the candidate rule in this copy (they are bound as in the earlier write pair and were checked offline only); the seven existing routes of the scene in playing use; a mute from any level other than raw 222; that raw 59 is silence; operation alongside TotalMix; endurance; behaviour after a USB loss; crash-safe restoration. The level before a mute lives only in the running controller; after a reload nothing is returned automatically. This was one pass.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
