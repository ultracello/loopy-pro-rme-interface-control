# Pad of the microphone inputs, and input steps that keep the page armed

Completed 17 November 2026, 02:06 to 02:38 (Europe/Berlin). Evidence: project-reported, two bounded native iPad/Babyface Pro FS runs and offline tests. This is not a live approval.

## What the earlier run had shown

The acceptance of the input gains earlier the same night had shown a difference between inputs and outputs: a confirmed step at an output prolongs the minute in which the page stays armed, a step at an input did not. After 60 seconds the next press asked for a new read.

## The pad shares its message with phantom power

The operator also wants the pad of the two microphone inputs on the page. In the protocol notes of the [oscmix project](https://github.com/michaelforney/oscmix/wiki/Babyface-Pro) the pad is set by a message that carries phantom power as well: one part says what changed, the other carries the current state, with one bit each for 48 V and pad of both inputs. The notes describe the write. They do not say where the unit reports these settings.

An eighth revision of the candidate rule, SHA-256 `db79bf4ae544fbd1b5a48c93c2def05fd42ff26042392647447aca2b3c35b9fe`, was built on one assumption, to be decided on the unit: that the low bits of the first state word mirror these settings. On this unit they had read hex 000C in every capture, with pad and phantom power off.

Phantom power stays out of reach by two independent means:

- the rule never sets a 48 V bit, neither as a change nor in the state part; while the unit reports 48 V on, or any setting bit the rule does not know, a pad press is refused and nothing is sent;
- the filter before the interface, SHA-256 `9ac2f209163c42b89e51d258eafff06eb88e7366247c48f169a6d3a37843eac6`, passes this message only when the change is exactly one pad bit and the state part carries no 48 V bit.

A pad press follows the course of a gain step: read the state, send one message, read again and compare. The page shows pad and 48 V of both inputs; the 48 V display is a display only.

The same revision lets a confirmed input step renew the armed minute.

Offline, 25 new tests passed and the 89 tests of the earlier revisions still pass. Of 29 deliberate falsifications 27 were noticed; the other two change no behaviour.

## On the interface

Nothing was connected to the inputs. After each press the unit was read directly.

| Check | Result |
|---|---|
| First pad press, input 1 | exactly one bit changed in the first four state words: word 0 from 009B000C to 009B001C; reason row "ok" |
| Pad of input 1 off again | back to 000C |
| Pad of input 2 on and off | 002C, then 000C |
| Both pads on, then off one after the other | 001C, 003C, 002C, 000C |
| Gain step with the pad on | input 1 up 1 dB and down 1 dB as before |
| A step 48 s after arming, without a new read | accepted |
| A step 97 s after arming, without a new read | accepted |

All 14 checks passed. The assumption holds on this unit: it reports the pad of input 1 in bit 4 and of input 2 in bit 5 of the first state word, and it accepts the write the notes describe. The 48 V displays stayed off throughout, the output gains did not change, and every setting and gain ended where it started.

## Measured with a loop cable

The operator then suggested a cable from an output into an input, and connected XLR output 1 to XLR input 1. With a clip looping and Main at −30 dB, the peak meters of the unit showed what pad and gain do to a signal. Each value is the highest peak of eight readings over a little more than one loop of the clip.

| State of input 1 | Peak at input 1 | Against pad off, gain 0 |
|---|---|---|
| Pad off, gain 0 dB | −26.6 dBFS | |
| Pad on | −36.8 dBFS | −10.2 dB |
| Pad off again | −26.6 dBFS | 0.0 dB |
| Gain 3 dB | −23.6 dBFS | +3.0 dB |
| Gain 6 dB | −20.6 dBFS | +6.0 dB |
| Gain back at 0 dB | −26.6 dBFS | 0.0 dB |

The pad attenuates by 10.2 dB on this unit (the manual says 11 dB), and the gain steps arrive as displayed. Main stayed at −30 dB and the gain at 6 dB or below, so that the loop could not feed back. Main was muted again afterwards.

## Remaining boundaries

Not established: the refusal of a pad press while 48 V is on, which was shown offline only because 48 V is not switched on for a test; the meaning of two further setting bits that stand set and are sent back as read; an evening of playing; operation alongside TotalMix; crash-safe recovery. Phantom power is deliberately not reachable.

Private native projects, scenes, identity maps, captures and access material are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
