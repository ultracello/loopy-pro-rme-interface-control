# The reference level of the two line inputs

Completed 17 November 2026, 23:27 to 23:31 (Europe/Berlin). Evidence: project-reported, offline tests and one bounded native iPad/Babyface Pro FS run in one session. Nothing was connected to the two inputs. This is not a live approval.

## What was added

The two line inputs of the interface can be set to one of two reference levels. The fifteenth revision of the candidate rule, SHA-256 `a8613ca02967ff6ac681c78a470c4104f390c7a372ccdf522f9fe8af82b1d49a`, switches each of them from the page: one button per input and one display of four fields that shows what the unit reports for both.

The course is the one of the pad of the microphone inputs: a fresh read, one message that changes exactly one setting bit and sends every other setting bit back as read, a check read, and OK or a named reason. The refusals of the pad hold here too: nothing is sent while phantom power is on or while an unknown setting bit stands, and no phantom power bit is ever sent. The filter before the interface passes the two new bits under the same conditions as a pad bit and nothing else new; its SHA-256 is `22f3e2c323cfb9131abb68d10f50a24b3e08ee92b55cf84f47884f3b5a5de9bd`.

## Where the meaning of the bits comes from

The protocol notes the project has used so far name the bits for phantom power and pad of this message and are silent about the two bits between them. The Linux driver of the interface names the same register: bits 0 and 1 phantom power, bits 2 and 3 the sensitivity of line input 3 and 4, bits 4 and 5 the pads, with a set sensitivity bit called +4 dBu and a clear one −10 dBV. The numbers for phantom power and pad agree with the notes. The labels on the page follow the driver.

## Offline

19 new tests passed, the 163 tests of the earlier revisions still pass, and all 23 deliberate falsifications of rule and filter were noticed. The pad messages of this revision are byte for byte the ones of the revision before, over all 64 combinations of the six setting bits.

## On the unit

| Button | Setting bits reported by the unit, before → after | Reason row | Display |
|---|---|---|---|
| Input 3 | 000c → 0008 | OK | 3: −10 · 4: +4 |
| Input 4 | 0008 → 0000 | OK | 3: −10 · 4: −10 |
| Input 3 | 0000 → 0004 | OK | 3: +4 · 4: −10 |
| Input 4 | 0004 → 000c | OK | 3: +4 · 4: +4 |
| Input 3 | 000c → 0008 | OK | 3: −10 · 4: +4 |
| Pad of input 1 | 0008 → 0018 | OK | 3: −10 · 4: +4 |
| Pad of input 1 | 0018 → 0008 | OK | 3: −10 · 4: +4 |
| Input 3 | 0008 → 000c | OK | 3: +4 · 4: +4 |

Eight of eight. A gain step of input 4 up and down, with one sensitivity bit clear, arrived and left the setting bits alone. A press on the locked page said that the page has to be read first and changed nothing. At the end the unit stood as at the start, with nothing to bring back.

So the unit accepts the message for each of the two bits, reports the bit, and keeps every other setting.

## Not established: what the switch does to a signal

Nothing was connected, so the run read the idle noise of the two inputs before and after every switch, hoping it would move with the sensitivity. It did not: input 3 stood between −100.1 and −98.1 dBFS, input 4 between −105.6 and −104.5 dBFS, in every position. Differences of at most 2 dB are within the spread of this reading. Which position is +4 dBu and which is −10 dBV therefore rests on the naming of the driver alone. A measurement needs a source at one of the inputs.

## The same afternoon: the routing app in the background

The displays of the page still pass through a separate routing app, and an earlier report found that app suspended once, seven minutes after it had been started. A read-only look this afternoon did not repeat that: the app was still running after at least 92 minutes untouched in the background, and after being ended and started again it ran through ten minutes of observation; each time the displays followed at once without the app being touched. The tablet was on power; battery operation was not observed. The app's own idle timeout for battery operation was set from one hour to never.

Keeping that app visible next to the host was not possible: the tablet shows its apps full screen, and its multitasking mode, a setting of the operating system, was left as it is.

## Remaining boundaries

Not established: the effect of the reference level on a signal; the refusal while phantom power is on, on the unit (tested offline; phantom power is never switched for a test); the routing app in the background on battery; a setup that recovers from a replug without any touch. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
