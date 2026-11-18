# What the unit forgets when it loses power

Completed 18 November 2026, 16:17 to 16:23 (Europe/Berlin). Evidence: project-reported, bounded native iPad/Babyface Pro FS runs of one session, with nothing connected to the unit but USB, and one replug of that cable by the owner. This is not a live approval.

## The set-up, and a correction

The owner pulled the USB cable of the unit at the hub and plugged it in again after a few seconds. He also told us that the unit has had no power supply of its own for some days: it is fed over that USB cable alone. So this replug was a loss of power, and so was every replug of the last days. Earlier reports of this project spoke of the unit's USB connection "being built anew"; for those runs that meant a loss of power too. A replug with the unit kept alive by its own supply has not been tried.

## Before

On output AS1, which leads to no socket in use: playback 1 on the output at 0 dB, loopback of the output on, and an equaliser that makes +12 dB at the test tone. Read through loopback with the project's diagnostic app: the tone at 0.00 dB without the equaliser and at +12.00 dB with it. The unit's headphone meter read 14.50 dB below the playback meter, which is the owner's headphone cell at the headphone level he uses. Loopy Pro stayed open throughout; the rate was 48 kHz before and after.

## After, with nothing sent

The state message showed every level, gain and input setting as before, among them the level of AS1 that had been set for this run. The tone was missing on the input channel, and the headphone meter read nothing.

Then one thing at a time was sent again, with a reading after each:

| Sent again | Tone on the input channel |
|---|---|
| nothing | none |
| the mixer cell playback 1 to AS1 | none |
| loopback of AS1 | 0.00 dB |
| the device setting "EQ for Record", as found before | 0.00 dB |
| the equaliser message | +12.00 dB |

So after a loss of power the unit keeps output levels, gains and input settings, and it forgets the mixer, loopback and the equaliser. Whether "EQ for Record" survived cannot be told from this order: when it could first be seen, it had already been sent again.

A host therefore has to keep its own record of mixer, loopback and equaliser and send all three again when the unit comes back.

At the end everything of this run was switched off, the owner's two headphone cells were sent again and read 14.50 dB below playback as before, the levels were as found, and Loopy Pro was in front with the project that had been loaded, its transport stopped.

## Remaining boundaries

Not established: a replug with the unit powered by its own supply; whether "EQ for Record", the clock source and the optical format survive a loss of power; phantom power. Loopback shows what the unit sends to the host, not what leaves its sockets. No microphone or instrument was connected.

Private native projects, scenes, identity maps, captures and access material, among them the diagnostic app, are not distributed. This facts-only report includes no controller source, native archive or public installation package. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
