# Hearing the inputs on the headphones, measured with a loop cable

Completed 17 November 2026, 02:53 to 03:01 (Europe/Berlin). Evidence: project-reported, one bounded native iPad/Babyface Pro FS run and offline tests. This is not a live approval.

## A function the unit does not report back

The operator wants to hear each of the four analog inputs on the headphones with a level of its own, without TotalMix. That is the mixer of the unit. The message for it is in the protocol notes of the [oscmix project](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro), and two fixed levels of it had already been seen to work on this unit, for the way of the playback to the headphones.

Unlike gains and the pad, the unit does not report its mixer. A rule cannot read first and compare here. The ninth revision of the candidate rule, SHA-256 `ad45c86275a008fb695b9f78dd191630125344e7b6e2d68caefed3d02b1e85fa`, therefore keeps its own picture:

- after loading, every way is "unknown", with a level of −12 dB kept; the first press makes it known;
- one control per input switches the way on or off, others move the level between −60 and 0 dB in half dB, held at the ends and never above 0 dB;
- while a way is not on, a level step only changes the level that is kept, and nothing is sent;
- after a send the rule asks the unit for its state and reports "ok" when it answers, which also keeps the page armed. From the answer it cannot tell whether the level arrived.

The filter before the interface, SHA-256 `2cb14e440c06ddb49644a5bcf70593ae8c9da1c5dfacf8b29329e854c4a5a902`, additionally passes mixer messages only for the eight places that put inputs 1 to 4 on the left and right headphone channel, and only up to unity.

Offline, 26 new tests passed and the 106 tests of the earlier revisions still pass. All 30 deliberate falsifications were noticed.

## Measured, because nothing else can decide it

The operator had suggested a cable from an output into an input and left it in place: XLR output 1 into XLR input 1. With a clip looping and Main at −30 dB, input 1 carried a peak of −26.6 dBFS. The playback itself was not routed to the headphones, so the peak meter of the headphone output showed the monitoring alone. Expected there: the peak at input 1, plus the monitoring level, plus the level of the headphone output (−14.5 dB).

| State | Peak at the headphone output, left and right | Expected | Difference |
|---|---|---|---|
| Before anything was written | no signal | | |
| Input 1 on at −12 dB | −53.1 dBFS | −53.1 dBFS | 0.0 dB |
| Input 1 at −6 dB | −47.1 dBFS | −47.1 dBFS | 0.0 dB |
| Input 1 at 0 dB | −41.1 dBFS | −41.1 dBFS | 0.0 dB |
| One more step up at 0 dB | refused; unchanged | | |
| Input 1 back at −12 dB | −53.1 dBFS | −53.1 dBFS | 0.0 dB |
| Input 1 off | no signal | no signal | |
| Inputs 2, 3 and 4 on | −124.5 dBFS, their noise floor | nothing from input 1 | |
| Two level steps while off | no signal | no signal | |

Each value is the highest peak of several readings over a little more than one loop of the clip. All 19 presses showed the expected reason and displays. After the first read the page showed all four ways as unknown at −12 dB.

This establishes on this unit that the mixer message puts an input on the headphones with a freely chosen level, and that the four inputs are addressed as the notes say. Main stayed at −30 dB and was muted again afterwards; every monitoring way was left off.

## Remaining boundaries

Not established: monitoring with a microphone or an instrument connected, and its latency; monitoring together with playback on the headphones; levels below −12 dB on the interface; monitoring on Main, which is deliberately not built because with a microphone and speakers it is the way to feedback. If TotalMix or a loss of power changes the mixer, the rule does not notice: its picture stands until a way is switched again.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
